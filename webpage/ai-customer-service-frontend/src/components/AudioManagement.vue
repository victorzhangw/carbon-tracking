<!-- AudioManagement.vue -->
<template>
  <div class="audio-management">
    <Card class="audio-card" :bordered="false">
      <template #title>
        <div class="card-title">
          <Icon type="ios-musical-notes" size="24" />
          <span>錄音管理</span>
        </div>
      </template>

      <!-- 搜索和過濾器 -->
      <AudioSearchFilter
        :keyword="searchKeyword"
        :staffId="selectedStaffId"
        :staffList="staffList"
        @update:keyword="searchKeyword = $event"
        @update:staffId="selectedStaffId = $event"
        @refresh="refreshData(true)"
        @open-recorder="openRecorder"
        @before-upload="handleBeforeUpload"
      />

      <!-- 音頻表格 -->
      <AudioTable
        :loading="loading"
        :columns="columns"
        :audioList="audioList"
        @play="playAudio"
        @download="downloadAudio"
        @edit="openAudioModal"
        @edit-audio="editAudio"
        @delete="deleteAudio"
      />

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

      <!-- 音頻播放器彈窗 -->
      <AudioPlayer
        :visible="audioPlayerVisible"
        :audio="currentAudio"
        :src="audioSrc"
        @update:visible="audioPlayerVisible = $event"
        @download="downloadAudio"
      />

      <!-- 編輯錄音彈窗 -->
      <AudioEditModal
        :visible="audioModalVisible"
        :loading="modalLoading"
        :audioForm="audioForm"
        :staffList="staffList"
        @update:visible="audioModalVisible = $event"
        @save="handleSaveAudio"
      />

      <!-- 錄音功能彈窗 -->
      <AudioRecorder
        :visible="recorderModalVisible"
        :staffList="staffList"
        @update:visible="recorderModalVisible = $event"
        @upload-success="handleUploadSuccess"
      />

      <!-- 編輯音頻彈窗 -->
      <AudioEditor
        :visible="editorModalVisible"
        :audioData="editorAudioData"
        @update:visible="editorModalVisible = $event"
        @save="handleSaveEditedAudio"
      />
    </Card>
  </div>
</template>

<script>
import axios from "axios";
import AudioSearchFilter from "@/components/Audio/AudioSearchFilter.vue";
import AudioTable from "@/components/Audio/AudioTable.vue";
import AudioPlayer from "@/components/Audio/AudioPlayer.vue";
import AudioEditModal from "@/components/Audio/AudioEditModal.vue";
import AudioRecorder from "@/components/Audio/AudioRecorder.vue";
import AudioEditor from "@/components/Audio/AudioEditor.vue";

export default {
  name: "AudioManagement",
  components: {
    AudioSearchFilter,
    AudioTable,
    AudioPlayer,
    AudioEditModal,
    AudioRecorder,
    AudioEditor,
  },
  data() {
    return {
      loading: false,
      modalLoading: false,
      audioList: [],
      staffList: [],
      total: 0,
      page: 1,
      pageSize: 10,
      searchKeyword: "",
      selectedStaffId: "",

      audioModalVisible: false,
      audioForm: {
        id: "",
        name: "",
        staff_id: "",
        status: "active",
        description: "",
      },

      audioPlayerVisible: false,
      currentAudio: {},
      audioSrc: "",

      recorderModalVisible: false,

      editorModalVisible: false,
      editorAudioData: null,

      columns: [
        { title: "名稱", key: "name", minWidth: 150 },
        {
          title: "專員",
          slot: "staff",
          width: 150,
        },
        {
          title: "時長",
          slot: "duration",
          width: 100,
        },
        { title: "檔案大小", key: "file_size", width: 100 },
        {
          title: "狀態",
          slot: "status",
          width: 80,
        },
        {
          title: "建立時間",
          key: "created_at",
          width: 170,
          render: (h, params) => {
            return h("span", this.formatDateTime(params.row.created_at));
          },
        },
        { title: "描述", key: "description", minWidth: 150 },
        {
          title: "操作",
          slot: "action",
          fixed: "right",
          width: 220,
          align: "center",
        },
      ],
    };
  },
  created() {
    this.refreshData();
    this.fetchStaffList();
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

    handleBeforeUpload(file) {
      // 攔截上傳，顯示上傳對話框
      const formData = new FormData();
      formData.append("file", file);

      // 設置默認名稱 (移除副檔名)
      const name = file.name.replace(/\.[^/.]+$/, "");

      // 顯示上傳表單讓用戶填寫詳細資訊
      this.$Modal.confirm({
        title: "上傳錄音",
        render: (h) => {
          return h(
            "div",
            {
              style: { padding: "16px 0" },
            },
            [
              h(
                "Form",
                {
                  props: { labelWidth: 80 },
                },
                [
                  h(
                    "FormItem",
                    {
                      props: { label: "名稱", required: true },
                    },
                    [
                      h("Input", {
                        props: {
                          value: name,
                          placeholder: "請輸入錄音名稱",
                        },
                        on: {
                          input: (val) => {
                            formData.set("name", val);
                          },
                        },
                      }),
                    ]
                  ),
                  h(
                    "FormItem",
                    {
                      props: { label: "專員" },
                    },
                    [
                      h(
                        "Select",
                        {
                          props: {
                            placeholder: "選擇專員",
                            clearable: true,
                          },
                          on: {
                            "on-change": (val) => {
                              if (val) {
                                formData.set("staff_id", val);
                              } else {
                                formData.delete("staff_id");
                              }
                            },
                          },
                        },
                        this.staffList.map((staff) => {
                          return h("Option", {
                            props: {
                              value: staff.id,
                              label: `${staff.name} (${staff.code})`,
                            },
                          });
                        })
                      ),
                    ]
                  ),
                  h(
                    "FormItem",
                    {
                      props: { label: "描述" },
                    },
                    [
                      h("Input", {
                        props: {
                          type: "textarea",
                          rows: 3,
                          placeholder: "請輸入描述",
                        },
                        on: {
                          input: (val) => {
                            formData.set("description", val);
                          },
                        },
                      }),
                    ]
                  ),
                ]
              ),
            ]
          );
        },
        onOk: () => {
          // 確保有設置名稱
          if (!formData.has("name") || formData.get("name") === "") {
            formData.set("name", name);
          }

          // 顯示上傳中提示
          const loadingMsg = this.$Message.loading({
            content: "上傳中...",
            duration: 0,
          });

          // 上傳文件
          axios
            .post("/api/audio/upload", formData, {
              headers: { "Content-Type": "multipart/form-data" },
            })
            .then(() => {
              this.$Message.success("上傳成功");
              this.refreshData();
            })
            .catch((error) => {
              const errorMsg = error.response?.data?.error || error.message;
              this.$Message.error(`上傳失敗: ${errorMsg}`);
            })
            .finally(() => {
              // 關閉上傳中提示
              setTimeout(loadingMsg, 0);
            });
        },
      });

      // 返回 false 阻止默認上傳
      return false;
    },

    editAudio(audio) {
      // 首先需要獲取音頻數據
      this.loading = true;
      fetch(`/api/audio/stream/${audio.id}`)
        .then((response) => response.blob())
        .then((blob) => {
          this.loading = false;
          // 打開編輯器
          this.editorAudioData = {
            blob: blob,
            name: audio.name,
            staffId: audio.staff_id,
            description: audio.description || "",
          };
          this.editorModalVisible = true;
        })
        .catch((error) => {
          this.loading = false;
          this.$Message.error(`獲取音頻數據失敗: ${error.message}`);
        });
    },

    async refreshData(resetPage = false) {
      if (resetPage) {
        this.page = 1;
      }

      this.loading = true;
      try {
        const response = await axios.get("/api/audio", {
          params: {
            page: this.page,
            size: this.pageSize,
            keyword: this.searchKeyword,
            staff_id: this.selectedStaffId,
          },
        });

        this.audioList = response.data.items || [];
        this.total = response.data.total || 0;
      } catch (error) {
        this.$Message.error("獲取錄音列表失敗");
        console.error("獲取錄音列表失敗:", error);
      } finally {
        this.loading = false;
      }
    },

    async fetchStaffList() {
      try {
        const response = await axios.get("/api/staff", {
          params: {
            size: 100, // 獲取足夠多的專員
            status: "active",
          },
        });

        this.staffList = response.data.items || [];
      } catch (error) {
        console.error("獲取專員列表失敗:", error);
      }
    },

    onPageChange(page) {
      this.page = page;
      this.refreshData();
    },

    playAudio(audio) {
      this.currentAudio = audio;
      this.audioSrc = `/api/audio/stream/${audio.id}`;
      this.audioPlayerVisible = true;
    },

    downloadAudio(audioId) {
      window.open(`/api/audio/download/${audioId}`, "_blank");
    },

    openAudioModal(type, audio = null) {
      this.audioForm = {
        id: audio?.id || "",
        name: audio?.name || "",
        staff_id: audio?.staff_id || "",
        status: audio?.status || "active",
        description: audio?.description || "",
      };

      this.audioModalVisible = true;
    },

    async handleSaveAudio(formData) {
      this.modalLoading = true;
      try {
        await axios.put(`/api/audio/${formData.id}`, formData);

        this.audioModalVisible = false;
        this.refreshData();
        this.$Message.success("更新錄音資訊成功");
      } catch (error) {
        const errorMsg = error.response?.data?.error || error.message;
        this.$Message.error(`更新錄音資訊失敗: ${errorMsg}`);
      } finally {
        this.modalLoading = false;
      }
    },

    async deleteAudio(id) {
      this.loading = true;
      try {
        await axios.delete(`/api/audio/${id}`);
        this.$Message.success("刪除錄音成功");
        this.refreshData();
      } catch (error) {
        const errorMsg = error.response?.data?.error || error.message;
        this.$Message.error(`刪除錄音失敗: ${errorMsg}`);
      } finally {
        this.loading = false;
      }
    },

    openRecorder() {
      this.recorderModalVisible = true;
    },

    openEditor(audioBlob) {
      this.editorAudioData = audioBlob;
      this.editorModalVisible = true;
    },

    handleUploadSuccess() {
      this.$Message.success("上傳錄音成功");
      this.refreshData();
    },

    handleSaveEditedAudio(editedAudio) {
      // 處理編輯後的音頻上傳
      this.editorModalVisible = false;

      // 上傳編輯後的音頻文件
      const formData = new FormData();
      formData.append("file", editedAudio.blob);
      formData.append("name", editedAudio.name);
      if (editedAudio.staff_id) {
        formData.append("staff_id", editedAudio.staff_id);
      }
      formData.append("description", editedAudio.description || "");

      axios
        .post("/api/audio/upload", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        })
        .then(() => {
          this.$Message.success("編輯後的錄音上傳成功");
          this.refreshData();
        })
        .catch((error) => {
          const errorMsg = error.response?.data?.error || error.message;
          this.$Message.error(`上傳失敗: ${errorMsg}`);
        });
    },
  },
};
</script>

<style scoped>
.audio-management {
  max-width: 1200px;
  margin: 0 auto;
}

.audio-card {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.audio-card:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

.card-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  color: #17233d;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}
</style>
