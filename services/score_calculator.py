"""
評分計算服務
計算情緒、語音、文字三個維度的評分
"""
import re
from collections import Counter

class ScoreCalculator:
    
    def __init__(self):
        # 評分權重配置
        self.weights = {
            'emotion': {
                'diversity': 0.30,
                'appropriateness': 0.40,
                'intensity': 0.20,
                'consistency': 0.10
            },
            'voice': {
                'clarity': 0.40,
                'volume': 0.20,
                'speed': 0.20,
                'fluency': 0.20
            },
            'content': {
                'length': 0.20,
                'richness': 0.30,
                'coherence': 0.30,
                'engagement': 0.20
            }
        }
    
    def calculate_all_scores(self, conversations):
        """計算所有維度的評分"""
        # 分離用戶和 AI 對話
        user_conversations = [c for c in conversations if c['speaker'] == 'user']
        
        # 計算各維度評分
        emotion_score, emotion_details = self.calculate_emotion_score(conversations)
        voice_score, voice_details = self.calculate_voice_score(user_conversations)
        content_score, content_details = self.calculate_content_score(user_conversations)
        
        # 計算綜合評分
        overall_score = self.calculate_overall_score(
            emotion_score, voice_score, content_score
        )
        
        # 合併所有詳情
        all_details = emotion_details + voice_details + content_details
        
        # 生成改進建議
        suggestions = self.generate_suggestions({
            'emotion': emotion_score,
            'voice': voice_score,
            'content': content_score,
            'emotion_details': {d['sub_category']: d['score'] for d in emotion_details},
            'voice_details': {d['sub_category']: d['score'] for d in voice_details},
            'content_details': {d['sub_category']: d['score'] for d in content_details}
        })
        
        return {
            'emotion': round(emotion_score, 1),
            'voice': round(voice_score, 1),
            'content': round(content_score, 1),
            'overall': round(overall_score, 1),
            'details': all_details,
            'suggestions': suggestions
        }
    
    # ==================== 情緒評分 ====================
    
    def calculate_emotion_score(self, conversations):
        """計算情緒表達評分"""
        if not conversations:
            return 0, []
        
        # 提取所有情緒
        sentiments = [c.get('sentiment') for c in conversations if c.get('sentiment')]
        
        # 1. 情緒多樣性 (30%)
        unique_sentiments = len(set(sentiments))
        diversity_score = min(unique_sentiments * 10, 30)
        
        # 2. 情緒恰當性 (40%) - 簡化版：假設情緒都是恰當的
        appropriateness_score = 35.0 if sentiments else 0
        
        # 3. 情緒強度 (20%) - 基於情緒分數
        sentiment_scores = [c.get('sentiment_score', 0.5) for c in conversations if c.get('sentiment_score')]
        avg_intensity = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.5
        intensity_score = avg_intensity * 20
        
        # 4. 情緒一致性 (10%) - 簡化版：基於情緒變化
        consistency_score = 8.0 if len(sentiments) > 1 else 10.0
        
        total_score = diversity_score + appropriateness_score + intensity_score + consistency_score
        
        details = [
            {
                'category': 'emotion',
                'sub_category': 'diversity',
                'score': diversity_score,
                'weight': self.weights['emotion']['diversity'],
                'description': f'情緒多樣性：出現 {unique_sentiments} 種不同情緒'
            },
            {
                'category': 'emotion',
                'sub_category': 'appropriateness',
                'score': appropriateness_score,
                'weight': self.weights['emotion']['appropriateness'],
                'description': '情緒恰當性：情緒與內容匹配'
            },
            {
                'category': 'emotion',
                'sub_category': 'intensity',
                'score': intensity_score,
                'weight': self.weights['emotion']['intensity'],
                'description': f'情緒強度：平均強度 {avg_intensity:.2f}'
            },
            {
                'category': 'emotion',
                'sub_category': 'consistency',
                'score': consistency_score,
                'weight': self.weights['emotion']['consistency'],
                'description': '情緒一致性：情緒轉換合理'
            }
        ]
        
        return min(total_score, 100), details
    
    # ==================== 語音評分 ====================
    
    def calculate_voice_score(self, user_conversations):
        """計算語音品質評分"""
        if not user_conversations:
            return 0, []
        
        # 1. 清晰度 (40%) - 基於 ASR 信心度（模擬）
        clarity_score = 35.0  # 假設清晰度良好
        
        # 2. 音量 (20%) - 檢查音量是否適中
        volumes = [c.get('audio_volume', 50) for c in user_conversations if c.get('audio_volume')]
        avg_volume = sum(volumes) / len(volumes) if volumes else 50
        # 理想音量範圍 40-70
        if 40 <= avg_volume <= 70:
            volume_score = 20.0
        elif 30 <= avg_volume < 40 or 70 < avg_volume <= 80:
            volume_score = 15.0
        else:
            volume_score = 10.0
        
        # 3. 語速 (20%) - 檢查語速是否適中
        speeds = [c.get('words_per_minute', 150) for c in user_conversations if c.get('words_per_minute')]
        avg_speed = sum(speeds) / len(speeds) if speeds else 150
        # 理想語速 120-180 字/分鐘
        if 120 <= avg_speed <= 180:
            speed_score = 20.0
        elif 100 <= avg_speed < 120 or 180 < avg_speed <= 200:
            speed_score = 15.0
        else:
            speed_score = 10.0
        
        # 4. 流暢度 (20%) - 基於停頓次數
        pauses = [c.get('pause_count', 0) for c in user_conversations if c.get('pause_count') is not None]
        avg_pauses = sum(pauses) / len(pauses) if pauses else 0
        # 理想停頓次數 < 3
        if avg_pauses < 3:
            fluency_score = 20.0
        elif avg_pauses < 5:
            fluency_score = 15.0
        else:
            fluency_score = 10.0
        
        total_score = clarity_score + volume_score + speed_score + fluency_score
        
        details = [
            {
                'category': 'voice',
                'sub_category': 'clarity',
                'score': clarity_score,
                'weight': self.weights['voice']['clarity'],
                'description': '清晰度：發音清晰'
            },
            {
                'category': 'voice',
                'sub_category': 'volume',
                'score': volume_score,
                'weight': self.weights['voice']['volume'],
                'description': f'音量：平均 {avg_volume:.0f}'
            },
            {
                'category': 'voice',
                'sub_category': 'speed',
                'score': speed_score,
                'weight': self.weights['voice']['speed'],
                'description': f'語速：{avg_speed:.0f} 字/分鐘'
            },
            {
                'category': 'voice',
                'sub_category': 'fluency',
                'score': fluency_score,
                'weight': self.weights['voice']['fluency'],
                'description': f'流暢度：平均停頓 {avg_pauses:.1f} 次'
            }
        ]
        
        return min(total_score, 100), details
    
    # ==================== 文字評分 ====================
    
    def calculate_content_score(self, user_conversations):
        """計算文字內容評分"""
        if not user_conversations:
            return 0, []
        
        # 1. 內容長度 (20%) - 平均每次對話的字數
        word_counts = [c.get('word_count', 0) for c in user_conversations]
        avg_length = sum(word_counts) / len(word_counts) if word_counts else 0
        # 理想長度 20-50 字
        if 20 <= avg_length <= 50:
            length_score = 20.0
        elif 10 <= avg_length < 20 or 50 < avg_length <= 80:
            length_score = 15.0
        else:
            length_score = 10.0
        
        # 2. 內容豐富度 (30%) - 詞彙多樣性
        all_text = ' '.join([c.get('text', '') for c in user_conversations])
        total_words = len(all_text)
        unique_words = len(set(all_text))
        diversity_ratio = unique_words / total_words if total_words > 0 else 0
        richness_score = min(diversity_ratio * 60, 30)
        
        # 3. 邏輯連貫性 (30%) - 簡化版：基於對話輪數
        conversation_count = len(user_conversations)
        if conversation_count >= 5:
            coherence_score = 30.0
        elif conversation_count >= 3:
            coherence_score = 25.0
        else:
            coherence_score = 20.0
        
        # 4. 互動參與度 (20%) - 基於對話輪數和回應質量
        if conversation_count >= 8:
            engagement_score = 20.0
        elif conversation_count >= 5:
            engagement_score = 15.0
        else:
            engagement_score = 10.0
        
        total_score = length_score + richness_score + coherence_score + engagement_score
        
        details = [
            {
                'category': 'content',
                'sub_category': 'length',
                'score': length_score,
                'weight': self.weights['content']['length'],
                'description': f'內容長度：平均 {avg_length:.0f} 字'
            },
            {
                'category': 'content',
                'sub_category': 'richness',
                'score': richness_score,
                'weight': self.weights['content']['richness'],
                'description': f'內容豐富度：詞彙多樣性 {diversity_ratio:.2%}'
            },
            {
                'category': 'content',
                'sub_category': 'coherence',
                'score': coherence_score,
                'weight': self.weights['content']['coherence'],
                'description': f'邏輯連貫性：{conversation_count} 輪對話'
            },
            {
                'category': 'content',
                'sub_category': 'engagement',
                'score': engagement_score,
                'weight': self.weights['content']['engagement'],
                'description': f'互動參與度：{conversation_count} 輪對話'
            }
        ]
        
        return min(total_score, 100), details
    
    # ==================== 綜合評分 ====================
    
    def calculate_overall_score(self, emotion_score, voice_score, content_score):
        """計算綜合評分"""
        overall = (
            emotion_score * 0.35 +
            voice_score * 0.35 +
            content_score * 0.30
        )
        return overall
    
    # ==================== 改進建議 ====================
    
    def generate_suggestions(self, scores):
        """生成改進建議"""
        suggestions = []
        
        # 情緒表達建議
        if scores['emotion'] < 75:
            emotion_details = scores.get('emotion_details', {})
            
            if emotion_details.get('diversity', 0) < 20:
                suggestions.append({
                    'category': '情緒表達',
                    'icon': '😊',
                    'text': '嘗試表達更多樣的情緒，讓對話更生動',
                    'priority': 'high'
                })
            
            if emotion_details.get('intensity', 0) < 15:
                suggestions.append({
                    'category': '情緒表達',
                    'icon': '💪',
                    'text': '可以更明確地表達你的感受和情緒',
                    'priority': 'medium'
                })
        
        # 語音品質建議
        if scores['voice'] < 75:
            voice_details = scores.get('voice_details', {})
            
            if voice_details.get('clarity', 0) < 30:
                suggestions.append({
                    'category': '語音品質',
                    'icon': '🎤',
                    'text': '說話時可以更清晰一些，注意發音',
                    'priority': 'high'
                })
            
            if voice_details.get('volume', 0) < 15:
                suggestions.append({
                    'category': '語音品質',
                    'icon': '🔊',
                    'text': '調整音量，保持在適中範圍',
                    'priority': 'medium'
                })
            
            if voice_details.get('speed', 0) < 15:
                suggestions.append({
                    'category': '語音品質',
                    'icon': '⏱️',
                    'text': '調整語速，不要太快或太慢',
                    'priority': 'medium'
                })
        
        # 文字內容建議
        if scores['content'] < 75:
            content_details = scores.get('content_details', {})
            
            if content_details.get('length', 0) < 15:
                suggestions.append({
                    'category': '文字內容',
                    'icon': '📝',
                    'text': '可以說得更詳細一些，豐富對話內容',
                    'priority': 'medium'
                })
            
            if content_details.get('richness', 0) < 20:
                suggestions.append({
                    'category': '文字內容',
                    'icon': '📚',
                    'text': '嘗試使用更多樣的詞彙和表達方式',
                    'priority': 'low'
                })
            
            if content_details.get('coherence', 0) < 20:
                suggestions.append({
                    'category': '文字內容',
                    'icon': '🔗',
                    'text': '注意對話的邏輯連貫性',
                    'priority': 'high'
                })
        
        # 按優先級排序
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        suggestions.sort(key=lambda x: priority_order[x['priority']])
        
        # 最多返回 5 條建議
        return suggestions[:5]

# 創建全局實例
score_calculator = ScoreCalculator()
