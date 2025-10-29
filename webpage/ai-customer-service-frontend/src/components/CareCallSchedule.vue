<template>
  <div class="care-call-schedule-container">
    <Card>
      <template #title>
        <div class="card-title">
          <Icon type="ios-calendar" size="18" />
          <span>外撥關懷排程管理</span>
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
          <FormItem label="狀態">
            <Select v-model="searchForm.status" style="width: 150px" clearable>
              <Option value="">請選擇</Option>
              <Option value="pending">待撥打</Option>
              <Option value="completed">已完成</Option>
              <Option value="canceled">已取消</Option>
              <Option value="failed">未接通</Option>
            </Select>
          </FormItem>
          <FormItem label="關懷組別">
            <Select v-model="searchForm.groupId" style="width: 150px" clearable>
              <Option value="">請選擇</Option>
              <Option
                v-for="group in careGroups"
                :value="group.id"
                :key="group.id"
              >
                {{ group.name }}
              </Option>
            </Select>
          </FormItem>
          <FormItem label=" ">
            <Button
              type="primary"
              icon="ios-search"
              @click="fetchSchedules"
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
              class="stat-card total-schedules"
              :class="{ 'card-animated': showCardAnimation }"
            >
              <div class="stat-content">
                <div class="stat-value">{{ statistics.totalSchedules }}</div>
                <div class="stat-label">總排程數</div>
              </div>
              <div class="stat-icon">
                <Icon type="ios-calendar-outline" size="36" />
              </div>
            </Card>
          </Col>
          <Col span="6">
            <Card
              class="stat-card pending-calls"
              :class="{ 'card-animated': showCardAnimation }"
            >
              <div class="stat-content">
                <div class="stat-value">{{ statistics.pendingCalls }}</div>
                <div class="stat-label">待撥打</div>
              </div>
              <div class="stat-icon">
                <Icon type="ios-time" size="36" />
              </div>
            </Card>
          </Col>
          <Col span="6">
            <Card
              class="stat-card completed-calls"
              :class="{ 'card-animated': showCardAnimation }"
            >
              <div class="stat-content">
                <div class="stat-value">{{ statistics.completedCalls }}</div>
                <div class="stat-label">已完成</div>
              </div>
              <div class="stat-icon">
                <Icon type="ios-checkmark-circle" size="36" />
              </div>
            </Card>
          </Col>
          <Col span="6">
            <Card
              class="stat-card failed-calls"
              :class="{ 'card-animated': showCardAnimation }"
            >
              <div class="stat-content">
                <div class="stat-value">{{ statistics.failedCalls }}</div>
                <div class="stat-label">未接通</div>
              </div>
              <div class="stat-icon">
                <Icon type="ios-close-circle" size="36" />
              </div>
            </Card>
          </Col>
        </Row>
      </div>

      <div class="operation-bar">
        <Button
          type="primary"
          icon="md-add"
          @click="showCreateModal"
          class="create-button"
          >新增排程</Button
        >
        <Button
          type="success"
          icon="md-cloud-upload"
          @click="showBatchScheduleModal"
          class="batch-button"
          style="margin-left: 8px"
          >批量排程</Button
        >
      </div>

      <Table
        :columns="tableColumns"
        :data="scheduleList"
        :loading="isLoading"
        stripe
        border
        class="schedule-table"
      >
        <template #status="{ row }">
          <Tag :color="getStatusColor(row.status)">{{
            getStatusText(row.status)
          }}</Tag>
        </template>
        <template #action="{ row }">
          <Button
            type="primary"
            size="small"
            style="margin-right: 5px"
            @click="viewScheduleDetail(row)"
            >詳情</Button
          >
          <Button
            type="info"
            size="small"
            style="margin-right: 5px"
            @click="editSchedule(row)"
            v-if="row.status === 'pending'"
            >編輯</Button
          >
          <Button
            type="error"
            size="small"
            @click="cancelSchedule(row)"
            v-if="row.status === 'pending'"
            >取消</Button
          >
          <Button
            type="success"
            size="small"
            @click="updateCallResult(row)"
            v-if="row.status === 'pending'"
            >更新結果</Button
          >
        </template>
      </Table>

      <div class="pagination" style="margin-top: 20px; text-align: right">
        <Page
          :total="totalSchedules"
          :current="currentPage"
          :page-size="pageSize"
          @on-change="handlePageChange"
          show-total
          show-elevator
        ></Page>
      </div>

      <!-- 新增/編輯排程 Modal -->
      <Modal
        v-model="scheduleModal.visible"
        :title="scheduleModal.isEdit ? '編輯排程' : '新增排程'"
        :mask-closable="false"
        width="650"
      >
        <Form :model="scheduleModal.form" :label-width="100">
          <FormItem label="關懷對象" required>
            <Select
              v-model="scheduleModal.form.careTargetId"
              style="width: 100%"
              filterable
              remote
              :remote-method="remoteSearchCareTargets"
              :loading="careTargetsLoading"
            >
              <Option
                v-for="target in filteredCareTargets"
                :value="target.id"
                :key="target.id"
              >
                {{ target.name }} ({{ target.phone }})
              </Option>
            </Select>
          </FormItem>
          <FormItem label="排程日期" required>
            <DatePicker
              type="date"
              v-model="scheduleModal.form.scheduleDate"
              style="width: 100%"
              :options="futureDateOptions"
            ></DatePicker>
          </FormItem>
          <FormItem label="排程時段" required>
            <TimePicker
              type="time"
              v-model="scheduleModal.form.scheduleTime"
              style="width: 100%"
              format="HH:mm"
            ></TimePicker>
          </FormItem>
          <FormItem label="專員">
            <Select v-model="scheduleModal.form.staffId" style="width: 100%">
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
          <FormItem label="備註">
            <Input
              type="textarea"
              v-model="scheduleModal.form.notes"
              :rows="4"
              placeholder="請輸入排程備註..."
            ></Input>
          </FormItem>
          <FormItem label="優先級別">
            <RadioGroup v-model="scheduleModal.form.priority">
              <Radio label="low">低</Radio>
              <Radio label="normal">中</Radio>
              <Radio label="high">高</Radio>
            </RadioGroup>
          </FormItem>
        </Form>
        <template #footer>
          <Button @click="scheduleModal.visible = false">取消</Button>
          <Button
            type="primary"
            @click="saveSchedule"
            :loading="scheduleModal.saving"
            >確定</Button
          >
        </template>
      </Modal>

      <!-- 批量排程 Modal -->
      <Modal
        v-model="batchModal.visible"
        title="批量排程"
        :mask-closable="false"
        width="650"
      >
        <Form :model="batchModal.form" :label-width="100">
          <FormItem label="關懷組別" required>
            <Select v-model="batchModal.form.groupId" style="width: 100%">
              <Option
                v-for="group in careGroups"
                :value="group.id"
                :key="group.id"
              >
                {{ group.name }} ({{ group.count }}人)
              </Option>
            </Select>
          </FormItem>
          <FormItem label="開始日期" required>
            <DatePicker
              type="date"
              v-model="batchModal.form.startDate"
              style="width: 100%"
              :options="futureDateOptions"
            ></DatePicker>
          </FormItem>
          <FormItem label="結束日期" required>
            <DatePicker
              type="date"
              v-model="batchModal.form.endDate"
              style="width: 100%"
              :options="futureDateOptions"
            ></DatePicker>
          </FormItem>
          <FormItem label="每日開始時間" required>
            <TimePicker
              type="time"
              v-model="batchModal.form.startTime"
              style="width: 100%"
              format="HH:mm"
            ></TimePicker>
          </FormItem>
          <FormItem label="每日結束時間" required>
            <TimePicker
              type="time"
              v-model="batchModal.form.endTime"
              style="width: 100%"
              format="HH:mm"
            ></TimePicker>
          </FormItem>
          <FormItem label="每日排程數量" required>
            <InputNumber
              v-model="batchModal.form.dailyCount"
              :min="1"
              :max="100"
              style="width: 100%"
            ></InputNumber>
          </FormItem>
          <FormItem label="指定專員">
            <Select v-model="batchModal.form.staffId" style="width: 100%">
              <Option value="">自動分配</Option>
              <Option
                v-for="staff in staffList"
                :value="staff.id"
                :key="staff.id"
              >
                {{ staff.name }}
              </Option>
            </Select>
          </FormItem>
        </Form>
        <template #footer>
          <Button @click="batchModal.visible = false">取消</Button>
          <Button
            type="primary"
            @click="createBatchSchedules"
            :loading="batchModal.saving"
            >確定</Button
          >
        </template>
      </Modal>

      <!-- 撥打結果 Modal -->
      <Modal
        v-model="resultModal.visible"
        title="更新撥打結果"
        :mask-closable="false"
        width="650"
      >
        <div class="call-target-info" v-if="resultModal.schedule">
          <Descriptions :column="2" border size="small">
            <DescriptionsItem label="關懷對象">{{
              resultModal.schedule.targetName
            }}</DescriptionsItem>
            <DescriptionsItem label="聯絡電話">{{
              resultModal.schedule.targetPhone
            }}</DescriptionsItem>
            <DescriptionsItem label="排程時間">{{
              resultModal.schedule.scheduleDateTime
            }}</DescriptionsItem>
            <DescriptionsItem label="專員">{{
              resultModal.schedule.staffName || "未指派"
            }}</DescriptionsItem>
          </Descriptions>
        </div>
        <Form
          :model="resultModal.form"
          :label-width="100"
          style="margin-top: 16px"
        >
          <FormItem label="撥打結果" required>
            <RadioGroup v-model="resultModal.form.status">
              <Radio label="completed">已完成</Radio>
              <Radio label="failed">未接通</Radio>
              <Radio label="canceled">已取消</Radio>
            </RadioGroup>
          </FormItem>
          <FormItem
            label="通話時長"
            v-if="resultModal.form.status === 'completed'"
          >
            <InputNumber
              v-model="resultModal.form.duration"
              :min="0"
              style="width: 100%"
              placeholder="通話時長（分鐘）"
            ></InputNumber>
          </FormItem>
          <FormItem label="結果備註">
            <Input
              type="textarea"
              v-model="resultModal.form.resultNotes"
              :rows="4"
              placeholder="請輸入撥打結果備註..."
            ></Input>
          </FormItem>
          <FormItem label="後續跟進">
            <RadioGroup v-model="resultModal.form.followupNeeded">
              <Radio :label="true">需要跟進</Radio>
              <Radio :label="false">不需跟進</Radio>
            </RadioGroup>
          </FormItem>
          <FormItem label="跟進日期" v-if="resultModal.form.followupNeeded">
            <DatePicker
              type="date"
              v-model="resultModal.form.followupDate"
              style="width: 100%"
              :options="futureDateOptions"
            ></DatePicker>
          </FormItem>
        </Form>
        <template #footer>
          <Button @click="resultModal.visible = false">取消</Button>
          <Button
            type="primary"
            @click="saveCallResult"
            :loading="resultModal.saving"
            >確定</Button
          >
        </template>
      </Modal>

      <!-- 排程詳情 Modal -->
      <Modal
        v-model="detailModal.visible"
        title="排程詳情"
        :mask-closable="false"
        width="700"
      >
        <div class="schedule-detail" v-if="detailModal.schedule">
          <Divider orientation="left">基本資訊</Divider>
          <Descriptions border>
            <DescriptionsItem label="排程 ID">{{
              detailModal.schedule.id
            }}</DescriptionsItem>
            <DescriptionsItem label="關懷對象">{{
              detailModal.schedule.targetName
            }}</DescriptionsItem>
            <DescriptionsItem label="聯絡電話">{{
              detailModal.schedule.targetPhone
            }}</DescriptionsItem>
            <DescriptionsItem label="排程時間">{{
              detailModal.schedule.scheduleDateTime
            }}</DescriptionsItem>
            <DescriptionsItem label="專員">{{
              detailModal.schedule.staffName || "未指派"
            }}</DescriptionsItem>
            <DescriptionsItem label="建立時間">{{
              detailModal.schedule.createdAt
            }}</DescriptionsItem>
            <DescriptionsItem label="狀態">
              <Tag :color="getStatusColor(detailModal.schedule.status)">
                {{ getStatusText(detailModal.schedule.status) }}
              </Tag>
            </DescriptionsItem>
            <DescriptionsItem label="優先級別">
              <Tag :color="getPriorityColor(detailModal.schedule.priority)">
                {{ getPriorityText(detailModal.schedule.priority) }}
              </Tag>
            </DescriptionsItem>
            <DescriptionsItem label="備註" :span="2">{{
              detailModal.schedule.notes || "無"
            }}</DescriptionsItem>
          </Descriptions>

          <Divider
            orientation="left"
            v-if="detailModal.schedule.status !== 'pending'"
            >撥打結果</Divider
          >
          <Descriptions border v-if="detailModal.schedule.status !== 'pending'">
            <DescriptionsItem label="撥打時間">{{
              detailModal.schedule.callDateTime || "無資料"
            }}</DescriptionsItem>
            <DescriptionsItem
              label="通話時長"
              v-if="detailModal.schedule.status === 'completed'"
            >
              {{ detailModal.schedule.duration }} 分鐘
            </DescriptionsItem>
            <DescriptionsItem label="結果備註" :span="2">{{
              detailModal.schedule.resultNotes || "無"
            }}</DescriptionsItem>
          </Descriptions>

          <Divider orientation="left" v-if="detailModal.schedule.followupNeeded"
            >後續跟進</Divider
          >
          <Descriptions border v-if="detailModal.schedule.followupNeeded">
            <DescriptionsItem label="跟進日期">{{
              detailModal.schedule.followupDate
            }}</DescriptionsItem>
            <DescriptionsItem label="跟進狀態">
              <Tag
                :color="
                  getFollowupStatusColor(detailModal.schedule.followupStatus)
                "
              >
                {{ getFollowupStatusText(detailModal.schedule.followupStatus) }}
              </Tag>
            </DescriptionsItem>
            <DescriptionsItem label="跟進備註" :span="2">{{
              detailModal.schedule.followupNotes || "無"
            }}</DescriptionsItem>
          </Descriptions>
        </div>
        <template #footer>
          <Button @click="detailModal.visible = false">關閉</Button>
        </template>
      </Modal>
    </Card>
  </div>
</template>

<script>
export default {
  name: "CareCallSchedule",
  data() {
    return {
      searchForm: {
        startDate: "",
        endDate: "",
        staffId: "",
        status: "",
        groupId: "",
      },
      isLoading: false,
      showCardAnimation: false,
      currentPage: 1,
      pageSize: 10,
      totalSchedules: 0,
      scheduleList: [],
      staffList: [],
      careGroups: [],
      filteredCareTargets: [],
      careTargetsLoading: false,

      statistics: {
        totalSchedules: 0,
        pendingCalls: 0,
        completedCalls: 0,
        failedCalls: 0,
      },

      // 表格列定義
      tableColumns: [
        {
          title: "ID",
          key: "id",
          width: 100,
        },
        {
          title: "關懷對象",
          key: "targetName",
          minWidth: 120,
        },
        {
          title: "聯絡電話",
          key: "targetPhone",
          width: 120,
        },
        {
          title: "排程時間",
          key: "scheduleDateTime",
          width: 150,
        },
        {
          title: "專員",
          key: "staffName",
          width: 100,
        },
        {
          title: "狀態",
          slot: "status",
          width: 100,
        },
        {
          title: "優先級別",
          key: "priorityText",
          width: 100,
        },
        {
          title: "操作",
          slot: "action",
          width: 220,
          align: "center",
        },
      ],

      // 新增/編輯排程 Modal
      scheduleModal: {
        visible: false,
        isEdit: false,
        saving: false,
        form: {
          id: null,
          careTargetId: "",
          scheduleDate: "",
          scheduleTime: "",
          staffId: "",
          notes: "",
          priority: "normal",
        },
      },

      // 批量排程 Modal
      batchModal: {
        visible: false,
        saving: false,
        form: {
          groupId: "",
          startDate: "",
          endDate: "",
          startTime: "",
          endTime: "",
          dailyCount: 10,
          staffId: "",
        },
      },

      // 撥打結果 Modal
      resultModal: {
        visible: false,
        saving: false,
        schedule: null,
        form: {
          scheduleId: null,
          status: "completed",
          duration: 0,
          resultNotes: "",
          followupNeeded: false,
          followupDate: "",
        },
      },

      // 排程詳情 Modal
      detailModal: {
        visible: false,
        schedule: null,
      },

      // 日期選擇器配置
      dateOptions: {
        disabledDate(date) {
          return date && date.valueOf() > Date.now();
        },
      },

      // 未來日期選擇器配置
      futureDateOptions: {
        disabledDate(date) {
          return date && date.valueOf() < Date.now() - 86400000;
        },
      },
    };
  },

  mounted() {
    this.initDefaultDateRange();
    this.fetchStaffList();
    this.fetchCareGroups();
    this.fetchSchedules();
  },

  methods: {
    // 初始化默認查詢日期範圍（未來7天）
    initDefaultDateRange() {
      const today = new Date();
      const endDate = new Date();
      endDate.setDate(today.getDate() + 7);

      this.searchForm.startDate = today;
      this.searchForm.endDate = endDate;
    },

    // 獲取客服專員列表
    fetchStaffList() {
      // 模擬 API 獲取專員列表
      setTimeout(() => {
        this.staffList = [
          { id: "1", name: "C220001" },
          { id: "2", name: "C220002" },
          { id: "3", name: "C230003" },
          { id: "4", name: "C230004" },
          { id: "5", name: "C240005" },
        ];
      }, 300);
    },

    // 獲取關懷組別
    fetchCareGroups() {
      // 模擬 API 獲取關懷組別
      setTimeout(() => {
        this.careGroups = [
          { id: "1", name: "高齡長者", count: 125 },
          { id: "2", name: "慢性病患者", count: 89 },
          { id: "3", name: "獨居老人", count: 56 },
          { id: "4", name: "行動不便", count: 32 },
          { id: "5", name: "社區新成員", count: 47 },
        ];
      }, 300);
    },

    // 遠程搜索關懷對象
    remoteSearchCareTargets(query) {
      if (query.length < 2) return;
      this.careTargetsLoading = true;

      // 模擬 API 搜索關懷對象
      setTimeout(() => {
        this.filteredCareTargets = [
          { id: "101", name: "陳○○", phone: "0912XX5678" },
          { id: "102", name: "王○○", phone: "0923XX6789" },
          { id: "103", name: "呂○○", phone: "0934XX7890" },
          { id: "104", name: "李○○", phone: "0945XX8901" },
          { id: "105", name: "張○○", phone: "0956XX9012" },
        ].filter(
          (item) => item.name.includes(query) || item.phone.includes(query)
        );
        this.careTargetsLoading = false;
      }, 500);
    },

    // 獲取排程列表
    fetchSchedules() {
      this.isLoading = true;
      this.showCardAnimation = false;

      // 模擬 API 獲取排程列表
      setTimeout(() => {
        // 模擬根據搜索條件過濾數據
        const mockData = this.generateMockSchedules();

        this.scheduleList = mockData.items;
        this.totalSchedules = mockData.total;

        // 計算統計數據
        this.calculateStatistics();

        // 顯示統計卡片動畫
        this.$nextTick(() => {
          this.showCardAnimation = true;
          this.isLoading = false;
        });
      }, 800);
    },

    // 生成模擬排程數據
    generateMockSchedules() {
      const statuses = ["pending", "completed", "failed", "canceled"];
      const priorities = ["low", "normal", "high"];
      const staffNames = ["C220001", "C220002", "C230003", "C230004", "C240005"];

      const mockData = [];
      const total = 68; // 模擬總數據量

      // 生成模擬數據
      for (let i = 1; i <= total; i++) {
        const status = statuses[Math.floor(Math.random() * statuses.length)];
        const priority =
          priorities[Math.floor(Math.random() * priorities.length)];
        const staffIndex = Math.floor(Math.random() * staffNames.length);

        // 生成隨機排程日期（前後10天內）
        const today = new Date();
        const scheduleDate = new Date(today);
        scheduleDate.setDate(
          today.getDate() - 5 + Math.floor(Math.random() * 15)
        );

        // 格式化時間
        const year = scheduleDate.getFullYear();
        const month = String(scheduleDate.getMonth() + 1).padStart(2, "0");
        const day = String(scheduleDate.getDate()).padStart(2, "0");
        const hours = String(9 + Math.floor(Math.random() * 8)).padStart(
          2,
          "0"
        );
        const minutes = String(Math.floor(Math.random() * 60)).padStart(2, "0");

        const scheduleDateTime = `${year}-${month}-${day} ${hours}:${minutes}`;

        // 生成模擬撥打記錄
        let callDateTime = null;
        let duration = null;
        let resultNotes = null;
        let followupNeeded = false;
        let followupDate = null;
        let followupStatus = null;
        let followupNotes = null;

        if (status !== "pending") {
          // 模擬撥打時間
          const callDate = new Date(scheduleDate);
          callDate.setHours(
            parseInt(hours),
            parseInt(minutes) + Math.floor(Math.random() * 30)
          );

          const callYear = callDate.getFullYear();
          const callMonth = String(callDate.getMonth() + 1).padStart(2, "0");
          const callDay = String(callDate.getDate()).padStart(2, "0");
          const callHours = String(callDate.getHours()).padStart(2, "0");
          const callMinutes = String(callDate.getMinutes()).padStart(2, "0");

          callDateTime = `${callYear}-${callMonth}-${callDay} ${callHours}:${callMinutes}`;

          // 模擬通話時長（僅當狀態為已完成時）
          if (status === "completed") {
            duration = Math.floor(Math.random() * 20) + 3; // 3-22分鐘
            resultNotes = "已與關懷對象溝通完成，整體狀況良好。";

            // 隨機決定是否需要跟進
            followupNeeded = Math.random() > 0.7;
            if (followupNeeded) {
              const followupDateObj = new Date(callDate);
              followupDateObj.setDate(
                callDate.getDate() + 7 + Math.floor(Math.random() * 7)
              );

              const fyear = followupDateObj.getFullYear();
              const fmonth = String(followupDateObj.getMonth() + 1).padStart(
                2,
                "0"
              );
              const fday = String(followupDateObj.getDate()).padStart(2, "0");

              followupDate = `${fyear}-${fmonth}-${fday}`;
              followupStatus = Math.random() > 0.5 ? "pending" : "completed";
              followupNotes =
                followupStatus === "completed"
                  ? "已完成跟進，建議持續關注。"
                  : "待跟進";
            }
          } else if (status === "failed") {
            resultNotes = "未能接通關懷對象，建議更換時間再次撥打。";
          } else if (status === "canceled") {
            resultNotes = "根據家屬要求取消本次關懷電話。";
          }
        }

        mockData.push({
          id: `SCH${String(i).padStart(5, "0")}`,
          targetName: ["陳○○", "王○○", "呂○○", "李○○", "張○○"][
            Math.floor(Math.random() * 5)
          ],
          targetPhone: [
            "0912XX5678",
            "0923XX6789",
            "0934XX7890",
            "0945XX8901",
            "0956XX9012",
          ][Math.floor(Math.random() * 5)],
          scheduleDateTime,
          staffId: this.staffList[staffIndex]?.id || null,
          staffName: staffNames[staffIndex],
          status,
          priority,
          priorityText: this.getPriorityText(priority),
          notes: "定期關懷電話，了解近況與需求。",
          callDateTime,
          duration,
          resultNotes,
          followupNeeded,
          followupDate,
          followupStatus,
          followupNotes,
          createdAt: `${year}-${month}-${String(
            Math.floor(Math.random() * 28) + 1
          ).padStart(2, "0")} 08:${String(
            Math.floor(Math.random() * 60)
          ).padStart(2, "0")}`,
        });
      }

      // 模擬分頁
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;

      return {
        items: mockData.slice(start, end),
        total,
      };
    },

    // 計算統計數據
    calculateStatistics() {
      // 在真實環境中，這些數據應該從API獲取
      this.statistics = {
        totalSchedules: this.totalSchedules,
        pendingCalls: Math.floor(this.totalSchedules * 0.4),
        completedCalls: Math.floor(this.totalSchedules * 0.35),
        failedCalls: Math.floor(this.totalSchedules * 0.25),
      };
    },

    // 處理分頁變更
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchSchedules();
    },

    // 重置搜索條件
    resetSearch() {
      this.searchForm = {
        startDate: "",
        endDate: "",
        staffId: "",
        status: "",
        groupId: "",
      };
      this.initDefaultDateRange();
      this.currentPage = 1;
      this.fetchSchedules();
    },

    // 顯示創建排程模態框
    showCreateModal() {
      this.scheduleModal.isEdit = false;
      this.scheduleModal.form = {
        id: null,
        careTargetId: "",
        scheduleDate: new Date(),
        scheduleTime: "09:00",
        staffId: "",
        notes: "",
        priority: "normal",
      };
      this.scheduleModal.visible = true;
    },

    // 顯示編輯排程模態框
    editSchedule(row) {
      this.scheduleModal.isEdit = true;

      // 模擬時間解析
      const [dateStr, timeStr] = row.scheduleDateTime.split(" ");

      this.scheduleModal.form = {
        id: row.id,
        careTargetId: "101", // 假設這是對應的ID
        scheduleDate: new Date(dateStr),
        scheduleTime: timeStr,
        staffId: row.staffId,
        notes: row.notes,
        priority: row.priority,
      };

      this.scheduleModal.visible = true;
    },

    // 保存排程
    saveSchedule() {
      // 表單驗證
      if (!this.scheduleModal.form.careTargetId) {
        this.$Message.error("請選擇關懷對象");
        return;
      }

      if (!this.scheduleModal.form.scheduleDate) {
        this.$Message.error("請選擇排程日期");
        return;
      }

      if (!this.scheduleModal.form.scheduleTime) {
        this.$Message.error("請選擇排程時段");
        return;
      }

      this.scheduleModal.saving = true;

      // 模擬API保存操作
      setTimeout(() => {
        // 成功提示
        this.$Message.success({
          content: this.scheduleModal.isEdit
            ? "排程更新成功！"
            : "排程建立成功！",
          duration: 3,
        });

        this.scheduleModal.saving = false;
        this.scheduleModal.visible = false;

        // 重新獲取列表
        this.fetchSchedules();
      }, 800);
    },

    // 顯示批量排程模態框
    showBatchScheduleModal() {
      // 設置默認值
      const today = new Date();
      const endDate = new Date();
      endDate.setDate(today.getDate() + 7);

      this.batchModal.form = {
        groupId: "",
        startDate: today,
        endDate: endDate,
        startTime: "09:00",
        endTime: "17:00",
        dailyCount: 10,
        staffId: "",
      };

      this.batchModal.visible = true;
    },

    // 創建批量排程
    createBatchSchedules() {
      // 表單驗證
      if (!this.batchModal.form.groupId) {
        this.$Message.error("請選擇關懷組別");
        return;
      }

      if (!this.batchModal.form.startDate || !this.batchModal.form.endDate) {
        this.$Message.error("請選擇日期範圍");
        return;
      }

      if (!this.batchModal.form.startTime || !this.batchModal.form.endTime) {
        this.$Message.error("請選擇時間範圍");
        return;
      }

      // 檢查開始日期不能晚於結束日期
      if (
        new Date(this.batchModal.form.startDate) >
        new Date(this.batchModal.form.endDate)
      ) {
        this.$Message.error("開始日期不能晚於結束日期");
        return;
      }

      this.batchModal.saving = true;

      // 模擬API批量創建操作
      setTimeout(() => {
        const groupName =
          this.careGroups.find((g) => g.id === this.batchModal.form.groupId)
            ?.name || "";
        const totalScheduled = Math.floor(Math.random() * 20) + 10;

        // 成功提示
        this.$Message.success({
          content: `成功為「${groupName}」創建了 ${totalScheduled} 筆排程！`,
          duration: 3,
        });

        this.batchModal.saving = false;
        this.batchModal.visible = false;

        // 重新獲取列表
        this.fetchSchedules();
      }, 1200);
    },

    // 查看排程詳情
    viewScheduleDetail(row) {
      this.detailModal.schedule = { ...row };
      this.detailModal.visible = true;
    },

    // 取消排程
    cancelSchedule(row) {
      this.$Modal.confirm({
        title: "確認取消",
        content: `確定要取消 ${row.targetName} 的排程嗎？`,
        onOk: () => {
          // 模擬API操作
          setTimeout(() => {
            this.$Message.success("排程已成功取消");
            this.fetchSchedules();
          }, 500);
        },
      });
    },

    // 更新撥打結果
    updateCallResult(row) {
      this.resultModal.schedule = { ...row };
      this.resultModal.form = {
        scheduleId: row.id,
        status: "completed",
        duration: 0,
        resultNotes: "",
        followupNeeded: false,
        followupDate: "",
      };

      this.resultModal.visible = true;
    },

    // 保存撥打結果
    saveCallResult() {
      // 表單驗證
      if (
        this.resultModal.form.status === "completed" &&
        !this.resultModal.form.duration
      ) {
        this.$Message.error("請輸入通話時長");
        return;
      }

      if (
        this.resultModal.form.followupNeeded &&
        !this.resultModal.form.followupDate
      ) {
        this.$Message.error("請選擇跟進日期");
        return;
      }

      this.resultModal.saving = true;

      // 模擬API保存操作
      setTimeout(() => {
        // 成功提示
        this.$Message.success({
          content: "撥打結果已更新！",
          duration: 3,
        });

        this.resultModal.saving = false;
        this.resultModal.visible = false;

        // 重新獲取列表
        this.fetchSchedules();
      }, 800);
    },

    // 獲取狀態顏色
    getStatusColor(status) {
      const colors = {
        pending: "blue",
        completed: "success",
        failed: "error",
        canceled: "default",
      };
      return colors[status] || "default";
    },

    // 獲取狀態文字
    getStatusText(status) {
      const texts = {
        pending: "待撥打",
        completed: "已完成",
        failed: "未接通",
        canceled: "已取消",
      };
      return texts[status] || "未知";
    },

    // 獲取優先級顏色
    getPriorityColor(priority) {
      const colors = {
        low: "default",
        normal: "primary",
        high: "warning",
      };
      return colors[priority] || "default";
    },

    // 獲取優先級文字
    getPriorityText(priority) {
      const texts = {
        low: "低",
        normal: "中",
        high: "高",
      };
      return texts[priority] || "未知";
    },

    // 獲取跟進狀態顏色
    getFollowupStatusColor(status) {
      const colors = {
        pending: "blue",
        completed: "success",
        inProgress: "warning",
      };
      return colors[status] || "default";
    },

    // 獲取跟進狀態文字
    getFollowupStatusText(status) {
      const texts = {
        pending: "待跟進",
        completed: "已完成",
        inProgress: "跟進中",
      };
      return texts[status] || "未知";
    },
  },
};
</script>

<style scoped>
.care-call-schedule-container {
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

.total-schedules {
  background: linear-gradient(135deg, #ffffff 0%, #f0f2f5 100%);
  border-left: 4px solid #2d8cf0;
}

.total-schedules .stat-value {
  color: #2d8cf0;
}

.pending-calls {
  background: linear-gradient(135deg, #ffffff 0%, #e8f3ff 100%);
  border-left: 4px solid #2d8cf0;
}

.pending-calls .stat-value {
  color: #2d8cf0;
}

.completed-calls {
  background: linear-gradient(135deg, #ffffff 0%, #e8f7ef 100%);
  border-left: 4px solid #19be6b;
}

.completed-calls .stat-value {
  color: #19be6b;
}

.failed-calls {
  background: linear-gradient(135deg, #ffffff 0%, #fff0f0 100%);
  border-left: 4px solid #ed4014;
}

.failed-calls .stat-value {
  color: #ed4014;
}

.operation-bar {
  margin-bottom: 16px;
  display: flex;
}

.create-button {
  background-color: #2d8cf0;
  border-color: #2d8cf0;
}

.batch-button {
  background-color: #19be6b;
  border-color: #19be6b;
}

.schedule-table {
  margin-bottom: 16px;
}

.call-target-info {
  margin-bottom: 16px;
  background-color: #f8f8f9;
  padding: 12px;
  border-radius: 4px;
}

/* 排程詳情樣式 */
.schedule-detail .ivu-descriptions-item {
  padding: 12px 16px;
}

.schedule-detail .ivu-divider {
  margin: 16px 0;
}
</style>
