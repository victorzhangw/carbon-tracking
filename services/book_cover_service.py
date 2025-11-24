#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
書籍封面獲取服務
使用 Google Books API 搜尋書籍封面
"""

import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class BookCoverService:
    """書籍封面獲取服務"""
    
    GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes"
    
    @staticmethod
    def fetch_cover_url(book_title: str, author: str = None) -> Optional[str]:
        """
        從 Google Books API 獲取書籍封面 URL
        
        Args:
            book_title: 書名
            author: 作者（可選）
            
        Returns:
            封面圖片 URL，找不到則返回 None
        """
        try:
            # 構建搜尋查詢
            query = book_title
            if author:
                query = f"{book_title} {author}"
            
            # 呼叫 Google Books API
            params = {
                'q': query,
                'maxResults': 1,
                'printType': 'books'
            }
            
            response = requests.get(
                BookCoverService.GOOGLE_BOOKS_API,
                params=params,
                timeout=5
            )
            
            if response.status_code != 200:
                logger.warning(f"Google Books API 返回錯誤: {response.status_code}")
                return None
            
            data = response.json()
            
            # 檢查是否有結果
            if 'items' not in data or len(data['items']) == 0:
                logger.info(f"找不到書籍封面: {book_title}")
                return None
            
            # 獲取封面圖片
            volume_info = data['items'][0].get('volumeInfo', {})
            image_links = volume_info.get('imageLinks', {})
            
            # 優先使用較大的圖片
            cover_url = (
                image_links.get('large') or
                image_links.get('medium') or
                image_links.get('thumbnail') or
                image_links.get('smallThumbnail')
            )
            
            if cover_url:
                # 將 http 改為 https
                cover_url = cover_url.replace('http://', 'https://')
                logger.info(f"成功獲取封面: {book_title} -> {cover_url}")
                return cover_url
            else:
                logger.info(f"書籍資料中沒有封面圖片: {book_title}")
                return None
                
        except requests.Timeout:
            logger.error(f"獲取封面超時: {book_title}")
            return None
        except requests.RequestException as e:
            logger.error(f"獲取封面時發生網路錯誤: {e}")
            return None
        except Exception as e:
            logger.error(f"獲取封面時發生錯誤: {e}")
            return None
    
    @staticmethod
    def fetch_cover_url_batch(books: list) -> dict:
        """
        批量獲取多本書的封面
        
        Args:
            books: 書籍列表，每個元素為 {'title': str, 'author': str}
            
        Returns:
            字典，key 為書名，value 為封面 URL
        """
        results = {}
        
        for book in books:
            title = book.get('title')
            author = book.get('author')
            
            if title:
                cover_url = BookCoverService.fetch_cover_url(title, author)
                results[title] = cover_url
        
        return results


# 創建全域實例
book_cover_service = BookCoverService()
