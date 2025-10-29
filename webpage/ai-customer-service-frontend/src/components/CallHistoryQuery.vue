<template>
  <div class="call-history-container">
    <Card>
      <template #title>
        <div class="card-title">
          <Icon type="ios-analytics" size="18" />
          <span>歷史撥打記錄查詢</span>
        </div>
      </template>

      <div class="search-section">
        <Form :model="searchForm" inline>
          <FormItem label="開始日期">
            <DatePicker
              type="date"
              placeholder="選擇開始日期"
              v-model="searchForm.startDate"
              style="width: 150px"
              :options="dateOptions"
            ></DatePicker>
          </FormItem>
          <FormItem label="結束日期">
            <DatePicker
              type="date"
              placeholder="選擇結束日期"
              v-model="searchForm.endDate"
              style="width: 150px"
              :options="dateOptions"
            ></DatePicker>
          </FormItem>
          <FormItem label="專員">
            <Select v-model="searchForm.staffId" style="width: 150px" clearable>
              <Option value="">請選擇</Option>
              <Option
                v-for="staff in staffList"
                :value="staff.id"
                :key="staff.id"
              >
                {{ staff.name }}
              </Option>
            </Select>
          </FormItem>
          <FormItem label="情緒分析">
            <Select
              v-model="searchForm.emotionType"
              style="width: 150px"
              clearable
            >
              <Option value="">請選擇</Option>
              <Option value="positive">正面情緒</Option>
              <Option value="neutral">中性情緒</Option>
              <Option value="negative">負面情緒</Option>
            </Select>
          </FormItem>
          <FormItem label=" ">
            <Button
              type="primary"
              icon="ios-search"
              @click="fetchCallRecords"
              :loading="isLoading"
              class="search-button"
              >查詢</Button
            >
            <Button
              style="margin-left: 8px"
              icon="md-refresh"
              @click="resetSearch"
              :disabled="isLoading"
              class="reset-button"
              >重置</Button
            >
          </FormItem>
        </Form>
      </div>

      <div class="stat-cards">
        <Row :gutter="16">
          <Col span="6">
            <Card
              class="stat-card total-calls"
              :class="{ 'card-animated': showCardAnimation }"
            >
              <div class="stat-content">
                <div class="stat-value">{{ statistics.totalCalls }}</div>
                <div class="stat-label">總通話數</div>
              </div>
              <div class="stat-icon">
                <Icon type="ios-call" size="36" />
              </div>
            </Card>
          </Col>
          <Col span="6">
            <Card
              class="stat-card positive-emotion"
              :class="{ 'card-animated': showCardAnimation }"
            >
              <div class="stat-content">
                <div class="stat-value">{{ statistics.positiveEmotions }}</div>
                <div class="stat-label">正面情緒</div>
              </div>
              <div class="stat-icon">
                <Icon type="ios-happy" size="36" />
              </div>
            </Card>
          </Col>
          <Col span="6">
            <Card
              class="stat-card neutral-emotion"
              :class="{ 'card-animated': showCardAnimation }"
            >
              <div class="stat-content">
                <div class="stat-value">{{ statistics.neutralEmotions }}</div>
                <div class="stat-label">中性情緒</div>
              </div>
              <div class="stat-icon">
                <Icon type="ios-contacts" size="36" />
              </div>
            </Card>
          </Col>
          <Col span="6">
            <Card
              class="stat-card negative-emotion"
              :class="{ 'card-animated': showCardAnimation }"
            >
              <div class="stat-content">
                <div class="stat-value">{{ statistics.negativeEmotions }}</div>
                <div class="stat-label">負面情緒</div>
              </div>
              <div class="stat-icon">
                <Icon type="ios-sad" size="36" />
              </div>
            </Card>
          </Col>
        </Row>
      </div>

      <!-- 使用子組件 -->
      <CallHistoryTable
        :callRecords="callRecords"
        :isLoading="isLoading"
        :totalRecords="totalRecords"
        :currentPage="currentPage"
        :pageSize="pageSize"
        @page-change="handlePageChange"
        @view-detail="viewCallDetail"
        @edit-followup="editFollowup"
      />

      <Modal
        v-model="detailModal.visible"
        width="700"
        title="通話詳細資訊"
        :mask-closable="false"
      >
        <div class="call-detail" v-if="detailModal.record">
          <Divider orientation="left">基本資訊</Divider>
          <Descriptions border>
            <DescriptionsItem label="案件編號">{{
              detailModal.record.id
            }}</DescriptionsItem>
            <DescriptionsItem label="客戶姓名">{{
              detailModal.record.customerName
            }}</DescriptionsItem>
            <DescriptionsItem label="聯絡電話">{{
              detailModal.record.phoneNumber
            }}</DescriptionsItem>
            <DescriptionsItem label="通話時間">{{
              detailModal.record.callTime
            }}</DescriptionsItem>
            <DescriptionsItem label="通話長度"
              >{{ detailModal.record.duration }} 分鐘</DescriptionsItem
            >
            <DescriptionsItem label="專員姓名">{{
              detailModal.record.staffName
            }}</DescriptionsItem>
            <DescriptionsItem
              label="部門"
              v-if="detailModal.record.department"
              >{{ detailModal.record.department }}</DescriptionsItem
            >
            <DescriptionsItem
              label="客戶類型"
              v-if="detailModal.record.customerType"
              >{{ detailModal.record.customerType }}</DescriptionsItem
            >
          </Descriptions>

          <Divider orientation="left">情緒分析</Divider>
          <div class="emotion-analysis">
            <Progress
              :percent="detailModal.record.emotionAnalysis.positive"
              status="success"
              :stroke-width="12"
            >
              <span
                >正面情緒
                {{ detailModal.record.emotionAnalysis.positive }}%</span
              >
            </Progress>
            <Progress
              :percent="detailModal.record.emotionAnalysis.neutral"
              :stroke-width="12"
            >
              <span
                >中性情緒
                {{ detailModal.record.emotionAnalysis.neutral }}%</span
              >
            </Progress>
            <Progress
              :percent="detailModal.record.emotionAnalysis.negative"
              status="wrong"
              :stroke-width="12"
            >
              <span
                >負面情緒
                {{ detailModal.record.emotionAnalysis.negative }}%</span
              >
            </Progress>
          </div>

          <Divider orientation="left">通話內容摘要</Divider>
          <div class="call-summary">
            <p>{{ detailModal.record.summary }}</p>
          </div>

          <Divider orientation="left">關鍵詞分析</Divider>
          <div class="keyword-tags">
            <Tag
              v-for="(keyword, index) in detailModal.record.keywords"
              :key="index"
              :color="getTagColor(keyword.sentiment)"
              class="keyword-tag"
            >
              {{ keyword.word }} ({{ keyword.count }})
            </Tag>
          </div>

          <Divider orientation="left">後續行動</Divider>
          <Form :model="detailModal.followupForm" :label-width="100">
            <FormItem label="跟進狀態">
              <RadioGroup v-model="detailModal.followupForm.status">
                <Radio label="pending">待處理</Radio>
                <Radio label="inProgress">處理中</Radio>
                <Radio label="completed">已完成</Radio>
                <Radio label="noAction">無需跟進</Radio>
              </RadioGroup>
            </FormItem>
            <FormItem label="跟進備註">
              <Input
                type="textarea"
                v-model="detailModal.followupForm.notes"
                :rows="4"
                placeholder="請輸入跟進備註..."
              />
            </FormItem>
          </Form>
        </div>
        <template #footer>
          <Button type="default" @click="detailModal.visible = false"
            >關閉</Button
          >
          <Button type="primary" @click="saveFollowup" :loading="isSaving"
            >保存跟進資訊</Button
          >
        </template>
      </Modal>
    </Card>
  </div>
</template>

<script>
import {
  generateCallRecords,
  getStatistics,
  staffList,
} from "@/data/mock-data";
import CallHistoryTable from "./Tables/CallHistoryTable.vue";

export default {
  name: "CallHistoryQuery",
  components: {
    CallHistoryTable,
  },
  data() {
    return {
      searchForm: {
        startDate: "",
        endDate: "",
        staffId: "",
        emotionType: "",
      },
      callRecords: [],
      staffList: [],
      isLoading: false,
      isSaving: false,
      currentPage: 1,
      pageSize: 10,
      totalRecords: 0,
      statistics: {
        totalCalls: 0,
        positiveEmotions: 0,
        neutralEmotions: 0,
        negativeEmotions: 0,
      },
      detailModal: {
        visible: false,
        record: null,
        followupForm: {
          status: "pending",
          notes: "",
        },
      },
      showCardAnimation: false,
      dateOptions: {
        disabledDate(date) {
          return date && date.valueOf() > Date.now();
        },
      },
    };
  },
  mounted() {
    this.fetchStaffList();
    this.initDefaultDateRange();
    this.fetchCallRecords();
  },
  methods: {
    initDefaultDateRange() {
      // 初始化默認查詢日期範圍（過去7天）
      const endDate = new Date();
      const startDate = new Date();
      startDate.setDate(startDate.getDate() - 7);

      this.searchForm.endDate = endDate;
      this.searchForm.startDate = startDate;
    },
    fetchStaffList() {
      // 從模擬數據中獲取專員列表
      this.staffList = staffList;
    },
    fetchCallRecords() {
      this.isLoading = true;
      this.showCardAnimation = false;

      // 使用 mock-data.js 中的函數獲取模擬數據
      setTimeout(() => {
        const params = {
          startDate: this.searchForm.startDate,
          endDate: this.searchForm.endDate,
          staffId: this.searchForm.staffId,
          emotionType: this.searchForm.emotionType,
          page: this.currentPage,
          pageSize: this.pageSize,
        };

        const result = generateCallRecords(params);
        this.callRecords = result.records;
        this.totalRecords = result.total;

        // 計算統計數據
        const stats = getStatistics(this.callRecords);

        // 使用動畫效果更新統計數字
        this.$nextTick(() => {
          this.statistics = stats;
          this.showCardAnimation = true;
        });

        this.isLoading = false;
      }, 800);
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchCallRecords();
    },
    resetSearch() {
      this.searchForm = {
        startDate: "",
        endDate: "",
        staffId: "",
        emotionType: "",
      };
      this.initDefaultDateRange();
      this.currentPage = 1;
      this.fetchCallRecords();
    },
    viewCallDetail(record) {
      this.detailModal.record = { ...record };
      this.detailModal.followupForm.status = record.followupStatus;
      this.detailModal.followupForm.notes = record.followupNotes || "";
      this.detailModal.visible = true;
    },
    editFollowup(record) {
      this.viewCallDetail(record);
    },
    saveFollowup() {
      this.isSaving = true;

      // 模擬保存跟進資訊
      setTimeout(() => {
        if (this.detailModal.record) {
          const index = this.callRecords.findIndex(
            (r) => r.id === this.detailModal.record.id
          );
          if (index > -1) {
            this.$set(
              this.callRecords[index],
              "followupStatus",
              this.detailModal.followupForm.status
            );
            this.$set(
              this.callRecords[index],
              "followupNotes",
              this.detailModal.followupForm.notes
            );

            this.$Message.success({
              content: "跟進資訊已成功更新",
              duration: 3,
            });
            this.detailModal.visible = false;
          }
        }
        this.isSaving = false;
      }, 500);
    },
    getTagColor(sentiment) {
      const colors = {
        positive: "success",
        neutral: "primary",
        negative: "error",
      };
      return colors[sentiment] || "default";
    },
  },
};
</script>

<style scoped>
.call-history-container {
  padding-bottom: 20px;
}

.card-title {
  display: flex;
  align-items: center;
}

.card-title span {
  margin-left: 8px;
  font-weight: 500;
}

.search-section {
  margin-bottom: 24px;
  padding: 18px;
  background-color: #f8f8f9;
  border-radius: 6px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.search-section:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.09);
}

.search-button {
  background-color: #2d8cf0;
  border-color: #2d8cf0;
}

.reset-button {
  border-color: #dcdee2;
  background-color: #fff;
}

.stat-cards {
  margin-bottom: 24px;
}

.stat-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-radius: 6px;
  overflow: hidden;
  position: relative;
  transition: all 0.3s ease;
  min-height: 110px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-animated .stat-value {
  animation: countUp 1s ease-out forwards;
}

@keyframes countUp {
  0% {
    opacity: 0;
    transform: translateY(10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.stat-content {
  z-index: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 8px;
  color: #2d8cf0;
}

.stat-label {
  font-size: 14px;
  color: #515a6e;
}

.stat-icon {
  opacity: 0.3;
  transition: all 0.3s ease;
}

.stat-card:hover .stat-icon {
  opacity: 0.6;
  transform: scale(1.1);
}

.total-calls {
  background: linear-gradient(135deg, #ffffff 0%, #f0f2f5 100%);
  border-left: 4px solid #2d8cf0;
}

.total-calls .stat-value {
  color: #2d8cf0;
}

.positive-emotion {
  background: linear-gradient(135deg, #ffffff 0%, #e8f7ef 100%);
  border-left: 4px solid #19be6b;
}

.positive-emotion .stat-value {
  color: #19be6b;
}

.neutral-emotion {
  background: linear-gradient(135deg, #ffffff 0%, #e8f3ff 100%);
  border-left: 4px solid #2d8cf0;
}

.neutral-emotion .stat-value {
  color: #2d8cf0;
}

.emotion-analysis {
  margin: 16px 0;
}

.keyword-tags {
  margin: 16px 0;
  display: flex;
  flex-wrap: wrap;
}

.keyword-tag {
  margin: 4px;
  font-size: 13px;
  padding: 6px 10px;
}

.call-summary {
  background-color: #f8f8f9;
  padding: 16px;
  border-radius: 6px;
  font-size: 14px;
  line-height: 1.6;
  border-left: 3px solid #2d8cf0;
}

/* 添加詳情模態框中的樣式 */
.call-detail .ivu-descriptions-item {
  padding: 12px 16px;
}

.call-detail .ivu-progress {
  margin-bottom: 16px;
}
</style>
