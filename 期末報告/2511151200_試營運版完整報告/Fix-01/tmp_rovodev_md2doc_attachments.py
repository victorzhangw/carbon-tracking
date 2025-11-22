import os
from pathlib import Path
from tmp_rovodev_md2doc import convert_file  # reuse functions

def main():
    base = Path(__file__).parent / '佐證資料'
    targets = [
        '附件1_長者滿意度調查問卷_試營運版.md',
        '附件2_社工人員訪談紀錄_試營運版.md',
        '附件3_交通工具使用調查統計_試營運版.md',
        '附件4_每月執行成果統計表_試營運版.md',
    ]
    for name in targets:
        md = base / name
        if md.exists():
            out = md.with_suffix('.doc')
            convert_file(md, out)
            print(f'Converted: {md.name} -> {out.name}')
        else:
            print(f'Skip missing: {md}')

if __name__ == '__main__':
    main()
