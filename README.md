\# 🖋️ AI Font Generation \& Packaging Project



本專案致力於利用 AI 深度學習技術生成手寫/自訂字體，並提供完整的自動化打包工具，將生成的圖片資產轉換為實際可用的字型檔案 (TTF/SVG Font)。



專案主要分為兩大核心模組：\*\*HW02 (FontPacker)\*\* 與 \*\*HW03 (FontDiffuser-Finetune)\*\*。



\---



\## 📂 專案結構



\### 1. `hw02/FontPacker/` - 字體打包與格式轉換



負責處理從圖片資產到最終字型檔案的後處理工作流水線。



\*\*核心功能：\*\*

\- `svg2png.py` / `potrace.py`：負責 PNG 與 SVG 向量圖檔之間的互相轉換（利用 `potrace` 進行高質量向量化）。

\- `merge\_to\_svgfont.py`：將散落的單一字元圖片/向量檔合併封裝成單一的 SVG Font。

\- `run\_pico.py`：自動化處理腳本，進行圖片與字型最佳化。



\*\*目錄結構：\*\*

\- `png/`、`svg/`：儲存轉換過程中的中繼圖檔。

\- `final\_font/`：最終輸出的可用字體檔案。



\---



\### 2. `hw03/fontdiffuser-finetune/` - 擴散模型微調與字體生成



基於擴散模型 (Diffusion Model) 的字體生成模組。給定少量的手寫/特定風格參考圖，自動生成包含數千字的完整中文字庫。



\*\*核心功能：\*\*

\- \*\*模型微調 (Finetuning)\*\*：支援針對特定字體風格進行客製化微調 (`train.py`, `train\_phase\_1.bat`)。

\- \*\*大規模自動生成\*\*：針對缺字表 (如 `Strong.txt` 中的 7000+ 字) 進行批次生成。

\- \*\*自動後處理\*\*：包含自動將生成的圖片縮放校正為 300x300 尺寸 (`resize\_outputs.py`)。



\---



\## 🚀 最新訓練與優化成果 (HW03)



為了提升生成字體的「細節銳利度」與「筆畫穩定性」，我們對 FontDiffuser 進行了深度優化：



\### 1. 超參數優化 (Hyperparameter Tuning)

\- 總訓練步數 (`max\_train\_steps`) 提升至 \*\*10,000 步\*\*，使模型有充足的時間收斂並學習繁雜中文字的細節。

\- 梯度累積步數 (`gradient\_accumulation\_steps`) 設定為 \*\*2\*\*（有效 Batch Size = 16），大幅減少 Loss 震盪，提升訓練軌跡的平滑度。

\- 採用 `Cosine` 餘弦退火學習率排程器 (Learning Rate Scheduler)，並將基礎學習率下調至 `2e-5`，以穩定取得最佳解。



\### 2. 高品質推論 (High-Quality Sampling)

\- 將 DPM-Solver++ 的推論步數 (`num\_inference\_steps`) 提高至 \*\*50 步\*\*，有效消除生成邊緣的雜訊與破圖。



\### 3. 自動化生成流水線 (Automated Pipeline)

\- 整合 `generate\_strong.bat` 與 `resize\_outputs.py`，實現了\*\*「一鍵載入 10000 步權重 → 生成 7,200+ 缺字 → 統一縮放 300x300 尺寸」\*\*的完整工作流。



\---



\## 🛠️ 如何使用 (Workflow)



\### Step 1：訓練字體生成模型 (HW03)



```bash

\# 於 hw03/fontdiffuser-finetune/ 目錄下執行

train\_phase\_1.bat

```



> 訓練過程會自動將 Checkpoint 儲存於 `outputs/FontDiffuser\_Finetune/`



\---



\### Step 2：批次生成缺字圖片 (HW03)



當訓練達標後，使用最新權重（如 `global\_step\_10000`）進行字體生成與尺寸校正：



```bash

.\\generate\_strong.bat

```



> 生成的 300x300 高品質字體圖片會儲存於 `outputs\_Strong/`



\---



\### Step 3：打包為字型檔案 (HW02)



將生成的字元圖片移至 `hw02/FontPacker/` 中，進行向量化與打包：



```bash

cd ../../hw02/FontPacker

python potrace.py

python merge\_to\_svgfont.py

```



> 最終安裝檔將輸出至 `final\_font/` 目錄



\---



\## 📦 環境依賴 (Requirements)



\- Python 3.10+

\- `torch`, `torchvision`, `torchaudio`（CUDA 支援）

\- `accelerate`, `diffusers`

\- `opencv-python`, `Pillow`

\- `potrace`（用於 HW02 向量化）



安裝所有依賴：



```bash

pip install -r hw03/fontdiffuser-finetune/requirements.txt

```

