import os
import subprocess
import time
import shutil
from pathlib import Path
from PIL import Image, ImageFilter

def find_potrace():
    # 1. Check if potrace is in PATH
    potrace_path = shutil.which("potrace")
    if potrace_path:
        return potrace_path
    
    # 2. Check known project locations
    # Path(__file__).parent is 'hw03'
    # We want 'hw02/FontPacker/potrace.exe'
    base_path = Path(__file__).parent.parent
    project_potrace = base_path / "hw02" / "FontPacker" / "potrace.exe"
    if project_potrace.exists():
        return str(project_potrace)
    
    # 3. Try potrace.exe in PATH (Windows)
    potrace_exe_path = shutil.which("potrace.exe")
    if potrace_exe_path:
        return potrace_exe_path
        
    return "potrace" # fallback to default

POTRACE_EXEC = find_potrace()

def process_potrace(input_folder_name, output_folder_name):
    base_path = Path(__file__).parent
    input_dir = base_path / input_folder_name
    output_dir = base_path / output_folder_name

    if not input_dir.exists():
        print(f"找不到輸入資料夾: {input_dir}")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    png_files = list(input_dir.glob("*.png"))
    # 修正 Bug: 排除暫存的 bmp 檔案，避免重複處理
    bmp_files = [f for f in input_dir.glob("*.bmp") if ".potrace_temp" not in f.name]
    image_files = png_files + bmp_files

    if not image_files:
        print(f"在 {input_folder_name} 中找不到 .png 或 .bmp 檔案")
        return

    print(f"開始處理 {input_folder_name} -> {output_folder_name} ({len(image_files)} 個檔案)...")
    print(f"使用 Potrace 執行檔: {POTRACE_EXEC}")
    start_time = time.time()
    
    for i, img_path in enumerate(image_files):
        svg_path = output_dir / f"{img_path.stem}.svg"
        
        # 跳過已存在的檔案
        if svg_path.exists():
            continue

        # 簡易進度顯示
        if (i + 1) % 100 == 0 or i == 0 or i == len(image_files) - 1:
            print(f"進度: {i+1}/{len(image_files)}")
            
        temp_bmp = img_path.with_suffix(".potrace_temp.bmp")

        try:
            with Image.open(img_path) as img:
                img = img.convert("L")
                img = img.filter(ImageFilter.GaussianBlur(radius=0.5)) 
                
                threshold = 140 
                binary_img = img.point(lambda p: 255 if p > threshold else 0, mode='1')
                binary_img.save(temp_bmp)

            subprocess.run(
                [
                    POTRACE_EXEC, 
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