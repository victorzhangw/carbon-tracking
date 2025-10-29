<template>
  <div class="table-container">
    <div class="table-section">
      <Table
        border
        :columns="tableColumns"
        :data="callRecords"
        :loading="isLoading"
        stripe
        highlight-row
      >
      </Table>
      <div class="pagination-container">
        <Page
          :total="totalRecords"
          :current="currentPage"
          :page-size="pageSize"
          show-total
          show-elevator
          @on-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CallHistoryTable",
  props: {
    callRecords: {
      type: Array,
      required: true,
    },
    isLoading: {
      type: Boolean,
      default: false,
    },
    totalRecords: {
      type: Number,
      default: 0,
    },
    currentPage: {
      type: Number,
      default: 1,
    },
    pageSize: {
      type: Number,
      default: 10,
    },
  },
  data() {
    return {
      tableColumns: [
        {
          title: "序號",
          type: "index",
          width: 70,
          align: "center",
        },
        {
          title: "客戶姓名",
          key: "customerName",
          width: 100,
        },
        {
          title: "聯絡電話",
          key: "phoneNumber",
          width: 130,
        },
        {
          title: "通話時間",
          key: "callTime",
          width: 150,
          sortable: true,
        },
        {
          title: "通話長度",
          key: "duration",
          width: 110,
          sortable: true,
          render: (h, params) => {
            return h("span", {}, params.row.duration + " 分鐘");
          },
        },
        {
          title: "專員姓名",
          key: "staffName",
          width: 100,
        },
        {
          title: "部門",
          key: "department",
          width: 100,
        },
        {
          title: "主要情緒",
          key: "mainEmotion",
          width: 100,
          render: (h, params) => {
            const emotions = {
              positive: { text: "正面", color: "#19be6b" },
              neutral: { text: "中性", color: "#2d8cf0" },
              negative: { text: "負面", color: "#ed4014" },
            };
            const emotion = emotions[params.row.mainEmotion];

            return h(
              "Tag",
              {
                props: {
                  color: emotion.color,
                },
              },
              emotion.text
            );
          },
        },
        {
          title: "跟進狀態",
          key: "followupStatus",
          width: 120,
          filters: [
            { label: "待處理", value: "pending" },
            { label: "處理中", value: "inProgress" },
            { label: "已完成", value: "completed" },
            { label: "無需跟進", value: "noAction" },
          ],
          filterMethod: (value, row) => {
            return row.followupStatus === value;
          },
          render: (h, params) => {
            const status = {
              pending: { text: "待處理", color: "warning" },
              inProgress: { text: "處理中", color: "primary" },
              completed: { text: "已完成", color: "success" },
              noAction: { text: "無需跟進", color: "default" },
            };

            return h(
              "Tag",
              {
                props: {
                  color: status[params.row.followupStatus].color,
                },
              },
              status[params.row.followupStatus].text
            );
          },
        },
        {
          title: "操作",
          key: "action",
          width: 150,
          fixed: "right",
          render: (h, params) => {
            return h("div", [
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small",
                    icon: "ios-eye",
                  },
                  style: {
                    marginRight: "5px",
                  },
                  on: {
                    click: () => {
                      this.$emit("view-detail", params.row);
                    },
                  },
                },
                "詳情"
              ),
              h(
                "Button",
                {
                  props: {
                    type: "warning",
                    size: "small",
                    icon: "ios-create",
                  },
                  on: {
                    click: () => {
                      this.$emit("edit-followup", params.row);
                    },
                  },
                },
                "跟進"
              ),
            ]);
          },
        },
      ],
    };
  },
  methods: {
    handlePageChange(page) {
      this.$emit("page-change", page);
    },
  },
};
</script>

<style scoped>
.table-container {
  width: 100%;
}

.table-section {
  margin-top: 24px;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style>
