"""
試營運報告圖表生成腳本
生成所有統計圖表
"""

import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 設定中文字體
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 配色方案
COLORS = {
    'primary': '#4A90E2',
    'success': '#51CF66',
    'warning': '#FFB84D',
    'danger': '#FF6B6B',
    'neutral': '#868E96'
}

def generate_service_trend():
    """生成服務量趨勢圖"""
    months = ['第1月', '第2月', '第3月', '第4月']
    physical = [50, 45, 40, 35]
    voice = [10, 25, 35, 45]
    total = [60, 70, 75, 80]
    
    plt.figure(figsize=(12, 6))
    plt.plot(months, physical, marker='o', label='實體訪視', 
             color=COLORS['primary'], linewidth=2)
    plt.plot(months, voice, marker='s', label='語音關懷', 
             color=COLORS['success'], linewidth=2)
    plt.plot(months, total, marker='^', label='總服務量', 
             color=COLORS['neutral'], linewidth=2, linestyle='--')
    
    plt.title('每月服務量趨勢', fontsize=16, fontweight='bold')
    plt.xlabel('月份', fontsize=12)
    plt.ylabel('服務次數', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('服務量趨勢.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✓ 服務量趨勢圖已生成')

def generate_service_distribution():
    """生成服務類型分布圖"""
    labels = ['實體訪視', '語音關懷', '廣播劇']
    sizes = [35, 45, 20]
    colors = [COLORS['primary'], COLORS['success'], COLORS['warning']]
    explode = (0.05, 0.05, 0.05)
    
    plt.figure(figsize=(10, 8))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90,
            textprops={'fontsize': 12})
    plt.title('服務類型分布', fontsize=16, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('服務類型分布.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✓ 服務類型分布圖已生成')

def generate_carbon_comparison():
    """生成碳排放對比圖"""
    categories = ['導入前', '導入後']
    values = [150, 75]
    colors_list = [COLORS['danger'], COLORS['success']]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, values, color=colors_list, width=0.5)
    
    plt.title('月平均碳排放對比', fontsize=16, fontweight='bold')
    plt.ylabel('碳排放量 (kg CO₂e)', fontsize=12)
    plt.ylim(0, 180)
    
    # 添加數值標籤
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height} kg\n(-50%)', ha='center', va='bottom', fontsize=11)
    
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('碳排放對比.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✓ 碳排放對比圖已生成')

def generate_carbon_trend():
    """生成碳排放趨勢圖"""
    months = ['第1月', '第2月', '第3月', '第4月']
    before = [150, 150, 150, 150]
    after = [120, 95, 80, 75]
    
    plt.figure(figsize=(12, 6))
    plt.plot(months, before, marker='o', label='導入前（推估）', 
             color=COLORS['danger'], linewidth=2, linestyle='--')
    plt.plot(months, after, marker='s', label='導入後（實際）', 
             color=COLORS['success'], linewidth=2)
    
    plt.title('碳排放趨勢比較', fontsize=16, fontweight='bold')
    plt.xlabel('月份', fontsize=12)
    plt.ylabel('碳排放量 (kg CO₂e)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('碳排放趨勢.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✓ 碳排放趨勢圖已生成')

def generate_cost_comparison():
    """生成成本對比圖"""
    categories = ['人力成本', '交通成本', '系統成本', '總成本']
    before = [80000, 15000, 0, 95000]
    after = [60000, 8000, 5000, 73000]
    
    x = np.arange(len(categories))
    width = 0.35
    
    plt.figure(figsize=(12, 6))
    bars1 = plt.bar(x - width/2, before, width, label='導入前', 
                    color=COLORS['danger'], alpha=0.8)
    bars2 = plt.bar(x + width/2, after, width, label='導入後', 
                    color=COLORS['success'], alpha=0.8)
    
    plt.title('成本對比分析', fontsize=16, fontweight='bold')
    plt.ylabel('金額 (元)', fontsize=12)
    plt.xticks(x, categories)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3, axis='y')
    
    # 添加數值標籤
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('成本對比.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✓ 成本對比圖已生成')

def generate_satisfaction_radar():
    """生成滿意度雷達圖"""
    categories = ['語音清晰度', '互動自然度', '內容實用性', '操作便利性', '整體滿意度']
    values = [4.5, 4.2, 4.6, 4.0, 4.4]
    
    # 計算角度
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    ax.plot(angles, values, 'o-', linewidth=2, color=COLORS['primary'])
    ax.fill(angles, values, alpha=0.25, color=COLORS['primary'])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11)
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['1', '2', '3', '4', '5'], fontsize=9)
    ax.grid(True)
    
    plt.title('長者滿意度評估（滿分5分）', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('長者滿意度雷達圖.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✓ 長者滿意度雷達圖已生成')

def generate_roi_prediction():
    """生成ROI預測曲線"""
    years = ['第1年', '第2年', '第3年', '第4年', '第5年']
    investment = [-500000, 0, 0, 0, 0]
    operating_cost = [-100000, -100000, -100000, -100000, -100000]
    benefit = [250000, 300000, 300000, 300000, 300000]
    net_benefit = [i + o + b for i, o, b in zip(investment, operating_cost, benefit)]
    cumulative = np.cumsum(net_benefit)
    
    plt.figure(figsize=(12, 6))
    plt.plot(years, cumulative, marker='o', linewidth=2, 
             color=COLORS['success'], markersize=8)
    plt.axhline(y=0, color=COLORS['neutral'], linestyle='--', alpha=0.5)
    plt.fill_between(range(len(years)), cumulative, 0, 
                     where=(np.array(cumulative) >= 0), 
                     color=COLORS['success'], alpha=0.2)
    
    plt.title('投資回報率（ROI）預測', fontsize=16, fontweight='bold')
    plt.xlabel('年度', fontsize=12)
    plt.ylabel('累計淨效益 (元)', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # 標註回本點
    for i, val in enumerate(cumulative):
        if val >= 0:
            plt.annotate('回本點', xy=(i, val), xytext=(i+0.3, val+50000),
                        arrowprops=dict(arrowstyle='->', color=COLORS['danger']),
                        fontsize=11, color=COLORS['danger'])
            break
    
    plt.tight_layout()
    plt.savefig('ROI預測.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✓ ROI預測圖已生成')

def main():
    """主函數"""
    print('開始生成圖表...\n')
    
    generate_service_trend()
    generate_service_distribution()
    generate_carbon_comparison()
    generate_carbon_trend()
    generate_cost_comparison()
    generate_satisfaction_radar()
    generate_roi_prediction()
    
    print('\n✅ 所有圖表生成完成！')
    print('圖表已儲存至當前目錄')

if __name__ == '__main__':
    main()
