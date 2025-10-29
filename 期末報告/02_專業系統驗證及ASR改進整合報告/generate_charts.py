#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
專業系統驗證及ASR改進整合報告 - 圖表生成程式
"""

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

# 設置中文字體
try:
    matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei']
except:
    print("警告: 無法設置中文字體")

matplotlib.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['figure.dpi'] = 100

# 創建輸出目錄
output_dir = './期末報告/02_專業系統驗證及ASR改進整合報告/charts'
os.makedirs(output_dir, exist_ok=True)

print("開始生成專業系統驗證及ASR改進整合報告圖表...")

# 1. 驗證指標達成對比
print("\n生成圖表 1/7: 驗證指標達成對比...")
metrics = ['系統驗證\n通過率', 'ASR整體\n準確率', '高齡語音\n識別率', 
           '低SNR\n環境提升', '標註一致性\nKappa', '複掃再驗證\n合格率']
targets = [95, 90, 88, 3, 0.8, 95]
actuals = [99.4, 94.2, 91.0, 5.8, 0.88, 99.6]

# 標準化顯示 (Kappa 轉為百分比)
targets_display = [95, 90, 88, 3, 80, 95]
actuals_display = [99.4, 94.2, 91.0, 5.8, 88, 99.6]

x = np.arange(len(metrics))
width = 0.35

fig, ax = plt.subplots(figsize=(14, 8))
bars1 = ax.bar(x - width/2, targets_display, width, label='目標值', color='#95E1D3', alpha=0.8)
bars2 = ax.bar(x + width/2, actuals_display, width, label='實際達成', color='#4ECDC4', alpha=0.8)

ax.set_xlabel('驗證指標', fontsize=14, fontweight='bold')
ax.set_ylabel('數值', fontsize=14, fontweight='bold')
ax.set_title('專業系統驗證指標達成對比', fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(metrics, fontsize=11)
ax.legend(fontsize=12)
ax.grid(axis='y', alpha=0.3)

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.1f}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(f'{output_dir}/01_驗證指標達成對比.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 驗證指標達成對比圖已生成")

# 2. ASR實驗組性能對比
print("生成圖表 2/7: ASR實驗組性能對比...")
experiments = ['Baseline', 'Exp-A\n(增強)', 'Exp-B\n(增強+凍結)', 'Exp-C\n(增強+分層LR)']
wer_values = [10.2, 8.5, 7.9, 5.8]
accuracy_values = [89.8, 91.5, 92.1, 94.2]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# 左圖: WER對比
bars = ax1.bar(experiments, wer_values, color=['#FF6B6B', '#FFA502', '#4ECDC4', '#95E1D3'], alpha=0.8)
ax1.set_ylabel('字錯誤率 WER (%)', fontsize=12, fontweight='bold')
ax1.set_title('ASR實驗組 WER 對比', fontsize=14, fontweight='bold')
ax1.axhline(y=10, color='red', linestyle='--', linewidth=2, label='目標值 (10%)')
ax1.legend(fontsize=10)
ax1.grid(axis='y', alpha=0.3)

for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

# 右圖: Accuracy對比
bars = ax2.bar(experiments, accuracy_values, color=['#FF6B6B', '#FFA502', '#4ECDC4', '#95E1D3'], alpha=0.8)
ax2.set_ylabel('準確率 (%)', fontsize=12, fontweight='bold')
ax2.set_title('ASR實驗組準確率對比', fontsize=14, fontweight='bold')
ax2.axhline(y=90, color='green', linestyle='--', linewidth=2, label='目標值 (90%)')
ax2.legend(fontsize=10)
ax2.set_ylim(85, 100)
ax2.grid(axis='y', alpha=0.3)

for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/02_ASR實驗組性能對比.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ ASR實驗組性能對比圖已生成")

# 3. 子集性能改善
print("生成圖表 3/7: 子集性能改善...")
subsets = ['全量樣本', '低SNR\n(<15dB)', '高齡族群\n(65+)']
baseline = [89.8, 81.3, 87.5]
exp_c = [94.2, 87.1, 91.0]
improvement = [4.4, 5.8, 3.5]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# 左圖: 準確率對比
x = np.arange(len(subsets))
width = 0.35
bars1 = ax1.bar(x - width/2, baseline, width, label='Baseline', color='#FF6B6B', alpha=0.8)
bars2 = ax1.bar(x + width/2, exp_c, width, label='Exp-C', color='#4ECDC4', alpha=0.8)

ax1.set_ylabel('準確率 (%)', fontsize=12, fontweight='bold')
ax1.set_title('不同子集準確率對比', fontsize=14, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(subsets, fontsize=11)
ax1.legend(fontsize=11)
ax1.set_ylim(75, 100)
ax1.grid(axis='y', alpha=0.3)

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=10)

# 右圖: 改善幅度
bars = ax2.barh(subsets, improvement, color='#95E1D3', alpha=0.8)
ax2.set_xlabel('改善幅度 (%)', fontsize=12, fontweight='bold')
ax2.set_title('各子集改善幅度', fontsize=14, fontweight='bold')
ax2.grid(axis='x', alpha=0.3)

for bar in bars:
    width = bar.get_width()
    ax2.text(width, bar.get_y() + bar.get_height()/2.,
            f'+{width:.1f}%', ha='left', va='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/03_子集性能改善.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 子集性能改善圖已生成")

# 4. 驗證流程時程
print("生成圖表 4/7: 驗證流程時程...")
stages = ['資產登錄', '工具選型', '性能測試', '結果匯總', '複掃驗證']
days = [1, 2, 7, 1, 9]
colors = ['#FF6B6B', '#FFA502', '#4ECDC4', '#95E1D3', '#F38181']

fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.barh(stages, days, color=colors, alpha=0.8)

ax.set_xlabel('工作天數', fontsize=14, fontweight='bold')
ax.set_title('專業系統驗證流程時程', fontsize=16, fontweight='bold', pad=20)
ax.grid(axis='x', alpha=0.3)

for bar in bars:
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height()/2.,
            f'{int(width)} 天', ha='left', va='center', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/04_驗證流程時程.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 驗證流程時程圖已生成")

# 5. 資料集分佈
print("生成圖表 5/7: 資料集分佈...")
age_groups = ['高齡\n(65+)', '中年\n(40-64)', '青年\n(18-39)']
samples = [18000, 12600, 5400]
colors = ['#FF6B6B', '#4ECDC4', '#95E1D3']

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(aspect="equal"))
wedges, texts, autotexts = ax.pie(samples, labels=age_groups, autopct='%1.1f%%',
                                    colors=colors, startangle=90, textprops={'fontsize': 12})

ax.set_title('年齡層資料集分佈 (總計36,000樣本)', fontsize=14, fontweight='bold', pad=20)

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(13)
    autotext.set_fontweight('bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/05_資料集分佈.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 資料集分佈圖已生成")

print("\n" + "="*60)
print("✅ 所有圖表生成完成！")
print(f"圖表保存位置: {output_dir}")
print("="*60)
