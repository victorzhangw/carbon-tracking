<template>
  <div class="group-management">
    <Row :gutter="16">
      <Col span="10">
        <Card>
          <template #title>
            <div class="panel-title">
              <Icon type="ios-folder" size="16" />
              <span>新增分組</span>
            </div>
          </template>
          <Form :model="groupForm" :label-width="80">
            <FormItem label="組別名稱" required>
              <Input v-model="groupForm.name" placeholder="請輸入組別名稱" />
            </FormItem>
            <FormItem label="描述">
              <Input
                v-model="groupForm.description"
                type="textarea"
                :rows="3"
                placeholder="請輸入組別描述"
              />
            </FormItem>
            <FormItem>
              <Button
                type="primary"
                @click="saveGroup"
                :loading="groupForm.saving"
              >
                {{ groupForm.id ? "更新組別" : "新增組別" }}
              </Button>
              <Button
                style="margin-left: 8px"
                @click="resetGroupForm"
                v-if="groupForm.id"
              >
                取消編輯
              </Button>
            </FormItem>
          </Form>
        </Card>
      </Col>
      <Col span="14">
        <Card>
          <template #title>
            <div class="panel-title">
              <Icon type="ios-list" size="16" />
              <span>組別列表</span>
            </div>
          </template>
          <Table
            :columns="groupColumns"
            :data="groupList"
            :loading="isLoading"
            border
          >
            <template #count="{ row }">
              <Badge
                :count="row.count"
                :overflow-count="999"
                type="primary"
              ></Badge>
            </template>
            <template #action="{ row }">
              <Button
                type="primary"
                size="small"
                @click="editGroup(row)"
                style="margin-right: 5px"
              >
                編輯
              </Button>
              <Button
                type="info"
                size="small"
                @click="viewGroupMembers(row)"
                style="margin-right: 5px"
              >
                查看成員
              </Button>
              <Button type="error" size="small" @click="deleteGroup(row)">
                刪除
              </Button>
            </template>
          </Table>
        </Card>
      </Col>
    </Row>

    <!-- 組別成員 Modal -->
    <Modal
      v-model="groupMembersModal.visible"
      :title="
        groupMembersModal.group
          ? `${groupMembersModal.group.name} - 成員列表`
          : '組別成員'
      "
      width="800"
      footer-hide
    >
      <div v-if="groupMembersModal.group">
        <div class="group-info" style="margin-bottom: 16px">
          <p>
            <strong>組別描述：</strong
            >{{ groupMembersModal.group.description || "無" }}
          </p>
          <p>
            <strong>成員數量：</strong>{{ groupMembersModal.members.length }} 人
          </p>
        </div>
        <Table
          :columns="memberColumns"
          :data="groupMembersModal.members"
          :loading="groupMembersModal.loading"
          border
        >
          <template #action="{ row }">
            <Button type="error" size="small" @click="removeFromGroup(row)">
              移出組別
            </Button>
          </template>
        </Table>
        <div style="margin-top: 16px; text-align: right">
          <Button @click="groupMembersModal.visible = false">關閉</Button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script>
export default {
  name: "GroupManagement",
  props: {
    groupList: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      isLoading: false,
      groupForm: {
        id: null,
        name: "",
        description: "",
        saving: false,
      },
      groupColumns: [
        {
          title: "組別名稱",
          key: "name",
          minWidth: 120,
        },
        {
          title: "描述",
          key: "description",
          minWidth: 200,
        },
        {
          title: "成員數",
          slot: "count",
          width: 100,
        },
        {
          title: "創建日期",
          key: "createdAt",
          width: 150,
        },
        {
          title: "操作",
          slot: "action",
          width: 220,
          align: "center",
        },
      ],

      // 組別成員 Modal
      groupMembersModal: {
        visible: false,
        group: null,
        members: [],
        loading: false,
      },

      // 組別成員列定義
      memberColumns: [
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
          title: "標籤",
          key: "tagText",
          minWidth: 150,
        },
        {
          title: "操作",
          slot: "action",
          width: 100,
          align: "center",
        },
      ],
    };
  },
  methods: {
    // 保存組別
    saveGroup() {
      if (!this.groupForm.name.trim()) {
        this.$Message.error("請輸入組別名稱");
        return;
      }

      this.groupForm.saving = true;

      // 模擬API操作
      setTimeout(() => {
        const isEdit = !!this.groupForm.id;

        // 觸發父組件事件
        this.$emit("save-group", {
          id: this.groupForm.id || `new-${Date.now()}`,
          name: this.groupForm.name,
          description: this.groupForm.description,
          count: this.groupForm.id
            ? this.groupList.find((g) => g.id === this.groupForm.id)?.count || 0
            : 0,
          createdAt: this.groupForm.id
            ? this.groupList.find((g) => g.id === this.groupForm.id)?.createdAt
            : new Date().toISOString().split("T")[0],
        });

        this.$Message.success(isEdit ? "組別更新成功！" : "組別新增成功！");

        this.groupForm.saving = false;
        this.resetGroupForm();
      }, 500);
    },

    // 重置組別表單
    resetGroupForm() {
      this.groupForm = {
        id: null,
        name: "",
        description: "",
        saving: false,
      };
    },

    // 編輯組別
    editGroup(row) {
      this.groupForm = {
        id: row.id,
        name: row.name,
        description: row.description,
        saving: false,
      };
    },

    // 查看組別成員
    viewGroupMembers(row) {
      this.groupMembersModal.group = row;
      this.groupMembersModal.loading = true;
      this.groupMembersModal.visible = true;

      // 模擬API獲取組別成員
      setTimeout(() => {
        // 生成模擬組別成員數據
        const members = [];
        for (let i = 1; i <= row.count; i++) {
          const gender = ["male", "female", "other"][
            Math.floor(Math.random() * 3)
          ];
          const genderText = { male: "男", female: "女", other: "其他" }[
            gender
          ];
          const age = Math.floor(Math.random() * 40) + 50;

          members.push({
            id: `T${String(i).padStart(5, "0")}`,
            name: ["陳○○", "王○○", "呂○○", "李○○", "張○○"][
              Math.floor(Math.random() * 5)
            ],
            phone: ["0912XX5678", "0923XX6789", "0934XX7890", "0945XX8901"][
              Math.floor(Math.random() * 4)
            ],
            age,
            gender,
            genderText,
            tagText: ["高齡", "獨居", "慢性病"][Math.floor(Math.random() * 3)],
          });
        }

        this.groupMembersModal.members = members;
        this.groupMembersModal.loading = false;
      }, 800);
    },

    // 從組別中移除成員
    removeFromGroup(row) {
      this.$Modal.confirm({
        title: "確認移出",
        content: `確定要將 ${row.name} 從「${this.groupMembersModal.group.name}」組別中移出嗎？`,
        onOk: () => {
          // 觸發父組件事件
          this.$emit("remove-from-group", {
            groupId: this.groupMembersModal.group.id,
            targetId: row.id,
          });

          // 模擬API操作
          setTimeout(() => {
            this.$Message.success("成員已成功從組別中移出");

            // 更新介面
            this.groupMembersModal.members =
              this.groupMembersModal.members.filter((m) => m.id !== row.id);

            // 更新組別計數
            if (this.groupMembersModal.group) {
              this.groupMembersModal.group.count--;
            }

            // 如果沒有成員了，關閉模態框
            if (this.groupMembersModal.members.length === 0) {
              this.groupMembersModal.visible = false;
            }
          }, 500);
        },
      });
    },

    // 刪除組別
    deleteGroup(row) {
      this.$Modal.confirm({
        title: "確認刪除",
        content: `確定要刪除「${row.name}」組別嗎？此操作不會刪除組別中的關懷對象，僅解除分組關聯。`,
        onOk: () => {
          // 觸發父組件事件
          this.$emit("delete-group", row.id);

          // 模擬API操作
          setTimeout(() => {
            this.$Message.success("組別已成功刪除");
          }, 500);
        },
      });
    },
  },
};
</script>

<style scoped>
.panel-title {
  display: flex;
  align-items: center;
}

.panel-title span {
  margin-left: 8px;
}
</style>
