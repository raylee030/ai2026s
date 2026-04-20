import os
import subprocess
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

BASE = Path(__file__).parent
input_folder = BASE / "output"
output_folder = BASE / "pico"

concurrency = 20

def process_single_file(filename):
    if not filename.endswith(".svg"):
        return
    input_path = input_folder / filename
    output_path = output_folder / filename
    try:
        with open(output_path, "w") as out_file:
            subprocess.run(["picosvg", str(input_path)], stdout=out_file, check=True)
        print(f"Successfully processed: {filename}")
    except Exception as e:
        print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    output_folder.mkdir(exist_ok=True)
    start_time = time.time()
    files = os.listdir(input_folder)
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        executor.map(process_single_file, files)
    print(f"Conversion complete! Time taken: {time.time() - start_time:.2f} seconds")