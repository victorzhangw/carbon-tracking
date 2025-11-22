#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qwen AI廣播劇服務 - Flask-AICares集成版本
這個模組將Qwen TTS API集成到Flask-AICares系統中
"""

import os
import base64
import uuid
from typing import List, Dict, Optional, Any
from bs4 import BeautifulSoup
import re

# 延遲導入，避免導入錯誤
try:
    from ebooklib import epub
    EPUB_AVAILABLE = True
except ImportError:
    epub = None
    EPUB_AVAILABLE = False

try:
    import dashscope
    DASHSCOPE_AVAILABLE = True
    dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'
except ImportError:
    dashscope = None
    DASHSCOPE_AVAILABLE = False

class QwenAudiobookService:
    """Qwen AI廣播劇服務類 - Flask-AICares集成版本"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化Qwen AI廣播劇服務
        
        Args:
            api_key (str): DashScope API密鑰
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.output_dir = os.path.join("static", "audiobooks")
        self.book_dir = os.path.join("TTS-API-Sample", "Epub")
        
        # 確保輸出目錄存在
        os.makedirs(self.output_dir, exist_ok=True)
    
    def is_available(self) -> bool:
        """
        檢查服務是否可用
        
        Returns:
            bool: 服務是否可用
        """
        return DASHSCOPE_AVAILABLE and EPUB_AVAILABLE and self.api_key is not None
    
    def extract_text_from_epub(self, epub_path: str) -> List[Dict[str, str]]:
        """
        從EPUB文件中提取文本內容
        
        Args:
            epub_path (str): EPUB文件路徑
            
        Returns:
            List[Dict[str, str]]: 包含章節標題和內容的列表
        """
        if not EPUB_AVAILABLE:
            raise ImportError("ebooklib 庫未安裝，無法處理EPUB文件")
        
        if not os.path.exists(epub_path):
            raise FileNotFoundError(f"EPUB文件不存在: {epub_path}")
        
        try:
            book = epub.read_epub(epub_path)
            chapters = []
            
            for item in book.get_items():
                # 檢查是否為 HTML/文檔類型（兼容新舊版本）
                is_document = False
                
                # 方法1：檢查類型（新版本）
                if isinstance(item, epub.EpubHtml):
                    is_document = True
                # 方法2：檢查 get_type（舊版本）
                elif hasattr(epub, 'ITEM_DOCUMENT') and hasattr(item, 'get_type'):
                    if item.get_type() == epub.ITEM_DOCUMENT:
                        is_document = True
                # 方法3：檢查 media_type
                elif hasattr(item, 'media_type') and item.media_type in ['application/xhtml+xml', 'text/html']:
                    is_document = True
                
                if is_document:
                    # 提取內容
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    
                    # 移除HTML標籤，保留文本（不清理，保留原始格式）
                    raw_text = soup.get_text()
                    
                    if not raw_text.strip():
                        continue
                    
                    # 嘗試從多種來源提取章節標題
                    title = None
                    
                    # 方法1：查找 h1, h2, h3 標籤
                    for tag in ['h1', 'h2', 'h3', 'h4']:
                        heading = soup.find(tag)
                        if heading and heading.get_text().strip():
                            title = heading.get_text().strip()
                            break
                    
                    # 方法2：查找 title 標籤
                    if not title:
                        title_tag = soup.find('title')
                        if title_tag and title_tag.get_text().strip():
                            title = title_tag.get_text().strip()
                    
                    # 方法3：從原始文本第一行提取（常見於中文小說）
                    if not title:
                        lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
                        if lines:
                            first_line = lines[0]
                            # 檢查是否為目錄頁（包含多個"第X章"）
                            import re
                            chapter_count = len(re.findall(r'第.{1,5}章', first_line))
                            
                            if chapter_count > 3:
                                # 這是目錄頁，給它特殊標題
                                title = '目錄'
                            elif '第' in first_line and '章' in first_line:
                                # 提取章節標題（通常在"第X章"之後）
                                match = re.search(r'第.{1,10}章[　\s]*(.{0,30})', first_line)
                                if match:
                                    extracted = match.group(0).strip()
                                    # 限制標題長度，避免提取過長
                                    if len(extracted) <= 20:
                                        title = extracted
                                    else:
                                        # 只取"第X章 標題"部分
                                        short_match = re.search(r'第.{1,5}章[　\s]*.{0,10}', first_line)
                                        if short_match:
                                            title = short_match.group(0).strip()
                            elif len(first_line) < 50:
                                title = first_line
                    
                    # 方法4：使用章節序號作為標題
                    if not title:
                        chapter_num = len(chapters) + 1
                        title = f'第 {chapter_num} 章'
                    
                    # 清理文本內容
                    text = self._clean_text(raw_text)
                    
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
    
    def generate_audiobook_mandarin(self, epub_path: str, book_id: Optional[str] = None) -> Dict[str, Any]:
        """
        生成普通話版本的AI廣播劇音頻
        
        Args:
            epub_path (str): EPUB文件路徑
            book_id (str, optional): 書籍ID，如果未提供則自動生成
            
        Returns:
            Dict[str, any]: 生成結果信息
        """
        return self._generate_audiobook(epub_path, book_id, "Ethan", "Chinese", "mandarin")
    
    def generate_audiobook_minan(self, epub_path: str, book_id: Optional[str] = None) -> Dict[str, Any]:
        """
        生成閩南語版本的AI廣播劇音頻
        
        Args:
            epub_path (str): EPUB文件路徑
            book_id (str, optional): 書籍ID，如果未提供則自動生成
            
        Returns:
            Dict[str, any]: 生成結果信息
        """
        return self._generate_audiobook(epub_path, book_id, "Roy", "Chinese", "minan")
    
    def parse_epub_only(self, epub_path: str, book_id: Optional[str] = None) -> Dict[str, Any]:
        """
        只解析 EPUB 並保存章節文本（不生成音頻）
        
        Args:
            epub_path (str): EPUB文件路徑
            book_id (str, optional): 書籍ID，如果未提供則自動生成
            
        Returns:
            Dict[str, any]: 書籍信息
        """
        if book_id is None:
            book_id = str(uuid.uuid4())
        
        try:
            # 提取 EPUB 內容
            chapters = self.extract_text_from_epub(epub_path)
            
            if not chapters:
                raise ValueError("EPUB文件中未找到有效內容")
            
            # 創建書籍目錄
            book_output_dir = os.path.join(self.output_dir, book_id)
            os.makedirs(book_output_dir, exist_ok=True)
            
            # 保存書籍元數據
            import json
            metadata = {
                'id': book_id,
                'title': self._extract_book_title(epub_path),
                'chapter_count': len(chapters),
                'created_at': str(uuid.uuid4()),
                'chapters': []
            }
            
            # 保存各章節文本
            for i, chapter in enumerate(chapters):
                chapter_id = f"chapter_{i+1:03d}"
                chapter_file = os.path.join(book_output_dir, f"{chapter_id}.txt")
                
                # 保存章節文本
                with open(chapter_file, 'w', encoding='utf-8') as f:
                    f.write(chapter['content'])
                
                metadata['chapters'].append({
                    'id': chapter_id,
                    'title': chapter.get('title', f'第{i+1}章'),
                    'text_file': chapter_file
                })
            
            # 保存元數據
            metadata_file = os.path.join(book_output_dir, 'metadata.json')
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            return metadata
            
        except Exception as e:
            raise Exception(f"解析EPUB時出錯: {str(e)}")
    
    def generate_chapter_audio(self, book_id: str, chapter_id: str, voice: str, output_file: str, language_type: str = "Chinese"):
        """
        生成單個章節的音頻文件（基於 Qwen 官方範例）
        
        Args:
            book_id (str): 書籍ID
            chapter_id (str): 章節ID
            voice (str): 語音角色（Ethan=普通話, Roy=閩南語）
            output_file (str): 輸出文件路徑
            language_type (str): 語言類型
        """
        if not DASHSCOPE_AVAILABLE:
            raise ImportError("dashscope 庫未安裝")
        
        try:
            # 讀取章節文本
            book_dir = os.path.join(self.output_dir, book_id)
            chapter_file = os.path.join(book_dir, f"{chapter_id}.txt")
            
            if not os.path.exists(chapter_file):
                raise FileNotFoundError(f"找不到章節文件: {chapter_id}")
            
            with open(chapter_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # 限制文本長度（Qwen TTS API 限制 600 字符，但可能按 bytes 計算）
            # 中文字符在 UTF-8 中通常佔 3 bytes，所以 200 個中文字符 = 600 bytes
            if len(text) > 200:
                text = text[:200]
            
            print(f"處理文本長度: {len(text)} 字符")
            print(f"處理文本 bytes: {len(text.encode('utf-8'))} bytes")
            print(f"文本內容: {text[:50]}...")
            
            # 收集所有 PCM 音頻數據
            pcm_data = []
            
            # 使用流式 API（參考官方範例）
            try:
                response = dashscope.MultiModalConversation.call(
                    api_key=self.api_key,
                    model="qwen3-tts-flash",
                    text=text,
                    voice=voice,
                    language_type=language_type,
                    speech_rate=0.8,  # 語速：0.5-2.0，預設1.0，0.8較慢適合長者
                    stream=True
                )
                
                chunk_count = 0
                for chunk in response:
                    chunk_count += 1
                    if chunk.output is not None:
                        audio = chunk.output.audio
                        if audio.data is not None:
                            # 解碼 Base64 音頻數據
                            wav_bytes = base64.b64decode(audio.data)
                            pcm_data.append(wav_bytes)
                    else:
                        # 檢查是否有錯誤
                        if hasattr(chunk, 'code') and chunk.code:
                            raise Exception(f"API 錯誤: {chunk.code} - {chunk.message if hasattr(chunk, 'message') else ''}")
                
                print(f"收到 {chunk_count} 個數據塊，生成 {len(pcm_data)} 個音頻片段")
                
            except Exception as api_error:
                raise Exception(f"API 調用失敗: {str(api_error)}")
            
            # 合併所有 PCM 數據並添加 WAV 文件頭
            if pcm_data:
                complete_pcm = b''.join(pcm_data)
                
                # 添加 WAV 文件頭（16-bit PCM, 24000Hz, mono）
                import struct
                import wave
                
                with wave.open(output_file, 'wb') as wav_file:
                    wav_file.setnchannels(1)  # mono
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(24000)  # 24kHz
                    wav_file.writeframes(complete_pcm)
            else:
                raise Exception("未生成任何音頻數據")
                
        except Exception as e:
            raise Exception(f"生成音頻失敗: {str(e)}")
    
    def synthesize_chapter_stream(self, book_id: str, chapter_id: str, voice: str, language_type: str = "Chinese"):
        """
        串流合成單個章節的音頻（即時生成）
        
        Args:
            book_id (str): 書籍ID
            chapter_id (str): 章節ID
            voice (str): 語音角色（Ethan=普通話, Roy=閩南語）
            language_type (str): 語言類型
            
        Yields:
            bytes: 音頻數據流
        """
        if not DASHSCOPE_AVAILABLE:
            raise ImportError("dashscope 庫未安裝")
        
        try:
            # 讀取章節文本
            book_dir = os.path.join(self.output_dir, book_id)
            chapter_file = os.path.join(book_dir, f"{chapter_id}.txt")
            
            if not os.path.exists(chapter_file):
                raise FileNotFoundError(f"找不到章節文件: {chapter_id}")
            
            with open(chapter_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # 分段處理長文本
            segments = self._split_text_into_segments(text, max_length=1000)
            
            # 逐段生成並串流音頻
            for segment in segments:
                response = dashscope.MultiModalConversation.call(
                    api_key=self.api_key,
                    model="qwen3-tts-flash",
                    text=segment,
                    voice=voice,
                    language_type=language_type,
                    speech_rate=0.8,  # 語速：0.5-2.0，預設1.0，0.8較慢適合長者
                    stream=True
                )
                
                for chunk in response:
                    if chunk.output is not None:
                        audio = chunk.output.audio
                        if audio.data is not None:
                            wav_bytes = base64.b64decode(audio.data)
                            yield wav_bytes
                            
        except Exception as e:
            raise Exception(f"串流合成失敗: {str(e)}")
    
    def _generate_audiobook(self, epub_path: str, book_id: Optional[str], voice: str, language_type: str, dialect: str) -> Dict[str, Any]:
        """
        生成AI廣播劇音頻（內部方法）
        
        Args:
            epub_path (str): EPUB文件路徑
            book_id (str): 書籍ID
            voice (str): 語音角色
            language_type (str): 語言類型
            dialect (str): 方言類型
            
        Returns:
            Dict[str, any]: 生成結果信息
        """
        if not self.is_available():
            raise Exception("Qwen TTS服務不可用，請檢查API密鑰和依賴庫")
        
        if book_id is None:
            book_id = str(uuid.uuid4())
            
        try:
            # 提取EPUB內容
            chapters = self.extract_text_from_epub(epub_path)
            
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
                'title': self._extract_book_title(epub_path),
                'dialect': dialect,
                'chapter_count': len(chapters),
                'chapters': chapter_files,
                'output_dir': book_output_dir
            }
            
            return book_info
            
        except Exception as e:
            raise Exception(f"生成AI廣播劇時出錯: {str(e)}")
    
    def _extract_book_title(self, epub_path: str) -> str:
        """
        從EPUB文件中提取書名
        
        Args:
            epub_path (str): EPUB文件路徑
            
        Returns:
            str: 書名
        """
        if not EPUB_AVAILABLE:
            return "未知書名"
        
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
        使用Qwen TTS API合成語音（基於官方範例代碼）
        
        Args:
            text (str): 要合成的文字
            output_file (str): 輸出文件路徑
            voice (str): 語音角色（Ethan=普通話, Roy=閩南語）
            language_type (str): 語言類型（Chinese）
        """
        if not DASHSCOPE_AVAILABLE:
            raise ImportError("dashscope 庫未安裝，無法使用Qwen TTS API")
        
        try:
            # 使用流式模式調用 API（參考官方範例）
            response = dashscope.MultiModalConversation.call(
                api_key=self.api_key,
                model="qwen3-tts-flash",
                text=text,
                voice=voice,
                language_type=language_type,
                speech_rate=0.8,  # 語速：0.5-2.0，預設1.0，0.8較慢適合長者
                stream=True  # 使用流式模式
            )
            
            # 收集所有音頻數據
            audio_chunks = []
            for chunk in response:
                if chunk.output is not None:
                    audio = chunk.output.audio
                    if audio.data is not None:
                        # 解碼音頻數據
                        wav_bytes = base64.b64decode(audio.data)
                        audio_chunks.append(wav_bytes)
            
            # 合併所有音頻數據並保存
            if audio_chunks:
                complete_audio = b''.join(audio_chunks)
                with open(output_file, 'wb') as f:
                    f.write(complete_audio)
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

# Flask路由整合
from flask import Blueprint, request, jsonify, current_app, send_file
import os

qwen_audiobook_bp = Blueprint('qwen_audiobook', __name__, url_prefix='/api/audiobook')

@qwen_audiobook_bp.route('/generate', methods=['POST'])
def generate_audiobook():
    """
    生成AI廣播劇音頻
    
    Request JSON:
        epub_file (str): EPUB文件名
        dialect (str): 方言類型 (mandarin|minan)
        api_key (str, optional): API密鑰
    
    Returns:
        JSON: 生成結果
    """
    try:
        data = request.get_json()
        epub_file = data.get('epub_file')
        dialect = data.get('dialect', 'mandarin')
        api_key = data.get('api_key')
        
        if not epub_file:
            return jsonify({'error': '缺少EPUB文件名'}), 400
        
        # 初始化服務
        service = QwenAudiobookService(api_key=api_key)
        
        if not service.is_available():
            return jsonify({'error': 'Qwen TTS服務不可用，請提供有效的API密鑰'}), 400
        
        # 構造EPUB文件路徑
        epub_path = os.path.join(current_app.root_path, 'TTS-API-Sample', 'Epub', epub_file)
        
        # 生成音頻
        if dialect == 'minan':
            result = service.generate_audiobook_minan(epub_path)
        else:
            result = service.generate_audiobook_mandarin(epub_path)
        
        return jsonify({
            'success': True,
            'message': 'AI廣播劇生成成功',
            'book_id': result['id'],
            'title': result['title'],
            'dialect': result['dialect'],
            'chapter_count': result['chapter_count'],
            'output_dir': result['output_dir']
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"生成AI廣播劇失敗: {str(e)}")
        return jsonify({'error': f'生成AI廣播劇失敗: {str(e)}'}), 500

@qwen_audiobook_bp.route('/upload-epub', methods=['POST'])
def upload_epub():
    """
    上傳 EPUB 並解析章節（不生成音頻）
    
    Returns:
        JSON: 書籍信息
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': '沒有上傳文件'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': '沒有選擇文件'}), 400
        
        if not file.filename.lower().endswith('.epub'):
            return jsonify({'error': '請上傳 EPUB 格式的文件'}), 400
        
        # 保存臨時文件
        import tempfile
        from werkzeug.utils import secure_filename
        
        temp_dir = tempfile.gettempdir()
        filename = secure_filename(file.filename)
        epub_path = os.path.join(temp_dir, filename)
        file.save(epub_path)
        
        # 初始化服務
        api_key = request.form.get('api_key')
        service = QwenAudiobookService(api_key=api_key)
        
        # 只解析 EPUB，不生成音頻
        result = service.parse_epub_only(epub_path)
        
        # 清理臨時文件
        try:
            os.remove(epub_path)
        except:
            pass
        
        return jsonify({
            'success': True,
            'message': 'EPUB 解析成功',
            'book': result
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"上傳EPUB失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'上傳失敗: {str(e)}'}), 500

@qwen_audiobook_bp.route('/library', methods=['GET'])
def library_page():
    """書庫首頁"""
    from flask import render_template
    return render_template('audiobook_library.html')

@qwen_audiobook_bp.route('/book/<book_id>/view', methods=['GET'])
def book_detail_page(book_id):
    """書籍詳情頁面"""
    from flask import render_template
    return render_template('qwen_audiobook_detail.html')

@qwen_audiobook_bp.route('/books', methods=['GET'])
def list_books():
    """
    獲取已上傳的書籍列表
    
    Returns:
        JSON: 書籍列表
    """
    import json
    from datetime import datetime
    
    try:
        # 使用絕對路徑
        audiobooks_dir = os.path.join(current_app.root_path, 'static', 'audiobooks')
        books = []
        
        print(f"=== DEBUG: 掃描目錄 ===")
        print(f"Root path: {current_app.root_path}")
        print(f"Audiobooks dir: {audiobooks_dir}")
        print(f"目錄存在: {os.path.exists(audiobooks_dir)}")
        
        if not os.path.exists(audiobooks_dir):
            print("目錄不存在，返回空列表")
            return jsonify({'success': True, 'books': []}), 200
        
        items = os.listdir(audiobooks_dir)
        print(f"找到 {len(items)} 個項目: {items}")
        
        # 遍歷所有書籍目錄
        for book_id in os.listdir(audiobooks_dir):
            book_dir = os.path.join(audiobooks_dir, book_id)
            
            print(f"\n檢查項目: {book_id}")
            print(f"  路徑: {book_dir}")
            print(f"  是目錄: {os.path.isdir(book_dir)}")
            
            # 跳過非目錄項
            if not os.path.isdir(book_dir):
                print(f"  跳過（不是目錄）")
                continue
            
            metadata_file = os.path.join(book_dir, 'metadata.json')
            print(f"  metadata 文件: {metadata_file}")
            print(f"  metadata 存在: {os.path.exists(metadata_file)}")
            
            # 跳過沒有 metadata 的目錄
            if not os.path.exists(metadata_file):
                print(f"  跳過（沒有 metadata）")
                continue
            
            try:
                # 讀取 metadata
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                print(f"  成功讀取 metadata")
                print(f"  標題: {metadata.get('title', '未命名')}")
                
                # 獲取創建時間
                created_time = datetime.fromtimestamp(os.path.getctime(book_dir))
                
                # 添加到列表
                book_data = {
                    'id': metadata.get('id', book_id),
                    'title': metadata.get('title', '未命名'),
                    'chapter_count': metadata.get('chapter_count', 0),
                    'created_at': created_time.isoformat()
                }
                books.append(book_data)
                print(f"  已添加到列表: {book_data}")
                
            except Exception as e:
                print(f"  錯誤: {str(e)}")
                current_app.logger.error(f"讀取書籍 {book_id} 失敗: {str(e)}")
                import traceback
                traceback.print_exc()
                continue
        
        # 按創建時間排序
        books.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        print(f"\n=== 最終結果 ===")
        print(f"總共找到 {len(books)} 本書")
        print(f"Books: {books}")
        
        return jsonify({
            'success': True,
            'books': books
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"獲取書籍列表時出錯: {str(e)}")
        return jsonify({'error': f'獲取書籍列表時發生錯誤: {str(e)}'}), 500

@qwen_audiobook_bp.route('/book/<book_id>/info', methods=['GET'])
def get_book_info(book_id):
    """
    獲取書籍詳細信息
    
    Args:
        book_id (str): 書籍ID
        
    Returns:
        JSON: 書籍詳細信息
    """
    try:
        audiobooks_dir = os.path.join(current_app.root_path, 'static', 'audiobooks')
        book_dir = os.path.join(audiobooks_dir, book_id)
        metadata_file = os.path.join(book_dir, 'metadata.json')
        
        if not os.path.exists(metadata_file):
            return jsonify({'error': '找不到書籍'}), 404
        
        import json
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        return jsonify({
            'success': True,
            'book': metadata
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"獲取書籍信息時出錯: {str(e)}")
        return jsonify({'error': f'獲取書籍信息時發生錯誤: {str(e)}'}), 500

@qwen_audiobook_bp.route('/book/<book_id>/bilingual-chapters', methods=['GET'])
def get_bilingual_chapters(book_id):
    """
    獲取雙語章節信息
    
    Args:
        book_id (str): 書籍ID
        
    Returns:
        JSON: 書籍詳細信息
    """
    try:
        audiobooks_dir = os.path.join(current_app.root_path, 'static', 'audiobooks')
        
        # 獲取普通話章節
        mandarin_dir = os.path.join(audiobooks_dir, f"{book_id}_mandarin")
        mandarin_chapters = []
        if os.path.exists(mandarin_dir):
            for filename in os.listdir(mandarin_dir):
                if filename.endswith('.wav'):
                    chapter_id = filename.replace('.wav', '')
                    mandarin_chapters.append({
                        'id': chapter_id,
                        'title': chapter_id,  # 需要從元數據中讀取
                        'audio_url': f'/api/qwen-audiobook/book/{book_id}/chapter/{chapter_id}/audio/mandarin'
                    })
        
        # 獲取閩南語章節
        minan_dir = os.path.join(audiobooks_dir, f"{book_id}_minan")
        minan_chapters = []
        if os.path.exists(minan_dir):
            for filename in os.listdir(minan_dir):
                if filename.endswith('.wav'):
                    chapter_id = filename.replace('.wav', '')
                    minan_chapters.append({
                        'id': chapter_id,
                        'title': chapter_id,  # 需要從元數據中讀取
                        'audio_url': f'/api/qwen-audiobook/book/{book_id}/chapter/{chapter_id}/audio/minan'
                    })
        
        book_info = {
            'id': book_id,
            'title': book_id,  # 需要從元數據中讀取
            'mandarin_chapters': mandarin_chapters,
            'minan_chapters': minan_chapters
        }
        
        return jsonify({
            'success': True,
            'book': book_info
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"獲取雙語章節信息時出錯: {str(e)}")
        return jsonify({'error': f'獲取雙語章節信息時發生錯誤: {str(e)}'}), 500

@qwen_audiobook_bp.route('/book/<book_id>/chapter/<chapter_id>/audio/<dialect>', methods=['GET'])
def get_or_generate_chapter_audio(book_id, chapter_id, dialect):
    """
    獲取章節音頻（如果不存在則生成）
    
    Args:
        book_id (str): 書籍ID
        chapter_id (str): 章節ID
        dialect (str): 方言類型 (mandarin|minan)
        
    Returns:
        File: 音頻文件
    """
    try:
        audiobooks_dir = os.path.join(current_app.root_path, 'static', 'audiobooks')
        audio_dir = os.path.join(audiobooks_dir, book_id, 'audio', dialect)
        audio_file = os.path.join(audio_dir, f"{chapter_id}.wav")
        
        # 如果音頻文件已存在，直接返回
        if os.path.exists(audio_file):
            return send_file(audio_file, mimetype='audio/wav')
        
        # 音頻不存在，需要生成
        os.makedirs(audio_dir, exist_ok=True)
        
        # 初始化服務
        service = QwenAudiobookService()
        
        if not service.is_available():
            return jsonify({'error': 'Qwen TTS服務不可用'}), 400
        
        # 設置語音參數
        voice = "Ethan" if dialect == "mandarin" else "Roy"
        
        # 生成音頻文件
        service.generate_chapter_audio(book_id, chapter_id, voice, audio_file)
        
        # 返回生成的音頻
        return send_file(audio_file, mimetype='audio/wav')
        
    except Exception as e:
        current_app.logger.error(f"獲取音頻時出錯: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'獲取音頻時發生錯誤: {str(e)}'}), 500