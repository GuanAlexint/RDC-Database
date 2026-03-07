<template>
  <div class="home-page">
    <div class="hero-section">
      <div class="logo-container">
        <h1 class="site-title">RDC Database</h1>
        <p class="site-subtitle">放射性诊疗化合物数据库</p>
      </div>
      
      <div class="search-container">
        <div class="search-box">
          <el-input
            v-model="searchKeyword"
            placeholder="请输入化合物名称、靶点、同位素等关键词..."
            size="large"
            clearable
            @keyup.enter="goToSearch"
            @focus="goToSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
        <p class="search-hint">支持名称、靶点、同位素、探针类型、DOI等多条件检索</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Search } from '@element-plus/icons-vue'

export default {
  name: 'HomePage',
  components: {
    Search
  },
  setup() {
    const router = useRouter()
    const searchKeyword = ref('')

    const goToSearch = () => {
      router.push({
        path: '/search',
        query: searchKeyword.value ? { name: searchKeyword.value } : {}
      })
    }

    return {
      searchKeyword,
      goToSearch
    }
  }
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.hero-section {
  text-align: center;
  max-width: 800px;
  width: 100%;
}

.logo-container {
  margin-bottom: 60px;
  animation: fadeInDown 0.8s ease-out;
}

.site-title {
  font-size: 56px;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 16px 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  letter-spacing: 2px;
}

.site-subtitle {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  font-weight: 300;
}

.search-container {
  animation: fadeInUp 0.8s ease-out 0.2s both;
}

.search-box {
  margin-bottom: 16px;
}

.search-box :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border-radius: 50px;
  padding: 12px 24px;
  transition: all 0.3s ease;
}

.search-box :deep(.el-input__wrapper:hover) {
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.search-box :deep(.el-input__inner) {
  font-size: 16px;
  color: #333;
}

.search-hint {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  margin: 0;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .site-title {
    font-size: 36px;
  }
  
  .site-subtitle {
    font-size: 16px;
  }
}
</style>

