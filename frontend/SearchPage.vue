<template>
  <div id="app" class="page-wrap">
    <div class="hero">
      <div class="title">RDC — 放射性诊疗化合物检索</div>
      <div class="subtitle">支持名称、靶点、同位素、探针类型、DOI、试验阶段等条件组合查询</div>
    </div>

    <!-- 检索栏（行内表单） -->
    <el-card class="search-card">
      <el-form :inline="true" :model="form" label-width="80px" @keyup.enter="fetchData(1)">
        <el-form-item label="名称">
          <el-input v-model="form.name" placeholder="化合物名称（模糊）" clearable />
        </el-form-item>
        <el-form-item label="靶点">
          <el-input v-model="form.target" placeholder="如 PSMA / SSTR2 / FAP ..." clearable />
        </el-form-item>
        <el-form-item label="同位素">
          <el-input v-model="form.isotope" placeholder="如 18F / 68Ga / 99mTc ..." clearable />
        </el-form-item>
        <el-form-item label="探针类型">
          <el-input v-model="form.probe_type" placeholder="Diagnostic PET / SPECT ..." clearable />
        </el-form-item>
        <el-form-item label="文献 DOI">
          <el-input v-model="form.doi" placeholder="doi 片段或链接片段" clearable />
        </el-form-item>
        <el-form-item label="试验阶段">
          <el-input v-model="form.trial_phase" placeholder="Phase I / II / III（预留）" clearable />
        </el-form-item>

        <!-- 搜索按钮紧贴最后一个输入框右侧 -->
        <el-form-item>
          <el-button type="primary" @click="fetchData(1)">
            <el-icon><Search /></el-icon>
            <span>搜索</span>
          </el-button>
          <el-button @click="reset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 结果表 -->
    <el-card class="table-card">
      <el-table :data="tableData" stripe border :header-cell-style="headerStyle" :cell-style="cellStyle">
        <el-table-column prop="compound_id" label="ID" width="80" align="center"/>
        <el-table-column prop="name" label="化合物名称" min-width="180" show-overflow-tooltip>
          <template #default="scope">
            <a class="compound-link" @click="goToDetail(scope.row.compound_id)">
              {{ scope.row.name }}
            </a>
          </template>
        </el-table-column>
        <el-table-column prop="cas_number" label="CAS号" min-width="140" show-overflow-tooltip/>
        <el-table-column prop="target" label="靶点" min-width="120" align="center"/>
        <el-table-column prop="isotope" label="同位素" min-width="120" align="center"/>
        <el-table-column prop="probe_type" label="探针类型" min-width="140" align="center"/>
        <el-table-column prop="ki" label="Ki" min-width="120" align="center"/>
        <el-table-column prop="kd" label="Kd" min-width="120" align="center"/>
        <el-table-column prop="ic50" label="IC50" min-width="120" align="center"/>
        <el-table-column prop="suv_max" label="SUVmax" min-width="200" show-overflow-tooltip/>
        <el-table-column prop="suv_mean" label="SUVmean" min-width="200" show-overflow-tooltip/>
        <el-table-column prop="tumor_uptake" label="肿瘤摄取" min-width="220" show-overflow-tooltip/>
        <el-table-column prop="kidney_uptake" label="肾摄取" min-width="220" show-overflow-tooltip/>
        <el-table-column prop="tumor_bone_ratio" label="T/Bone" min-width="160" show-overflow-tooltip/>
        <el-table-column prop="tumor_muscle_ratio" label="T/Muscle" min-width="160" show-overflow-tooltip/>
        <el-table-column prop="tumor_blood_ratio" label="T/Blood" min-width="160" show-overflow-tooltip/>
        <el-table-column prop="tumor_kidney_ratio" label="T/Kidney" min-width="160" show-overflow-tooltip/>

        <el-table-column prop="reference_link" label="文献链接" min-width="220">
          <template #default="scope">
            <a v-if="scope.row.reference_link" :href="scope.row.reference_link" target="_blank">{{ scope.row.reference_link }}</a>
            <span v-else>—</span>
          </template>
        </el-table-column>

        <el-table-column v-if="tableData.length && tableData[0].trial_phase !== undefined"
                         prop="trial_phase" label="试验阶段" min-width="120" align="center"/>
      </el-table>

      <div class="pager">
        <el-pagination
          background
          layout="prev, pager, next, sizes, jumper, total"
          :page-size="pageSize"
          :current-page="page"
          :total="total"
          :page-sizes="[10,20,50,100]"
          @current-change="onPageChange"
          @size-change="onSizeChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { Search } from '@element-plus/icons-vue'

export default {
  name: 'SearchPage',
  components: {
    Search
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const form = ref({
      name: '',
      target: '',
      isotope: '',
      probe_type: '',
      doi: '',
      trial_phase: ''
    })
    
    const tableData = ref([])
    const page = ref(1)
    const pageSize = ref(20)
    const total = ref(0)

    const fetchData = async (goPage = null) => {
      if (goPage) page.value = goPage
      const params = {
        page: page.value,
        page_size: pageSize.value
      }
      Object.keys(form.value).forEach(k => {
        const v = form.value[k]
        if (v !== null && v !== undefined && String(v).trim() !== '') {
          params[k] = v.trim()
        }
      })

      const { data } = await axios.get('http://localhost:8000/api/search', { params })
      tableData.value = data.results || []
      total.value = (data.pagination && data.pagination.total) || 0
    }

    const reset = () => {
      form.value = {
        name: '',
        target: '',
        isotope: '',
        probe_type: '',
        doi: '',
        trial_phase: ''
      }
      fetchData(1)
    }

    const onPageChange = (p) => {
      fetchData(p)
    }

    const onSizeChange = (s) => {
      pageSize.value = s
      fetchData(1)
    }

    const headerStyle = () => {
      return { textAlign: 'center', fontWeight: 600 }
    }

    const cellStyle = () => {
      return { verticalAlign: 'middle' }
    }

    const goToDetail = (compoundId) => {
      router.push(`/detail/${compoundId}`)
    }

    onMounted(() => {
      // 从路由参数初始化搜索条件
      if (route.query.name) {
        form.value.name = route.query.name
      }
      fetchData(1)
    })

    return {
      form,
      tableData,
      page,
      pageSize,
      total,
      fetchData,
      reset,
      onPageChange,
      onSizeChange,
      headerStyle,
      cellStyle,
      goToDetail
    }
  }
}
</script>

<style scoped>
html, body, #app { height: 100%; margin: 0; }
.page-wrap {
  min-height: 100%;
  background: #f6f8fb;
  padding-bottom: 40px;
}
.hero {
  background: linear-gradient(135deg, #1f6feb, #6ea8fe);
  color: #fff;
  padding: 36px 24px 28px;
  text-align: center;
}
.hero .title {
  font-size: 26px;
  font-weight: 700;
  letter-spacing: 0.5px;
}
.hero .subtitle {
  margin-top: 8px;
  font-size: 13px;
  opacity: 0.9;
}
.search-card, .table-card {
  width: 95%;
  max-width: 1280px;
  margin: 18px auto 0;
  border-radius: 12px;
  overflow: hidden;
}
.search-card :deep(.el-form-item) { 
  margin-bottom: 8px; 
}
.pager {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
.compound-link {
  color: #409eff;
  cursor: pointer;
  text-decoration: none;
}
.compound-link:hover {
  color: #66b1ff;
  text-decoration: underline;
}
</style>

