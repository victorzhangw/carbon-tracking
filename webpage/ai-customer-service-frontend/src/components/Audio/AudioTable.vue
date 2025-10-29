<!-- components/AudioTable.vue -->
<template>
  <div class="audio-table">
    <Table :loading="loading" border :columns="tableColumns" :data="audioList">
      <template #staff="{ row }">
        <span v-if="row.staff_name">
          {{ row.staff_name }} ({{ row.staff_code }})
        </span>
        <span v-else>-</span>
      </template>
      <template #duration="{ row }">
        <span>{{ formatDuration(row.duration) }}</span>
      </template>
      <template #status="{ row }">
        <Tag :color="row.status === 'active' ? 'success' : 'default'">
          {{ row.status === "active" ? "啟用" : "停用" }}
        </Tag>
      </template>
      <template #action="{ row }">
        <div class="action-group">
          <Button type="primary" size="small" @click="$emit('play', row)">
            <Icon type="ios-play" />
          </Button>
          <Button
            type="success"
            size="small"
            @click="$emit('download', row.id)"
          >
            <Icon type="ios-download" />
          </Button>
          <Button type="info" size="small" @click="$emit('edit', 'edit', row)">
            <Icon type="ios-create" />
          </Button>
          <Button type="warning" size="small" @click="$emit('edit-audio', row)">
            <Icon type="ios-cut" />
          </Button>
          <Poptip
            confirm
            title="確定要刪除此錄音嗎？"
            @on-ok="$emit('delete', row.id)"
          >
            <Button type="error" size="small">
              <Icon type="ios-trash" />
            </Button>
          </Poptip>
        </div>
      </template>
    </Table>
  </div>
</template>

<script>
export default {
  name: "AudioTable",
  props: {
    loading: {
      type: Boolean,
      default: false,
    },
    columns: {
      type: Array,
      required: true,
    },
    audioList: {
      type: Array,
      default: () => [],
    },
  },
  emits: ["play", "download", "edit", "edit-audio", "delete"],
  computed: {
    tableColumns() {
      return this.columns;
    },
  },
  methods: {
    formatDuration(seconds) {
      if (seconds === null || seconds === undefined) return "-";

      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = Math.floor(seconds % 60);
      return `${minutes.toString().padStart(2, "0")}:${remainingSeconds
        .toString()
        .padStart(2, "0")}`;
    },
  },
};
</script>

<style scoped>
.audio-table {
  background-color: #fff;
  border-radius: 4px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.audio-table:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.action-group {
  display: flex;
  justify-content: center;
  gap: 5px;
}

.action-group button {
  transition: all 0.2s ease;
}

.action-group button:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* Animation for table rows */
:deep(.ivu-table-row) {
  transition: background-color 0.3s ease;
}

:deep(.ivu-table-row:hover td) {
  background-color: #f0faff !important;
}
</style>
