#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
推廣成果摘要報告 - 圖表生成程式
生成所有推廣分析相關圖表
"""

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
from pathlib import Path

# 設定中文字體
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

# 創建圖表資料夾
charts_dir = Path('charts')
charts_dir.mkdir(exist_ok=True)

# 設定圖表樣式
plt.style.use('seaborn-v0_8-darkgrid')
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']

def create_kpi_achievement_chart():
    """核心KPI達成率圖表"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    kpis = ['網站曝光', '網站訪問', '點擊率', '轉換次數', '轉換率', '使用人次', '用戶滿意度']
    target = [100, 100, 100, 100, 100, 100, 100]
    actual = [122.5, 122.5, 120, 122.5, 125, 125, 109.1]
    
    x = np.arange(len(kpis))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, target, width, label='目標', color='#95B8D1', alpha=0.7)
    bars2 = ax.bar(x + width/2, actual, width, label='實際達成', color='#2E86AB')
    
    ax.set_xlabel('KPI 指標', fontsize=12, fontweight='bold')
    ax.set_ylabel('達成率 (%)', fontsize=12, fontweight='bold')
    ax.set_title('核心推廣指標達成情況', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(kpis, rotation=45, ha='right')
    ax.legend(fontsize=10)
    ax.axhline(y=100, color='red', linestyle='--', alpha=0.5, label='目標線')
    ax.grid(axis='y', alpha=0.3)
    
    # 添加數值標籤
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(charts_dir / '01_核心KPI達成率.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 生成: 01_核心KPI達成率.png")

def create_traffic_source_chart():
    """流量來源分析圖表"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 流量來源比例
    sources = ['關鍵字廣告', 'GDN展示', '社群媒體', '自然搜尋', '直接流量']
    visits = [45200, 18900, 9400, 5850, 2945]
    
    ax1.pie(visits, labels=sources, autopct='%1.1f%%', startangle=90, colors=colors)
    ax1.set_title('流量來源分佈', fontsize=12, fontweight='bold', pad=15)
    
    # 轉換率比較
    conversion_rates = [1.2, 0.8, 0.9, 1.0, 2.1]
    bars = ax2.barh(sources, conversion_rates, color=colors)
    ax2.set_xlabel('轉換率 (%)', fontsize=11, fontweight='bold')
    ax2.set_title('各流量來源轉換率', fontsize=12, fontweight='bold', pad=15)
    ax2.grid(axis='x', alpha=0.3)
    
    # 添加數值標籤
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax2.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%', ha='left', va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(charts_dir / '02_流量來源分析.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 生成: 02_流量來源分析.png")

def create_conversion_funnel_chart():
    """轉換漏斗圖表"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    stages = ['網站曝光', '點擊訪問', '轉換行動', '註冊會員', '正式訂閱']
    values = [2450000, 73500, 735, 294, 220]
    rates = [100, 3.0, 1.0, 40, 75]
    
    # 計算漏斗寬度
    max_val = max(values)
    widths = [v/max_val for v in values]
    
    y_positions = np.arange(len(stages))
    
    for i, (stage, width, value, rate) in enumerate(zip(stages, widths, values, rates)):
        # 繪製漏斗
        ax.barh(i, width, height=0.8, color=colors[i % len(colors)], alpha=0.7)
        
        # 添加標籤
        ax.text(width/2, i, f'{stage}\n{value:,}', 
               ha='center', va='center', fontsize=10, fontweight='bold', color='white')
        
        # 添加轉換率
        if i > 0:
            ax.text(width + 0.02, i, f'↓ {rate}%', 
                   ha='left', va='center', fontsize=9, color='red')
    
    ax.set_yticks([])
    ax.set_xlim(0, 1.2)
    ax.set_title('推廣轉換漏斗分析', fontsize=14, fontweight='bold', pad=20)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(charts_dir / '03_轉換漏斗分析.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 生成: 03_轉換漏斗分析.png")

def create_user_retention_chart():
    """用戶留存率圖表"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    periods = ['第1週', '第1個月', '第3個月', '第6個月']
    users = [4250, 3400, 2550, 1900]
    retention = [85, 68, 51, 38]
    
    x = np.arange(len(periods))
    
    # 用戶數柱狀圖
    ax1 = ax
    bars = ax1.bar(x, users, color='#2E86AB', alpha=0.7, label='活躍用戶數')
    ax1.set_xlabel('時間週期', fontsize=12, fontweight='bold')
    ax1.set_ylabel('活躍用戶數', fontsize=12, fontweight='bold', color='#2E86AB')
    ax1.tick_params(axis='y', labelcolor='#2E86AB')
    ax1.set_xticks(x)
    ax1.set_xticklabels(periods)
    
    # 留存率折線圖
    ax2 = ax1.twinx()
    line = ax2.plot(x, retention, color='#F18F01', marker='o', linewidth=2, 
                    markersize=8, label='留存率')
    ax2.set_ylabel('留存率 (%)', fontsize=12, fontweight='bold', color='#F18F01')
    ax2.tick_params(axis='y', labelcolor='#F18F01')
    ax2.set_ylim(0, 100)
    
    # 添加數值標籤
    for i, (bar, ret) in enumerate(zip(bars, retention)):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:,}', ha='center', va='bottom', fontsize=9)
        ax2.text(i, ret + 2, f'{ret}%', ha='center', va='bottom', 
                fontsize=9, color='#F18F01', fontweight='bold')
    
    ax1.set_title('用戶留存率趨勢', fontsize=14, fontweight='bold', pad=20)
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax1.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(charts_dir / '04_用戶留存率趨勢.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 生成: 04_用戶留存率趨勢.png")

def create_satisfaction_chart():
    """用戶滿意度圖表"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    categories = ['操作簡便性', '回應準確性', '情感溫暖度', '功能實用性', '整體滿意度']
    very_satisfied = [45, 38, 39, 41, 42.5]
    satisfied = [44, 45, 52, 45, 44.8]
    neutral = [9, 12, 7, 11, 11]
    dissatisfied = [2, 5, 2, 3, 3]
    
    x = np.arange(len(categories))
    width = 0.6
    
    p1 = ax.bar(x, very_satisfied, width, label='非常滿意', color='#2E86AB')
    p2 = ax.bar(x, satisfied, width, bottom=very_satisfied, label='滿意', color='#6A994E')
    p3 = ax.bar(x, neutral, width, 
               bottom=np.array(very_satisfied)+np.array(satisfied), 
               label='普通', color='#F18F01')
    p4 = ax.bar(x, dissatisfied, width,
               bottom=np.array(very_satisfied)+np.array(satisfied)+np.array(neutral),
               label='不滿意', color='#C73E1D')
    
    ax.set_ylabel('比例 (%)', fontsize=12, fontweight='bold')
    ax.set_title('用戶滿意度調查結果 (N=2,970)', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.legend(loc='upper right', fontsize=10)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)
    
    # 添加總滿意度標籤
    total_satisfied = [vs + s for vs, s in zip(very_satisfied, satisfied)]
    for i, total in enumerate(total_satisfied):
        ax.text(i, total + 2, f'{total:.1f}%', ha='center', va='bottom',
               fontsize=10, fontweight='bold', color='green')
    
    plt.tight_layout()
    plt.savefig(charts_dir / '05_用戶滿意度調查.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 生成: 05_用戶滿意度調查.png")

def create_age_acceptance_chart():
    """年齡層接受度圖表"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    age_groups = ['65-70歲', '71-75歲', '76-80歲', '80歲以上']
    acceptance = [92, 85, 78, 71]
    frequency = [4.5, 3.8, 3.2, 2.5]  # 使用頻率評分 (1-5)
    
    x = np.arange(len(age_groups))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, acceptance, width, label='接受度 (%)', color='#2E86AB')
    
    ax2 = ax.twinx()
    bars2 = ax2.bar(x + width/2, frequency, width, label='使用頻率', color='#F18F01', alpha=0.7)
    
    ax.set_xlabel('年齡層', fontsize=12, fontweight='bold')
    ax.set_ylabel('接受度 (%)', fontsize=12, fontweight='bold', color='#2E86AB')
    ax.tick_params(axis='y', labelcolor='#2E86AB')
    ax.set_xticks(x)
    ax.set_xticklabels(age_groups)
    ax.set_ylim(0, 100)
    
    ax2.set_ylabel('使用頻率評分 (1-5)', fontsize=12, fontweight='bold', color='#F18F01')
    ax2.tick_params(axis='y', labelcolor='#F18F01')
    ax2.set_ylim(0, 5)
    
    # 添加數值標籤
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height}%', ha='center', va='bottom', fontsize=9)
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}', ha='center', va='bottom', fontsize=9)
    
    ax.set_title('不同年齡層接受度與使用頻率', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(charts_dir / '06_年齡層接受度分析.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 生成: 06_年齡層接受度分析.png")

def create_regional_analysis_chart():
    """地區差異分析圖表"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    regions = ['都市地區', '郊區地區', '偏鄉地區']
    acceptance = [90, 82, 75]
    network = [95, 80, 60]  # 網路環境評分
    support = [90, 75, 50]  # 技術支援評分
    
    x = np.arange(len(regions))
    width = 0.25
    
    bars1 = ax.bar(x - width, acceptance, width, label='接受度', color='#2E86AB')
    bars2 = ax.bar(x, network, width, label='網路環境', color='#6A994E')
    bars3 = ax.bar(x + width, support, width, label='技術支援', color='#F18F01')
    
    ax.set_xlabel('地區類型', fontsize=12, fontweight='bold')
    ax.set_ylabel('評分 (%)', fontsize=12, fontweight='bold')
    ax.set_title('地區差異分析', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(regions)
    ax.legend(fontsize=10)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)
    
    # 添加數值標籤
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height}%', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(charts_dir / '07_地區差異分析.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 生成: 07_地區差異分析.png")

def create_revenue_forecast_chart():
    """營收預測圖表"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    years = ['2025', '2026', '2027']
    b2g = [30, 60, 100]
    b2b = [15, 30, 50]
    b2c = [5, 20, 50]
    
    x = np.arange(len(years))
    width = 0.6
    
    p1 = ax.bar(x, b2g, width, label='B2G (政府)', color='#2E86AB')
    p2 = ax.bar(x, b2b, width, bottom=b2g, label='B2B (企業)', color='#6A994E')
    p3 = ax.bar(x, b2c, width, bottom=np.array(b2g)+np.array(b2b), 
               label='B2C (家庭)', color='#F18F01')
    
    ax.set_xlabel('年度', fontsize=12, fontweight='bold')
    ax.set_ylabel('營收 (百萬元)', fontsize=12, fontweight='bold')
    ax.set_title('未來三年營收預測', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    
    # 添加總營收標籤
    total_revenue = [g + b + c for g, b, c in zip(b2g, b2b, b2c)]
    for i, total in enumerate(total_revenue):
        ax.text(i, total + 3, f'總計: {total}M', ha='center', va='bottom',
               fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(charts_dir / '08_營收預測.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 生成: 08_營收預測.png")

def create_partnership_chart():
    """合作單位統計圖表"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 合作單位類型
    types = ['政府機構', 'NGO/NPO', '企業']
    counts = [3, 5, 8]
    colors_pie = ['#2E86AB', '#6A994E', '#F18F01']
    
    ax1.pie(counts, labels=types, autopct='%1.0f%%', startangle=90, colors=colors_pie)
    ax1.set_title('合作單位類型分佈', fontsize=12, fontweight='bold', pad=15)
    
    # 服務成果
    categories = ['服務長者', '志工人次', '活動場次', '服務據點']
    values = [3300, 900, 77, 28]
    
    bars = ax2.barh(categories, values, color=colors[:4])
    ax2.set_xlabel('數量', fontsize=11, fontweight='bold')
    ax2.set_title('合作服務成果統計', fontsize=12, fontweight='bold', pad=15)
    ax2.grid(axis='x', alpha=0.3)
    
    # 添加數值標籤
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax2.text(width, bar.get_y() + bar.get_height()/2.,
                f'{values[i]:,}', ha='left', va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(charts_dir / '09_合作單位統計.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 生成: 09_合作單位統計.png")

def create_roi_analysis_chart():
    """ROI分析圖表"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    metrics = ['廣告支出', '預估收益', 'ROI']
    values = [918750, 2940000, 220]
    colors_bar = ['#C73E1D', '#6A994E', '#2E86AB']
    
    # 使用不同的y軸範圍
    ax1 = ax
    bars1 = ax1.bar([0, 1], [values[0]/1000, values[1]/1000], 
                    color=colors_bar[:2], alpha=0.7, width=0.6)
    ax1.set_ylabel('金額 (千元)', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, 3500)
    
    ax2 = ax1.twinx()
    bars2 = ax2.bar([2], [values[2]], color=colors_bar[2], alpha=0.7, width=0.6)
    ax2.set_ylabel('ROI (%)', fontsize=12, fontweight='bold', color='#2E86AB')
    ax2.tick_params(axis='y', labelcolor='#2E86AB')
    ax2.set_ylim(0, 300)
    
    ax1.set_xticks([0, 1, 2])
    ax1.set_xticklabels(metrics)
    ax1.set_title('行銷投資報酬率分析', fontsize=14, fontweight='bold', pad=20)
    
    # 添加數值標籤
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}K', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax1.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(charts_dir / '10_ROI分析.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 生成: 10_ROI分析.png")

def main():
    """主程式"""
    print("=" * 60)
    print("推廣成果摘要報告 - 圖表生成程式")
    print("=" * 60)
    print()
    
    try:
        create_kpi_achievement_chart()
        create_traffic_source_chart()
        create_conversion_funnel_chart()
        create_user_retention_chart()
        create_satisfaction_chart()
        create_age_acceptance_chart()
        create_regional_analysis_chart()
        create_revenue_forecast_chart()
        create_partnership_chart()
        create_roi_analysis_chart()
        
        print()
        print("=" * 60)
        print("✓ 所有圖表生成完成！")
        print(f"✓ 圖表保存位置: {charts_dir.absolute()}")
        print(f"✓ 共生成 10 張圖表")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ 錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
