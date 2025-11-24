/**
 * 語音波形視覺化模組
 * 使用 Web Audio API 和 Canvas 實現即時波形顯示
 */

class VoiceWaveform {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext("2d");
    this.analyser = null;
    this.dataArray = null;
    this.bufferLength = 0;
    this.animationId = null;
    this.isActive = false;

    // 設置 canvas 尺寸
    this.resizeCanvas();
    window.addEventListener("resize", () => this.resizeCanvas());
  }

  /**
   * 調整 canvas 尺寸
   */
  resizeCanvas() {
    const container = this.canvas.parentElement;
    this.canvas.width = container.clientWidth;
    this.canvas.height = container.clientHeight;
  }

  /**
   * 初始化分析器
   */
  init(audioContext, stream) {
    this.analyser = audioContext.createAnalyser();
    this.analyser.fftSize = 256;
    this.bufferLength = this.analyser.frequencyBinCount;
    this.dataArray = new Uint8Array(this.bufferLength);

    const source = audioContext.createMediaStreamSource(stream);
    source.connect(this.analyser);

    this.isActive = true;
    this.draw();
  }

  /**
   * 繪製波形
   */
  draw() {
    if (!this.isActive) return;

    this.animationId = requestAnimationFrame(() => this.draw());

    this.analyser.getByteFrequencyData(this.dataArray);

    // 清空 canvas
    this.ctx.fillStyle = "#f9f9f9";
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // 計算平均音量
    const average =
      this.dataArray.reduce((a, b) => a + b, 0) / this.bufferLength;
    const volumePercent = Math.min(100, (average / 255) * 100);

    // 繪製波形
    const barWidth = (this.canvas.width / this.bufferLength) * 2.5;
    let x = 0;

    for (let i = 0; i < this.bufferLength; i++) {
      const barHeight = (this.dataArray[i] / 255) * this.canvas.height * 0.8;

      // 商務藍色
      this.ctx.fillStyle = "#3498db";
      this.ctx.fillRect(x, this.canvas.height - barHeight, barWidth, barHeight);

      x += barWidth + 1;
    }

    // 繪製音量指示
    this.drawVolumeIndicator(volumePercent);
  }

  /**
   * 繪製音量指示器
   */
  drawVolumeIndicator(percent) {
    const padding = 10;
    const indicatorWidth = 100;
    const indicatorHeight = 8;
    const x = this.canvas.width - indicatorWidth - padding;
    const y = padding;

    // 背景
    this.ctx.fillStyle = "#e0e0e0";
    this.ctx.fillRect(x, y, indicatorWidth, indicatorHeight);

    // 音量條 - 商務風格單色
    const fillWidth = (indicatorWidth * percent) / 100;

    if (percent < 30) {
      this.ctx.fillStyle = "#27ae60";
    } else if (percent < 70) {
      this.ctx.fillStyle = "#f39c12";
    } else {
      this.ctx.fillStyle = "#e74c3c";
    }

    this.ctx.fillRect(x, y, fillWidth, indicatorHeight);

    // 文字
    this.ctx.fillStyle = "#2c3e50";
    this.ctx.font = "11px Arial";
    this.ctx.fillText(
      `${Math.round(percent)}%`,
      x + indicatorWidth + 5,
      y + indicatorHeight
    );
  }

  /**
   * 繪製靜音狀態
   */
  drawIdle() {
    this.ctx.fillStyle = "#f9f9f9";
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // 繪製靜態波形
    const centerY = this.canvas.height / 2;
    const amplitude = 20;
    const frequency = 0.02;

    this.ctx.beginPath();
    this.ctx.strokeStyle = "#ddd";
    this.ctx.lineWidth = 2;

    for (let x = 0; x < this.canvas.width; x++) {
      const y = centerY + Math.sin(x * frequency) * amplitude;
      if (x === 0) {
        this.ctx.moveTo(x, y);
      } else {
        this.ctx.lineTo(x, y);
      }
    }

    this.ctx.stroke();

    // 文字提示
    this.ctx.fillStyle = "#999";
    this.ctx.font = "14px Arial";
    this.ctx.textAlign = "center";
    this.ctx.fillText(
      "等待語音輸入...",
      this.canvas.width / 2,
      this.canvas.height / 2 + 40
    );
  }

  /**
   * 停止繪製
   */
  stop() {
    this.isActive = false;
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
    this.drawIdle();
  }

  /**
   * 清理資源
   */
  destroy() {
    this.stop();
    if (this.analyser) {
      this.analyser.disconnect();
      this.analyser = null;
    }
  }
}
