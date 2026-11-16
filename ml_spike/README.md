# ML spike — dự đoán fc / ft / εu (thử nghiệm, chưa phải bản chính thức)

Ngày: 2026-11-04. Mô hình: HistGradientBoosting nông (depth 3), ~70 biến.
Đánh giá: **leave-paper-out** (giấu nguyên bài báo khi kiểm tra = mô phỏng lab mới).

## Kết quả

| Đầu ra | Dữ liệu gốc (80 bài) | + 41 bài mới (110 bài) |
|---|---|---|
| fc | R² 0.64, MAE 22 MPa | R² 0.62, MAE 22 MPa |
| ft kéo trực tiếp | R² 0.57, MAE 1.8 MPa | R² 0.53, MAE 2.0 MPa |
| εu kéo trực tiếp | R² 0.31–0.38 | R² 0.36 |

Đường học (`learning_curves.png`): sai số chững lại khoảng 26–30% từ ~50 bài trở đi.
→ **Thêm bài báo không còn giúp nhiều.** Nút thắt là khác biệt giữa các lab.

## Hiệu chỉnh bằng mẫu của chính lab (`calib.py`)

Sai số tương đối trên bài báo chưa thấy, khi biết kết quả thật của k mẫu cùng lab:

| k mẫu đã đúc | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| fc | 34% | 17% | 15% | 14% |
| ft | 35% | 24% | 21% | 20% |

→ Đúc 1–3 mẫu ở lab của bạn giảm sai số khoảng một nửa.

## Dữ liệu mới (`additions/`) — CẦN BẠN KIỂM TRA trước khi gộp vào `03 Dataset_ratio.xlsx`

| File | Bài | Dòng |
|---|---|---|
| pvaecc.csv | 9 | 60 |
| geopolymer.csv | 11 | 117 |
| uhpc_steel.csv | 13 | 112 |
| uhpecc.csv | 8 | 37 |

- Header giống tên cột trong `03 Dataset_ratio.xlsx` (99 cột chính).
- Cột cuối "Conversions / notes" ghi quy đổi + chỗ nghi ngờ (tìm chữ VERIFY).
- Chỗ đáng xem: Guo 2024 (10.3390/ma17174356) có thể bị đảo FA/GGBS; Zuo 2022 là cường độ uốn (đã gắn "flexural").
- `*_rejected.txt`: bài đã xem nhưng loại, kèm lý do.
- Tất cả đọc qua Europe PMC full text (MDPI chủ yếu), chưa đối chiếu Crossref riêng.

## Tiến độ thu thập (cập nhật 2026-11-06)

| Đợt | Bài | Dòng | File |
|---|---|---|---|
| Gốc (03 Dataset_ratio.xlsx) | 83 | 724 | — |
| 1 | 41 | 326 | pvaecc, geopolymer, uhpc_steel, uhpecc |
| 2 | 49 | 587 | w2_* |
| 3 | 61 | 868 | w3_* |
| 4 | 68 | 514 | w4_* (ưu tiên kéo trực tiếp) |
| **Tổng** | **~302** | **~3000** | |

R² CatBoost, bộ đầu vào web (không kích thước mẫu, không thông số sợi):

| Đầu ra | Lab mới (giấu bài) | Đã có 50% mẫu của lab |
|---|---|---|
| fc (2382 dòng, 264 bài) | 0.71 | 0.93 |
| ft trực tiếp (1022 dòng, 175 bài) | 0.48 | 0.82 |
| εu (732 dòng, 143 bài) | 0.40 | 0.74 |

## Làm sạch dữ liệu (`clean/`, 2026-11-06)

Không xoá dòng nào — `clean/dataset_clean.csv` gắn `use_fc / use_ft / use_eps` + lý do loại.
Xem lại bằng `clean/cleaning_review.xlsx` (Summary, Excluded rows, Model outliers, VERIFY rows).

Quy tắc (chỉ giữ quy tắc nào làm mô hình tốt hơn trong `clean/ablation*.csv`):
- fc, ft: loại thí nghiệm đặc biệt (lửa, đóng băng, động), không sợi, outlier mô hình, binder lạ, thiếu W/B hoặc tuổi.
- εu: loại thí nghiệm đặc biệt, outlier, sai kiểm tra vật lý, có cốt liệu thô, binder lạ.
- Kiểu kéo nhận dạng lại: dog-bone / dumbbell / briquette → "direct"; notched tách riêng.

| Đầu ra | Trước: dòng / R² lab mới / R² lab đã biết | Sau |
|---|---|---|
| fc | 2382 / 0.71 / 0.93 | 1651 / **0.83** / **0.95** |
| ft trực tiếp | 1022 / 0.48 / 0.82 | 686 / **0.57** / 0.83 |
| εu | 732 / 0.40 / 0.74 | 667 / **0.46** / 0.74 |

Chạy lại: `clean/audit.py "../03 Dataset_ratio.xlsx" clean` → `clean/make_clean.py clean` → `clean/eval_clean.py "../03 Dataset_ratio.xlsx" clean`.

## Lọc theo density + Inventory (2026-11-09/10)

- Inventory of raw materials.xlsx: 19 → 69 vật liệu, mọi giá trị có nguồn (`inventory/*.json`, `inventory/merge_inventory.py`).
  35/200 ô năng lượng/CO₂/giá chưa có nguồn (để trống). 01 Datamix.xlsx đồng bộ: 69 vật liệu, web đọc đủ.
- 400 dòng dùng chất không có density có nguồn ("Other binder", sợi không rõ loại, phụ gia/hoạt hoá gộp) chuyển sang sheet
  **Removed** của 03 Dataset_ratio.xlsx (kèm lý do) → Dataset còn 2619 dòng / 285 bài. `inventory/move_rows_without_density.py`.
- Sau lọc + làm sạch (CatBoost):

| Đầu ra | Trước lọc density: R² lab mới / lab đã biết | Sau lọc density |
|---|---|---|
| fc | 0.83 / 0.95 (1651 dòng) | 0.81 / 0.95 (1460 dòng, 191 bài) |
| ft trực tiếp | 0.57 / 0.83 (686) | 0.52 / 0.83 (638, 128 bài) |
| εu | 0.46 / 0.74 (667) | 0.51 / 0.73 (610, 125 bài) |

- Môi trường Python: `ml_spike/.venv` (Smart App Control phải tắt, nếu không Windows chặn DLL của pandas/sklearn/catboost).

## Đã gộp vào 03 Dataset_ratio.xlsx (2026-11-06)

- 2295 dòng / 219 bài từ `additions/*.csv` nằm ở hàng 727–3021; 219 dòng mới trong `03 Dataset_sources.csv`.
- 218/219 DOI khớp Crossref (title + tác giả đầu); bài còn lại khớp title 100%, chỉ khác cách viết họ.
- Cột "Paper notes" bắt đầu bằng `[Agent-extracted …, <file>.csv]`; quy đổi của AI nằm ở cột "AI-derived values"; ô VERIFY tô vàng.
- Bản sao lưu trước khi gộp: `Backup/03 Dataset_ratio_backup_20261106_1055_before_merge.xlsx`, `Backup/03 Dataset_sources_backup_*_before_merge.csv`.
- `merge/verify_merge.py` xác nhận dữ liệu đọc từ workbook mới giống hệt file cũ + CSV (mọi ô, không tính thứ tự dòng).
- **Từ giờ chạy các script KHÔNG kèm tham số `additions`** (nếu không sẽ bị đếm trùng). `additions/` chỉ còn là kho lưu trữ + danh sách bỏ qua cho agent.

Hướng dẫn cho agent: `additions/AGENT_BRIEF.md`. Danh sách bỏ qua: `additions/existing_papers.txt`.

## Chạy lại

```
python spike.py "../03 Dataset_ratio.xlsx" <thư mục output> additions
python calib.py "../03 Dataset_ratio.xlsx" . additions
```
Cần: pandas, openpyxl, scikit-learn, matplotlib.

## So sánh 10 mô hình (2026-11-16, `benchmark10.py`)

Dữ liệu đã làm sạch (`clean/dataset_clean.csv`), 33 đầu vào web. **Chỉ số chính: 10-fold CV chia ngẫu nhiên × 3 seed.**

| Đầu ra (dòng / bài) | Tốt nhất | R² 10-fold | Lab mới (giấu bài) |
|---|---|---|---|
| fc (1460 / 191) | CatBoost | 0.952 | 0.81 |
| ft trực tiếp (638 / 128) | CatBoost | 0.830 | 0.52 |
| εu (610 / 125) | XGBoost 0.782 ≈ Extra Trees 0.781 | 0.78 | 0.47 |

Web dùng CatBoost (fc, ft) + Extra Trees (εu).

**Từ 2026-11-16 mô hình chỉ học từ `04 Dataset_web.xlsx`** (69 vật liệu của web + 5 điều kiện + 2 kết quả: nén, biến dạng kéo), tạo bằng `build_web_dataset.py`; đặc trưng tính trong `web_data.py` theo đúng công thức của web. Chạy: `python build_web_dataset.py` → `python benchmark10.py` → `python train_export.py ../strength_model.js`.
Trang kết quả: `benchmark.html`. Mục 5 của `index.html` thêm điều kiện bảo dưỡng + tuổi thí nghiệm.
