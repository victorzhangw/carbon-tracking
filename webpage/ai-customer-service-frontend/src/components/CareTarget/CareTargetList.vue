<template>
  <div class="care-target-list">
    <div class="search-section">
      <Form :model="searchForm" inline>
        <FormItem label="關鍵字">
          <Input
            v-model="searchForm.keyword"
            placeholder="姓名/電話/備註"
            style="width: 200px"
            clearable
          ></Input>
        </FormItem>
        <FormItem label="關懷組別">
          <Select v-model="searchForm.groupId" style="width: 150px" clearable>
            <Option value="">請選擇</Option>
            <Option
              v-for="group in groupList"
              :value="group.id"
              :key="group.id"
            >
              {{ group.name }}
            </Option>
          </Select>
        </FormItem>
        <FormItem label="標籤">
          <Select v-model="searchForm.tagId" style="width: 150px" clearable>
            <Option value="">請選擇</Option>
            <Option v-for="tag in tagList" :value="tag.id" :key="tag.id">
              {{ tag.name }}
            </Option>
          </Select>
        </FormItem>
        <FormItem label=" ">
          <Button
            type="primary"
            icon="ios-search"
            @click="handleSearch"
            :loading="isLoading"
            class="search-button"
            >查詢</Button
          >
          <Button
            style="margin-left: 8px"
            icon="md-refresh"
            @click="handleReset"
            :disabled="isLoading"
            class="reset-button"
            >重置</Button
          >
        </FormItem>
      </Form>
    </div>

    <div class="operation-bar">
      <Button
        type="primary"
        icon="md-add"
        @click="handleCreate"
        class="create-button"
        >新增關懷對象</Button
      >
      <Button
        type="success"
        icon="md-cloud-upload"
        style="margin-left: 8px"
        @click="handleShowImport"
        >批量匯入</Button
      >
      <Button
        type="info"
        icon="md-download"
        style="margin-left: 8px"
        @click="handleExport"
        >匯出數據</Button
      >
      <div class="batch-operation" v-if="selection.length > 0">
        <Divider type="vertical" />
        <span class="selected-count">已選 {{ selection.length }} 項</span>
        <Button
          type="warning"
          size="small"
          style="margin-left: 8px"
          @click="handleBatchTag"
          >批量標籤</Button
        >
        <Button
          type="info"
          size="small"
          style="margin-left: 8px"
          @click="handleBatchGroup"
          >批量分組</Button
        >
        <Button
          type="error"
          size="small"
          style="margin-left: 8px"
          @click="handleBatchDelete"
          >批量刪除</Button
        >
      </div>
    </div>

    <!-- 關懷對象表格 -->
    <Table
      :columns="tableColumns"
      :data="targetList"
      :loading="isLoading"
      stripe
      border
      class="target-table"
      @on-selection-change="handleSelectionChange"
    >
      <template #tags="{ row }">
        <div class="tag-list">
          <Tag
            v-for="tag in row.tags"
            :key="tag.id"
            :color="tag.color"
            class="target-tag"
          >
            {{ tag.name }}
          </Tag>
          <Button
            type="dashed"
            size="small"
            icon="md-add"
            v-if="row.tags.length < 5"
            @click="handleAddTag(row)"
            >標籤</Button
          >
        </div>
      </template>
      <template #group="{ row }">
        <div>
          <Tag color="blue" v-if="row.group">{{ row.group.name }}</Tag>
          <Button
            type="dashed"
            size="small"
            icon="md-add"
            v-if="!row.group"
            @click="handleAssignGroup(row)"
            >分組</Button
          >
        </div>
      </template>
      <template #action="{ row }">
        <Button
          type="primary"
          size="small"
          style="margin-right: 5px"
          @click="handleViewDetail(row)"
          >詳情</Button
        >
        <Button
          type="info"
          size="small"
          style="margin-right: 5px"
          @click="handleEdit(row)"
          >編輯</Button
        >
        <Button type="error" size="small" @click="handleDelete(row)"
          >刪除</Button
        >
      </template>
    </Table>

    <div class="pagination" style="margin-top: 20px; text-align: right">
      <Page
        :total="totalTargets"
        :current="currentPage"
        :page-size="pageSize"
        @on-change="handlePageChange"
        show-total
        show-elevator
      ></Page>
    </div>

    <!-- 新增/編輯關懷對象 Modal -->
    <Modal
      v-model="targetModal.visible"
      :title="targetModal.isEdit ? '編輯關懷對象' : '新增關懷對象'"
      :mask-closable="false"
      width="650"
    >
      <Form :model="targetModal.form" :label-width="100">
        <FormItem label="姓名" required>
          <Input v-model="targetModal.form.name" placeholder="請輸入姓名" />
        </FormItem>
        <FormItem label="聯絡電話" required>
          <Input
            v-model="targetModal.form.phone"
            placeholder="請輸入聯絡電話"
          />
        </FormItem>
        <Row>
          <Col span="12">
            <FormItem label="年齡" :label-width="100">
              <InputNumber
                v-model="targetModal.form.age"
                :min="0"
                :max="150"
                style="width: 100%"
              ></InputNumber>
            </FormItem>
          </Col>
          <Col span="12">
            <FormItem label="性別" :label-width="100">
              <RadioGroup v-model="targetModal.form.gender">
                <Radio label="male">男</Radio>
                <Radio label="female">女</Radio>
                <Radio label="other">其他</Radio>
              </RadioGroup>
            </FormItem>
          </Col>
        </Row>
        <FormItem label="地址">
          <Input v-model="targetModal.form.address" placeholder="請輸入地址" />
        </FormItem>
        <FormItem label="關懷組別">
          <Select v-model="targetModal.form.groupId" style="width: 100%">
            <Option value="">無組別</Option>
            <Option
              v-for="group in groupList"
              :value="group.id"
              :key="group.id"
            >
              {{ group.name }}
            </Option>
          </Select>
        </FormItem>
        <FormItem label="標籤">
          <Select
            v-model="targetModal.form.tagIds"
            style="width: 100%"
            multiple
            max-tag-count="3"
          >
            <Option v-for="tag in tagList" :value="tag.id" :key="tag.id">
              {{ tag.name }}
            </Option>
          </Select>
        </FormItem>
        <FormItem label="備註">
          <Input
            type="textarea"
            v-model="targetModal.form.notes"
            :rows="4"
            placeholder="請輸入備註..."
          ></Input>
        </FormItem>
      </Form>
      <template #footer>
        <Button @click="targetModal.visible = false">取消</Button>
        <Button type="primary" @click="saveTarget" :loading="targetModal.saving"
          >確定</Button
        >
      </template>
    </Modal>

    <!-- 關懷對象詳情 Modal -->
    <Modal
      v-model="detailModal.visible"
      title="關懷對象詳情"
      :mask-closable="false"
      width="700"
    >
      <div class="target-detail" v-if="detailModal.target">
        <Descriptions border>
          <DescriptionsItem label="編號">{{
            detailModal.target.id
          }}</DescriptionsItem>
          <DescriptionsItem label="姓名">{{
            detailModal.target.name
          }}</DescriptionsItem>
          <DescriptionsItem label="聯絡電話">{{
            detailModal.target.phone
          }}</DescriptionsItem>
          <DescriptionsItem label="年齡" v-if="detailModal.target.age"
            >{{ detailModal.target.age }} 歲</DescriptionsItem
          >
          <DescriptionsItem label="性別" v-if="detailModal.target.gender">
            {{
              { male: "男", female: "女", other: "其他" }[
                detailModal.target.gender
              ]
            }}
          </DescriptionsItem>
          <DescriptionsItem label="地址" v-if="detailModal.target.address">{{
            detailModal.target.address
          }}</DescriptionsItem>
          <DescriptionsItem label="關懷組別" v-if="detailModal.target.group">{{
            detailModal.target.group.name
          }}</DescriptionsItem>
          <DescriptionsItem label="建立日期">{{
            detailModal.target.createdAt
          }}</DescriptionsItem>
          <DescriptionsItem label="最後更新">{{
            detailModal.target.updatedAt
          }}</DescriptionsItem>
          <DescriptionsItem
            label="標籤"
            v-if="detailModal.target.tags && detailModal.target.tags.length"
          >
            <Tag
              v-for="tag in detailModal.target.tags"
              :key="tag.id"
              :color="tag.color"
              class="target-tag"
            >
              {{ tag.name }}
            </Tag>
          </DescriptionsItem>
          <DescriptionsItem label="備註" v-if="detailModal.target.notes">{{
            detailModal.target.notes
          }}</DescriptionsItem>
        </Descriptions>

        <div
          class="call-history"
          v-if="detailModal.callHistory && detailModal.callHistory.length"
        >
          <Divider orientation="left">通話記錄</Divider>
          <Table
            :columns="callHistoryColumns"
            :data="detailModal.callHistory"
            size="small"
            border
          ></Table>
        </div>
      </div>
      <template #footer>
        <Button @click="detailModal.visible = false">關閉</Button>
        <Button
          type="primary"
          @click="handleEdit(detailModal.target)"
          v-if="detailModal.target"
          >編輯</Button
        >
      </template>
    </Modal>

    <!-- 批量標籤 Modal -->
    <Modal
      v-model="batchTagModal.visible"
      title="批量設置標籤"
      :mask-closable="false"
      width="500"
    >
      <Form>
        <FormItem label="選擇標籤" label-width="80">
          <Select
            v-model="batchTagModal.tagIds"
            style="width: 100%"
            multiple
            placeholder="請選擇要添加的標籤"
          >
            <Option v-for="tag in tagList" :value="tag.id" :key="tag.id">
              {{ tag.name }}
            </Option>
          </Select>
        </FormItem>
        <FormItem label="操作方式" label-width="80">
          <RadioGroup v-model="batchTagModal.action">
            <Radio label="add">添加標籤（保留已有標籤）</Radio>
            <Radio label="replace">替換標籤（清除已有標籤）</Radio>
          </RadioGroup>
        </FormItem>
      </Form>
      <template #footer>
        <Button @click="batchTagModal.visible = false">取消</Button>
        <Button
          type="primary"
          @click="applyBatchTags"
          :loading="batchTagModal.saving"
          :disabled="batchTagModal.tagIds.length === 0"
          >確定</Button
        >
      </template>
    </Modal>

    <!-- 批量分組 Modal -->
    <Modal
      v-model="batchGroupModal.visible"
      title="批量設置分組"
      :mask-closable="false"
      width="500"
    >
      <Form>
        <FormItem label="選擇組別" label-width="80">
          <Select
            v-model="batchGroupModal.groupId"
            style="width: 100%"
            placeholder="請選擇要設置的組別"
          >
            <Option value="">無組別（清除已有組別）</Option>
            <Option
              v-for="group in groupList"
              :value="group.id"
              :key="group.id"
            >
              {{ group.name }}
            </Option>
          </Select>
        </FormItem>
      </Form>
      <template #footer>
        <Button @click="batchGroupModal.visible = false">取消</Button>
        <Button
          type="primary"
          @click="applyBatchGroup"
          :loading="batchGroupModal.saving"
          >確定</Button
        >
      </template>
    </Modal>

    <!-- 添加標籤 Modal -->
    <Modal
      v-model="addTagModal.visible"
      title="添加標籤"
      :mask-closable="false"
      width="500"
    >
      <Form>
        <FormItem label="選擇標籤" label-width="80">
          <Select
            v-model="addTagModal.tagIds"
            style="width: 100%"
            multiple
            placeholder="請選擇要添加的標籤"
          >
            <Option v-for="tag in availableTags" :value="tag.id" :key="tag.id">
              {{ tag.name }}
            </Option>
          </Select>
        </FormItem>
      </Form>
      <template #footer>
        <Button @click="addTagModal.visible = false">取消</Button>
        <Button
          type="primary"
          @click="saveAddTag"
          :loading="addTagModal.saving"
          :disabled="addTagModal.tagIds.length === 0"
          >確定</Button
        >
      </template>
    </Modal>

    <!-- 分配組別 Modal -->
    <Modal
      v-model="assignGroupModal.visible"
      title="分配組別"
      :mask-closable="false"
      width="500"
    >
      <Form>
        <FormItem label="選擇組別" label-width="80">
          <Select
            v-model="assignGroupModal.groupId"
            style="width: 100%"
            placeholder="請選擇要設置的組別"
          >
            <Option
              v-for="group in groupList"
              :value="group.id"
              :key="group.id"
            >
              {{ group.name }}
            </Option>
          </Select>
        </FormItem>
      </Form>
      <template #footer>
        <Button @click="assignGroupModal.visible = false">取消</Button>
        <Button
          type="primary"
          @click="saveAssignGroup"
          :loading="assignGroupModal.saving"
          :disabled="!assignGroupModal.groupId"
          >確定</Button
        >
      </template>
    </Modal>
  </div>
</template>

<script>
export default {
  name: "CareTargetList",
  props: {
    groupList: {
      type: Array,
      default: () => [],
    },
    tagList: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      searchForm: {
        keyword: "",
        groupId: "",
        tagId: "",
      },
      isLoading: false,
      currentPage: 1,
      pageSize: 10,
      totalTargets: 0,
      targetList: [],
      selection: [],

      // 表格列定義
      tableColumns: [
        {
          type: "selection",
          width: 60,
          align: "center",
        },
        {
          title: "姓名",
          key: "name",
          minWidth: 100,
        },
        {
          title: "聯絡電話",
          key: "phone",
          width: 120,
        },
        {
          title: "年齡",
          key: "age",
          width: 80,
        },
        {
          title: "性別",
          key: "genderText",
          width: 80,
        },
        {
          title: "關懷組別",
          slot: "group",
          width: 120,
        },
        {
          title: "標籤",
          slot: "tags",
          minWidth: 200,
        },
        {
          title: "操作",
          slot: "action",
          width: 180,
          align: "center",
        },
      ],

      // 新增/編輯關懷對象 Modal
      targetModal: {
        visible: false,
        isEdit: false,
        saving: false,
        form: {
          id: null,
          name: "",
          phone: "",
          age: null,
          gender: "other",
          address: "",
          groupId: "",
          tagIds: [],
          notes: "",
        },
      },

      // 詳情 Modal
      detailModal: {
        visible: false,
        target: null,
        callHistory: [],
      },

      // 批量標籤 Modal
      batchTagModal: {
        visible: false,
        tagIds: [],
        action: "add",
        saving: false,
      },

      // 批量分組 Modal
      batchGroupModal: {
        visible: false,
        groupId: "",
        saving: false,
      },

      // 添加標籤 Modal
      addTagModal: {
        visible: false,
        target: null,
        tagIds: [],
        saving: false,
      },

      // 分配組別 Modal
      assignGroupModal: {
        visible: false,
        target: null,
        groupId: "",
        saving: false,
      },

      // 通話記錄列定義
      callHistoryColumns: [
        {
          title: "撥打時間",
          key: "callTime",
          width: 150,
        },
        {
          title: "通話時長",
          key: "duration",
          width: 100,
        },
        {
          title: "專員",
          key: "staffName",
          width: 100,
        },
        {
          title: "情緒分析",
          key: "emotionType",
          width: 100,
        },
        {
          title: "備註",
          key: "notes",
          minWidth: 150,
        },
      ],
    };
  },

  computed: {
    // 可用於添加的標籤（未被目標擁有的標籤）
    availableTags() {
      if (!this.addTagModal.target || !this.addTagModal.target.tags) {
        return this.tagList;
      }

      const existingTagIds = this.addTagModal.target.tags.map((tag) => tag.id);
      return this.tagList.filter((tag) => !existingTagIds.includes(tag.id));
    },
  },

  mounted() {
    this.fetchTargets();
  },

  methods: {
    // 獲取關懷對象列表
    fetchTargets() {
      this.isLoading = true;

      // 模擬 API 獲取關懷對象列表
      setTimeout(() => {
        // 生成模擬數據
        const mockData = this.generateMockTargets();

        this.targetList = mockData.items;
        this.totalTargets = mockData.total;

        this.isLoading = false;
      }, 800);
    },

    // 生成模擬關懷對象數據
    generateMockTargets() {
      const mockData = [];
      const total = 85; // 模擬總數據量

      // 預設標籤
      const tags = [
        { id: "1", name: "高齡", color: "#2d8cf0" },
        { id: "2", name: "獨居", color: "#ff9900" },
        { id: "3", name: "慢性病", color: "#19be6b" },
        { id: "4", name: "行動不便", color: "#ed4014" },
        { id: "5", name: "需關懷", color: "#9c27b0" },
      ];

      // 預設分組
      const groups = [
        { id: "1", name: "高齡長者" },
        { id: "2", name: "慢性病患者" },
        { id: "3", name: "獨居老人" },
        { id: "4", name: "行動不便" },
        { id: "5", name: "社區新成員" },
      ];

      // 生成模擬資料
      for (let i = 1; i <= total; i++) {
        // 隨機性別
        const gender = ["male", "female", "other"][
          Math.floor(Math.random() * 3)
        ];
        const genderText = { male: "男", female: "女", other: "其他" }[gender];

        // 隨機年齡（50-90歲）
        const age = Math.floor(Math.random() * 40) + 50;

        // 隨機分配標籤（0-3個）
        const tagCount = Math.floor(Math.random() * 4);
        const shuffledTags = [...tags].sort(() => Math.random() - 0.5);
        const targetTags = shuffledTags.slice(0, tagCount);

        // 隨機分配組別（有 25% 的機率沒有組別）
        const hasGroup = Math.random() > 0.25;
        const group = hasGroup
          ? groups[Math.floor(Math.random() * groups.length)]
          : null;

        // 創建模擬數據
        mockData.push({
          id: `T${String(i).padStart(5, "0")}`,
          name: [
            "陳○○",
            "王○○",
            "呂○○",
            "李○○",
            "張○○",
            "林○○",
            "黃○○",
            "劉○○",
            "吳○○",
            "蔡○○",
          ][Math.floor(Math.random() * 10)],
          phone: [
            "0912XX5678",
            "0923XX6789",
            "0934XX7890",
            "0945XX8901",
            "0956XX9012",
            "0967XX0123",
            "0978XX1234",
            "0989XX2345",
            "0910XX3456",
            "0921XX4567",
          ][Math.floor(Math.random() * 10)],
          age,
          gender,
          genderText,
          address: [
            "台北市松山區松山路123號",
            "新北市板橋區板橋路456號",
            "台中市西區西區路789號",
          ][Math.floor(Math.random() * 3)],
          group,
          tags: targetTags,
          notes: "定期關懷對象，需要持續追蹤。",
          createdAt: "2025-03-15 10:30:45",
          updatedAt: "2025-05-10 15:20:30",
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

    // 處理分頁變更
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchTargets();
    },

    // 查詢關懷對象
    handleSearch() {
      this.currentPage = 1;
      this.fetchTargets();
    },

    // 重置搜索
    handleReset() {
      this.searchForm = {
        keyword: "",
        groupId: "",
        tagId: "",
      };
      this.currentPage = 1;
      this.fetchTargets();
    },

    // 處理表格選擇變更
    handleSelectionChange(selection) {
      this.selection = selection;
    },

    // 顯示新增關懷對象模態框
    handleCreate() {
      this.targetModal.isEdit = false;
      this.targetModal.form = {
        id: null,
        name: "",
        phone: "",
        age: null,
        gender: "other",
        address: "",
        groupId: "",
        tagIds: [],
        notes: "",
      };
      this.targetModal.visible = true;
    },

    // 顯示編輯關懷對象模態框
    handleEdit(row) {
      this.targetModal.isEdit = true;

      // 設置表單值
      this.targetModal.form = {
        id: row.id,
        name: row.name,
        phone: row.phone,
        age: row.age,
        gender: row.gender,
        address: row.address,
        groupId: row.group ? row.group.id : "",
        tagIds: row.tags ? row.tags.map((tag) => tag.id) : [],
        notes: row.notes,
      };

      this.targetModal.visible = true;

      // 如果是從詳情頁編輯，關閉詳情模態框
      if (this.detailModal.visible) {
        this.detailModal.visible = false;
      }
    },

    // 保存關懷對象
    saveTarget() {
      // 表單驗證
      if (!this.targetModal.form.name.trim()) {
        this.$Message.error("請輸入姓名");
        return;
      }

      if (!this.targetModal.form.phone.trim()) {
        this.$Message.error("請輸入聯絡電話");
        return;
      }

      this.targetModal.saving = true;

      // 模擬API保存操作
      setTimeout(() => {
        // 成功提示
        this.$Message.success({
          content: this.targetModal.isEdit
            ? "關懷對象更新成功！"
            : "關懷對象新增成功！",
          duration: 3,
        });

        this.targetModal.saving = false;
        this.targetModal.visible = false;

        // 重新獲取列表
        this.fetchTargets();
      }, 800);
    },

    // 查看關懷對象詳情
    handleViewDetail(row) {
      this.detailModal.target = { ...row };

      // 模擬獲取通話記錄
      this.detailModal.callHistory = [
        {
          callTime: "2025-05-15 14:30:25",
          duration: "8分鐘",
          staffName: "C220001",
          emotionType: "正面",
          notes: "對象心情良好，反應積極。",
        },
        {
          callTime: "2025-04-20 11:15:40",
          duration: "12分鐘",
          staffName: "C220002",
          emotionType: "中性",
          notes: "一般日常問候，無特殊情況。",
        },
        {
          callTime: "2025-03-10 09:45:12",
          duration: "5分鐘",
          staffName: "C230003",
          emotionType: "負面",
          notes: "對象感到不適，已安排社工前往訪視。",
        },
      ];

      this.detailModal.visible = true;
    },

    // 刪除關懷對象
    handleDelete(row) {
      this.$Modal.confirm({
        title: "確認刪除",
        content: `確定要刪除 ${row.name} 的資料嗎？此操作不可恢復！`,
        onOk: () => {
          // 模擬API操作
          setTimeout(() => {
            this.$Message.success("關懷對象已成功刪除");
            this.fetchTargets();
          }, 500);
        },
      });
    },

    // 批量刪除關懷對象
    handleBatchDelete() {
      if (this.selection.length === 0) {
        this.$Message.warning("請至少選擇一個關懷對象");
        return;
      }

      this.$Modal.confirm({
        title: "確認批量刪除",
        content: `確定要刪除選中的 ${this.selection.length} 個關懷對象嗎？此操作不可恢復！`,
        onOk: () => {
          // 模擬API操作
          setTimeout(() => {
            this.$Message.success(
              `成功刪除 ${this.selection.length} 個關懷對象`
            );
            this.selection = [];
            this.fetchTargets();
          }, 800);
        },
      });
    },

    // 顯示批量標籤模態框
    handleBatchTag() {
      if (this.selection.length === 0) {
        this.$Message.warning("請至少選擇一個關懷對象");
        return;
      }

      this.batchTagModal.tagIds = [];
      this.batchTagModal.action = "add";
      this.batchTagModal.visible = true;
    },

    // 應用批量標籤
    applyBatchTags() {
      if (this.batchTagModal.tagIds.length === 0) {
        this.$Message.warning("請至少選擇一個標籤");
        return;
      }

      this.batchTagModal.saving = true;

      // 模擬API操作
      setTimeout(() => {
        const action = this.batchTagModal.action === "add" ? "添加" : "設置";
        this.$Message.success(
          `成功為 ${this.selection.length} 個關懷對象${action}標籤`
        );

        this.batchTagModal.saving = false;
        this.batchTagModal.visible = false;
        this.selection = [];

        // 重新獲取列表
        this.fetchTargets();
      }, 800);
    },

    // 顯示批量分組模態框
    handleBatchGroup() {
      if (this.selection.length === 0) {
        this.$Message.warning("請至少選擇一個關懷對象");
        return;
      }

      this.batchGroupModal.groupId = "";
      this.batchGroupModal.visible = true;
    },

    // 應用批量分組
    applyBatchGroup() {
      this.batchGroupModal.saving = true;

      // 模擬API操作
      setTimeout(() => {
        const action = this.batchGroupModal.groupId ? "設置為" : "移除";
        const groupName = this.batchGroupModal.groupId
          ? this.groupList.find((g) => g.id === this.batchGroupModal.groupId)
              ?.name
          : "無";

        this.$Message.success(
          `成功將 ${this.selection.length} 個關懷對象的組別${action}「${groupName}」`
        );

        this.batchGroupModal.saving = false;
        this.batchGroupModal.visible = false;
        this.selection = [];

        // 重新獲取列表
        this.fetchTargets();
      }, 800);
    },

    // 顯示添加標籤模態框
    handleAddTag(row) {
      this.addTagModal.target = row;
      this.addTagModal.tagIds = [];
      this.addTagModal.visible = true;
    },

    // 保存添加標籤
    saveAddTag() {
      if (this.addTagModal.tagIds.length === 0) {
        this.$Message.warning("請至少選擇一個標籤");
        return;
      }

      this.addTagModal.saving = true;

      // 模擬API操作
      setTimeout(() => {
        this.$Message.success(
          `成功為 ${this.addTagModal.target.name} 添加標籤`
        );

        this.addTagModal.saving = false;
        this.addTagModal.visible = false;

        // 重新獲取列表
        this.fetchTargets();
      }, 500);
    },

    // 顯示分配組別模態框
    handleAssignGroup(row) {
      this.assignGroupModal.target = row;
      this.assignGroupModal.groupId = "";
      this.assignGroupModal.visible = true;
    },

    // 保存分配組別
    saveAssignGroup() {
      if (!this.assignGroupModal.groupId) {
        this.$Message.warning("請選擇一個組別");
        return;
      }

      this.assignGroupModal.saving = true;

      // 模擬API操作
      setTimeout(() => {
        const groupName = this.groupList.find(
          (g) => g.id === this.assignGroupModal.groupId
        )?.name;
        this.$Message.success(
          `成功將 ${this.assignGroupModal.target.name} 分配到「${groupName}」組別`
        );

        this.assignGroupModal.saving = false;
        this.assignGroupModal.visible = false;

        // 重新獲取列表
        this.fetchTargets();
      }, 500);
    },

    // 匯出數據
    handleExport() {
      this.$emit("export");
    },

    // 顯示匯入介面
    handleShowImport() {
      this.$emit("show-import");
    },
  },
};
</script>

<style scoped>
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

.operation-bar {
  margin-bottom: 16px;
  display: flex;
  align-items: center;
}

.target-table {
  margin-bottom: 16px;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
}

.target-tag {
  margin: 2px 4px 2px 0;
}

.batch-operation {
  display: flex;
  align-items: center;
  margin-left: auto;
}

.selected-count {
  font-size: 13px;
  color: #515a6e;
}
</style>
