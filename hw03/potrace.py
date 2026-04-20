import os
import subprocess
import time
from pathlib import Path
from PIL import Image, ImageFilter

def process_potrace(input_folder_name, output_folder_name):
    base_path = Path(__file__).parent
    input_dir = base_path / input_folder_name
    output_dir = base_path / output_folder_name

    if not input_dir.exists():
        print(f"找不到輸入資料夾: {input_dir}")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    png_files = list(input_dir.glob("*.png"))

    if not png_files:
        print(f"在 {input_folder_name} 中找不到 .png 檔案")
        return

    print(f"開始處理 {input_folder_name} -> {output_folder_name} ({len(png_files)} 個檔案)...")
    start_time = time.time()
    
    for i, img_path in enumerate(png_files):
        # 簡易進度顯示
        if (i + 1) % 100 == 0 or i == 0 or i == len(png_files) - 1:
            print(f"進度: {i+1}/{len(png_files)}")
            
        svg_path = output_dir / f"{img_path.stem}.svg"
        temp_bmp = img_path.with_suffix(".bmp")

        try:
            with Image.open(img_path) as img:
                img = img.convert("L")
                img = img.filter(ImageFilter.GaussianBlur(radius=0.5)) 
                
                threshold = 140 
                binary_img = img.point(lambda p: 255 if p > threshold else 0, mode='1')
                binary_img.save(temp_bmp)

            subprocess.run(
                [
                    "potrace", # 通常在環境變數中只需寫 potrace
                    "-s", 
                    "--turdsize", "20", 
                    "--alphamax", "0.8", 
                    "--opttolerance", "0.2",
                    str(temp_bmp), 
                    "-o", str(svg_path)
                ],
                check=True,
                capture_output=True
            )
            
            if temp_bmp.exists():
                os.remove(temp_bmp)

        except Exception as e:
            print(f"轉換 {img_path.name} 失敗: {e}")

    end_time = time.time()
    print(f"{output_folder_name} 處理完成，耗時: {end_time - start_time:.2f} 秒")

if __name__ == "__main__":
    # 這裡對應您原本的資料夾名稱
    modes = ['Simple', 'Medium', 'Strong']
    for mode in modes:
        process_potrace(f'outputs_{mode}', f'outputs_{mode}') # 直接輸出到原資料夾或改名，這裡維持在原資料夾以便 merge_to_svgfont.py 讀取