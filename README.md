# RDC Database — 放射性诊疗化合物数据库

一个面向核医学研究的放射性诊疗化合物（RDC）检索平台，支持多条件组合查询，可快速获取化合物的靶点、生物分布、成像数据及文献来源。

---

## 📌 项目简介

放射性诊疗化合物（Radiopharmaceuticals / RDC）的数据分散于大量文献中，检索效率低。本项目将相关数据结构化入库，提供友好的 Web 检索界面，帮助研究者快速定位目标化合物及其实验数据。

**支持检索字段：**
- 化合物名称（模糊匹配）
- 靶点（Target）
- 同位素（Isotope）
- 探针类型（Probe Type）
- 文献 DOI / 链接

---

## 🛠 技术栈

| 层级 | 技术 |
|---|---|
| 前端 | Vue 3 · Element Plus · Axios · Vue Router |
| 后端 | Python · FastAPI · MySQL Connector |
| 数据库 | MySQL |

---

## 🏗 系统架构

```
┌─────────────────────────────────┐
│           Vue 3 前端             │
│  HomePage → SearchPage → Detail │
└────────────┬────────────────────┘
             │ HTTP (Axios)
             ▼
┌─────────────────────────────────┐
│         FastAPI 后端             │
│  GET /api/search                │
│  GET /api/compound/{id}         │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│           MySQL (rdcdb)         │
│  compound_info   target_info    │
│  imaging_data    biodistribution│
│  ratios          reference_info │
└─────────────────────────────────┘
```

---

## 📂 数据库表结构

| 表名 | 说明 |
|---|---|
| `compound_info` | 化合物基础信息（名称、CAS号、分子式、分子量） |
| `target_info` | 靶点与亲和力数据（target、Ki、Kd、IC50、同位素、探针类型） |
| `imaging_data` | PET/SPECT 成像数据（SUVmax、SUVmean） |
| `biodistribution` | 各器官生物分布摄取值（肿瘤、肾、肝、脾、肺等12个部位） |
| `ratios` | 肿瘤对比度比率（T/Bone、T/Muscle、T/Blood、T/Kidney） |
| `reference_info` | 文献链接（DOI / URL） |

---

## ⚡ 快速开始

### 1. 克隆项目

```bash
git clone <repo_url>
cd rdc-database
```

### 2. 启动后端

```bash
cd backend
pip install fastapi uvicorn mysql-connector-python
uvicorn app:app --reload --port 8000
```

> 启动前请确保 MySQL 已运行，并在 `app.py` 中配置正确的数据库连接信息：
> ```python
> DB_CONFIG = {
>     "host": "localhost",
>     "user": "root",
>     "password": "",
>     "database": "rdcdb",
> }
> ```

### 3. 启动前端

```bash
cd frontend
npm install
npm run serve
```

前端默认运行在 `http://localhost:8080`，后端接口在 `http://localhost:8000`。

---

## 🔌 API 接口

### `GET /api/search` — 多条件检索

| 参数 | 类型 | 说明 |
|---|---|---|
| `name` | string | 化合物名称（模糊） |
| `target` | string | 靶点（模糊） |
| `isotope` | string | 同位素（模糊） |
| `probe_type` | string | 探针类型（模糊） |
| `doi` | string | 文献 DOI 或链接片段（模糊） |
| `page` | int | 页码，默认 1 |
| `page_size` | int | 每页数量，默认 20，最大 100 |

**返回示例：**
```json
{
  "results": [
    {
      "compound_id": 1,
      "name": "PSMA-617",
      "target": "PSMA",
      "isotope": "177Lu",
      "probe_type": "small molecule",
      "ki": "0.37 nM",
      "suv_max": "12.4",
      "tumor_uptake": "8.2 %ID/g",
      "reference_link": "https://doi.org/10.xxxx"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 42
  }
}
```

### `GET /api/compound/{compound_id}` — 化合物详情

返回指定化合物的全部字段，包含基础信息、靶点、成像数据、生物分布（12个器官）、比率数据及文献链接。

---

## 🖥 页面功能

| 页面 | 说明 |
|---|---|
| **首页 (HomePage)** | 搜索框入口，支持关键词快速跳转至检索页 |
| **检索页 (SearchPage)** | 多字段组合筛选，分页展示结果列表 |
| **详情页 (DetailPage)** | 展示单个化合物的完整数据，分模块卡片布局 |

---

## 💡 亮点

- **多表联查 + 动态 WHERE**：后端根据实际传入参数动态拼接 SQL，避免无效查询。
- **分页设计**：支持 page / page_size 参数，配合前端 Element Plus 分页组件。
- **前后端分离**：FastAPI 提供 RESTful 接口，Vue 3 Composition API 独立开发，通过 CORS 中间件连通。
- **可扩展**：数据库预留 `clinical_info` 临床试验表接口，后续可直接接入临床阶段数据。
