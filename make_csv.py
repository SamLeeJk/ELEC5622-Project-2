# make_csv.py
import csv, sys
from pathlib import Path

# 默认数据根目录：./data
data_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("./data")

splits = ["train", "val", "test"]  # 三个子目录
# 自动按 train 下的子文件夹推断类别（保证 train/val/test 都一致）
class_dirs = [p.name for p in sorted((data_dir/"train").iterdir()) if p.is_dir()]
print("Detected classes:", class_dirs)

# 写一个函数，遍历某个 split，生成 CSV
def write_csv(split):
    rows = []
    split_dir = data_dir / split
    for cls in class_dirs:
        cls_dir = split_dir / cls
        if not cls_dir.exists():
            print(f"[WARN] {split}/{cls} not found. Skipping.")
            continue
        for img in sorted(cls_dir.glob("*")):
            if img.suffix.lower() not in [".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"]:
                continue
            # 相对路径写入（和 dataset.py 常见实现兼容）
            rel_path = img.as_posix()
            label_name = cls
            label_id = class_dirs.index(cls)  # 0..C-1
            rows.append([rel_path, label_name, label_id])

    out_csv = data_dir / {
        "train": "gt_training.csv",
        "val": "gt_validation.csv",
        "test": "gt_test.csv",
    }[split]

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        # 常见三列命名（如果你的 dataset.py 列名不一样，后面我再帮你改成一致）
        w.writerow(["filepath", "label", "label_id"])
        w.writerows(rows)
    print(f"[OK] Wrote {out_csv} with {len(rows)} rows.")

for sp in splits:
    write_csv(sp)

print("\nDone. If anything breaks, tell me the expected column names in dataset.py.")
