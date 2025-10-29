#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 客服語音克隆系統 - 期末報告圖表生成程式
生成優化前後對比圖表
"""

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
from datetime import datetime
import seaborn as sns

# 設置中文字體
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

# 設置圖表風格
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['figure.dpi'] = 100

class ChartGenerator:
    def __init__(self, output_dir='./charts'):
        self.output_dir = output_dir
        import os
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_all_charts(self):
        """生成所有圖表"""
        print("開始生成期末報告圖表...")
        
        # 1. 核心指標對比圖
        self.generate_core_metrics_comparison()
        
        # 2. 模組性能雷達圖
        self.generate_module_performance_radar()
        
        # 3. 年齡層識別準確率對比
        self.generate_age_group_comparison()
        
        # 4. SNR 環境識別準確率對比
        self.generate_snr_comparison()
        
        # 5. 情緒識別準確率對比
        self.generate_emotion_comparison()
        
        # 6. 系統資源使用對比
        self.generate_resource_usage_comparison()
        
        # 7. 訓練過程曲線
        self.generate_training_curves()
        
        # 8. 錯誤類型分佈
        self.generate_error_distribution()
        
        # 9. 用戶滿意度趨勢
        self.generate_satisfaction_trend()
        
        # 10. 綜合成效儀表板
        self.generate_comprehensive_dashboard()
        
        print(f"✅ 所有圖表已生成至 {self.output_dir} 目錄")
    
    def generate_core_metrics_comparison(self):
        """生成核心指標對比圖"""
        metrics = ['語音辨識\n準確率', '情緒辨識\n準確率', '對話任務\n完成率', 
                   '系統\n穩定性', '用戶\n滿意度']
        before = [72.1, 68, 70, 85, 65]
        after = [94.2, 89.7, 92.1, 98.9, 87.3]
        target = [90, 85, 90, 95, 80]
        
        x = np.arange(len(metrics))
        width = 0.25
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        bars1 = ax.bar(x - width, before, width, label='優化前', color='#FF6B6B', alpha=0.8)
        bars2 = ax.bar(x, after, width, label='優化後', color='#4ECDC4', alpha=0.8)
        bars3 = ax.bar(x + width, target, width, label='目標值', color='#95E1D3', alpha=0.6)
        
        ax.set_xlabel('評估指標', fontsize=14, fontweight='bold')
        ax.set_ylabel('準確率 (%)', fontsize=14, fontweight='bold')
        ax.set_title('AI 客服系統核心指標優化前後對比', fontsize=16, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(metrics, fontsize=12)
        ax.legend(fontsize=12, loc='upper left')
        ax.set_ylim(0, 110)
        ax.grid(axis='y', alpha=0.3)
        
        # 添加數值標籤
        for bars in [bars1, bars2, bars3]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}%',
                       ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/01_核心指標對比.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 核心指標對比圖已生成")
    
    def generate_module_performance_radar(self):
        """生成模組性能雷達圖"""
        categories = ['語音辨識', '情緒識別', '對話管理', '系統穩定性', '回應速度']
        before = [72.1, 68, 70, 85, 40]  # 回應速度轉換為百分比
        after = [94.2, 89.7, 92.1, 98.9, 95]
        
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        before += before[:1]
        after += after[:1]
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        ax.plot(angles, before, 'o-', linewidth=2, label='優化前', color='#FF6B6B')
        ax.fill(angles, before, alpha=0.25, color='#FF6B6B')
        
        ax.plot(angles, after, 'o-', linewidth=2, label='優化後', color='#4ECDC4')
        ax.fill(angles, after, alpha=0.25, color='#4ECDC4')
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=12)
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], fontsize=10)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12)
        ax.set_title('系統模組性能雷達圖', fontsize=16, fontweight='bold', pad=20)
        ax.grid(True)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/02_模組性能雷達圖.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 模組性能雷達圖已生成")
    
    def generate_age_group_comparison(self):
        """生成年齡層識別準確率對比"""
        age_groups = ['高齡\n(65+)', '中年\n(40-64)', '青年\n(18-39)']
        before = [72.1, 78.5, 82.3]
        after = [88.6, 93.2, 96.1]
        samples = [18000, 12600, 5400]
        
        x = np.arange(len(age_groups))
        width = 0.35
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # 左圖: 準確率對比
        bars1 = ax1.bar(x - width/2, before, width, label='優化前', color='#FF6B6B', alpha=0.8)
        bars2 = ax1.bar(x + width/2, after, width, label='優化後', color='#4ECDC4', alpha=0.8)
        
        ax1.set_xlabel('年齡層', fontsize=14, fontweight='bold')
        ax1.set_ylabel('識別準確率 (%)', fontsize=14, fontweight='bold')
        ax1.set_title('不同年齡層語音識別準確率對比', fontsize=14, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(age_groups, fontsize=12)
        ax1.legend(fontsize=12)
        ax1.set_ylim(0, 110)
        ax1.grid(axis='y', alpha=0.3)
        
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%',
                        ha='center', va='bottom', fontsize=10)
        
        # 右圖: 樣本分佈
        colors = ['#FF6B6B', '#4ECDC4', '#95E1D3']
        wedges, texts, autotexts = ax2.pie(samples, labels=age_groups, autopct='%1.1f%%',
                                            colors=colors, startangle=90)
        ax2.set_title('年齡層樣本分佈', fontsize=14, fontweight='bold')
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(12)
            autotext.set_fontweight('bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/03_年齡層識別對比.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 年齡層識別對比圖已生成")
    
    def generate_snr_comparison(self):
        """生成 SNR 環境識別準確率對比"""
        snr_ranges = ['>20dB\n(清晰)', '15-20dB\n(良好)', '10-15dB\n(中等)', '<10dB\n(嚴重)']
        before = [85.2, 72.5, 58.3, 42.1]
        after = [97.8, 92.3, 85.4, 68.7]
        improvement = [12.6, 19.8, 27.1, 26.6]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # 左圖: 準確率對比
        x = np.arange(len(snr_ranges))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, before, width, label='優化前', color='#FF6B6B', alpha=0.8)
        bars2 = ax1.bar(x + width/2, after, width, label='優化後', color='#4ECDC4', alpha=0.8)
        
        ax1.set_xlabel('SNR 環境', fontsize=14, fontweight='bold')
        ax1.set_ylabel('識別準確率 (%)', fontsize=14, fontweight='bold')
        ax1.set_title('不同 SNR 環境語音識別準確率對比', fontsize=14, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(snr_ranges, fontsize=11)
        ax1.legend(fontsize=12)
        ax1.set_ylim(0, 110)
        ax1.grid(axis='y', alpha=0.3)
        
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%',
                        ha='center', va='bottom', fontsize=9)
        
        # 右圖: 改善幅度
        bars = ax2.barh(snr_ranges, improvement, color='#95E1D3', alpha=0.8)
        ax2.set_xlabel('改善幅度 (%)', fontsize=14, fontweight='bold')
        ax2.set_title('各 SNR 環境改善幅度', fontsize=14, fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)
        
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax2.text(width, bar.get_y() + bar.get_height()/2.,
                    f'+{width:.1f}%',
                    ha='left', va='center', fontsize=11, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/04_SNR環境識別對比.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ SNR 環境識別對比圖已生成")

    
    def generate_emotion_comparison(self):
        """生成情緒識別準確率對比"""
        emotions = ['中性', '開心', '焦慮', '滿意', '憤怒', '其他']
        before = [75, 75, 65, 72, 78, 62]
        after = [90.1, 94.1, 88.9, 91.7, 92.8, 84.5]
        samples = [25200, 2880, 5040, 2880, 1440, 2880]
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 左上: 準確率對比
        x = np.arange(len(emotions))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, before, width, label='優化前', color='#FF6B6B', alpha=0.8)
        bars2 = ax1.bar(x + width/2, after, width, label='優化後', color='#4ECDC4', alpha=0.8)
        
        ax1.set_xlabel('情緒類別', fontsize=12, fontweight='bold')
        ax1.set_ylabel('識別準確率 (%)', fontsize=12, fontweight='bold')
        ax1.set_title('不同情緒類別識別準確率對比', fontsize=13, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(emotions, fontsize=11)
        ax1.legend(fontsize=11)
        ax1.set_ylim(0, 110)
        ax1.grid(axis='y', alpha=0.3)
        
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%',
                        ha='center', va='bottom', fontsize=9)
        
        # 右上: 改善幅度
        improvement = [after[i] - before[i] for i in range(len(emotions))]
        bars = ax2.barh(emotions, improvement, color='#95E1D3', alpha=0.8)
        ax2.set_xlabel('改善幅度 (%)', fontsize=12, fontweight='bold')
        ax2.set_title('各情緒類別改善幅度', fontsize=13, fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)
        
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax2.text(width, bar.get_y() + bar.get_height()/2.,
                    f'+{width:.1f}%',
                    ha='left', va='center', fontsize=10, fontweight='bold')
        
        # 左下: 樣本分佈餅圖
        colors = ['#FF6B6B', '#4ECDC4', '#95E1D3', '#F38181', '#AA96DA', '#FCBAD3']
        wedges, texts, autotexts = ax3.pie(samples, labels=emotions, autopct='%1.1f%%',
                                            colors=colors, startangle=90)
        ax3.set_title('情緒類別樣本分佈', fontsize=13, fontweight='bold')
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')
        
        # 右下: 優化前後平均準確率
        avg_before = np.mean(before)
        avg_after = np.mean(after)
        
        categories = ['優化前', '優化後']
        values = [avg_before, avg_after]
        colors_bar = ['#FF6B6B', '#4ECDC4']
        
        bars = ax4.bar(categories, values, color=colors_bar, alpha=0.8, width=0.5)
        ax4.set_ylabel('平均準確率 (%)', fontsize=12, fontweight='bold')
        ax4.set_title('情緒識別平均準確率對比', fontsize=13, fontweight='bold')
        ax4.set_ylim(0, 100)
        ax4.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/05_情緒識別對比.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 情緒識別對比圖已生成")
    
    def generate_resource_usage_comparison(self):
        """生成系統資源使用對比"""
        resources = ['CPU\n使用率', '記憶體\n使用', 'GPU\n使用率', '磁碟\nI/O', '網路\n延遲']
        before = [75, 8.0, 45, 80, 150]
        after = [52, 4.5, 73, 45, 35]
        units = ['%', 'GB', '%', '%', 'ms']
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        axes = axes.flatten()
        
        for i, (resource, b, a, unit) in enumerate(zip(resources, before, after, units)):
            ax = axes[i]
            
            categories = ['優化前', '優化後']
            values = [b, a]
            
            # 根據資源類型選擇顏色 (越低越好的用綠色表示改善)
            if i in [0, 1, 3, 4]:  # CPU, 記憶體, 磁碟, 延遲 - 越低越好
                colors = ['#FF6B6B', '#4ECDC4']
            else:  # GPU - 越高越好
                colors = ['#FF6B6B', '#95E1D3']
            
            bars = ax.bar(categories, values, color=colors, alpha=0.8, width=0.5)
            
            ax.set_ylabel(f'{resource.replace(chr(10), "")} ({unit})', fontsize=11, fontweight='bold')
            ax.set_title(resource, fontsize=12, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}{unit}',
                       ha='center', va='bottom', fontsize=10, fontweight='bold')
            
            # 計算改善幅度
            if i in [0, 1, 3, 4]:
                improvement = ((b - a) / b) * 100
                improvement_text = f'↓ {improvement:.1f}%'
                color = 'green'
            else:
                improvement = ((a - b) / b) * 100
                improvement_text = f'↑ {improvement:.1f}%'
                color = 'blue'
            
            ax.text(0.5, 0.95, improvement_text, transform=ax.transAxes,
                   ha='center', va='top', fontsize=11, fontweight='bold',
                   color=color, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # 隱藏最後一個子圖
        axes[5].axis('off')
        
        # 添加總標題
        fig.suptitle('系統資源使用優化前後對比', fontsize=16, fontweight='bold', y=0.98)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/06_系統資源使用對比.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 系統資源使用對比圖已生成")
    
    def generate_training_curves(self):
        """生成訓練過程曲線"""
        epochs = np.arange(1, 11)
        
        # 模擬訓練數據
        train_loss = [0.85, 0.72, 0.61, 0.53, 0.47, 0.42, 0.38, 0.35, 0.33, 0.31]
        val_loss = [0.88, 0.75, 0.65, 0.58, 0.53, 0.49, 0.46, 0.44, 0.42, 0.41]
        train_acc = [72, 78, 83, 87, 89, 91, 92, 93, 94, 94.2]
        val_acc = [70, 76, 81, 85, 87, 89, 90, 91, 92, 92.3]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # 左圖: 損失曲線
        ax1.plot(epochs, train_loss, 'o-', linewidth=2, label='訓練損失', color='#FF6B6B', markersize=8)
        ax1.plot(epochs, val_loss, 's-', linewidth=2, label='驗證損失', color='#4ECDC4', markersize=8)
        ax1.set_xlabel('訓練輪次 (Epoch)', fontsize=14, fontweight='bold')
        ax1.set_ylabel('損失值 (Loss)', fontsize=14, fontweight='bold')
        ax1.set_title('模型訓練損失曲線', fontsize=14, fontweight='bold')
        ax1.legend(fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.set_xticks(epochs)
        
        # 右圖: 準確率曲線
        ax2.plot(epochs, train_acc, 'o-', linewidth=2, label='訓練準確率', color='#FF6B6B', markersize=8)
        ax2.plot(epochs, val_acc, 's-', linewidth=2, label='驗證準確率', color='#4ECDC4', markersize=8)
        ax2.axhline(y=90, color='green', linestyle='--', linewidth=2, label='目標準確率 (90%)')
        ax2.set_xlabel('訓練輪次 (Epoch)', fontsize=14, fontweight='bold')
        ax2.set_ylabel('準確率 (%)', fontsize=14, fontweight='bold')
        ax2.set_title('模型訓練準確率曲線', fontsize=14, fontweight='bold')
        ax2.legend(fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.set_xticks(epochs)
        ax2.set_ylim(65, 100)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/07_訓練過程曲線.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 訓練過程曲線已生成")
    
    def generate_error_distribution(self):
        """生成錯誤類型分佈"""
        error_types = ['音頻品質\n問題', '逐字稿\n問題', '標註\n問題', '格式\n問題']
        error_counts = [792, 1512, 324, 72]
        error_percentages = [36.7, 70.0, 15.0, 3.3]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # 左圖: 錯誤數量柱狀圖
        colors = ['#FF6B6B', '#4ECDC4', '#95E1D3', '#F38181']
        bars = ax1.bar(error_types, error_counts, color=colors, alpha=0.8)
        ax1.set_ylabel('錯誤數量', fontsize=14, fontweight='bold')
        ax1.set_title('錯誤類型數量分佈', fontsize=14, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # 右圖: 錯誤比例餅圖
        wedges, texts, autotexts = ax2.pie(error_counts, labels=error_types, autopct='%1.1f%%',
                                            colors=colors, startangle=90)
        ax2.set_title('錯誤類型比例分佈', fontsize=14, fontweight='bold')
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
            autotext.set_fontweight('bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/08_錯誤類型分佈.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 錯誤類型分佈圖已生成")
    
    def generate_satisfaction_trend(self):
        """生成用戶滿意度趨勢"""
        months = ['優化前', '第1個月', '第2個月', '第3個月', '當前']
        satisfaction = [65, 75, 82, 85, 87.3]
        usage_rate = [45, 58, 68, 75, 82]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # 左圖: 滿意度趨勢
        ax1.plot(months, satisfaction, 'o-', linewidth=3, markersize=10, 
                color='#4ECDC4', markerfacecolor='#FF6B6B')
        ax1.axhline(y=80, color='green', linestyle='--', linewidth=2, label='目標滿意度 (80%)')
        ax1.set_xlabel('時間階段', fontsize=14, fontweight='bold')
        ax1.set_ylabel('用戶滿意度 (%)', fontsize=14, fontweight='bold')
        ax1.set_title('用戶滿意度變化趨勢', fontsize=14, fontweight='bold')
        ax1.legend(fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(60, 95)
        
        for i, (x, y) in enumerate(zip(months, satisfaction)):
            ax1.text(i, y + 1.5, f'{y:.1f}%', ha='center', fontsize=11, fontweight='bold')
        
        # 右圖: 使用率趨勢
        ax2.plot(months, usage_rate, 's-', linewidth=3, markersize=10,
                color='#95E1D3', markerfacecolor='#F38181')
        ax2.set_xlabel('時間階段', fontsize=14, fontweight='bold')
        ax2.set_ylabel('系統使用率 (%)', fontsize=14, fontweight='bold')
        ax2.set_title('系統使用率變化趨勢', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(40, 90)
        
        for i, (x, y) in enumerate(zip(months, usage_rate)):
            ax2.text(i, y + 1.5, f'{y}%', ha='center', fontsize=11, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/09_用戶滿意度趨勢.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 用戶滿意度趨勢圖已生成")
    
    def generate_comprehensive_dashboard(self):
        """生成綜合成效儀表板"""
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. 核心指標儀表 (左上)
        ax1 = fig.add_subplot(gs[0, 0])
        metrics = ['語音\n辨識', '情緒\n識別', '對話\n管理']
        values = [94.2, 89.7, 92.1]
        colors = ['#4ECDC4', '#95E1D3', '#F38181']
        bars = ax1.bar(metrics, values, color=colors, alpha=0.8)
        ax1.set_ylabel('準確率 (%)', fontsize=11, fontweight='bold')
        ax1.set_title('核心模組準確率', fontsize=12, fontweight='bold')
        ax1.set_ylim(0, 100)
        ax1.axhline(y=90, color='green', linestyle='--', alpha=0.5)
        ax1.grid(axis='y', alpha=0.3)
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # 2. 改善幅度 (中上)
        ax2 = fig.add_subplot(gs[0, 1])
        improvements = ['語音辨識', '情緒識別', '對話管理', '系統穩定性']
        values = [22.1, 21.7, 22.1, 13.9]
        bars = ax2.barh(improvements, values, color='#4ECDC4', alpha=0.8)
        ax2.set_xlabel('改善幅度 (%)', fontsize=11, fontweight='bold')
        ax2.set_title('各模組改善幅度', fontsize=12, fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)
        for bar in bars:
            width = bar.get_width()
            ax2.text(width, bar.get_y() + bar.get_height()/2.,
                    f'+{width:.1f}%', ha='left', va='center', fontsize=10, fontweight='bold')
        
        # 3. 系統穩定性 (右上)
        ax3 = fig.add_subplot(gs[0, 2])
        stability_metrics = ['可用性', '錯誤率', '恢復率']
        values = [99.2, 1.2, 95]
        colors = ['#4ECDC4', '#FF6B6B', '#95E1D3']
        bars = ax3.bar(stability_metrics, values, color=colors, alpha=0.8)
        ax3.set_ylabel('百分比 (%)', fontsize=11, fontweight='bold')
        ax3.set_title('系統穩定性指標', fontsize=12, fontweight='bold')
        ax3.set_ylim(0, 105)
        ax3.grid(axis='y', alpha=0.3)
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # 4. 年齡層分佈 (左中)
        ax4 = fig.add_subplot(gs[1, 0])
        age_groups = ['高齡', '中年', '青年']
        samples = [18000, 12600, 5400]
        colors = ['#FF6B6B', '#4ECDC4', '#95E1D3']
        wedges, texts, autotexts = ax4.pie(samples, labels=age_groups, autopct='%1.1f%%',
                                            colors=colors, startangle=90)
        ax4.set_title('年齡層樣本分佈', fontsize=12, fontweight='bold')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')
        
        # 5. 情緒分佈 (中中)
        ax5 = fig.add_subplot(gs[1, 1])
        emotions = ['中性', '焦慮', '滿意', '其他']
        samples = [25200, 5040, 2880, 3180]
        colors = ['#4ECDC4', '#FF6B6B', '#95E1D3', '#F38181']
        wedges, texts, autotexts = ax5.pie(samples, labels=emotions, autopct='%1.1f%%',
                                            colors=colors, startangle=90)
        ax5.set_title('情緒類別樣本分佈', fontsize=12, fontweight='bold')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')
        
        # 6. 資源使用 (右中)
        ax6 = fig.add_subplot(gs[1, 2])
        resources = ['CPU', '記憶體', 'GPU']
        before = [75, 8.0, 45]
        after = [52, 4.5, 73]
        x = np.arange(len(resources))
        width = 0.35
        bars1 = ax6.bar(x - width/2, before, width, label='優化前', color='#FF6B6B', alpha=0.8)
        bars2 = ax6.bar(x + width/2, after, width, label='優化後', color='#4ECDC4', alpha=0.8)
        ax6.set_ylabel('使用率 (%)', fontsize=11, fontweight='bold')
        ax6.set_title('系統資源使用對比', fontsize=12, fontweight='bold')
        ax6.set_xticks(x)
        ax6.set_xticklabels(resources, fontsize=10)
        ax6.legend(fontsize=10)
        ax6.grid(axis='y', alpha=0.3)
        
        # 7. 訓練進度 (左下)
        ax7 = fig.add_subplot(gs[2, 0])
        epochs = np.arange(1, 11)
        accuracy = [72, 78, 83, 87, 89, 91, 92, 93, 94, 94.2]
        ax7.plot(epochs, accuracy, 'o-', linewidth=2, markersize=8, color='#4ECDC4')
        ax7.axhline(y=90, color='green', linestyle='--', linewidth=2, alpha=0.5)
        ax7.set_xlabel('訓練輪次', fontsize=11, fontweight='bold')
        ax7.set_ylabel('準確率 (%)', fontsize=11, fontweight='bold')
        ax7.set_title('模型訓練進度', fontsize=12, fontweight='bold')
        ax7.grid(True, alpha=0.3)
        ax7.set_ylim(65, 100)
        
        # 8. 滿意度趨勢 (中下)
        ax8 = fig.add_subplot(gs[2, 1])
        months = ['優化前', '1個月', '2個月', '3個月', '當前']
        satisfaction = [65, 75, 82, 85, 87.3]
        ax8.plot(months, satisfaction, 's-', linewidth=2, markersize=8, color='#95E1D3')
        ax8.axhline(y=80, color='green', linestyle='--', linewidth=2, alpha=0.5)
        ax8.set_xlabel('時間階段', fontsize=11, fontweight='bold')
        ax8.set_ylabel('滿意度 (%)', fontsize=11, fontweight='bold')
        ax8.set_title('用戶滿意度趨勢', fontsize=12, fontweight='bold')
        ax8.grid(True, alpha=0.3)
        ax8.set_ylim(60, 95)
        ax8.tick_params(axis='x', rotation=15)
        
        # 9. 綜合評分 (右下)
        ax9 = fig.add_subplot(gs[2, 2])
        categories = ['準確率', '穩定性', '效率', '滿意度']
        scores = [92.3, 98.9, 95, 87.3]
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        scores += scores[:1]
        angles += angles[:1]
        ax9 = plt.subplot(gs[2, 2], projection='polar')
        ax9.plot(angles, scores, 'o-', linewidth=2, color='#4ECDC4')
        ax9.fill(angles, scores, alpha=0.25, color='#4ECDC4')
        ax9.set_xticks(angles[:-1])
        ax9.set_xticklabels(categories, fontsize=10)
        ax9.set_ylim(0, 100)
        ax9.set_title('綜合評分雷達圖', fontsize=12, fontweight='bold', pad=20)
        ax9.grid(True)
        
        # 添加總標題
        fig.suptitle('AI 客服系統優化成效綜合儀表板', fontsize=18, fontweight='bold', y=0.98)
        
        plt.savefig(f'{self.output_dir}/10_綜合成效儀表板.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ 綜合成效儀表板已生成")

if __name__ == '__main__':
    generator = ChartGenerator(output_dir='./期末報告/charts')
    generator.generate_all_charts()
    print("\n" + "="*60)
    print("✅ 所有圖表生成完成！")
    print("="*60)
