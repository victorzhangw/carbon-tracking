<!-- components/AudioEditModal.vue -->
<template>
  <Modal
    v-model="isVisible"
    title="編輯錄音資訊"
    :loading="loading"
    @on-ok="handleSave"
    @on-cancel="handleCancel"
  >
    <Form :model="form" :rules="audioRules" ref="audioForm" :label-width="80">
      <FormItem label="名稱" prop="name">
        <Input v-model="form.name" placeholder="請輸入錄音名稱" />
      </FormItem>
      <FormItem label="專員" prop="staff_id">
        <Select
          v-model="form.staff_id"
          filterable
          clearable
          placeholder="選擇專員"
        >
          <Option v-for="staff in staffList" :key="staff.id" :value="staff.id">
            {{ staff.name }} ({{ staff.code }})
          </Option>
        </Select>
      </FormItem>
      <FormItem label="狀態" prop="status">
        <RadioGroup v-model="form.status">
          <Radio label="active">啟用</Radio>
          <Radio label="inactive">停用</Radio>
        </RadioGroup>
      </FormItem>
      <FormItem label="描述" prop="description">
        <Input
          v-model="form.description"
          type="textarea"
          :rows="4"
          placeholder="請輸入描述"
        />
      </FormItem>
    </Form>
  </Modal>
</template>

<script>
export default {
  name: "AudioEditModal",
  props: {
    visible: {
      type: Boolean,
      default: false,
    },
    loading: {
      type: Boolean,
      default: false,
    },
    audioForm: {
      type: Object,
      default: () => ({
        name: "",
        staff_id: "",
        status: "active",
        description: "",
      }),
    },
    staffList: {
      type: Array,
      default: () => [],
    },
  },
  emits: ["update:visible", "save"],
  data() {
    return {
      isVisible: this.visible,
      form: { ...this.audioForm },
      audioRules: {
        name: [
          { required: true, message: "請輸入錄音名稱", trigger: "blur" },
          {
            min: 1,
            max: 100,
            message: "錄音名稱長度應在1-100字符之間",
            trigger: "blur",
          },
        ],
        staff_id: [
          { type: "number", message: "請選擇專員", trigger: "change" },
        ],
        status: [{ required: true, message: "請選擇狀態", trigger: "change" }],
      },
    };
  },
  watch: {
    visible(val) {
      this.isVisible = val;
      if (val) {
        // 當模態框打開時，重置表單數據
        this.resetForm();
      }
    },
    isVisible(val) {
      this.$emit("update:visible", val);
    },
    audioForm: {
      handler(val) {
        if (val && typeof val === "object") {
          this.form = {
            name: val.name || "",
            staff_id: val.staff_id || "",
            status: val.status || "active",
            description: val.description || "",
          };
        }
      },
      deep: true,
      immediate: true,
    },
  },
  methods: {
    handleSave() {
      if (!this.$refs.audioForm) {
        console.error("表單引用不存在");
        return;
      }

      this.$refs.audioForm.validate((valid) => {
        if (valid) {
          // 驗證通過，發送保存事件
          const formData = { ...this.form };
          this.$emit("save", formData);
        } else {
          // 驗證失敗，停止loading狀態
          this.$Message.error("請檢查表單輸入");

          // 通知父組件停止loading
          this.$nextTick(() => {
            this.$emit("update:loading", false);
          });

          return false;
        }
      });
    },

    handleCancel() {
      // 重置表單到初始狀態
      this.resetForm();

      // 清除驗證狀態
      if (this.$refs.audioForm) {
        this.$refs.audioForm.resetFields();
      }
    },

    resetForm() {
      // 重置表單數據到props傳入的初始值
      this.form = {
        name: this.audioForm.name || "",
        staff_id: this.audioForm.staff_id || "",
        status: this.audioForm.status || "active",
        description: this.audioForm.description || "",
      };

      // 清除表單驗證狀態
      this.$nextTick(() => {
        if (this.$refs.audioForm) {
          this.$refs.audioForm.resetFields();
        }
      });
    },

    // 手動驗證特定字段
    validateField(prop) {
      if (this.$refs.audioForm) {
        this.$refs.audioForm.validateField(prop);
      }
    },

    // 清除特定字段驗證
    clearValidation(prop) {
      if (this.$refs.audioForm) {
        if (prop) {
          this.$refs.audioForm.clearValidate(prop);
        } else {
          this.$refs.audioForm.clearValidate();
        }
      }
    },
  },

  mounted() {
    // 組件掛載時初始化表單
    this.resetForm();
  },
};
</script>

<style scoped>
:deep(.ivu-form-item) {
  transition: all 0.3s ease;
  margin-bottom: 20px;
}

:deep(.ivu-input:focus),
:deep(.ivu-input:hover) {
  border-color: #57a3f3;
  box-shadow: 0 0 0 2px rgba(45, 140, 240, 0.2);
  transition: all 0.3s ease;
}

:deep(.ivu-select:hover .ivu-select-selection),
:deep(.ivu-select-focused .ivu-select-selection) {
  border-color: #57a3f3;
  box-shadow: 0 0 0 2px rgba(45, 140, 240, 0.2);
}

:deep(.ivu-modal-content) {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: scale(1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 8px;
}

:deep(.ivu-modal-content:hover) {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

:deep(.ivu-form-item-error-tip) {
  margin-top: 4px;
  font-size: 12px;
}

:deep(.ivu-radio-group) {
  display: flex;
  gap: 15px;
}

:deep(.ivu-textarea) {
  resize: vertical;
  min-height: 80px;
}
</style>
