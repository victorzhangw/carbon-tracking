<template>
  <div class="analytics-dashboard">
    <Card>
      <template #title>
        <div class="card-title">
          <Icon type="ios-stats" size="18" />
          <span>數據分析儀表板</span>
        </div>
      </template>
      <AnalyticsCharts />
    </Card>
  </div>
</template>

<script>
import AnalyticsCharts from "./Charts/AnalyticsCharts.vue";

export default {
  name: "AnalyticsDashboard",
  components: { AnalyticsCharts },
};
</script>
