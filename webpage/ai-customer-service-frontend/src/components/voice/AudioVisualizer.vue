<!-- AudioVisualizer.vue - 音頻可視化組件 -->
<template>
  <div
    class="audio-visualizer"
    :class="{ active: isActive }"
  >
    <div
      v-for="(bar, index) in visualBars"
      :key="index"
      class="bar"
      :style="{ height: `${bar}px` }"
    ></div>
  </div>
</template>

<script>
export default {
  name: "AudioVisualizer",
  props: {
    visualBars: {
      type: Array,
      default: () => Array(40).fill(5)
    },
    isActive: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.audio-visualizer {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  height: 60px;
  margin-bottom: 20px;
  gap: 2px;
  opacity: 0.3;
  transition: opacity 0.3s ease;
}

.audio-visualizer.active {
  opacity: 1;
}

.audio-visualizer .bar {
  width: 4px;
  background: linear-gradient(to top, #4361ee, #4cc9f0);
  border-radius: 2px;
  transition: height 0.1s ease;
  min-height: 4px;
}
</style>