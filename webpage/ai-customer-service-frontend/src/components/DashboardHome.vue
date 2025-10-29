<template>
  <div class="dashboard-home">
    <Row :gutter="16">
      <!-- 歡迎卡片 -->
      <Col span="24">
        <Card class="welcome-card enterprise-card">
          <div class="welcome-content">
            <div class="welcome-text">
              <h1>歡迎使用 AI客服管理系統</h1>
              <p class="user-info">
                <Icon type="ios-person" />
                當前用戶：{{ currentUser.full_name || currentUser.username }}
              </p>
              <p class="role-info">
                <Icon type="ios-ribbon" />
                用戶角色：{{ currentUser.roles ? currentUser.roles.join(', ') : '無' }}
              </p>
            </div>
            <div class="welcome-icon">
              <Icon type="ios-people" size="80" color="#7cb342" />
            </div>
          </div>
        </Card>
      </Col>
    </Row>

    <Row :gutter="16" style="margin-top: 20px;">
      <!-- 功能快捷入口 -->
      <Col span="6" v-if="hasPermission('perm_audio_create')">
        <Card class="feature-card enterprise-card" hoverable @click.native="navigateTo('voice')">
          <div class="feature-content">
            <Icon type="ios-mic" size="48" color="#7cb342" />
            <h3>語音互動</h3>
            <p>進行語音對話和分析</p>
          </div>
        </Card>
      </Col>
      
      <Col span="6" v-if="hasPermission('perm_staff_read')">
        <Card class="feature-card enterprise-card" hoverable @click.native="navigateTo('staff')">
          <div class="feature-content">
            <Icon type="ios-people" size="48" color="#9ccc65" />
            <h3>客服專員管理</h3>
            <p>管理客服專員資料</p>
          </div>
        </Card>
      </Col>
      
      <Col span="6" v-if="hasPermission('perm_audio_read')">
        <Card class="feature-card enterprise-card" hoverable @click.native="navigateTo('audio')">
          <div class="feature-content">
            <Icon type="ios-musical-notes" size="48" color="#689f38" />
            <h3>音頻管理</h3>
            <p>管理音頻檔案和記錄</p>
          </div>
        </Card>
      </Col>
      
      <Col span="6" v-if="hasRole('admin') || hasRole('manager')">
        <Card class="feature-card enterprise-card" hoverable @click.native="navigateTo('analytics')">
          <div class="feature-content">
            <Icon type="ios-analytics" size="48" color="#faad14" />
            <h3>數據分析</h3>
            <p>查看系統統計數據</p>
          </div>
        </Card>
      </Col>
    </Row>

    <Row :gutter="16" style="margin-top: 20px;">
      <!-- 系統統計 -->
      <Col span="12">
        <Card title="系統概覽" class="enterprise-card">
          <div class="stats-grid">
            <div class="stat-item">
              <Icon type="ios-people" size="24" color="#7cb342" />
              <div class="stat-content">
                <div class="stat-number">{{ stats.staffCount }}</div>
                <div class="stat-label">客服專員</div>
              </div>
            </div>
            
            <div class="stat-item">
              <Icon type="ios-musical-notes" size="24" color="#9ccc65" />
              <div class="stat-content">
                <div class="stat-number">{{ stats.audioCount }}</div>
                <div class="stat-label">音頻記錄</div>
              </div>
            </div>
            
            <div class="stat-item">
              <Icon type="ios-time" size="24" color="#689f38" />
              <div class="stat-content">
                <div class="stat-number">{{ stats.totalDuration }}</div>
                <div class="stat-label">總時長(分鐘)</div>
              </div>
            </div>
            
            <div class="stat-item">
              <Icon type="ios-calendar" size="24" color="#faad14" />
              <div class="stat-content">
                <div class="stat-number">{{ stats.todayCount }}</div>
                <div class="stat-label">今日記錄</div>
              </div>
            </div>
          </div>
        </Card>
      </Col>

      <!-- 最近活動 -->
      <Col span="12">
        <Card title="最近活動" class="enterprise-card">
          <div class="activity-list">
            <div class="activity-item" v-for="activity in recentActivities" :key="activity.id">
              <div class="activity-icon">
                <Icon :type="activity.icon" :color="activity.color" />
              </div>
              <div class="activity-content">
                <div class="activity-title">{{ activity.title }}</div>
                <div class="activity-time">{{ activity.time }}</div>
              </div>
            </div>
            
            <div v-if="recentActivities.length === 0" class="no-activity">
              <Icon type="ios-information-circle" size="24" color="#c5c8ce" />
              <p>暫無最近活動</p>
            </div>
          </div>
        </Card>
      </Col>
    </Row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'DashboardHome',
  data() {
    return {
      stats: {
        staffCount: 0,
        audioCount: 0,
        totalDuration: 0,
        todayCount: 0
      },
      recentActivities: []
    }
  },
  computed: {
    ...mapGetters('auth', ['currentUser', 'hasPermission', 'hasRole'])
  },
  mounted() {
    this.loadStats()
    this.loadRecentActivities()
  },
  methods: {
    navigateTo(menu) {
      // 直接使用路由跳轉
      const routeMap = {
        'voice': '/voice',
        'staff': '/staff',
        'audio': '/audio',
        'analytics': '/analytics'
      }
      
      if (routeMap[menu]) {
        this.$router.push(routeMap[menu])
      }
    },
    
    async loadStats() {
      try {
        // 這裡可以調用 API 獲取統計數據
        // 暫時使用模擬數據
        this.stats = {
          staffCount: 12,
          audioCount: 156,
          totalDuration: 2340,
          todayCount: 8
        }
      } catch (error) {
        console.error('載入統計數據失敗:', error)
      }
    },
    
    async loadRecentActivities() {
      try {
        // 這裡可以調用 API 獲取最近活動
        // 暫時使用模擬數據
        this.recentActivities = [
          {
            id: 1,
            title: '新增客服專員：C250009',
            time: '2小時前',
            icon: 'ios-person-add',
            color: '#7cb342'
          },
          {
            id: 2,
            title: '上傳音頻檔案：客戶諮詢_001.wav',
            time: '4小時前',
            icon: 'ios-cloud-upload',
            color: '#9ccc65'
          },
          {
            id: 3,
            title: '系統備份完成',
            time: '1天前',
            icon: 'ios-checkmark-circle',
            color: '#689f38'
          }
        ]
      } catch (error) {
        console.error('載入最近活動失敗:', error)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard-home {
  .welcome-card {
    .welcome-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .welcome-text {
        h1 {
          color: var(--text-primary);
          margin-bottom: 16px;
          font-size: 28px;
          font-weight: 600;
        }
        
        .user-info, .role-info {
          display: flex;
          align-items: center;
          gap: 8px;
          color: var(--text-secondary);
          font-size: 16px;
          margin-bottom: 8px;
        }
      }
      
      .welcome-icon {
        opacity: 0.8;
      }
    }
  }
  
  .feature-card {
    cursor: pointer;
    transition: all var(--transition-medium) ease;
    
    &:hover {
      transform: translateY(-4px);
      box-shadow: var(--shadow-medium);
    }
    
    .feature-content {
      text-align: center;
      padding: 20px 10px;
      
      h3 {
        margin: 16px 0 8px;
        color: var(--text-primary);
        font-size: 18px;
        font-weight: 600;
      }
      
      p {
        color: var(--text-secondary);
        font-size: 14px;
        margin: 0;
      }
    }
  }
  
  .stats-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    
    .stat-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 16px;
      background: var(--bg-tertiary);
      border-radius: var(--border-radius-medium);
      
      .stat-content {
        .stat-number {
          font-size: 24px;
          font-weight: 600;
          color: var(--text-primary);
          line-height: 1;
        }
        
        .stat-label {
          font-size: 12px;
          color: var(--text-secondary);
          margin-top: 4px;
        }
      }
    }
  }
  
  .activity-list {
    .activity-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 0;
      border-bottom: 1px solid var(--border-secondary);
      
      &:last-child {
        border-bottom: none;
      }
      
      .activity-icon {
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--bg-tertiary);
        border-radius: 50%;
      }
      
      .activity-content {
        flex: 1;
        
        .activity-title {
          font-size: 14px;
          color: var(--text-primary);
          margin-bottom: 4px;
        }
        
        .activity-time {
          font-size: 12px;
          color: var(--text-secondary);
        }
      }
    }
    
    .no-activity {
      text-align: center;
      padding: 40px 20px;
      color: var(--text-quaternary);
      
      p {
        margin: 8px 0 0;
        font-size: 14px;
      }
    }
  }
}

// 響應式設計
@media (max-width: 1200px) {
  .dashboard-home {
    .feature-card {
      margin-bottom: 16px;
    }
  }
}

@media (max-width: 768px) {
  .dashboard-home {
    .welcome-card .welcome-content {
      flex-direction: column;
      text-align: center;
      gap: 20px;
    }
    
    .stats-grid {
      grid-template-columns: 1fr;
    }
  }
}
</style>