#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI廣播劇服務模組
提供EPUB文件轉換為音頻廣播劇的功能
"""

import os
import uuid
import logging
from ebooklib import epub
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Optional
from ..voice_processing.voice_synthesis_service import VoiceSynthesisService
from ..voice_processing.voice_config import VoiceConfig

logger = logging.getLogger(__name__)

class AudiobookService:
    """AI廣播劇服務類"""
    
    def __init__(self, output_dir: str = "audiobooks"):
        """
        初始化AI廣播劇服務
        
        Args:
            output_dir (str): 音頻文件輸出目錄
        """
        self.output_dir = output_dir
        self.voice_service = VoiceSynthesisService()
        self.voice_config = VoiceConfig()
        
        # 確保輸出目錄存在
        os.makedirs(self.output_dir, exist_ok=True)
        
    def extract_text_from_epub(self, epub_path: str) -> List[Dict[str, str]]:
        """
        從EPUB文件中提取文本內容
        
        Args:
            epub_path (str): EPUB文件路徑
            
        Returns:
            List[Dict[str, str]]: 包含章節標題和內容的列表
        """
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
            logger.error(f"解析EPUB文件時出錯: {str(e)}")
            raise
    
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
        
        # 移除特殊字符
        text = re.sub(r'[^\w\s\u4e00-\u9fff。，！？；：""''（）【】《》\-]', '', text)
        
        return text.strip()
    
    def generate_audiobook(self, epub_path: str, book_id: Optional[str] = None) -> Dict[str, any]:
        """
        生成AI廣播劇音頻
        
        Args:
            epub_path (str): EPUB文件路徑
            book_id (str, optional): 書籍ID，如果未提供則自動生成
            
        Returns:
            Dict[str, any]: 生成結果信息
        """
        if book_id is None:
            book_id = str(uuid.uuid4())
            
        try:
            # 提取EPUB內容
            chapters = self.extract_text_from_epub(epub_path)
            
            if not chapters:
                raise ValueError("EPUB文件中未找到有效內容")
            
            # 創建書籍目錄
            book_dir = os.path.join(self.output_dir, book_id)
            os.makedirs(book_dir, exist_ok=True)
            
            # 生成各章節音頻
            chapter_files = []
            for i, chapter in enumerate(chapters):
                chapter_id = f"chapter_{i+1:03d}"
                audio_file = self._generate_chapter_audio(
                    chapter['content'], 
                    chapter_id, 
                    book_dir,
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
                'title': self._extract_book_title(epub_path),
                'chapter_count': len(chapters),
                'chapters': chapter_files,
                'output_dir': book_dir
            }
            
            return book_info
            
        except Exception as e:
            logger.error(f"生成AI廣播劇時出錯: {str(e)}")
            raise
    
    def _extract_book_title(self, epub_path: str) -> str:
        """
        從EPUB文件中提取書名
        
        Args:
            epub_path (str): EPUB文件路徑
            
        Returns:
            str: 書名
        """
        try:
            book = epub.read_epub(epub_path)
            return book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else "未知書名"
        except:
            return "未知書名"
    
    def _generate_chapter_audio(self, text: str, chapter_id: str, output_dir: str, title: str = "") -> str:
        """
        生成單個章節的音頻文件
        
        Args:
            text (str): 章節文本
            chapter_id (str): 章節ID
            output_dir (str): 輸出目錄
            title (str): 章節標題
            
        Returns:
            str: 音頻文件路徑
        """
        try:
            # 分段處理長文本
            segments = self._split_text_into_segments(text)
            
            # 生成各段落音頻
            audio_files = []
            for i, segment in enumerate(segments):
                segment_id = f"{chapter_id}_part_{i+1:03d}"
                audio_file = os.path.join(output_dir, f"{segment_id}.wav")
                
                # 使用現有的語音合成服務
                self.voice_service.synthesize_speech(
                    text=segment,
                    output_file=audio_file,
                    voice_config=self.voice_config
                )
                audio_files.append(audio_file)
            
            # 合併音頻文件
            final_audio_file = os.path.join(output_dir, f"{chapter_id}.mp3")
            self._merge_audio_files(audio_files, final_audio_file)
            
            # 清理臨時文件
            for audio_file in audio_files:
                if os.path.exists(audio_file):
                    os.remove(audio_file)
            
            return final_audio_file
            
        except Exception as e:
            logger.error(f"生成章節音頻時出錯: {str(e)}")
            raise
    
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
    
    def _merge_audio_files(self, audio_files: List[str], output_file: str):
        """
        合併多個音頻文件
        
        Args:
            audio_files (List[str]): 音頻文件列表
            output_file (str): 輸出文件路徑
        """
        try:
            # 這裡需要實現音頻文件合併邏輯
            # 可以使用pydub或其他音頻處理庫
            pass
        except Exception as e:
            logger.error(f"合併音頻文件時出錯: {str(e)}")
            raise

# 服務實例
audiobook_service = AudiobookService()