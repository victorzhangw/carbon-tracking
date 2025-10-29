<template>
  <div class="analytics-charts">
    <!-- 第一行：關鍵指標 -->
    <div class="chart-row">
      <div class="chart-container full-width">
        <div ref="keyMetricsChart" style="height: 300px"></div>
      </div>
    </div>

    <!-- 第二行：趨勢分析 -->
    <div class="chart-row">
      <div class="chart-container">
        <div ref="callTrendChart" style="height: 350px"></div>
      </div>
      <div class="chart-container">
        <div ref="carePerformanceChart" style="height: 350px"></div>
      </div>
    </div>

    <!-- 第三行：分布分析 -->
    <div class="chart-row">
      <div class="chart-container">
        <div ref="emotionRadarChart" style="height: 320px"></div>
      </div>
      <div class="chart-container">
        <div ref="durationDistributionChart" style="height: 320px"></div>
      </div>
      <div class="chart-container">
        <div ref="followupStatusChart" style="height: 320px"></div>
      </div>
    </div>

    <!-- 第四行：深度分析 -->
    <div class="chart-row">
      <div class="chart-container">
        <div ref="customerTypeChart" style="height: 380px"></div>
      </div>
      <div class="chart-container">
        <div ref="questionTypeChart" style="height: 380px"></div>
      </div>
    </div>

    <!-- 第五行：專員排名 -->
    <div class="chart-row">
      <div class="chart-container full-width">
        <div ref="staffRankingChart" style="height: 400px"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from "echarts";
import _ from "lodash";
import {
  getCallsByDate,
  getStatistics,
  getMonthlyCarePerformance,
  getStatsByCustomerType,
  getQuestionTypeStats,
  getStatsByStaff,
  generateCallRecords, // 新增此導入
  getStatsByDepartment,
} from "@/data/mock-data";

// 通用顏色配置
const chartColors = [
  "#5470C6",
  "#91CC75",
  "#FAC858",
  "#EE6666",
  "#73C0DE",
  "#3BA272",
  "#FC8452",
  "#9A60B4",
];

export default {
  name: "EnhancedAnalyticsCharts",
  mounted() {
    this.renderAllCharts();
    window.addEventListener("resize", this.debouncedResize);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.debouncedResize);
    this.charts.forEach((chart) => chart.dispose());
  },
  methods: {
    async renderAllCharts() {
      const [
        callTrendData,
        monthlyCareData,
        customerTypeData,
        questionStats,
        staffStats,
      ] = await Promise.all([
        getCallsByDate(),
        getMonthlyCarePerformance(),
        getStatsByCustomerType(),
        getQuestionTypeStats(),
        getStatsByStaff(),
      ]);

      this.renderKeyMetrics();
      this.renderCallTrend(callTrendData);
      this.renderCarePerformance(monthlyCareData);
      this.renderCustomerTypeAnalysis(customerTypeData);
      this.renderQuestionTypeAnalysis(questionStats);
      this.renderStaffRanking(staffStats);
      this.renderAdvancedCharts();
    },

    // 關鍵指標卡牌式圖表
    renderKeyMetrics() {
      const chart = this.initChart("keyMetricsChart");
      const { records } = generateCallRecords({ pageSize: 1000 });
      const stats = getStatistics(records);
      const { totalCalls, averageDuration, completedFollowups } = stats;

      const option = {
        title: { text: "核心運營指標", left: "center" },
        grid: { containLabel: true },
        xAxis: { show: false },
        yAxis: { show: false },
        series: [
          {
            type: "pie",
            radius: ["60%", "70%"],
            itemStyle: { borderWidth: 3, borderColor: "#fff" },
            label: { show: false },
            data: [
              {
                value: totalCalls,
                name: "總通話數",
                itemStyle: { color: chartColors[0] },
              },
              {
                value: averageDuration,
                name: "平均時長",
                itemStyle: { color: chartColors[1] },
              },
              {
                value: completedFollowups,
                name: "已完成跟進",
                itemStyle: { color: chartColors[2] },
              },
            ],
          },
        ],
        graphic: [
          {
            type: "text",
            left: "center",
            top: "35%",
            style: {
              text: totalCalls,
              fontSize: 28,
              fontWeight: "bold",
              fill: chartColors[0],
            },
          },
          {
            type: "text",
            left: "center",
            top: "50%",
            style: {
              text: "總通話數",
              fontSize: 14,
              fill: "#666",
            },
          },
        ],
      };
      chart.setOption(option);
    },

    // 增強版通話趨勢分析
    renderCallTrend(data) {
      const chart = this.initChart("callTrendChart");
      const option = {
        title: { text: "每日通話趨勢分析" },
        tooltip: { trigger: "axis" },
        legend: {
          data: ["總通話量", "正面情緒", "負面情緒"],
          top: 30,
        },
        xAxis: {
          type: "category",
          data: data.map((d) => d.date.split("-").slice(1).join("/")),
        },
        yAxis: [{ type: "value", name: "通話量" }],
        series: [
          {
            name: "總通話量",
            type: "bar",
            data: data.map((d) => d.total),
            itemStyle: { color: chartColors[0] },
          },
          {
            name: "正面情緒",
            type: "line",
            smooth: true,
            data: data.map((d) => d.positive),
            itemStyle: { color: chartColors[1] },
          },
          {
            name: "負面情緒",
            type: "line",
            smooth: true,
            data: data.map((d) => d.negative),
            itemStyle: { color: chartColors[3] },
          },
        ],
      };
      chart.setOption(option);
    },

    // 月度關懷績效趨勢
    renderCarePerformance(data) {
      const chart = this.initChart("carePerformanceChart");
      const option = {
        title: { text: "月度關懷績效趨勢" },
        tooltip: { trigger: "axis" },
        legend: {
          data: ["解決率", "滿意度", "跟進率"],
          top: 30,
        },
        xAxis: {
          type: "category",
          data: data.map((d) => d.month),
        },
        yAxis: {
          type: "value",
          axisLabel: { formatter: "{value}%" },
        },
        series: [
          {
            name: "解決率",
            type: "line",
            smooth: true,
            data: data.map((d) => (d.resolutionRate * 100).toFixed(1)),
            itemStyle: { color: chartColors[0] },
          },
          {
            name: "滿意度",
            type: "line",
            smooth: true,
            data: data.map((d) => (d.satisfactionRate * 100).toFixed(1)),
            itemStyle: { color: chartColors[1] },
          },
          {
            name: "跟進率",
            type: "bar",
            data: data.map((d) => (d.followupRate * 100).toFixed(1)),
            itemStyle: { color: chartColors[2] },
          },
        ],
      };
      chart.setOption(option);
    },

    // 客戶類型多維分析
    renderCustomerTypeAnalysis(data) {
      const chart = this.initChart("customerTypeChart");
      const option = {
        title: { text: "客戶類型多維分析" },
        tooltip: { trigger: "item" },
        radar: {
          indicator: data.map((d) => ({
            name: d.type,
            max: Math.max(...data.map((d) => d.total)) * 1.2,
          })),
        },
        series: [
          {
            type: "radar",
            data: [
              {
                value: data.map((d) => d.total),
                name: "通話量",
                areaStyle: { color: "rgba(84, 112, 198, 0.2)" },
              },
            ],
          },
        ],
      };
      chart.setOption(option);
    },

    // 問題類型解決率分析
    renderQuestionTypeAnalysis(data) {
      const chart = this.initChart("questionTypeChart");
      // 生成x軸類別陣列
      const xAxisData = data.map((d) => d.type);
      // 生成對應的數據點，x為類別索引，y為解決率，第三項為count
      const scatterData = data.map((d, index) => [
        index,
        d.resolutionRate,
        d.count,
      ]);
      const option = {
        title: { text: "問題類型解決率分析" },
        tooltip: {
          formatter: function (params) {
            const d = data[params.dataIndex];
            return `
          ${d.type}<br/>
          出現次數: ${d.count}<br/>
          平均解決率: ${(d.resolutionRate * 100).toFixed(1)}%
        `;
          },
        },
        xAxis: {
          type: "category",
          data: xAxisData,
          axisLabel: { rotate: 45 }, // 類別名稱若較長可旋轉
        },
        yAxis: {
          type: "value",
          axisLabel: {
            formatter: (value) => `${(value * 100).toFixed(0)}%`, // Y軸顯示百分比
          },
        },
        series: [
          {
            type: "scatter",
            symbolSize: (val) => Math.sqrt(val[2]) * 8, // 第三個參數是count，控制大小
            data: scatterData,
            itemStyle: {
              color: chartColors[3],
              opacity: 0.7,
            },
          },
        ],
      };
      chart.setOption(option);
    },

    // 專員績效排名
    renderStaffRanking(data) {
      const chart = this.initChart("staffRankingChart");
      const sortedData = [...data].sort(
        (a, b) => b.satisfactionScore - a.satisfactionScore
      );

      const option = {
        title: { text: "專員服務滿意度排名" },
        tooltip: { trigger: "axis" },
        xAxis: {
          type: "category",
          data: sortedData.map((d) => d.staffName),
          axisLabel: { rotate: 45 },
        },
        yAxis: {
          type: "value",
          axisLabel: { formatter: "{value} 分" },
        },
        series: [
          {
            type: "bar",
            data: sortedData.map((d) => ({
              value: d.satisfactionScore.toFixed(1),
              itemStyle: {
                color:
                  d.satisfactionScore > 75 ? chartColors[1] : chartColors[3],
              },
            })),
            label: {
              show: true,
              position: "top",
              formatter: "{c}",
            },
          },
        ],
      };
      chart.setOption(option);
    },

    // 其他高級圖表
    renderAdvancedCharts() {
      this.renderEmotionRadar();
      this.renderDurationDistribution();
      this.renderFollowupStatus();
    },
    // 情緒雷達圖
    async renderEmotionRadar() {
      const data = await getStatsByDepartment();

      const chart = this.initChart("emotionRadarChart");
      const indicator = data.map((d) => ({
        name: d.department,
        max: Math.max(...data.map((d) => d.total)) * 1.2,
      }));
      const option = {
        title: { text: "各組通話情緒分布" },
        tooltip: { trigger: "item" },
        radar: {
          indicator: indicator,
        },
        series: [
          {
            name: "情緒分布",
            type: "radar",
            data: [
              {
                value: data.map((d) => (d.positive / d.total) * 100), // 轉換為百分比
                name: "正面情绪比例",
                areaStyle: { color: "rgba(84, 112, 198, 0.4)" },
              },
            ],
          },
        ],
      };
      chart.setOption(option);
    },
    // 通話時長分布
    async renderDurationDistribution() {
      const durations = (
        await generateCallRecords({ pageSize: 1000 })
      ).records.map((r) => r.duration);

      const chart = this.initChart("durationDistributionChart");
      const option = {
        title: { text: "通話時長分布" },
        tooltip: { trigger: "axis" },
        xAxis: {
          type: "category",
          data: ["<5", "5-10", "10-15", "15-20", "20-30", ">30"],
        },
        yAxis: { type: "value" },
        series: [
          {
            type: "bar",
            data: this.generateDurationBins(durations),
          },
        ],
      };
      chart.setOption(option);
    },
    generateDurationBins(durations) {
      const bins = [0, 0, 0, 0, 0, 0];
      durations.forEach((d) => {
        if (d < 5) bins[0]++;
        else if (d <= 10) bins[1]++;
        else if (d <= 15) bins[2]++;
        else if (d <= 20) bins[3]++;
        else if (d <= 30) bins[4]++;
        else bins[5]++;
      });
      return bins;
    },
    // 跟進狀態環形圖
    async renderFollowupStatus() {
      const { records } = await generateCallRecords({ pageSize: 1000 });
      const statusCounts = records.reduce((acc, r) => {
        acc[r.followupStatus] = (acc[r.followupStatus] || 0) + 1;
        return acc;
      }, {});
      const chart = this.initChart("followupStatusChart");
      const option = {
        title: { text: "跟進狀態分布" },
        tooltip: { trigger: "item" },
        series: [
          {
            type: "pie",
            radius: ["40%", "70%"],
            label: {
              formatter: "{b}: {d}%",
            },
            data: [
              { value: statusCounts.pending || 0, name: "待處理" },
              { value: statusCounts.inProgress || 0, name: "處理中" },
              { value: statusCounts.completed || 0, name: "已完成" },
              { value: statusCounts.noAction || 0, name: "無需處理" },
            ],
          },
        ],
      };
      chart.setOption(option);
    },
    // 通用初始化方法
    initChart(refName) {
      const chart = echarts.init(this.$refs[refName]);
      this.charts.push(chart);
      return chart;
    },

    // 防抖處理窗口resize
    debouncedResize: _.debounce(function () {
      this.charts.forEach((chart) => chart.resize());
    }, 300),
  },
  data() {
    return {
      charts: [],
    };
  },
};
</script>

<style scoped>
.analytics-charts {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.chart-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.chart-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.full-width {
  grid-column: 1 / -1;
}
/* 增加最小高度防止容器塌陷 */
.chart-container {
  min-height: 320px;
  position: relative;
}
/* 旋轉標籤時的間距調整 */
.echarts .x-axis text {
  transform: rotate(30deg);
  transform-origin: 70% 100%;
}
@media (max-width: 768px) {
  .chart-row {
    grid-template-columns: 1fr;
  }
}
</style>
