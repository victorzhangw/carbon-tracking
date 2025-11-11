"""
語音資料集驗證儀表板
Voice Dataset Validation Dashboard
"""

import sys
import os
# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
import json
from datetime import datetime, timedelta
from voice_dataset_validation_system import VoiceDatasetValidator, DatasetQualityMonitor

class ValidationDashboard:
    """驗證儀表板"""
    
    def __init__(self):
        self.validator = VoiceDatasetValidator()
        self.monitor = DatasetQualityMonitor(self.validator)
    
    def load_data(self):
        """載入資料"""
        try:
            conn = sqlite3.connect(self.validator.db_path)
            
            # 載入語音樣本資料
            samples_df = pd.read_sql_query('''
            SELECT * FROM voice_samples
            ORDER BY created_at DESC
            ''', conn)
            
            # 載入驗證日誌
            logs_df = pd.read_sql_query('''
            SELECT * FROM validation_logs
            ORDER BY timestamp DESC
            LIMIT 1000
            ''', conn)
            
            conn.close()
            
            return samples_df, logs_df
            
        except Exception as e:
            st.error(f"載入資料失敗: {str(e)}")
            return pd.DataFrame(), pd.DataFrame()
    
    def render_overview(self, samples_df):
        """渲染概覽頁面"""
        st.header("📊 資料集概覽")
        
        if samples_df.empty:
            st.warning("暫無資料")
            return
        
        # 基本統計
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_samples = len(samples_df)
            st.metric("總樣本數", total_samples)
        
        with col2:
            passed_samples = len(samples_df[samples_df['validation_status'] == 'passed'])
            st.metric("通過驗證", passed_samples)
        
        with col3:
            pass_rate = passed_samples / total_samples if total_samples > 0 else 0
            st.metric("通過率", f"{pass_rate:.1%}")
        
        with col4:
            total_duration = samples_df[samples_df['validation_status'] == 'passed']['duration'].sum()
            st.metric("有效時長", f"{total_duration/3600:.1f} 小時")
        
        # 驗證狀態分佈
        st.subheader("驗證狀態分佈")
        status_counts = samples_df['validation_status'].value_counts()
        
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="驗證狀態分佈",
            color_discrete_map={
                'passed': '#28a745',
                'failed': '#dc3545',
                'pending': '#ffc107'
            }
        )
        st.plotly_chart(fig_status, use_container_width=True)
        
        # 品質分數分佈
        st.subheader("品質分數分佈")
        passed_df = samples_df[samples_df['validation_status'] == 'passed']
        
        if not passed_df.empty:
            fig_quality = px.histogram(
                passed_df,
                x='quality_score',
                nbins=20,
                title="品質分數分佈",
                labels={'quality_score': '品質分數', 'count': '樣本數'}
            )
            fig_quality.add_vline(
                x=0.7, 
                line_dash="dash", 
                line_color="red",
                annotation_text="最低標準 (0.7)"
            )
            st.plotly_chart(fig_quality, use_container_width=True)
    
    def render_distribution_analysis(self, samples_df):
        """渲染分佈分析頁面"""
        st.header("📈 分佈分析")
        
        if samples_df.empty:
            st.warning("暫無資料")
            return
        
        passed_df = samples_df[samples_df['validation_status'] == 'passed']
        
        if passed_df.empty:
            st.warning("暫無通過驗證的資料")
            return
        
        # 創建子圖
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('情緒分佈', '意圖分佈', '年齡分佈', '性別分佈'),
            specs=[[{"type": "pie"}, {"type": "pie"}],
                   [{"type": "pie"}, {"type": "pie"}]]
        )
        
        # 情緒分佈
        emotion_counts = passed_df['emotion'].value_counts()
        fig.add_trace(
            go.Pie(labels=emotion_counts.index, values=emotion_counts.values, name="情緒"),
            row=1, col=1
        )
        
        # 意圖分佈
        intent_counts = passed_df['intent'].value_counts()
        fig.add_trace(
            go.Pie(labels=intent_counts.index, values=intent_counts.values, name="意圖"),
            row=1, col=2
        )
        
        # 年齡分佈
        age_counts = passed_df['age_group'].value_counts()
        fig.add_trace(
            go.Pie(labels=age_counts.index, values=age_counts.values, name="年齡"),
            row=2, col=1
        )
        
        # 性別分佈
        gender_counts = passed_df['gender'].value_counts()
        fig.add_trace(
            go.Pie(labels=gender_counts.index, values=gender_counts.values, name="性別"),
            row=2, col=2
        )
        
        fig.update_layout(height=800, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
        # 平衡性分析
        st.subheader("資料平衡性分析")
        balance_report = self.monitor.check_data_balance()
        
        for dimension, info in balance_report.items():
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.metric(
                    f"{dimension.replace('_', ' ').title()} 平衡比例",
                    f"{info['ratio']:.2f}",
                    delta=None
                )
                
                if info['recommendation'] == 'balanced':
                    st.success("✅ 平衡")
                else:
                    st.warning("⚠️ 不平衡")
            
            with col2:
                # 顯示詳細分佈
                dist_df = pd.DataFrame(list(info['distribution'].items()), 
                                     columns=['類別', '數量'])
                st.bar_chart(dist_df.set_index('類別'))
    
    def render_quality_monitoring(self, samples_df):
        """渲染品質監控頁面"""
        st.header("🔍 品質監控")
        
        # 品質警告
        alerts = self.monitor.generate_quality_alerts()
        
        if alerts:
            st.subheader("⚠️ 品質警告")
            for alert in alerts:
                severity_color = {
                    'high': 'error',
                    'medium': 'warning',
                    'low': 'info'
                }
                
                getattr(st, severity_color.get(alert['severity'], 'info'))(
                    f"**{alert['message']}**\n\n建議: {alert['recommendation']}"
                )
        else:
            st.success("✅ 目前無品質警告")
        
        if samples_df.empty:
            return
        
        # 時間趨勢分析
        st.subheader("驗證趨勢")
        
        # 按日期統計驗證結果
        samples_df['date'] = pd.to_datetime(samples_df['created_at']).dt.date
        daily_stats = samples_df.groupby(['date', 'validation_status']).size().unstack(fill_value=0)
        
        if not daily_stats.empty:
            fig_trend = px.line(
                daily_stats.reset_index(),
                x='date',
                y=['passed', 'failed'],
                title="每日驗證趨勢",
                labels={'value': '樣本數', 'date': '日期'}
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        
        # 常見錯誤分析
        st.subheader("常見驗證錯誤")
        failed_df = samples_df[samples_df['validation_status'] == 'failed']
        
        if not failed_df.empty:
            # 解析錯誤訊息
            error_counts = {}
            for errors_json in failed_df['validation_errors'].dropna():
                try:
                    errors = json.loads(errors_json)
                    for error in errors:
                        error_counts[error] = error_counts.get(error, 0) + 1
                except:
                    continue
            
            if error_counts:
                error_df = pd.DataFrame(list(error_counts.items()), 
                                      columns=['錯誤類型', '出現次數'])
                error_df = error_df.sort_values('出現次數', ascending=False).head(10)
                
                fig_errors = px.bar(
                    error_df,
                    x='出現次數',
                    y='錯誤類型',
                    orientation='h',
                    title="前10個常見錯誤"
                )
                st.plotly_chart(fig_errors, use_container_width=True)
        else:
            st.info("暫無驗證失敗的樣本")
    
    def render_sample_details(self, samples_df):
        """渲染樣本詳情頁面"""
        st.header("📋 樣本詳情")
        
        if samples_df.empty:
            st.warning("暫無資料")
            return
        
        # 篩選選項
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox(
                "驗證狀態",
                ['全部'] + list(samples_df['validation_status'].unique())
            )
        
        with col2:
            emotion_filter = st.selectbox(
                "情緒類型",
                ['全部'] + list(samples_df['emotion'].unique())
            )
        
        with col3:
            age_filter = st.selectbox(
                "年齡群組",
                ['全部'] + list(samples_df['age_group'].unique())
            )
        
        # 應用篩選
        filtered_df = samples_df.copy()
        
        if status_filter != '全部':
            filtered_df = filtered_df[filtered_df['validation_status'] == status_filter]
        
        if emotion_filter != '全部':
            filtered_df = filtered_df[filtered_df['emotion'] == emotion_filter]
        
        if age_filter != '全部':
            filtered_df = filtered_df[filtered_df['age_group'] == age_filter]
        
        # 顯示篩選結果
        st.write(f"共找到 {len(filtered_df)} 個樣本")
        
        # 樣本列表
        if not filtered_df.empty:
            # 選擇要顯示的欄位
            display_columns = [
                'file_id', 'transcript', 'speaker_type', 'emotion', 'intent',
                'age_group', 'gender', 'quality_score', 'validation_status'
            ]
            
            display_df = filtered_df[display_columns].copy()
            display_df['transcript'] = display_df['transcript'].str[:50] + '...'
            
            st.dataframe(display_df, use_container_width=True)
            
            # 匯出功能
            if st.button("匯出篩選結果"):
                csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="下載 CSV 檔案",
                    data=csv,
                    file_name=f"voice_samples_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    def render_logs(self, logs_df):
        """渲染日誌頁面"""
        st.header("📝 驗證日誌")
        
        if logs_df.empty:
            st.warning("暫無日誌資料")
            return
        
        # 日誌統計
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("總日誌數", len(logs_df))
        
        with col2:
            success_logs = len(logs_df[logs_df['status'] == 'passed'])
            st.metric("成功驗證", success_logs)
        
        with col3:
            failed_logs = len(logs_df[logs_df['status'] == 'failed'])
            st.metric("驗證失敗", failed_logs)
        
        # 日誌類型分佈
        st.subheader("日誌類型分佈")
        type_counts = logs_df['validation_type'].value_counts()
        
        fig_types = px.bar(
            x=type_counts.index,
            y=type_counts.values,
            title="驗證類型分佈",
            labels={'x': '驗證類型', 'y': '次數'}
        )
        st.plotly_chart(fig_types, use_container_width=True)
        
        # 最近日誌
        st.subheader("最近日誌 (最新100筆)")
        recent_logs = logs_df.head(100)
        
        # 格式化顯示
        display_logs = recent_logs[['timestamp', 'file_id', 'validation_type', 'status', 'message']].copy()
        display_logs['timestamp'] = pd.to_datetime(display_logs['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
        display_logs['message'] = display_logs['message'].str[:100] + '...'
        
        st.dataframe(display_logs, use_container_width=True)

def main():
    """主函數"""
    st.set_page_config(
        page_title="語音資料集驗證系統",
        page_icon="🎤",
        layout="wide"
    )
    
    st.title("🎤 高齡語音資料集驗證與監控系統")
    st.markdown("---")
    
    # 初始化儀表板
    dashboard = ValidationDashboard()
    
    # 載入資料
    with st.spinner("載入資料中..."):
        samples_df, logs_df = dashboard.load_data()
    
    # 側邊欄導航
    st.sidebar.title("導航")
    page = st.sidebar.selectbox(
        "選擇頁面",
        ["概覽", "分佈分析", "品質監控", "樣本詳情", "驗證日誌"]
    )
    
    # 顯示對應頁面
    if page == "概覽":
        dashboard.render_overview(samples_df)
    elif page == "分佈分析":
        dashboard.render_distribution_analysis(samples_df)
    elif page == "品質監控":
        dashboard.render_quality_monitoring(samples_df)
    elif page == "樣本詳情":
        dashboard.render_sample_details(samples_df)
    elif page == "驗證日誌":
        dashboard.render_logs(logs_df)
    
    # 側邊欄資訊
    st.sidebar.markdown("---")
    st.sidebar.info(
        "**系統資訊**\n\n"
        "- 資料集規模: 450 小時\n"
        "- 訓練集: 360 小時\n"
        "- 驗證集: 45 小時\n"
        "- 測試集: 45 小時\n"
        "- 標註準確度: 96%+"
    )

if __name__ == "__main__":
    main()