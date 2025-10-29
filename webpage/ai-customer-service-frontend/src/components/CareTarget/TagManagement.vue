<template>
  <div class="tag-management">
    <Row :gutter="16">
      <Col span="10">
        <Card>
          <template #title>
            <div class="panel-title">
              <Icon type="ios-pricetags" size="16" />
              <span>新增標籤</span>
            </div>
          </template>
          <Form :model="tagForm" :label-width="80">
            <FormItem label="標籤名稱" required>
              <Input v-model="tagForm.name" placeholder="請輸入標籤名稱" />
            </FormItem>
            <FormItem label="標籤顏色">
              <ColorPicker v-model="tagForm.color" />
            </FormItem>
            <FormItem label="描述">
              <Input
                v-model="tagForm.description"
                type="textarea"
                :rows="3"
                placeholder="請輸入標籤描述"
              />
            </FormItem>
            <FormItem>
              <Button type="primary" @click="saveTag" :loading="tagForm.saving">
                {{ tagForm.id ? "更新標籤" : "新增標籤" }}
              </Button>
              <Button
                style="margin-left: 8px"
                @click="resetTagForm"
                v-if="tagForm.id"
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
              <span>標籤列表</span>
            </div>
          </template>
          <Table
            :columns="tagColumns"
            :data="tagList"
            :loading="isLoading"
            border
          >
            <template #color="{ row }">
              <div
                class="color-preview"
                :style="{ backgroundColor: row.color }"
              ></div>
              <span style="margin-left: 8px">{{ row.color }}</span>
            </template>
            <template #action="{ row }">
              <Button
                type="primary"
                size="small"
                @click="editTag(row)"
                style="margin-right: 5px"
              >
                編輯
              </Button>
              <Button type="error" size="small" @click="deleteTag(row)">
                刪除
              </Button>
            </template>
          </Table>
        </Card>
      </Col>
    </Row>
  </div>
</template>

<script>
export default {
  name: "TagManagement",
  props: {
    tagList: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      isLoading: false,
      tagForm: {
        id: null,
        name: "",
        color: "#2d8cf0",
        description: "",
        saving: false,
      },
      tagColumns: [
        {
          title: "標籤名稱",
          key: "name",
          minWidth: 100,
        },
        {
          title: "標籤顏色",
          slot: "color",
          width: 150,
        },
        {
          title: "描述",
          key: "description",
          minWidth: 150,
        },
        {
          title: "使用次數",
          key: "useCount",
          width: 100,
        },
        {
          title: "操作",
          slot: "action",
          width: 150,
          align: "center",
        },
      ],
    };
  },
  methods: {
    // 保存標籤
    saveTag() {
      if (!this.tagForm.name.trim()) {
        this.$Message.error("請輸入標籤名稱");
        return;
      }

      this.tagForm.saving = true;

      // 模擬API操作
      setTimeout(() => {
        const isEdit = !!this.tagForm.id;

        // 觸發父組件事件
        this.$emit("save-tag", {
          id: this.tagForm.id || `new-${Date.now()}`,
          name: this.tagForm.name,
          color: this.tagForm.color,
          description: this.tagForm.description,
        });

        this.$Message.success(isEdit ? "標籤更新成功！" : "標籤新增成功！");

        this.tagForm.saving = false;
        this.resetTagForm();
      }, 500);
    },

    // 重置標籤表單
    resetTagForm() {
      this.tagForm = {
        id: null,
        name: "",
        color: "#2d8cf0",
        description: "",
        saving: false,
      };
    },

    // 編輯標籤
    editTag(row) {
      this.tagForm = {
        id: row.id,
        name: row.name,
        color: row.color,
        description: row.description,
        saving: false,
      };
    },

    // 刪除標籤
    deleteTag(row) {
      this.$Modal.confirm({
        title: "確認刪除",
        content: `確定要刪除「${row.name}」標籤嗎？此操作不可恢復！`,
        onOk: () => {
          // 觸發父組件事件
          this.$emit("delete-tag", row.id);

          // 模擬API操作
          setTimeout(() => {
            this.$Message.success("標籤已成功刪除");
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

.color-preview {
  display: inline-block;
  width: 16px;
  height: 16px;
  border-radius: 2px;
  vertical-align: middle;
}
</style>
