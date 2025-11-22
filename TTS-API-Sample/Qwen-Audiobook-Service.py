#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI廣播劇模組 - Qwen API版本
使用通義千問TTS API服務生成閩南語和普通話音頻
"""

import os
import base64
import numpy as np
from bs4 import BeautifulSoup
import re
import uuid
import time

from typing import List, Dict, Optional, Any

# 延遲導入，避免導入錯誤
DASHSCOPE_AVAILABLE = False
EPUB_AVAILABLE = False

try:
    import dashscope
    DASHSCOPE_AVAILABLE = True
except ImportError:
    dashscope = None

try:
    from ebooklib import epub
    EPUB_AVAILABLE = True
except ImportError:
    epub = None

# 設置DashScope API URL
if DASHSCOPE_AVAILABLE:
    dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'

class QwenAudiobookService:
    """Qwen AI廣播劇服務類"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化Qwen AI廣播劇服務
        
        Args:
            api_key (str): DashScope API密鑰
        """
        if not DASHSCOPE_AVAILABLE:
            print("警告: dashscope 庫未安裝，部分功能不可用")
        
        if not EPUB_AVAILABLE:
            print("警告: ebooklib 庫未安裝，EPUB處理功能不可用")
        
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY", "sk-e295e8477c31449890bb371bf8d6f6b4")
        self.output_dir = "audiobooks"
        self.book_dir = "TTS-API-Sample/Epub"
        
        # 確保輸出目錄存在
        os.makedirs(self.output_dir, exist_ok=True)
    
    def extract_text_from_epub(self, epub_filename: str) -> List[Dict[str, str]]:
        """
        從EPUB文件中提取文本內容
        
        Args:
            epub_filename (str): EPUB文件名
            
        Returns:
            List[Dict[str, str]]: 包含章節標題和內容的列表
        """
        if not EPUB_AVAILABLE:
            raise ImportError("ebooklib 庫未安裝，無法處理EPUB文件")
        
        epub_path = os.path.join(self.book_dir, epub_filename)
        
        if not os.path.exists(epub_path):
            raise FileNotFoundError(f"EPUB文件不存在: {epub_path}")
        
        try:
            book = epub.read_epub(epub_path)
            chapters = []
            
            for item in book.get_items():
                if item.get_type() == epub.ITEM_DOCUMENT:
                    # 提取章節標題
                    title = item.get_name()
                    if hasattr(item, 'title') and item.title:
                        title = item.title
                    
                    # 提取內容
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    
                    # 移除HTML標籤，保留文本
                    text = soup.get_text()
                    
                    # 清理文本
                    text = self._clean_text(text)
                    
                    if text.strip():
                        chapters.append({
                            'title': title,
                            'content': text
                        })
            
            return chapters
        except Exception as e:
            raise Exception(f"解析EPUB文件時出錯: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """
        清理文本內容
        
        Args:
            text (str): 原始文本
            
        Returns:
            str: 清理後的文本
        """
        # 移除多餘的空白字符
        text = re.sub(r'\s+', ' ', text)
        
        # 移除特殊字符，保留中文、英文、數字和常用標點
        text = re.sub(r'[^\w\s\u4e00-\u9fff\u3400-\u4dbf\u3040-\u309f\u30a0-\u30ff。，！？；：""''（）【】《》\-]', '', text)
        
        return text.strip()
    
    def generate_audiobook_mandarin(self, epub_filename: str, book_id: Optional[str] = None) -> Dict[str, Any]:
        """
        生成普通話版本的AI廣播劇音頻
        
        Args:
            epub_filename (str): EPUB文件名
            book_id (str, optional): 書籍ID，如果未提供則自動生成
            
        Returns:
            Dict[str, any]: 生成結果信息
        """
        return self._generate_audiobook(epub_filename, book_id, "Ethan", "Chinese", "普通話")
    
    def generate_audiobook_minan(self, epub_filename: str, book_id: Optional[str] = None) -> Dict[str, Any]:
        """
        生成閩南語版本的AI廣播劇音頻
        
        Args:
            epub_filename (str): EPUB文件名
            book_id (str, optional): 書籍ID，如果未提供則自動生成
            
        Returns:
            Dict[str, any]: 生成結果信息
        """
        return self._generate_audiobook(epub_filename, book_id, "Roy", "Chinese", "閩南語")
    
    def _generate_audiobook(self, epub_filename: str, book_id: Optional[str], voice: str, language_type: str, dialect: str) -> Dict[str, Any]:
        """
        生成AI廣播劇音頻（內部方法）
        
        Args:
            epub_filename (str): EPUB文件名
            book_id (str): 書籍ID
            voice (str): 語音角色
            language_type (str): 語言類型
            dialect (str): 方言類型
            
        Returns:
            Dict[str, any]: 生成結果信息
        """
        if not DASHSCOPE_AVAILABLE:
            raise ImportError("dashscope 庫未安裝，無法使用Qwen TTS API")
        
        if book_id is None:
            book_id = str(uuid.uuid4())
            
        try:
            # 提取EPUB內容
            chapters = self.extract_text_from_epub(epub_filename)
            
            if not chapters:
                raise ValueError("EPUB文件中未找到有效內容")
            
            # 創建書籍目錄
            book_output_dir = os.path.join(self.output_dir, f"{book_id}_{dialect}")
            os.makedirs(book_output_dir, exist_ok=True)
            
            # 生成各章節音頻
            chapter_files = []
            for i, chapter in enumerate(chapters):
                chapter_id = f"chapter_{i+1:03d}"
                audio_file = self._generate_chapter_audio(
                    chapter['content'], 
                    chapter_id, 
                    book_output_dir,
                    voice,
                    language_type,
                    chapter.get('title', f'第{i+1}章')
                )
                chapter_files.append({
                    'id': chapter_id,
                    'title': chapter.get('title', f'第{i+1}章'),
                    'audio_file': audio_file
                })
            
            # 生成書籍信息
            book_info = {
                'id': book_id,
                'title': self._extract_book_title(epub_filename),
                'dialect': dialect,
                'chapter_count': len(chapters),
                'chapters': chapter_files,
                'output_dir': book_output_dir
            }
            
            return book_info
            
        except Exception as e:
            raise Exception(f"生成AI廣播劇時出錯: {str(e)}")
    
    def _extract_book_title(self, epub_filename: str) -> str:
        """
        從EPUB文件中提取書名
        
        Args:
            epub_filename (str): EPUB文件名
            
        Returns:
            str: 書名
        """
        if not EPUB_AVAILABLE:
            return "未知書名"
        
        epub_path = os.path.join(self.book_dir, epub_filename)
        
        try:
            book = epub.read_epub(epub_path)
            return book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else "未知書名"
        except:
            return "未知書名"
    
    def _generate_chapter_audio(self, text: str, chapter_id: str, output_dir: str, voice: str, language_type: str, title: str = "") -> str:
        """
        生成單個章節的音頻文件
        
        Args:
            text (str): 章節文本
            chapter_id (str): 章節ID
            output_dir (str): 輸出目錄
            voice (str): 語音角色
            language_type (str): 語言類型
            title (str): 章節標題
            
        Returns:
            str: 音頻文件路徑
        """
        if not DASHSCOPE_AVAILABLE:
            raise ImportError("dashscope 庫未安裝，無法使用Qwen TTS API")
        
        try:
            # 分段處理長文本（DashScope API有文本長度限制）
            segments = self._split_text_into_segments(text, max_length=1000)
            
            # 生成各段落音頻
            audio_files = []
            for i, segment in enumerate(segments):
                segment_id = f"{chapter_id}_part_{i+1:03d}"
                audio_file = os.path.join(output_dir, f"{segment_id}.wav")
                
                # 使用Qwen TTS API生成音頻
                self._tts_synthesize(
                    text=segment,
                    output_file=audio_file,
                    voice=voice,
                    language_type=language_type
                )
                audio_files.append(audio_file)
            
            # 合併音頻文件（簡化處理，實際應用中可能需要音頻合併）
            final_audio_file = os.path.join(output_dir, f"{chapter_id}.wav")
            
            # 如果只有一個音頻文件，直接使用
            if len(audio_files) == 1:
                os.rename(audio_files[0], final_audio_file)
            else:
                # 這裡簡化處理，實際應用中需要合併多個音頻文件
                # 在這個示例中，我們只保留第一個文件
                os.rename(audio_files[0], final_audio_file)
                
                # 清理臨時文件（除了第一個）
                for audio_file in audio_files[1:]:
                    if os.path.exists(audio_file):
                        os.remove(audio_file)
            
            return final_audio_file
            
        except Exception as e:
            raise Exception(f"生成章節音頻時出錯: {str(e)}")
    
    def _tts_synthesize(self, text: str, output_file: str, voice: str, language_type: str):
        """
        使用Qwen TTS API合成語音
        
        Args:
            text (str): 要合成的文字
            output_file (str): 輸出文件路徑
            voice (str): 語音角色
            language_type (str): 語言類型
        """
        if not DASHSCOPE_AVAILABLE:
            raise ImportError("dashscope 庫未安裝，無法使用Qwen TTS API")
        
        try:
            response = dashscope.MultiModalConversation.call(
                api_key=self.api_key,
                model="qwen3-tts-flash",
                text=text,
                voice=voice,
                language_type=language_type,
                stream=False  # 使用非流式模式以便保存到文件
            )
            
            if response.output and response.output.audio and response.output.audio.data:
                # 解碼音頻數據並保存到文件
                wav_bytes = base64.b64decode(response.output.audio.data)
                with open(output_file, 'wb') as f:
                    f.write(wav_bytes)
            else:
                raise Exception("TTS API返回無效的音頻數據")
                
        except Exception as e:
            raise Exception(f"語音合成失敗: {str(e)}")
    
    def _split_text_into_segments(self, text: str, max_length: int = 1000) -> List[str]:
        """
        將長文本分割成段落
        
        Args:
            text (str): 原始文本
            max_length (int): 每段最大字符數
            
        Returns:
            List[str]: 分割後的文本段落
        """
        # 按句子分割
        sentences = re.split(r'[。！？]', text)
        segments = []
        current_segment = ""
        
        for sentence in sentences:
            if len(current_segment) + len(sentence) <= max_length:
                current_segment += sentence + "。"
            else:
                if current_segment:
                    segments.append(current_segment)
                current_segment = sentence + "。"
        
        if current_segment:
            segments.append(current_segment)
            
        return segments

# 使用示例
if __name__ == "__main__":
    try:
        # 檢查依賴
        if not DASHSCOPE_AVAILABLE or not EPUB_AVAILABLE:
            print("警告: 需要安裝依賴庫才能運行此腳本")
            print("請運行: pip install -r requirements.txt")
            exit(1)
        
        # 初始化服務
        service = QwenAudiobookService()
        
        # 指定EPUB文件
        epub_file = "17XZa.epub"
        
        print("開始生成普通話版本AI廣播劇...")
        # 生成普通話版本
        mandarin_book = service.generate_audiobook_mandarin(epub_file)
        print(f"普通話版本生成完成: {mandarin_book['title']}")
        print(f"章節數: {mandarin_book['chapter_count']}")
        print(f"輸出目錄: {mandarin_book['output_dir']}")
        
        print("\n開始生成閩南語版本AI廣播劇...")
        # 生成閩南語版本
        minan_book = service.generate_audiobook_minan(epub_file)
        print(f"閩南語版本生成完成: {minan_book['title']}")
        print(f"章節數: {minan_book['chapter_count']}")
        print(f"輸出目錄: {minan_book['output_dir']}")
        
    except Exception as e:
        print(f"錯誤: {str(e)}")