\# 🖋️ AI Font Generation \& Packaging Project

&#x20;   2

&#x20;   3 本專案致力於利用 AI

&#x20;     深度學習技術生成手寫/自訂字體，並提供完整的自動化打包工具，將生成的圖片資產轉換為實際可用的字型檔案 (TTF/SVG

&#x20;     Font)。

&#x20;   4

&#x20;   5 專案主要分為兩大核心模組：\*\*HW02 (FontPacker)\*\* 與 \*\*HW03 (FontDiffuser-Finetune)\*\*。

&#x20;   6

&#x20;   7 ---

&#x20;   8

&#x20;   9 ## 📂 專案結構

&#x20;  10

&#x20;  11 ### 1. `hw02/FontPacker/` - 字體打包與格式轉換

&#x20;  12 負責處理從圖片資產到最終字型檔案的後處理工作流水線。

&#x20;  13

&#x20;  14 \*   \*\*核心功能\*\*：

&#x20;  15     \*   `svg2png.py` / `potrace.py`：負責 PNG 與 SVG 向量圖檔之間的互相轉換（利用 `potrace` 進行高質量向量化）。

&#x20;  16     \*   `merge\_to\_svgfont.py`：將散落的單一字元圖片/向量檔合併封裝成單一的 SVG Font。

&#x20;  17     \*   `run\_pico.py`：自動化處理腳本，進行圖片與字型最佳化。

&#x20;  18 \*   \*\*目錄結構\*\*：

&#x20;  19     \*   `png/`、`svg/`：儲存轉換過程中的中繼圖檔。

&#x20;  20     \*   `final\_font/`：最終輸出的可用字體檔案。

&#x20;  21

&#x20;  22 ### 2. `hw03/fontdiffuser-finetune/` - 擴散模型微調與字體生成

&#x20;  23 基於擴散模型 (Diffusion Model) 的字體生成模組。給定少量的手寫/特定風格參考圖，自動生成包含數千字的完整中文字庫。

&#x20;  24

&#x20;  25 \*   \*\*核心功能\*\*：

&#x20;  26     \*   \*\*模型微調 (Finetuning)\*\*：支援針對特定字體風格進行客製化微調 (`train.py`, `train\_phase\_1.bat`)。

&#x20;  27     \*   \*\*大規模自動生成\*\*：針對缺字表 (如 `Strong.txt` 中的 7000+ 字) 進行批次生成。

&#x20;  28     \*   \*\*自動後處理\*\*：包含自動將生成的圖片縮放校正為 300x300 尺寸 (`resize\_outputs.py`)。

&#x20;  29

&#x20;  30 ---

&#x20;  31

&#x20;  32 ## 🚀 最新訓練與優化成果 (HW03)

&#x20;  33

&#x20;  34 為了提升生成字體的「細節銳利度」與「筆畫穩定性」，我們對 FontDiffuser 進行了深度優化：

&#x20;  35

&#x20;  36 1.  \*\*超參數優化 (Hyperparameter Tuning)\*\*：

&#x20;  37     \*   總訓練步數 (`max\_train\_steps`) 提升至 \*\*10,000 步\*\*，使模型有充足的時間收斂並學習繁雜中文字的細節。

&#x20;  38     \*   梯度累積步數 (`gradient\_accumulation\_steps`) 設定為 \*\*2\*\* (有效 Batch Size = 16)，大幅減少 Loss

&#x20;     震盪，提升訓練軌跡的平滑度。

&#x20;  39     \*   採用 `Cosine` 餘弦退火學習率排程器 (Learning Rate Scheduler)，並將基礎學習率下調至

&#x20;     `2e-5`，以穩定取得最佳解。

&#x20;  40 2.  \*\*高品質推論 (High-Quality Sampling)\*\*：

&#x20;  41     \*   將 DPM-Solver++ 的推論步數 (`num\_inference\_steps`) 提高至 \*\*50 步\*\*，有效消除生成邊緣的雜訊與破圖。

&#x20;  42 3.  \*\*自動化生成流水線 (Automated Pipeline)\*\*：

&#x20;  43     \*   整合 `generate\_strong.bat` 與 `resize\_outputs.py`，實現了\*\*「一鍵載入 10000 步權重 $\\rightarrow$ 生成

&#x20;     7,200+ 缺字 $\\rightarrow$ 統一縮放 300x300 尺寸」\*\*的完整工作流。

&#x20;  44

&#x20;  45 ---

&#x20;  46

&#x20;  47 ## 🛠️ 如何使用 (Workflow)

&#x20;  48

&#x20;  49 ### Step 1: 訓練字體生成模型 (HW03)

&#x20;  1 \*(訓練過程會自動將 Checkpoint 儲存於 `outputs/FontDiffuser\_Finetune/`)\*

&#x20;  2

&#x20;  3 ### Step 2: 批次生成缺字圖片 (HW03)

&#x20;  4 當訓練達標後，使用最新權重 (如 `global\_step\_10000`) 進行字體生成與尺寸校正：

&#x20; .\\generate\_strong.bat



&#x20;  1 \*(生成的 300x300 高品質字體圖片會儲存於 `outputs\_Strong/`)\*

&#x20;  2

&#x20;  3 ### Step 3: 打包為字型檔案 (HW02)

&#x20;  4 將生成的字元圖片移至 `hw02/FontPacker/` 中，進行向量化與打包：

&#x20; cd ../../hw02/FontPacker

&#x20; python potrace.py

&#x20; python merge\_to\_svgfont.py



&#x20;   1 \*(最終安裝檔將輸出至 `final\_font/` 目錄)\*

&#x20;   2

&#x20;   3 ---

&#x20;   4

&#x20;   5 ## 📦 環境依賴 (Requirements)

&#x20;   6

&#x20;   7 \*   Python 3.10+

&#x20;   8 \*   `torch`, `torchvision`, `torchaudio` (CUDA 支援)

&#x20;   9 \*   `accelerate`, `diffusers`

&#x20;  10 \*   `opencv-python`, `Pillow`

&#x20;  11 \*   `potrace` (用於 HW02 向量化)

&#x20; pip install -r hw03/fontdiffuser-finetune/requirements.txt

