<!-- StaffManagement.vue -->
<template>
  <div class="staff-management">
    <Card class="staff-card" :bordered="false">
      <template #title>
        <div class="card-title">
          <Icon type="ios-people" size="24" />
          <span>客服專員管理</span>
        </div>
      </template>

      <div class="staff-actions">
        <div class="search-box">
          <Input
            v-model="searchKeyword"
            search
            placeholder="搜尋專員姓名或代號..."
            @on-search="refreshData(true)"
          />
        </div>
        <div class="action-buttons">
          <Button type="primary" icon="ios-add" @click="openStaffModal('add')"
            >新增專員</Button
          >
          <Button type="default" icon="ios-refresh" @click="refreshData(true)"
            >重新整理</Button
          >
        </div>
      </div>

      <div class="staff-table">
        <Table :loading="loading" border :columns="columns" :data="staffList">
          <template #status="{ row }">
            <Tag :color="row.status === 'active' ? 'success' : 'default'">
              {{ row.status === "active" ? "啟用" : "停用" }}
            </Tag>
          </template>
          <template #action="{ row }">
            <div class="action-group">
              <Button
                type="primary"
                size="small"
                @click="openStaffModal('edit', row)"
                >編輯</Button
              >
              <Poptip
                confirm
                title="確定要刪除此專員嗎？"
                @on-ok="deleteStaff(row.id)"
              >
                <Button type="error" size="small">刪除</Button>
              </Poptip>
            </div>
          </template>
        </Table>

        <div class="pagination">
          <Page
            :total="total"
            :current="page"
            :page-size="pageSize"
            show-total
            show-elevator
            @on-change="onPageChange"
          />
        </div>
      </div>

      <Modal
        v-model="staffModalVisible"
        :title="staffModalType === 'add' ? '新增客服專員' : '編輯客服專員'"
        :loading="modalLoading"
        @on-ok="handleSaveStaff"
        @on-cancel="staffModalVisible = false"
      >
        <Form
          :model="staffForm"
          :rules="staffRules"
          ref="staffForm"
          :label-width="80"
        >
          <FormItem label="姓名" prop="name">
            <Input v-model="staffForm.name" placeholder="請輸入姓名" />
          </FormItem>
          <FormItem label="代號" prop="code">
            <Input
              v-model="staffForm.code"
              placeholder="請輸入專員代號"
              :disabled="staffModalType === 'edit'"
            />
          </FormItem>
          <FormItem label="電話" prop="phone">
            <Input v-model="staffForm.phone" placeholder="請輸入聯絡電話" />
          </FormItem>
          <FormItem label="電子郵件" prop="email">
            <Input v-model="staffForm.email" placeholder="請輸入電子郵件" />
          </FormItem>
          <FormItem label="狀態" prop="status">
            <RadioGroup v-model="staffForm.status">
              <Radio label="active">啟用</Radio>
              <Radio label="inactive">停用</Radio>
            </RadioGroup>
          </FormItem>
          <FormItem label="描述" prop="description">
            <Input
              v-model="staffForm.description"
              type="textarea"
              :rows="4"
              placeholder="請輸入描述"
            />
          </FormItem>
        </Form>
      </Modal>
    </Card>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "StaffManagement",
  data() {
    return {
      loading: false,
      modalLoading: false,
      staffList: [],
      total: 0,
      page: 1,
      pageSize: 10,
      searchKeyword: "",

      staffModalVisible: false,
      staffModalType: "add", // 'add' or 'edit'
      staffForm: {
        id: "",
        name: "",
        code: "",
        phone: "",
        email: "",
        status: "active",
        description: "",
      },
      staffRules: {
        name: [{ required: true, message: "請輸入姓名", trigger: "blur" }],
        code: [{ required: true, message: "請輸入專員代號", trigger: "blur" }],
      },

      columns: [
        { title: "姓名", key: "name", width: 120 },
        { title: "代號", key: "code", width: 120 },
        { title: "電話", key: "phone", width: 150 },
        { title: "電子郵件", key: "email", width: 200 },
        {
          title: "狀態",
          slot: "status",
          width: 100,
        },
        {
          title: "建立時間",
          key: "created_at",
          width: 170,
          render: (h, params) => {
            return h("span", this.formatDateTime(params.row.created_at));
          },
        },
        {
          title: "更新時間",
          key: "updated_at",
          width: 170,
          render: (h, params) => {
            return h("span", this.formatDateTime(params.row.updated_at));
          },
        },
        { title: "描述", key: "description", minWidth: 200 },
        {
          title: "操作",
          slot: "action",
          fixed: "right",
          width: 150,
          align: "center",
        },
      ],
    };
  },
  created() {
    this.refreshData();
  },
  methods: {
    formatDateTime(dateTimeStr) {
      if (!dateTimeStr) return "-";

      try {
        const date = new Date(dateTimeStr);
        return date.toLocaleString("zh-TW");
      } catch (e) {
        return dateTimeStr;
      }
    },

    async refreshData(resetPage = false) {
      if (resetPage) {
        this.page = 1;
      }

      this.loading = true;
      try {
        const response = await axios.get("/api/staff", {
          params: {
            page: this.page,
            size: this.pageSize,
            keyword: this.searchKeyword,
          },
        });

        this.staffList = response.data.items || [];
        this.total = response.data.total || 0;
      } catch (error) {
        this.$Message.error("獲取客服專員列表失敗");
        console.error("獲取客服專員列表失敗:", error);
      } finally {
        this.loading = false;
      }
    },

    onPageChange(page) {
      this.page = page;
      this.refreshData();
    },

    resetStaffForm() {
      this.staffForm = {
        id: "",
        name: "",
        code: "",
        phone: "",
        email: "",
        status: "active",
        description: "",
      };
      if (this.$refs.staffForm) {
        this.$refs.staffForm.resetFields();
      }
    },

    openStaffModal(type, staff = null) {
      this.staffModalType = type;
      this.resetStaffForm();

      if (type === "edit" && staff) {
        this.staffForm = { ...staff };
      }

      this.staffModalVisible = true;
      this.$nextTick(() => {
        this.$refs.staffForm.resetFields();
      });
    },

    async handleSaveStaff() {
      this.$refs.staffForm.validate(async (valid) => {
        if (!valid) {
          this.modalLoading = false;
          return false;
        }

        this.modalLoading = true;
        try {
          if (this.staffModalType === "add") {
            await this.addStaff();
          } else {
            await this.updateStaff();
          }

          this.staffModalVisible = false;
          this.refreshData();
          this.$Message.success(
            `${this.staffModalType === "add" ? "新增" : "更新"}客服專員成功`
          );
        } catch (error) {
          const errorMsg = error.response?.data?.error || error.message;
          this.$Message.error(
            `${
              this.staffModalType === "add" ? "新增" : "更新"
            }客服專員失敗: ${errorMsg}`
          );
        } finally {
          this.modalLoading = false;
        }
      });
    },

    async addStaff() {
      return axios.post("/api/staff", this.staffForm);
    },

    async updateStaff() {
      return axios.put(`/api/staff/${this.staffForm.id}`, this.staffForm);
    },

    async deleteStaff(id) {
      this.loading = true;
      try {
        await axios.delete(`/api/staff/${id}`);
        this.$Message.success("刪除客服專員成功");
        this.refreshData();
      } catch (error) {
        const errorMsg = error.response?.data?.error || error.message;
        this.$Message.error(`刪除客服專員失敗: ${errorMsg}`);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.staff-management {
  max-width: 1200px;
  margin: 0 auto;
}

.staff-card {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.staff-card:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

.card-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  color: #17233d;
}

.staff-actions {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.search-box {
  width: 300px;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.staff-table {
  background-color: #fff;
  border-radius: 4px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.action-group {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.action-group button {
  transition: all 0.2s ease;
}

.action-group button:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* Animation for table rows */
.ivu-table-row {
  transition: background-color 0.3s ease;
}

.ivu-table-row:hover td {
  background-color: #f0faff !important;
}

/* Form item animations */
.ivu-form-item {
  transition: all 0.3s ease;
}

.ivu-input:focus,
.ivu-input:hover {
  border-color: #57a3f3;
  box-shadow: 0 0 0 2px rgba(45, 140, 240, 0.2);
}

/* Modal animations */
.ivu-modal-content {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: scale(1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.ivu-modal-content:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}
</style>
