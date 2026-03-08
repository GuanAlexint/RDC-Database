# 运行：uvicorn app:app --reload --port 8000
# 先到指定文件夹，再运行


from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from typing import Optional, List

app = FastAPI()

# 允许来自本地 Vue 的跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === 数据库切换为 rdcdb ===
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "rdcdb",
}

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

@app.get("/api/search")
def search(
    name: Optional[str] = Query(None, description="化合物名称（模糊）"),
    target: Optional[str] = Query(None, description="靶点（模糊）"),
    isotope: Optional[str] = Query(None, description="同位素（模糊）"),
    probe_type: Optional[str] = Query(None, description="探针类型（模糊）"),
    doi: Optional[str] = Query(None, description="文献 DOI 或链接 片段（模糊）"),
    trial_phase: Optional[str] = Query(None, description="试验阶段（预留，库中存在时生效）"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    offset = (page - 1) * page_size

    # 基础 SELECT 与 JOIN
    
    base_sql = """
        SELECT
            ci.compound_id,
            ANY_VALUE(ci.name)              AS name,
            ANY_VALUE(ci.cas_number)        AS cas_number,
            ANY_VALUE(ti.target)            AS target,
            ANY_VALUE(ti.isotope)           AS isotope,
            ANY_VALUE(ti.probe_type)        AS probe_type,
            ANY_VALUE(ti.ki)                AS ki,
            ANY_VALUE(ti.kd)                AS kd,
            ANY_VALUE(ti.ic50)              AS ic50,
            ANY_VALUE(im.suv_max)           AS suv_max,
            ANY_VALUE(im.suv_mean)          AS suv_mean,
            ANY_VALUE(bd.tumor_uptake)      AS tumor_uptake,
            ANY_VALUE(bd.kidney_uptake)     AS kidney_uptake,
            ANY_VALUE(r.tumor_bone_ratio)   AS tumor_bone_ratio,
            ANY_VALUE(r.tumor_muscle_ratio) AS tumor_muscle_ratio,
            ANY_VALUE(r.tumor_blood_ratio)  AS tumor_blood_ratio,
            ANY_VALUE(r.tumor_kidney_ratio) AS tumor_kidney_ratio,
            ANY_VALUE(ref.reference_link)   AS reference_link
            -- , ANY_VALUE(cl.trial_phase)     AS trial_phase  -- 若后续接入临床表可放开
        FROM compound_info ci
        LEFT JOIN target_info ti       ON ci.compound_id = ti.compound_id
        LEFT JOIN imaging_data im      ON ci.compound_id = im.compound_id
        LEFT JOIN biodistribution bd   ON ci.compound_id = bd.compound_id
        LEFT JOIN ratios r             ON ci.compound_id = r.compound_id
        LEFT JOIN reference_info ref   ON ci.compound_id = ref.compound_id
        -- LEFT JOIN clinical_info cl     ON ci.compound_id = cl.compound_id
    """

    # 动态 WHERE
    where_clauses: List[str] = []
    params: List[str] = []

    if name:
        where_clauses.append("ci.name LIKE %s")
        params.append(f"%{name}%")
    if target:
        where_clauses.append("ti.target LIKE %s")
        params.append(f"%{target}%")
    if isotope:
        where_clauses.append("ti.isotope LIKE %s")
        params.append(f"%{isotope}%")
    if probe_type:
        where_clauses.append("ti.probe_type LIKE %s")
        params.append(f"%{probe_type}%")
    if doi:
        # reference_info.reference_link 中包含 DOI 或完整链接
        where_clauses.append("ref.reference_link LIKE %s")
        params.append(f"%{doi}%")
    if trial_phase:
        # 预留条件：仅当你后续真的有 cl.trial_phase 时，此条件才会生效
        where_clauses.append("cl.trial_phase LIKE %s")
        params.append(f"%{trial_phase}%")

    sql = base_sql
    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)

    sql += " GROUP BY ci.compound_id"   # 粗略去重
    sql += " ORDER BY ci.compound_id ASC"
    sql += " LIMIT %s OFFSET %s"
    params.extend([page_size, offset])

    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, params)
    rows = cursor.fetchall()

    # 统计总数（用于分页，和上面条件一致）
    count_sql = "SELECT COUNT(DISTINCT ci.compound_id) AS total FROM compound_info ci " \
                "LEFT JOIN target_info ti ON ci.compound_id = ti.compound_id " \
                "LEFT JOIN reference_info ref ON ci.compound_id = ref.compound_id "
                # 若启用临床：+ "LEFT JOIN clinical_info cl ON ci.compound_id = cl.compound_id "
    if where_clauses:
        count_sql += " WHERE " + " AND ".join(where_clauses)

    count_cursor = conn.cursor(dictionary=True)
    count_cursor.execute(count_sql, params[:-2])  # 去掉 limit/offset
    total = count_cursor.fetchone().get("total", 0)

    cursor.close()
    count_cursor.close()
    conn.close()

    return {
        "results": rows,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total
        }
    }


@app.get("/api/compound/{compound_id}")
def get_compound_detail(compound_id: int):
    """
    获取化合物的详细信息，包含所有相关表的数据
    """
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    
    # 查询化合物的完整信息，从所有相关表中获取
    sql = """
        SELECT
            ci.compound_id,
            ci.name,
            ci.cas_number,
            ci.molecular_formula,
            ci.molecular_weight,
            ti.target,
            ti.isotope,
            ti.probe_type,
            ti.ki,
            ti.kd,
            ti.ic50,
            im.suv_max,
            im.suv_mean,
            bd.tumor_uptake,
            bd.kidney_uptake,
            bd.liver_uptake,
            bd.spleen_uptake,
            bd.lung_uptake,
            bd.heart_uptake,
            bd.muscle_uptake,
            bd.bone_uptake,
            bd.blood_uptake,
            bd.brain_uptake,
            bd.stomach_uptake,
            bd.prostate_uptake,
            r.tumor_bone_ratio,
            r.tumor_muscle_ratio,
            r.tumor_blood_ratio,
            r.tumor_kidney_ratio,
            ref.reference_link
        FROM compound_info ci
        LEFT JOIN target_info ti       ON ci.compound_id = ti.compound_id
        LEFT JOIN imaging_data im      ON ci.compound_id = im.compound_id
        LEFT JOIN biodistribution bd   ON ci.compound_id = bd.compound_id
        LEFT JOIN ratios r             ON ci.compound_id = r.compound_id
        LEFT JOIN reference_info ref   ON ci.compound_id = ref.compound_id
        WHERE ci.compound_id = %s
        LIMIT 1
    """
    
    cursor.execute(sql, (compound_id,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if not result:
        raise HTTPException(status_code=404, detail="Compound not found")
    
    return result

