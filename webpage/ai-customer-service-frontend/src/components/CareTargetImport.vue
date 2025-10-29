<template>
  <div class="care-target-import-container">
    <Card>
      <template #title>
        <div class="card-title">
          <Icon type="ios-people" size="18" />
          <span>關懷對象管理與匯入</span>
        </div>
      </template>

      <!-- 功能選項卡 -->
      <Tabs v-model="activeTab" class="main-tabs">
        <TabPane label="關懷對象列表" name="list">
          <CareTargetList
            :groupList="groupList"
            :tagList="tagList"
            @export="handleExport"
            @show-import="activeTab = 'import'"
          />
        </TabPane>

        <TabPane label="批量匯入" name="import">
          <ImportWizard
            :groupList="groupList"
            @create-group="handleCreateGroup"
            @complete-import="activeTab = 'list'"
          />
        </TabPane>

        <TabPane label="標籤管理" name="tags">
          <TagManagement
            :tagList="tagList"
            @save-tag="handleSaveTag"
            @delete-tag="handleDeleteTag"
          />
        </TabPane>

        <TabPane label="分組管理" name="groups">
          <GroupManagement
            :groupList="groupList"
            @save-group="handleSaveGroup"
            @delete-group="handleDeleteGroup"
            @remove-from-group="handleRemoveFromGroup"
          />
        </TabPane>
      </Tabs>
    </Card>
  </div>
</template>

<script>
import CareTargetList from './CareTarget/CareTargetList.vue'
import ImportWizard from './CareTarget/ImportWizard.vue'
import TagManagement from './CareTarget/TagManagement.vue'
import GroupManagement from './CareTarget/GroupManagement.vue'

export default {
  name: "CareTargetImport",
  components: {
    CareTargetList,
    ImportWizard,
    TagManagement,
    GroupManagement,
  },
  data() {
    return {
      activeTab: "list",
      groupList: [],
      tagList: [],
    };
  },

  mounted() {
    this.fetchGroups();
    this.fetchTags();
  },

  methods: {
    // 獲取關懷組別列表
    fetchGroups() {
      // 模擬 API 獲取關懷組別
      setTimeout(() => {
        this.groupList = [
          {
            id: "1",
            name: "高齡長者",
            description: "65歲以上高齡長者",
            count: 32,
            createdAt: "2025-01-15",
          },
          {
            id: "2",
            name: "慢性病患者",
            description: "需要長期照護的慢性病患者",
            count: 27,
            createdAt: "2025-01-20",
          },
          {
            id: "3",
            name: "獨居老人",
            description: "獨自生活的老人",
            count: 18,
            createdAt: "2025-02-10",
          },
          {
            id: "4",
            name: "行動不便",
            description: "行動不便需要特別協助的對象",
            count: 15,
            createdAt: "2025-03-05",
          },
          {
            id: "5",
            name: "社區新成員",
            description: "最近加入社區的新成員",
            count: 23,
            createdAt: "2025-04-12",
          },
        ];
      }, 500);
    },

    // 獲取標籤列表
    fetchTags() {
      // 模擬 API 獲取標籤
      setTimeout(() => {
        this.tagList = [
          {
            id: "1",
            name: "高齡",
            color: "#2d8cf0",
            description: "高齡長者",
            useCount: 32,
          },
          {
            id: "2",
            name: "獨居",
            color: "#ff9900",
            description: "獨居老人",
            useCount: 18,
          },
          {
            id: "3",
            name: "慢性病",
            color: "#19be6b",
            description: "慢性病患者",
            useCount: 27,
          },
          {
            id: "4",
            name: "行動不便",
            color: "#ed4014",
            description: "行動不便需要特別協助",
            useCount: 15,
          },
          {
            id: "5",
            name: "需關懷",
            color: "#9c27b0",
            description: "需要特別關懷的對象",
            useCount: 42,
          },
        ];
      }, 500);
    },

    // 處理標籤儲存
    handleSaveTag(tagData) {
      const existingIndex = this.tagList.findIndex(
        (tag) => tag.id === tagData.id
      );

      if (existingIndex > -1) {
        // 更新現有標籤
        this.$set(this.tagList, existingIndex, {
          ...this.tagList[existingIndex],
          ...tagData,
        });
      } else {
        // 新增標籤
        this.tagList.push({
          ...tagData,
          useCount: 0,
        });
      }
    },

    // 處理標籤刪除
    handleDeleteTag(tagId) {
      this.tagList = this.tagList.filter((tag) => tag.id !== tagId);
    },

    // 處理分組儲存
    handleSaveGroup(groupData) {
      const existingIndex = this.groupList.findIndex(
        (group) => group.id === groupData.id
      );

      if (existingIndex > -1) {
        // 更新現有分組
        this.$set(this.groupList, existingIndex, {
          ...this.groupList[existingIndex],
          ...groupData,
        });
      } else {
        // 新增分組
        this.groupList.push(groupData);
      }
    },

    // 處理分組刪除
    handleDeleteGroup(groupId) {
      this.groupList = this.groupList.filter((group) => group.id !== groupId);
    },

    // 處理從分組中移除成員
    handleRemoveFromGroup(data) {
      const group = this.groupList.find((g) => g.id === data.groupId);
      if (group && group.count > 0) {
        group.count--;
      }
    },

    // 處理創建新分組（從匯入嚮導觸發）
    handleCreateGroup(groupData) {
      this.groupList.push(groupData);
    },

    // 處理匯出數據
    handleExport() {
      // 模擬導出過程
      setTimeout(() => {
        // 模擬下載文件
        const link = document.createElement("a");
        link.href = "#";
        link.setAttribute("download", "關懷對象資料.xlsx");
        link.click();

        this.$Message.success("數據匯出成功，下載已開始");
      }, 1500);
    },
  },
};
</script>

<style scoped>
.care-target-import-container {
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
</style>
