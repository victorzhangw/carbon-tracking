#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
碳排放減少效益分析報告 - 圖表生成程式
生成所有碳排放分析相關圖表
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

def create_carbon_reduction_summary():
    """碳排放減少總覽圖表"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = ['交通減排', '系統排放', '淨減排', '保守估計', '最終結果']
    values = [60.47, -25.45, 35.02, 32.22, 30.23]
    colors_bar = ['#6A994E', '#C73E1D', '#2E86AB', '#F18F01', '#2E86AB']
    
    bars = ax.bar(categories, values, color=colors_bar, alpha=0.8)
    
    ax.set_ylabel('碳排放量 (噸 CO2e)', fontsize=12, fontweight='bold')
    ax.set_title('碳排放減少計算流程', fontsize=14, fontweight='bold', pad=20)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    ax.grid(axis='y', alpha=0.3)
    
    # 添加數值標籤
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.2f}', ha='center', 
               va='bottom' if height > 0 else 'top',
               fontsize=10, fontweight='bold')
    
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    plt.savefig(charts_dir / '01_碳排放減少總覽.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 生成: 01_碳排放減少總覽.png")

def create_monthly_trend():
    """每月碳排放減少趨勢"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    months = ['6月', '7月', '8月', '9月', '10月', '11月']
    monthly = [5.84, 5.84, 5.84, 5.84, 5.84, 5.84]
    cumulative = [5.84, 11.68, 17.52, 23.36, 29.20, 35.04]
    
    x = np.arange(len(months))
    width = 0.6
    
    # 每月減排柱狀圖
    bars = ax.bar(x, monthly, width, label='每月減排', color='#2E86AB', alpha=0.7)
    
    # 累積減排折線圖
    ax2 = ax.twinx()
    line = ax2.plot(x, cumulative, color='#F18F01', marker='o', linewidth=2.5,
                    markersize=8, label='累積減排')
    
    ax.set_xlabel('月份', fontsize=12, fontweight='bold')
    ax.set_ylabel('每月碳排放減少 (噸 CO2e)', fontsize=11, fontweight='bold', color='#2E86AB')
    ax2.set_ylabel('累積碳排放減少 (噸 CO2e)', fontsize=11, fontweight='bold', color='#F18F01')
    ax.tick_params(axis='y', labelcolor='#2E86AB')
    ax2.tick_params(axis='y', labelcolor='#F18F01')
    ax.set_xticks(x)
    ax.set_xticklabels(months)
    
    # 添加數值標籤
    for i, (bar, cum) in enumerate(zip(bars, cumulative)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.2f}', ha='center', va='bottom', fontsize=9)
        ax2.text(i, cum + 1, f'{cum:.2f}', ha='center', va='bottom',
                fontsize=9, color='#F18F01', fontweight='bold')
    
    ax.set_title('每月碳排放減少趨勢', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(charts_dir / '02_每月碳排放趨勢.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 生成: 02_每月碳排放趨勢.png")

def create_regional_comparison():
    """地區別碳排放減少比較"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    regions = ['台中市', '彰化縣', '雲林縣']
    elders = [1200, 1100, 1000]
    distance = [7, 18, 25]
    reduction = [10.26, 24.19, 30.54]
    
    x = np.arange(len(regions))
    width = 0.25
    
    bars1 = ax.bar(x - width, elders, width, label='服務長者數', color='#2E86AB')
    bars2 = ax.bar(x, distance, width, label='平均距離 (km)', color='#6A994E')
    bars3 = ax.bar(x + width, reduction, width, label='碳減量 (噸)', color='#F18F01')
    
    ax.set_xlabel('地區', fontsize=12, fontweight='bold')
    ax.set_ylabel('數值', fontsize=12, fontweight='bold')
    ax.set_title('地區別碳排放減少比較', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(regions)
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    
    # 添加數值標籤
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.0f}' if height > 100 else f'{height:.1f}',
                   ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(charts_dir / '03_地區別碳排放比較.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 生成: 03_地區別碳排放比較.png")

def create_vehicle_type_analysis():
    """車輛類型碳排放分析"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 使用比例圓餅圖
    types = ['機車', '汽車', '大眾運輸']
    usage = [65, 30, 5]
    colors_pie = ['#2E86AB', '#F18F01', '#6A994E']
    
    ax1.pie(usage, labels=types, autopct='%1.0f%%', startangle=90, colors=colors_pie)
    ax1.set_title('交通工具使用比例', fontsize=12, fontweight='bold', pad=15)
    
    # 碳排放減少柱狀圖
    emission_factors = [0.0695, 0.1850, 0.0295]
    reductions = [26.83, 32.97, 0.88]
    
    bars = ax2.barh(types, reductions, color=colors_pie)
    ax2.set_xlabel('碳排放減少 (噸 CO2e)', fontsize=11, fontweight='bold')
    ax2.set_title('各車輛類型碳排放減少', fontsize=12, fontweight='bold', pad=15)
    ax2.grid(axis='x', alpha=0.3)
    
    # 添加數值標籤
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax2.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.2f} 噸\n({emission_factors[i]:.4f} kg/km)',
                ha='left', va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(charts_dir / '04_車輛類型分析.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 生成: 04_車輛類型分析.png")

def create_environmental_benefits():
    """環境效益多維度分析"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    categories = ['碳排放減少\n(噸 CO2e)', '等效植樹\n(棵)', '節約汽油\n(千公升)',
                  '減少里程\n(萬公里)', '節省成本\n(萬元)']
    values = [30.23, 1374, 19.064, 59.4, 63.7]
    colors_bar = ['#2E86AB', '#6A994E', '#F18F01', '#A23B72', '#C73E1D']
    
    # 標準化數值以便比較
    normalized = [v / max(values) * 100 for v in values]
    
    bars = ax.barh(categories, normalized, color=colors_bar, alpha=0.8)
    
    ax.set_xlabel('相對值 (%)', fontsize=12, fontweight='bold')
    ax.set_title('環境效益多維度分析', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, 110)
    ax.grid(axis='x', alpha=0.3)
    
    # 添加實際數值標籤
    for i, (bar, val) in enumerate(zip(bars, values)):
        width = bar.get_width()
        if val > 100:
            label = f'{val:.0f}'
        elif val > 10:
            label = f'{val:.1f}'
        else:
            label = f'{val:.2f}'
        ax.text(width + 2, bar.get_y() + bar.get_height()/2.,
               label, ha='left', va='center', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(charts_dir / '05_環境效益分析.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 生成: 05_環境效益分析.png")

def create_pollutant_reduction():
    """其他污染物減少圖表"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    pollutants = ['氮氧化物\n(NOx)', '懸浮微粒\n(PM2.5)', '揮發性有機物\n(VOCs)', '一氧化碳\n(CO)']
    amounts = [47.5, 8.3, 17.8, 142.6]
    colors_bar = ['#C73E1D', '#A23B72', '#F18F01', '#6A994E']
    
    bars = ax.bar(pollutants, amounts, color=colors_bar, alpha=0.8)
    
    ax.set_ylabel('減少量 (kg)', fontsize=12, fontweight='bold')
    ax.set_title('空氣污染物減少統計', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3)
    
    # 添加數值標籤
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.1f} kg', ha='center', va='bottom',
               fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(charts_dir / '06_污染物減少統計.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 生成: 06_污染物減少統計.png")

def create_future_projection():
    """未來推廣碳減潛力預測"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    years = ['試營運\n2024', '第一階段\n2025', '第二階段\n2026', '第三階段\n2027']
    users = [3.3, 30, 100, 200]
    annual_reduction = [60, 550, 1833, 3666]
    cumulative = [60, 610, 2443, 6109]
    
    x = np.arange(len(years))
    width = 0.35
    
    # 年度減排柱狀圖
    bars = ax.bar(x - width/2, annual_reduction, width, label='年度減排', color='#2E86AB', alpha=0.7)
    
    # 累積減排折線圖
    ax2 = ax.twinx()
    line = ax2.plot(x, cumulative, color='#F18F01', marker='o', linewidth=2.5,
                    markersize=10, label='累積減排', linestyle='--')
    
    ax.set_xlabel('推廣階段', fontsize=12, fontweight='bold')
    ax.set_ylabel('年度碳排放減少 (噸 CO2e)', fontsize=11, fontweight='bold', color='#2E86AB')
    ax2.set_ylabel('累積碳排放減少 (噸 CO2e)', fontsize=11, fontweight='bold', color='#F18F01')
    ax.tick_params(axis='y', labelcolor='#2E86AB')
    ax2.tick_params(axis='y', labelcolor='#F18F01')
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    
    # 添加數值標籤
    for i, (bar, cum, user) in enumerate(zip(bars, cumulative, users)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.0f}噸\n({user:.1f}萬人)',
               ha='center', va='bottom', fontsize=9)
        ax2.text(i, cum + 200, f'{cum:.0f}噸', ha='center', va='bottom',
                fontsize=9, color='#F18F01', fontweight='bold')
    
    ax.set_title('未來推廣碳減潛力預測', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(charts_dir / '07_未來碳減潛力.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 生成: 07_未來碳減潛力.png")

def create_economic_benefits():
    """經濟效益分析圖表"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = ['節省燃料費', '節省時間成本', '減少醫療支出', '總經濟效益']
    values = [57, 495, 85, 637]
    colors_bar = ['#2E86AB', '#6A994E', '#F18F01', '#A23B72']
    
    bars = ax.bar(categories, values, color=colors_bar, alpha=0.8)
    
    ax.set_ylabel('金額 (萬元)', fontsize=12, fontweight='bold')
    ax.set_title('經濟效益分析（6 個月）', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3)
    
    # 添加數值標籤
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.0f} 萬元', ha='center', va='bottom',
               fontsize=10, fontweight='bold')
    
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    plt.savefig(charts_dir / '08_經濟效益分析.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ 生成: 08_經濟效益分析.png")

def main():
    """主程式"""
    print("=" * 60)
    print("碳排放減少效益分析報告 - 圖表生成程式")
    print("=" * 60)
    print()
    
    try:
        create_carbon_reduction_summary()
        create_monthly_trend()
        create_regional_comparison()
        create_vehicle_type_analysis()
        create_environmental_benefits()
        create_pollutant_reduction()
        create_future_projection()
        create_economic_benefits()
        
        print()
        print("=" * 60)
        print("✓ 所有圖表生成完成！")
        print(f"✓ 圖表保存位置: {charts_dir.absolute()}")
        print(f"✓ 共生成 8 張圖表")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ 錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
