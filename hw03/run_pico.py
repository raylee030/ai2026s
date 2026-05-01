import os
import subprocess
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

BASE = Path(__file__).parent

concurrency = 10

if __name__ == "__main__":
    start_time = time.time()
    for mode in ["Simple", "Medium", "Strong"]:
        input_folder = BASE / f"outputs_{mode}"
        output_folder = BASE / f"pico_{mode}"
        
        if not input_folder.exists():
            print(f"Skipping {mode}: {input_folder} does not exist.")
            continue
            
        output_folder.mkdir(exist_ok=True)
        
        files = [f for f in os.listdir(input_folder) if f.endswith(".svg")]
        
        # 檢查是否所有檔案都已存在於輸出資料夾
        existing_files = [f for f in os.listdir(output_folder) if f.endswith(".svg")]
        if len(existing_files) >= len(files) and len(files) > 0:
            print(f"Skipping {mode}: All files already processed in {output_folder}.")
            continue

        print(f"Processing {mode}...")
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            def process_file(filename):
                input_path = input_folder / filename
                output_path = output_folder / filename
                
                # Skip if already exists and not empty
                if output_path.exists() and output_path.stat().st_size > 0:
                    return

                try:
                    with open(output_path, "w") as out_file:
                        subprocess.run(["picosvg", str(input_path)], stdout=out_file, check=True)
                except Exception as e:
                    print(f"Error processing {filename} in {mode}: {e}")
                    # If failed, remove the potentially empty/broken file
                    if output_path.exists():
                        output_path.unlink()

            executor.map(process_file, files)
            
    print(f"Conversion complete! Time taken: {time.time() - start_time:.2f} seconds")