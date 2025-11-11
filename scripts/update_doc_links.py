#!/usr/bin/env python3
"""
Script to update internal links in markdown files after file reorganization.
Scans all .md files and updates relative links to reflect new file locations.
"""

import sys
import os
# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set

# Load migration log
def load_migration_log() -> Dict:
    """Load the migration log to get file movement mappings."""
    with open('migration_log.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Build path mapping from migration log
def build_path_mapping(migration_log: Dict) -> Dict[str, str]:
    """Build a mapping of old paths to new paths."""
    mapping = {}
    for migration in migration_log.get('migrations', []):
        old_path = migration['original_path']
        new_path = migration['new_path']
        mapping[old_path] = new_path
    return mapping

# Additional known file movements from tasks 4.2-4.6
ADDITIONAL_MAPPINGS = {
    # Guides (4.2)
    '開始使用_README.md': 'docs/guides/quick_start.md',
    '碳排放追蹤系統_使用說明.md': 'docs/guides/carbon_tracking_usage.md',
    'VOICE_CLONE_GUIDE.md': 'docs/guides/voice_clone_guide.md',
    'build_android_app.md': 'docs/guides/android_app_build.md',
    'deploy_to_render.md': 'docs/guides/deployment_guide.md',
    '快速參考卡.md': 'docs/guides/快速參考卡.md',
    'PWA檢查清單.md': 'docs/guides/PWA檢查清單.md',
    '部署檢查清單.md': 'docs/guides/部署檢查清單.md',
    '最終檢查清單.md': 'docs/guides/最終檢查清單.md',
    '🚀快速啟動指南.md': 'docs/guides/🚀快速啟動指南.md',
    '🚀APK建置與上架完整指南.md': 'docs/guides/🚀APK建置與上架完整指南.md',
    
    # Technical docs (4.3)
    'project-structure.md': 'docs/technical/architecture/project-structure.md',
    'SYSTEM_ARCHITECTURE_DIAGRAM.svg': 'docs/technical/architecture/SYSTEM_ARCHITECTURE_DIAGRAM.svg',
    'BACKEND_TECHNICAL_DOCUMENTATION.md': 'docs/technical/backend/BACKEND_TECHNICAL_DOCUMENTATION.md',
    'FRONTEND_TECHNICAL_DOCUMENTATION.md': 'docs/technical/frontend/FRONTEND_TECHNICAL_DOCUMENTATION.md',
    'ADVANCED_VOICE_SEPARATION_GUIDE.md': 'docs/technical/voice/ADVANCED_VOICE_SEPARATION_GUIDE.md',
    'AUDIO_SEPARATION_GUIDE.md': 'docs/technical/voice/AUDIO_SEPARATION_GUIDE.md',
    'VOICE_DATASET_VALIDATION_GUIDE.md': 'docs/technical/voice/VOICE_DATASET_VALIDATION_GUIDE.md',
    'GPT_SOVITS_FINE_TUNING_GUIDE.md': 'docs/technical/voice/GPT_SOVITS_FINE_TUNING_GUIDE.md',
    'VOICE_CLONE_SETUP.md': 'docs/technical/voice/VOICE_CLONE_SETUP.md',
    'MODEL_STORAGE_DEPLOYMENT_GUIDE.md': 'docs/technical/voice/MODEL_STORAGE_DEPLOYMENT_GUIDE.md',
    'MODEL_WEIGHTS_CONFIGURATION_GUIDE.md': 'docs/technical/voice/MODEL_WEIGHTS_CONFIGURATION_GUIDE.md',
    'VOLUME_BALANCE_SOLUTION.md': 'docs/technical/voice/VOLUME_BALANCE_SOLUTION.md',
    'NATURAL_VS_ADVANCED_COMPARISON.md': 'docs/technical/voice/NATURAL_VS_ADVANCED_COMPARISON.md',
    'setup_asr_environment.md': 'docs/technical/asr/setup_asr_environment.md',
    
    # Reports (4.4)
    'AI_CORE_MODULES_ARCHITECTURE_REPORT.md': 'docs/reports/AI_CORE_MODULES_ARCHITECTURE_REPORT.md',
    'VOICE_DATA_PROCESSING_AND_AI_MODULES_REPORT.md': 'docs/reports/VOICE_DATA_PROCESSING_AND_AI_MODULES_REPORT.md',
    'NOISE_REDUCTION_IMPROVEMENT_REPORT.md': 'docs/reports/NOISE_REDUCTION_IMPROVEMENT_REPORT.md',
    'MODULE_TESTING_REPORT.md': 'docs/reports/MODULE_TESTING_REPORT.md',
    'ELDERLY_VOICE_DATASET_VALIDATION_REPORT.md': 'docs/reports/ELDERLY_VOICE_DATASET_VALIDATION_REPORT.md',
    'CLEANUP_SUMMARY.md': 'docs/reports/CLEANUP_SUMMARY.md',
    '優化後模型成效比較報告.md': 'docs/reports/優化後模型成效比較報告.md',
    '專業系統驗證及ASR改進整合報告.md': 'docs/reports/專業系統驗證及ASR改進整合報告.md',
    '推廣成果摘要報告.md': 'docs/reports/推廣成果摘要報告.md',
    '碳排放減少效益分析.md': 'docs/reports/碳排放減少效益分析.md',
    '專案技術分析報告.md': 'docs/reports/專案技術分析報告.md',
    
    # Status docs (4.5)
    '✅碳排放追蹤系統_建置完成.md': 'docs/status/completed/✅碳排放追蹤系統_建置完成.md',
    '✅工號自動帶出姓名功能完成.md': 'docs/status/completed/✅工號自動帶出姓名功能完成.md',
    '✅搜尋與篩選功能完成.md': 'docs/status/completed/✅搜尋與篩選功能完成.md',
    '✅記錄編輯刪除功能完成.md': 'docs/status/completed/✅記錄編輯刪除功能完成.md',
    '✅資料匯出功能完成.md': 'docs/status/completed/✅資料匯出功能完成.md',
    '✅優化完成_立即測試.md': 'docs/status/completed/✅優化完成_立即測試.md',
    '✅PWA_Android_App完成.md': 'docs/status/completed/✅PWA_Android_App完成.md',
    '✅完成報告_所有佐證資料已就緒.md': 'docs/status/completed/✅完成報告_所有佐證資料已就緒.md',
    '🎉部署成功_開始建置APK.md': 'docs/status/deployment/🎉部署成功_開始建置APK.md',
    '🎉部署完成_下一步行動.md': 'docs/status/deployment/🎉部署完成_下一步行動.md',
    '🎉PWA轉換完成_快速開始.md': 'docs/status/completed/🎉PWA轉換完成_快速開始.md',
    '🎊完整方案_PWA+Android全部完成.md': 'docs/status/completed/🎊完整方案_PWA+Android全部完成.md',
    '🎊PWA完整方案_全部完成.md': 'docs/status/completed/🎊PWA完整方案_全部完成.md',
    '🔧修復完成_等待部署.md': 'docs/status/deployment/🔧修復完成_等待部署.md',
    '🌿淡化綠色主題+分頁功能完成.md': 'docs/status/completed/🌿淡化綠色主題+分頁功能完成.md',
    '🌿環保綠色主題優化完成.md': 'docs/status/completed/🌿環保綠色主題優化完成.md',
    '📱轉換為Android_App指南.md': 'docs/status/completed/📱轉換為Android_App指南.md',
    '📱Android_App建置完成.md': 'docs/status/completed/📱Android_App建置完成.md',
    'UI優化完成說明.md': 'docs/status/completed/UI優化完成說明.md',
    '完成清單_稽核佐證資料.md': 'docs/status/completed/完成清單_稽核佐證資料.md',
    
    # Other docs (4.6)
    '系統改進建議.md': 'docs/系統改進建議.md',
    '部署架構優化方案.md': 'docs/technical/architecture/部署架構優化方案.md',
    '部署模式說明.md': 'docs/technical/architecture/部署模式說明.md',
    'Render部署問題排查.md': 'docs/status/deployment/Render部署問題排查.md',
    'Android_App功能相容性分析.md': 'docs/technical/Android_App功能相容性分析.md',
    'PYTHON_313_COMPATIBILITY_FIX.md': 'docs/technical/PYTHON_313_COMPATIBILITY_FIX.md',
    'emotion_color_guide.md': 'docs/technical/voice/emotion_color_guide.md',
}

def find_all_markdown_files() -> List[Path]:
    """Find all markdown files in the project."""
    md_files = []
    for root, dirs, files in os.walk('.'):
        # Skip certain directories
        skip_dirs = {'.git', 'venv', 'node_modules', '__pycache__', '.kiro', 'backups', 'archive'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file.endswith('.md'):
                md_files.append(Path(root) / file)
    
    return md_files

def extract_markdown_links(content: str) -> List[Tuple[str, str]]:
    """Extract markdown links from content. Returns list of (full_match, link_path) tuples."""
    # Match markdown links: [text](path)
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = []
    
    for match in re.finditer(pattern, content):
        full_match = match.group(0)
        link_path = match.group(2)
        
        # Skip external links (http://, https://, mailto:, etc.)
        if not link_path.startswith(('http://', 'https://', 'mailto:', '#', 'ftp://')):
            matches.append((full_match, link_path))
    
    return matches

def normalize_path(path: str) -> str:
    """Normalize path for comparison."""
    # Remove leading ./ and trailing /
    path = path.lstrip('./')
    path = path.rstrip('/')
    # Handle URL fragments
    if '#' in path:
        path = path.split('#')[0]
    return path

def calculate_relative_path(from_file: Path, to_file: str) -> str:
    """Calculate relative path from one file to another."""
    from_dir = from_file.parent
    to_path = Path(to_file)
    
    try:
        rel_path = os.path.relpath(to_path, from_dir)
        # Convert Windows paths to Unix-style for markdown
        rel_path = rel_path.replace('\\', '/')
        return rel_path
    except ValueError:
        # If paths are on different drives (Windows), return absolute
        return to_file

def update_links_in_file(file_path: Path, path_mapping: Dict[str, str]) -> Tuple[int, List[str]]:
    """Update links in a single markdown file. Returns (num_updates, list_of_changes)."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0, []
    
    original_content = content
    links = extract_markdown_links(content)
    updates = 0
    changes = []
    
    for full_match, link_path in links:
        # Extract the actual file path (remove anchors)
        clean_link = link_path.split('#')[0] if '#' in link_path else link_path
        anchor = '#' + link_path.split('#')[1] if '#' in link_path else ''
        
        # Normalize the link path
        normalized_link = normalize_path(clean_link)
        
        # Check if this file has been moved
        if normalized_link in path_mapping:
            new_path = path_mapping[normalized_link]
            
            # Calculate new relative path from current file to new location
            new_relative_path = calculate_relative_path(file_path, new_path)
            
            # Add anchor back if it existed
            new_link = new_relative_path + anchor
            
            # Create the new markdown link
            text = full_match.split('](')[0][1:]  # Extract link text
            new_full_match = f'[{text}]({new_link})'
            
            # Replace in content
            content = content.replace(full_match, new_full_match)
            updates += 1
            changes.append(f"  {link_path} → {new_link}")
    
    # Write back if changes were made
    if updates > 0:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            return 0, []
    
    return updates, changes

def main():
    """Main function to update all markdown links."""
    print("=" * 80)
    print("Updating Internal Links in Markdown Files")
    print("=" * 80)
    print()
    
    # Load migration log and build path mapping
    print("Loading migration log...")
    migration_log = load_migration_log()
    path_mapping = build_path_mapping(migration_log)
    
    # Add additional known mappings
    path_mapping.update(ADDITIONAL_MAPPINGS)
    
    print(f"Loaded {len(path_mapping)} file path mappings")
    print()
    
    # Find all markdown files
    print("Scanning for markdown files...")
    md_files = find_all_markdown_files()
    print(f"Found {len(md_files)} markdown files")
    print()
    
    # Update links in each file
    print("Updating links...")
    print("-" * 80)
    
    total_updates = 0
    files_updated = 0
    all_changes = []
    
    for md_file in md_files:
        updates, changes = update_links_in_file(md_file, path_mapping)
        if updates > 0:
            files_updated += 1
            total_updates += updates
            print(f"\n✓ {md_file}")
            for change in changes:
                print(change)
            all_changes.append({
                'file': str(md_file),
                'updates': updates,
                'changes': changes
            })
    
    print()
    print("-" * 80)
    print(f"\nSummary:")
    print(f"  Files scanned: {len(md_files)}")
    print(f"  Files updated: {files_updated}")
    print(f"  Total link updates: {total_updates}")
    print()
    
    # Save update log
    update_log = {
        'timestamp': '2025-11-11T12:00:00',
        'task': '4.7',
        'files_scanned': len(md_files),
        'files_updated': files_updated,
        'total_updates': total_updates,
        'changes': all_changes
    }
    
    with open('doc_links_update_log.json', 'w', encoding='utf-8') as f:
        json.dump(update_log, f, indent=2, ensure_ascii=False)
    
    print("Update log saved to: doc_links_update_log.json")
    print()
    print("=" * 80)
    print("Link update complete!")
    print("=" * 80)

if __name__ == '__main__':
    main()
