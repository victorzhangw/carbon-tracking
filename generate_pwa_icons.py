"""
生成 PWA 所需的各種尺寸 Icon
需要安裝 Pillow: pip install Pillow
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_path):
    """建立指定尺寸的 Icon"""
    # 建立圖片
    img = Image.new('RGB', (size, size), color='#689F38')
    draw = ImageDraw.Draw(img)
    
    # 繪製圓角矩形背景
    margin = size // 10
    draw.rounded_rectangle(
        [(margin, margin), (size - margin, size - margin)],
        radius=size // 8,
        fill='#8BC34A'
    )
    
    # 繪製葉子圖案（簡化版）
    center_x, center_y = size // 2, size // 2
    leaf_size = size // 3
    
    # 葉子主體
    draw.ellipse(
        [center_x - leaf_size//2, center_y - leaf_size,
         center_x + leaf_size//2, center_y + leaf_size//2],
        fill='#F1F8E9'
    )
    
    # 葉脈
    draw.line(
        [(center_x, center_y - leaf_size), (center_x, center_y + leaf_size//2)],
        fill='#689F38',
        width=max(2, size // 64)
    )
    
    # 儲存圖片
    img.save(output_path, 'PNG', quality=95)
    print(f'✅ 已生成: {output_path} ({size}x{size})')

def main():
    """生成所有需要的 Icon 尺寸"""
    # 建立 icons 資料夾
    icons_dir = 'static/icons'
    os.makedirs(icons_dir, exist_ok=True)
    
    # 需要的尺寸
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    
    print('🎨 開始生成 PWA Icons...\n')
    
    for size in sizes:
        output_path = os.path.join(icons_dir, f'icon-{size}x{size}.png')
        create_icon(size, output_path)
    
    print(f'\n✅ 完成！已生成 {len(sizes)} 個 Icon')
    print(f'📁 位置: {icons_dir}/')
    
    # 建立 Apple Touch Icon
    apple_icon_path = os.path.join(icons_dir, 'apple-touch-icon.png')
    create_icon(180, apple_icon_path)
    print(f'✅ 已生成 Apple Touch Icon: {apple_icon_path}')
    
    # 建立 Favicon
    favicon_path = 'static/favicon.ico'
    img = Image.new('RGB', (32, 32), color='#689F38')
    draw = ImageDraw.Draw(img)
    draw.ellipse([8, 8, 24, 24], fill='#F1F8E9')
    img.save(favicon_path, 'ICO')
    print(f'✅ 已生成 Favicon: {favicon_path}')

if __name__ == '__main__':
    try:
        main()
    except ImportError:
        print('❌ 錯誤：需要安裝 Pillow')
        print('請執行：pip install Pillow')
    except Exception as e:
        print(f'❌ 錯誤：{e}')
