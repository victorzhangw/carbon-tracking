#!/usr/bin/env python3
"""
檔案重組回滾腳本

此腳本根據 migration_log.json 還原檔案到重組前的位置。
支援完整回滾或選擇性回滾特定類別的檔案。

使用方式:
    python scripts/rollback.py --all                    # 回滾所有檔案
    python scripts/rollback.py --category config        # 只回滾配置檔案
    python scripts/rollback.py --category scripts       # 只回滾腳本檔案
    python scripts/rollback.py --task 3.3               # 只回滾特定任務的檔案
    python scripts/rollback.py --dry-run                # 預覽回滾操作（不實際執行）
    python scripts/rollback.py --backup <path>          # 從指定備份還原
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# 添加專案根目錄到 Python 路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 顏色輸出（Windows 支援）
try:
    import colorama
    colorama.init()
    GREEN = colorama.Fore.GREEN
    YELLOW = colorama.Fore.YELLOW
    RED = colorama.Fore.RED
    BLUE = colorama.Fore.BLUE
    RESET = colorama.Style.RESET_ALL
except ImportError:
    GREEN = YELLOW = RED = BLUE = RESET = ""


class RollbackManager:
    """檔案回滾管理器"""
    
    def __init__(self, migration_log_path='migration_log.json', dry_run=False):
        """
        初始化回滾管理器
        
        Args:
            migration_log_path: 遷移日誌檔案路徑
            dry_run: 是否為預覽模式（不實際執行）
        """
        self.migration_log_path = migration_log_path
        self.dry_run = dry_run
        self.project_root = Path(__file__).parent.parent
        self.migration_data = None
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'skipped': 0
        }
        
    def load_migration_log(self):
        """載入遷移日誌"""
        log_path = self.project_root / self.migration_log_path
        
        if not log_path.exists():
            print(f"{RED}錯誤: 找不到遷移日誌檔案 {log_path}{RESET}")
            return False
            
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                self.migration_data = json.load(f)
            print(f"{GREEN}✓ 成功載入遷移日誌{RESET}")
            return True
        except Exception as e:
            print(f"{RED}錯誤: 無法載入遷移日誌 - {e}{RESET}")
            return False
    
    def get_migrations_by_category(self, category):
        """根據類別篩選遷移記錄"""
        if not self.migration_data:
            return []
        
        migrations = self.migration_data.get('migrations', [])
        test_migrations = self.migration_data.get('test_migrations', [])
        all_migrations = migrations + test_migrations
        
        if category == 'all':
            return all_migrations
        
        return [m for m in all_migrations if m.get('category') == category]
    
    def get_migrations_by_task(self, task):
        """根據任務編號篩選遷移記錄"""
        if not self.migration_data:
            return []
        
        migrations = self.migration_data.get('migrations', [])
        test_migrations = self.migration_data.get('test_migrations', [])
        all_migrations = migrations + test_migrations
        
        return [m for m in all_migrations if m.get('task') == task]
    
    def rollback_file(self, migration):
        """回滾單個檔案"""
        original_path = self.project_root / migration['original_path']
        new_path = self.project_root / migration['new_path']
        
        self.stats['total'] += 1
        
        # 檢查新位置的檔案是否存在
        if not new_path.exists():
            print(f"{YELLOW}⊘ 跳過: {new_path} (檔案不存在){RESET}")
            self.stats['skipped'] += 1
            return False
        
        # 檢查原始位置是否已有檔案
        if original_path.exists():
            print(f"{YELLOW}⊘ 跳過: {original_path} (目標位置已有檔案){RESET}")
            self.stats['skipped'] += 1
            return False
        
        if self.dry_run:
            print(f"{BLUE}[預覽] {new_path} → {original_path}{RESET}")
            self.stats['success'] += 1
            return True
        
        try:
            # 確保目標目錄存在
            original_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 移動檔案
            if new_path.is_dir():
                shutil.move(str(new_path), str(original_path))
            else:
                shutil.move(str(new_path), str(original_path))
            
            print(f"{GREEN}✓ 回滾: {new_path} → {original_path}{RESET}")
            self.stats['success'] += 1
            return True
            
        except Exception as e:
            print(f"{RED}✗ 失敗: {new_path} - {e}{RESET}")
            self.stats['failed'] += 1
            return False
    
    def rollback_migrations(self, migrations):
        """回滾多個檔案"""
        if not migrations:
            print(f"{YELLOW}沒有找到符合條件的遷移記錄{RESET}")
            return
        
        print(f"\n{BLUE}準備回滾 {len(migrations)} 個檔案...{RESET}\n")
        
        # 按照遷移時間倒序排列（先移動的後回滾）
        migrations_sorted = sorted(
            migrations,
            key=lambda x: x.get('moved_at', ''),
            reverse=True
        )
        
        for migration in migrations_sorted:
            self.rollback_file(migration)
        
        self.print_stats()
    
    def restore_from_backup(self, backup_path):
        """從備份目錄還原所有檔案"""
        backup_dir = Path(backup_path)
        
        if not backup_dir.exists():
            print(f"{RED}錯誤: 備份目錄不存在 {backup_dir}{RESET}")
            return False
        
        print(f"\n{BLUE}從備份還原: {backup_dir}{RESET}\n")
        
        if self.dry_run:
            print(f"{BLUE}[預覽] 將從 {backup_dir} 還原所有檔案{RESET}")
            return True
        
        try:
            # 詢問確認
            response = input(f"{YELLOW}警告: 這將覆蓋當前的專案檔案。確定要繼續嗎？ (yes/no): {RESET}")
            if response.lower() != 'yes':
                print(f"{YELLOW}已取消還原操作{RESET}")
                return False
            
            # 複製備份檔案到專案根目錄
            for item in backup_dir.iterdir():
                if item.name in ['.git', 'venv', 'node_modules', '__pycache__']:
                    continue
                
                dest = self.project_root / item.name
                
                if item.is_dir():
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(item, dest)
                else:
                    shutil.copy2(item, dest)
                
                print(f"{GREEN}✓ 還原: {item.name}{RESET}")
            
            print(f"\n{GREEN}✓ 成功從備份還原所有檔案{RESET}")
            return True
            
        except Exception as e:
            print(f"{RED}錯誤: 還原失敗 - {e}{RESET}")
            return False
    
    def print_stats(self):
        """列印統計資訊"""
        print(f"\n{'='*60}")
        print(f"{BLUE}回滾統計:{RESET}")
        print(f"  總計: {self.stats['total']}")
        print(f"  {GREEN}成功: {self.stats['success']}{RESET}")
        print(f"  {RED}失敗: {self.stats['failed']}{RESET}")
        print(f"  {YELLOW}跳過: {self.stats['skipped']}{RESET}")
        print(f"{'='*60}\n")
    
    def list_categories(self):
        """列出所有可用的類別"""
        if not self.migration_data:
            return
        
        migrations = self.migration_data.get('migrations', [])
        test_migrations = self.migration_data.get('test_migrations', [])
        all_migrations = migrations + test_migrations
        
        categories = {}
        for m in all_migrations:
            cat = m.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        print(f"\n{BLUE}可用的類別:{RESET}")
        for cat, count in sorted(categories.items()):
            print(f"  - {cat}: {count} 個檔案")
        print()
    
    def list_tasks(self):
        """列出所有可用的任務"""
        if not self.migration_data:
            return
        
        migrations = self.migration_data.get('migrations', [])
        test_migrations = self.migration_data.get('test_migrations', [])
        all_migrations = migrations + test_migrations
        
        tasks = {}
        for m in all_migrations:
            task = m.get('task', 'unknown')
            tasks[task] = tasks.get(task, 0) + 1
        
        print(f"\n{BLUE}可用的任務:{RESET}")
        for task, count in sorted(tasks.items()):
            print(f"  - {task}: {count} 個檔案")
        print()


def main():
    """主函數"""
    parser = argparse.ArgumentParser(
        description='檔案重組回滾腳本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  python scripts/rollback.py --all                    # 回滾所有檔案
  python scripts/rollback.py --category config        # 只回滾配置檔案
  python scripts/rollback.py --task 3.3               # 只回滾任務 3.3 的檔案
  python scripts/rollback.py --dry-run --all          # 預覽回滾操作
  python scripts/rollback.py --backup backups/pre-reorganization-20251111_093015
  python scripts/rollback.py --list-categories        # 列出所有類別
  python scripts/rollback.py --list-tasks             # 列出所有任務
        """
    )
    
    parser.add_argument('--all', action='store_true',
                       help='回滾所有檔案')
    parser.add_argument('--category', type=str,
                       help='只回滾指定類別的檔案 (config, script, test, asset, data, module, archive)')
    parser.add_argument('--task', type=str,
                       help='只回滾指定任務的檔案 (例如: 3.3, 5.2)')
    parser.add_argument('--backup', type=str,
                       help='從指定備份目錄還原所有檔案')
    parser.add_argument('--dry-run', action='store_true',
                       help='預覽模式，不實際執行回滾操作')
    parser.add_argument('--list-categories', action='store_true',
                       help='列出所有可用的類別')
    parser.add_argument('--list-tasks', action='store_true',
                       help='列出所有可用的任務')
    parser.add_argument('--log', type=str, default='migration_log.json',
                       help='遷移日誌檔案路徑 (預設: migration_log.json)')
    
    args = parser.parse_args()
    
    # 建立回滾管理器
    manager = RollbackManager(migration_log_path=args.log, dry_run=args.dry_run)
    
    # 載入遷移日誌
    if not manager.load_migration_log():
        return 1
    
    # 列出類別
    if args.list_categories:
        manager.list_categories()
        return 0
    
    # 列出任務
    if args.list_tasks:
        manager.list_tasks()
        return 0
    
    # 從備份還原
    if args.backup:
        success = manager.restore_from_backup(args.backup)
        return 0 if success else 1
    
    # 回滾檔案
    if args.all:
        migrations = manager.get_migrations_by_category('all')
        manager.rollback_migrations(migrations)
    elif args.category:
        migrations = manager.get_migrations_by_category(args.category)
        manager.rollback_migrations(migrations)
    elif args.task:
        migrations = manager.get_migrations_by_task(args.task)
        manager.rollback_migrations(migrations)
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
