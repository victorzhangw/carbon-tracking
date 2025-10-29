<!-- components/AudioSearchFilter.vue -->
<template>
  <div class="audio-actions">
    <div class="filter-box">
      <Input
        v-model="keywordValue"
        search
        placeholder="搜尋錄音名稱..."
        @on-search="handleSearch"
        class="search-input"
      />

      <Select
        v-model="staffIdValue"
        placeholder="選擇專員"
        clearable
        @on-change="handleStaffChange"
        style="width: 200px"
      >
        <Option value="">全部專員</Option>
        <Option v-for="staff in staffList" :key="staff.id" :value="staff.id">
          {{ staff.name }} ({{ staff.code }})
        </Option>
      </Select>
    </div>

    <div class="action-buttons">
      <Button type="success" icon="ios-mic" @click="openRecorder"
        >錄製音頻</Button
      >
      <Upload
        :action="uploadUrl"
        :headers="uploadHeaders"
        :format="['mp3', 'wav', 'ogg']"
        :max-size="10240"
        :on-success="handleUploadSuccess"
        :on-error="handleUploadError"
        :on-format-error="handleFormatError"
        :on-exceeded-size="handleMaxSizeExceeded"
        :before-upload="handleBeforeUpload"
        style="display: inline-block"
      >
        <Button type="primary" icon="ios-cloud-upload">上傳錄音</Button>
      </Upload>
      <Button type="default" icon="ios-refresh" @click="$emit('refresh')"
        >重新整理</Button
      >
    </div>
  </div>
</template>

<script>
export default {
  name: "AudioSearchFilter",
  props: {
    keyword: {
      type: String,
      default: "",
    },
    staffId: {
      type: String,
      default: "",
    },
    staffList: {
      type: Array,
      default: () => [],
    },
  },
  emits: [
    "update:keyword",
    "update:staffId",
    "refresh",
    "open-recorder",
    "before-upload",
  ],
  data() {
    return {
      keywordValue: this.keyword,
      staffIdValue: this.staffId,
      uploadUrl: "/api/audio/upload",
      uploadHeaders: {},
    };
  },
  watch: {
    keyword(val) {
      this.keywordValue = val;
    },
    staffId(val) {
      this.staffIdValue = val;
    },
  },
  methods: {
    handleSearch() {
      this.$emit("update:keyword", this.keywordValue);
      this.$emit("refresh");
    },
    handleStaffChange(value) {
      this.$emit("update:staffId", value);
      this.$emit("refresh");
    },
    openRecorder() {
      this.$emit("open-recorder");
    },
    handleBeforeUpload(file) {
      this.$emit("before-upload", file);
      return false; // 阻止自動上傳
    },
    handleUploadSuccess() {
      this.$Message.success("上傳錄音成功");
      this.$emit("refresh");
    },
    handleUploadError(error) {
      const errorMsg = error.response?.data?.error || error.message;
      this.$Message.error(`上傳錄音失敗: ${errorMsg}`);
    },
    handleFormatError() {
      this.$Message.error("檔案格式不支援，僅支援 mp3/wav/ogg 格式");
    },
    handleMaxSizeExceeded() {
      this.$Message.error("檔案大小超過限制 (10MB)");
    },
  },
};
</script>

<style scoped>
.audio-actions {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.filter-box {
  display: flex;
  gap: 10px;
  flex: 1;
  max-width: 550px;
}

.search-input {
  width: 250px;
}

.action-buttons {
  display: flex;
  gap: 10px;
}
</style>
