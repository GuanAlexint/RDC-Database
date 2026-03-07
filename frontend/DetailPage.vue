<template>
  <div class="detail-page">
    <div class="hero">
      <div class="title">化合物详细信息</div>
      <div class="subtitle">Compound Details</div>
    </div>

    <div class="content-wrap">
      <el-button class="back-btn" @click="goBack">
        <el-icon><ArrowLeft /></el-icon>
        <span>返回检索</span>
      </el-button>

      <el-card v-if="loading" class="loading-card">
        <el-skeleton :rows="10" animated />
      </el-card>

      <div v-else-if="compoundData">
        <!-- 基础信息 -->
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">基础信息 (Basic Information)</span>
            </div>
          </template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="化合物ID">{{ compoundData.compound_id }}</el-descriptions-item>
            <el-descriptions-item label="化合物名称">{{ compoundData.name || '—' }}</el-descriptions-item>
            <el-descriptions-item label="CAS号">{{ compoundData.cas_number || '—' }}</el-descriptions-item>
            <el-descriptions-item label="分子式">{{ compoundData.molecular_formula || '—' }}</el-descriptions-item>
            <el-descriptions-item label="分子量">{{ compoundData.molecular_weight || '—' }}</el-descriptions-item>
          </el-descriptions>
        </el-card>

        <!-- 靶点信息 -->
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">靶点与探针信息 (Target & Probe Information)</span>
            </div>
          </template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="靶点">{{ compoundData.target || '—' }}</el-descriptions-item>
            <el-descriptions-item label="同位素">{{ compoundData.isotope || '—' }}</el-descriptions-item>
            <el-descriptions-item label="探针类型">{{ compoundData.probe_type || '—' }}</el-descriptions-item>
            <el-descriptions-item label="Ki">{{ compoundData.ki || '—' }}</el-descriptions-item>
            <el-descriptions-item label="Kd">{{ compoundData.kd || '—' }}</el-descriptions-item>
            <el-descriptions-item label="IC50">{{ compoundData.ic50 || '—' }}</el-descriptions-item>
          </el-descriptions>
        </el-card>

        <!-- 成像数据 -->
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">成像数据 (Imaging Data)</span>
            </div>
          </template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="SUVmax" :span="2">
              <div class="long-text">{{ compoundData.suv_max || '—' }}</div>
            </el-descriptions-item>
            <el-descriptions-item label="SUVmean" :span="2">
              <div class="long-text">{{ compoundData.suv_mean || '—' }}</div>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>

        <!-- 生物分布 -->
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">生物分布 (Biodistribution)</span>
            </div>
          </template>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="肿瘤摄取 (Tumor Uptake)">
              <div class="long-text">{{ compoundData.tumor_uptake || '—' }}</div>
            </el-descriptions-item>
            <el-descriptions-item label="肾摄取 (Kidney Uptake)">
              <div class="long-text">{{ compoundData.kidney_uptake || '—' }}</div>
            </el-descriptions-item>
            <el-descriptions-item label="肝摄取 (Liver Uptake)">
              <div class="long-text">{{ compoundData.liver_uptake || '—' }}</div>
            </el-descriptions-item>
            <el-descriptions-item label="脾摄取 (Spleen Uptake)">
              <div class="long-text">{{ compoundData.spleen_uptake || '—' }}</div>
            </el-descriptions-item>
            <el-descriptions-item label="肺摄取 (Lung Uptake)">
              <div class="long-text">{{ compoundData.lung_uptake || '—' }}</div>
            </el-descriptions-item>
            <el-descriptions-item label="心脏摄取 (Heart Uptake)">
              <div class="long-text">{{ compoundData.heart_uptake || '—' }}</div>
            </el-descriptions-item>
            <el-descriptions-item label="肌肉摄取 (Muscle Uptake)">
              <div class="long-text">{{ compoundData.muscle_uptake || '—' }}</div>
            </el-descriptions-item>
            <el-descriptions-item label="骨摄取 (Bone Uptake)">
              <div class="long-text">{{ compoundData.bone_uptake || '—' }}</div>
            </el-descriptions-item>
            <el-descriptions-item label="血液摄取 (Blood Uptake)">
              <div class="long-text">{{ compoundData.blood_uptake || '—' }}</div>
            </el-descriptions-item>
            <el-descriptions-item label="脑摄取 (Brain Uptake)">
              <div class="long-text">{{ compoundData.brain_uptake || '—' }}</div>
            </el-descriptions-item>
            <el-descriptions-item label="胃摄取 (Stomach Uptake)">
              <div class="long-text">{{ compoundData.stomach_uptake || '—' }}</div>
            </el-descriptions-item>
            <el-descriptions-item label="前列腺摄取 (Prostate Uptake)">
              <div class="long-text">{{ compoundData.prostate_uptake || '—' }}</div>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>

        <!-- 比率数据 -->
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">比率数据 (Ratio Data)</span>
            </div>
          </template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="肿瘤/骨比率 (T/Bone)">
              <div class="long-text">{{ compoundData.tumor_bone_ratio || '—' }}</div>
            </el-descriptions-item>
            <el-descriptions-item label="肿瘤/肌肉比率 (T/Muscle)">
              <div class="long-text">{{ compoundData.tumor_muscle_ratio || '—' }}</div>
            </el-descriptions-item>
            <el-descriptions-item label="肿瘤/血液比率 (T/Blood)">
              <div class="long-text">{{ compoundData.tumor_blood_ratio || '—' }}</div>
            </el-descriptions-item>
            <el-descriptions-item label="肿瘤/肾比率 (T/Kidney)">
              <div class="long-text">{{ compoundData.tumor_kidney_ratio || '—' }}</div>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>

        <!-- 参考文献 -->
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">参考文献 (Reference)</span>
            </div>
          </template>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="文献链接">
              <a v-if="compoundData.reference_link" :href="compoundData.reference_link" target="_blank" class="ref-link">
                {{ compoundData.reference_link }}
              </a>
              <span v-else>—</span>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </div>

      <el-card v-else class="error-card">
        <el-empty description="未找到该化合物信息" />
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { ArrowLeft } from '@element-plus/icons-vue'

export default {
  name: 'DetailPage',
  components: {
    ArrowLeft
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const compoundData = ref(null)
    const loading = ref(true)

    const fetchCompoundDetail = async () => {
      try {
        loading.value = true
        const compoundId = route.params.id
        const { data } = await axios.get(`http://localhost:8000/api/compound/${compoundId}`)
        compoundData.value = data
      } catch (error) {
        console.error('获取化合物详情失败:', error)
        compoundData.value = null
      } finally {
        loading.value = false
      }
    }

    const goBack = () => {
      router.back()
    }

    onMounted(() => {
      fetchCompoundDetail()
    })

    return {
      compoundData,
      loading,
      goBack
    }
  }
}
</script>

<style scoped>
.detail-page {
  min-height: 100vh;
  background: #f6f8fb;
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

.content-wrap {
  width: 95%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 20px 0 40px;
}

.back-btn {
  margin-bottom: 20px;
}

.info-card {
  margin-bottom: 20px;
  border-radius: 12px;
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.long-text {
  max-height: 200px;
  overflow-y: auto;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

.ref-link {
  color: #409eff;
  text-decoration: none;
  word-break: break-all;
}

.ref-link:hover {
  color: #66b1ff;
  text-decoration: underline;
}

.loading-card,
.error-card {
  border-radius: 12px;
  overflow: hidden;
}
</style>

