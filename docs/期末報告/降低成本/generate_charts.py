#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI關懷系統 - 降低成本圖表生成腳本
自動生成所有佐證文件中的視覺化圖表
"""

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from pathlib import Path

# 設定中文字體
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

# 輸出資料夾
OUTPUT_DIR = Path(__file__).parent / "圖表輸出"
OUTPUT_DIR.mkdir(exist_ok=True)

def generate_chart_1_daily_visit():
    """圖表1：每日拜訪量對比"""
    categories = ['導入前', '導入後']
    single_worker = [2, 5]
    team_total = [30, 75]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 單位社工
    bars1 = ax1.bar(categories, single_worker, color=['#FF6B6B', '#4ECDC4'])
    ax1.set_ylabel('拜訪人數（位）')
    ax1.set_title('單位社工每日拜訪量對比')
    ax1.set_ylim(0, 6)
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}位', ha='center', va='bottom')
    
    # 15人團隊
    bars2 = ax2.bar(categories, team_total, color=['#FF6B6B', '#4ECDC4'])
    ax2.set_ylabel('拜訪人數（位）')
    ax2.set_title('15人團隊每日拜訪總量對比')
    ax2.set_ylim(0, 80)
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}位', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '圖表1_每日拜訪量對比.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 已生成：圖表1_每日拜訪量對比.png")

def generate_chart_2_monthly_coverage():
    """圖表2：月度服務覆蓋對比"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = ['單人月度', '團隊月度']
    before = [60, 900]
    after = [150, 2250]
    
    x = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, before, width, label='導入前', color='#FF6B6B')
    bars2 = ax.bar(x + width/2, after, width, label='導入後', color='#4ECDC4')
    
    ax.set_ylabel('服務人次')
    ax.set_title('月度服務覆蓋對比')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '圖表2_月度服務覆蓋對比.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 已生成：圖表2_月度服務覆蓋對比.png")

def generate_chart_3_time_allocation():
    """圖表3：工作時間分配變化"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 導入前
    labels1 = ['通勤時間\n4小時', '拜訪時間\n4小時']
    sizes1 = [50, 50]
    colors1 = ['#FF6B6B', '#4ECDC4']
    ax1.pie(sizes1, labels=labels1, colors=colors1, autopct='%1.1f%%', startangle=90)
    ax1.set_title('導入前時間分配')
    
    # 導入後
    labels2 = ['通勤時間\n2小時', '拜訪時間\n5小時', '行政時間\n1小時']
    sizes2 = [25, 62.5, 12.5]
    colors2 = ['#FF6B6B', '#4ECDC4', '#95E1D3']
    ax2.pie(sizes2, labels=labels2, colors=colors2, autopct='%1.1f%%', startangle=90)
    ax2.set_title('導入後時間分配')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '圖表3_工作時間分配變化.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 已生成：圖表3_工作時間分配變化.png")

def generate_chart_4_service_mode():
    """圖表4：服務模式分布"""
    labels = ['實地拜訪\n60位', 'AI語音關懷\n90位']
    sizes = [40, 60]
    colors = ['#FF6B6B', '#4ECDC4']
    explode = (0.05, 0.05)
    
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title('導入後混合服務模式（單人月度150位）')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '圖表4_服務模式分布.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 已生成：圖表4_服務模式分布.png")

def generate_chart_5_efficiency_trend():
    """圖表5：效率提升趨勢"""
    months = ['2025/2', '2025/3', '2025/4', '2025/5', '2025/6', '2025/7', '2025/8', '2025/9', '2025/10']
    field_visit = [60, 60, 60, 60, 60, 60, 60, 60, 60]
    ai_voice = [0, 30, 45, 60, 75, 85, 90, 90, 90]
    total = [60, 90, 105, 120, 135, 145, 150, 150, 150]
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.plot(months, field_visit, marker='o', label='實地拜訪', linewidth=2, color='#FF6B6B')
    ax.plot(months, ai_voice, marker='s', label='AI語音', linewidth=2, color='#4ECDC4')
    ax.plot(months, total, marker='^', label='總計', linewidth=2, color='#F38181')
    
    ax.set_xlabel('月份')
    ax.set_ylabel('服務人次')
    ax.set_title('月度拜訪量趨勢（單位社工）- 2025年2月至10月')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '圖表5_效率提升趨勢.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 已生成：圖表5_效率提升趨勢.png")

def generate_chart_6_kpi():
    """圖表6：KPI達成狀況"""
    kpis = ['每日拜訪量', '月度覆蓋量', '車資降低', '長者滿意度', '系統穩定性']
    achievement = [100, 100, 100, 105, 102]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(kpis, achievement, color=['#4ECDC4' if x >= 100 else '#FF6B6B' for x in achievement])
    
    ax.set_xlabel('達成率（%）')
    ax.set_title('KPI達成狀況')
    ax.axvline(x=100, color='red', linestyle='--', alpha=0.5, label='目標線')
    ax.legend()
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
               f'{achievement[i]}%', ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '圖表6_KPI達成狀況.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 已生成：圖表6_KPI達成狀況.png")

def generate_chart_7_efficiency_factors():
    """圖表7：效率提升因素分析"""
    factors = ['AI語音關懷', '路線優化', '系統管理']
    contribution = [60, 25, 15]
    colors = ['#4ECDC4', '#95E1D3', '#F38181']
    
    plt.figure(figsize=(8, 6))
    plt.pie(contribution, labels=factors, colors=colors, autopct='%1.1f%%',
            startangle=90, explode=(0.1, 0, 0))
    plt.title('效率提升因素分析')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '圖表7_效率提升因素分析.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 已生成：圖表7_效率提升因素分析.png")

def generate_chart_8_quality():
    """圖表8：服務品質對比"""
    indicators = ['長者滿意度', '問題發現率', '回應時效', '記錄完整性']
    before = [87, 85, 24, 78]
    after = [89, 92, 12, 95]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(indicators))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, before, width, label='導入前', color='#FF6B6B')
    bars2 = ax.bar(x + width/2, after, width, label='導入後', color='#4ECDC4')
    
    ax.set_ylabel('數值')
    ax.set_title('服務品質指標對比')
    ax.set_xticks(x)
    ax.set_xticklabels(indicators)
    ax.legend()
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '圖表8_服務品質對比.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 已生成：圖表8_服務品質對比.png")

def generate_chart_9_monthly_trend_team():
    """圖表9：15人團隊月度趨勢"""
    months = ['2025/2', '2025/3', '2025/4', '2025/5', '2025/6', '2025/7', '2025/8', '2025/9', '2025/10']
    field_visit = [900, 900, 900, 900, 900, 900, 900, 900, 900]
    ai_voice = [0, 450, 675, 900, 1125, 1275, 1350, 1350, 1350]
    total = [900, 1350, 1575, 1800, 2025, 2175, 2250, 2250, 2250]
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    width = 0.25
    x = np.arange(len(months))
    
    bars1 = ax.bar(x - width, field_visit, width, label='實地拜訪', color='#FF6B6B')
    bars2 = ax.bar(x, ai_voice, width, label='AI語音', color='#4ECDC4')
    bars3 = ax.bar(x + width, total, width, label='總計', color='#F38181')
    
    ax.set_xlabel('月份')
    ax.set_ylabel('服務人次')
    ax.set_title('15人團隊月度服務量趨勢 - 2025年2月至10月')
    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '圖表9_團隊月度趨勢.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 已生成：圖表9_團隊月度趨勢.png")

def main():
    """主程式"""
    print("=" * 50)
    print("AI關懷系統 - 圖表生成工具")
    print("數據統計期間：2025年2月-2025年10月")
    print("=" * 50)
    print()
    
    generate_chart_1_daily_visit()
    generate_chart_2_monthly_coverage()
    generate_chart_3_time_allocation()
    generate_chart_4_service_mode()
    generate_chart_5_efficiency_trend()
    generate_chart_6_kpi()
    generate_chart_7_efficiency_factors()
    generate_chart_8_quality()
    generate_chart_9_monthly_trend_team()
    
    print()
    print("=" * 50)
    print(f"✓ 所有圖表已生成完成！")
    print(f"✓ 輸出位置：{OUTPUT_DIR}")
    print(f"✓ 統計期間：2025年2月-2025年10月")
    print("=" * 50)

if __name__ == "__main__":
    main()
