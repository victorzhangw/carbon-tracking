#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 客服語音克隆系統 - 期末報告圖表生成程式 (簡化版)
不需要 seaborn,僅使用 matplotlib
"""

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

# 設置中文字體
try:
    matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial Unicode MS']
except:
    print("警告: 無法設置中文字體,圖表可能無法正確顯示中文")

matplotlib.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['figure.dpi'] = 100

# 創建輸出目錄
output_dir = './期末報告/charts'
os.makedirs(output_dir, exist_ok=True)

print("開始生成期末報告圖表...")
print(f"輸出目錄: {output_dir}")

# 1. 核心指標對比圖
print("\n生成圖表 1/10: 核心指標對比圖...")
metrics = ['語音辨識\n準確率', '情緒辨識\n準確率', '對話任務\n完成率', '系統\n穩定性', '用戶\n滿意度']
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

for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.1f}%', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(f'{output_dir}/01_核心指標對比.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 核心指標對比圖已生成")

# 2. 改善幅度對比圖
print("生成圖表 2/10: 改善幅度對比圖...")
improvements = ['語音辨識', '情緒辨識', '對話管理', '系統穩定性', '用戶滿意度']
values = [22.1, 21.7, 22.1, 13.9, 22.3]

fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.barh(improvements, values, color='#4ECDC4', alpha=0.8)
ax.set_xlabel('改善幅度 (%)', fontsize=14, fontweight='bold')
ax.set_title('各模組改善幅度對比', fontsize=16, fontweight='bold', pad=20)
ax.grid(axis='x', alpha=0.3)

for bar in bars:
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height()/2.,
            f'+{width:.1f}%', ha='left', va='center', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/02_改善幅度對比.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 改善幅度對比圖已生成")

# 3. 訓練過程曲線
print("生成圖表 3/10: 訓練過程曲線...")
epochs = np.arange(1, 11)
train_acc = [72, 78, 83, 87, 89, 91, 92, 93, 94, 94.2]
val_acc = [70, 76, 81, 85, 87, 89, 90, 91, 92, 92.3]

fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(epochs, train_acc, 'o-', linewidth=2, label='訓練準確率', color='#FF6B6B', markersize=8)
ax.plot(epochs, val_acc, 's-', linewidth=2, label='驗證準確率', color='#4ECDC4', markersize=8)
ax.axhline(y=90, color='green', linestyle='--', linewidth=2, label='目標準確率 (90%)')
ax.set_xlabel('訓練輪次 (Epoch)', fontsize=14, fontweight='bold')
ax.set_ylabel('準確率 (%)', fontsize=14, fontweight='bold')
ax.set_title('模型訓練準確率曲線', fontsize=16, fontweight='bold', pad=20)
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)
ax.set_xticks(epochs)
ax.set_ylim(65, 100)

plt.tight_layout()
plt.savefig(f'{output_dir}/03_訓練過程曲線.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 訓練過程曲線已生成")

# 4. 年齡層識別對比
print("生成圖表 4/10: 年齡層識別對比...")
age_groups = ['高齡\n(65+)', '中年\n(40-64)', '青年\n(18-39)']
before_age = [72.1, 78.5, 82.3]
after_age = [88.6, 93.2, 96.1]

x = np.arange(len(age_groups))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 8))
bars1 = ax.bar(x - width/2, before_age, width, label='優化前', color='#FF6B6B', alpha=0.8)
bars2 = ax.bar(x + width/2, after_age, width, label='優化後', color='#4ECDC4', alpha=0.8)

ax.set_xlabel('年齡層', fontsize=14, fontweight='bold')
ax.set_ylabel('識別準確率 (%)', fontsize=14, fontweight='bold')
ax.set_title('不同年齡層語音識別準確率對比', fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(age_groups, fontsize=12)
ax.legend(fontsize=12)
ax.set_ylim(0, 110)
ax.grid(axis='y', alpha=0.3)

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(f'{output_dir}/04_年齡層識別對比.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 年齡層識別對比圖已生成")

# 5. 情緒識別對比
print("生成圖表 5/10: 情緒識別對比...")
emotions = ['中性', '開心', '焦慮', '滿意', '憤怒', '其他']
before_emotion = [75, 75, 65, 72, 78, 62]
after_emotion = [90.1, 94.1, 88.9, 91.7, 92.8, 84.5]

x = np.arange(len(emotions))
width = 0.35

fig, ax = plt.subplots(figsize=(14, 8))
bars1 = ax.bar(x - width/2, before_emotion, width, label='優化前', color='#FF6B6B', alpha=0.8)
bars2 = ax.bar(x + width/2, after_emotion, width, label='優化後', color='#4ECDC4', alpha=0.8)

ax.set_xlabel('情緒類別', fontsize=14, fontweight='bold')
ax.set_ylabel('識別準確率 (%)', fontsize=14, fontweight='bold')
ax.set_title('不同情緒類別識別準確率對比', fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(emotions, fontsize=12)
ax.legend(fontsize=12)
ax.set_ylim(0, 110)
ax.grid(axis='y', alpha=0.3)

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(f'{output_dir}/05_情緒識別對比.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 情緒識別對比圖已生成")

print("\n" + "="*60)
print("✅ 所有圖表生成完成！")
print(f"圖表保存位置: {output_dir}")
print("="*60)
