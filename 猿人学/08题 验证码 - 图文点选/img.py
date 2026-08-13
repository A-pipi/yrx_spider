import os
import cv2, numpy as np
import pytesseract
from PIL import Image


# IMAGE_PATH = "da.jpg"

# pytesseract.pytesseract.tesseract_cmd = r"D:\Program Files\Tesseract-OCR\tesseract.exe"


def split_grid(path, save_dir, rows, cols):
    img = Image.open(path)

    w, h = img.size

    os.makedirs(save_dir, exist_ok=True)

    block_w = w // cols
    block_h = h // rows

    index = 0

    for i in range(rows):
        for j in range(cols):
            left = j * block_w
            top = i * block_h

            right = left + block_w
            bottom = top + block_h

            crop = img.crop(
                (left, top, right, bottom)
            )

            crop.save(
                f"{save_dir}/{index}.png"
            )

            index += 1


def remove_lines(binary):
    """连通域形状分析去除细长干扰线"""
    inv = cv2.bitwise_not(binary)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(inv, connectivity=8)
    h, w = binary.shape
    mask = np.full(h * w, 255, dtype=np.uint8).reshape(h, w)

    for i in range(1, n):
        area = stats[i, cv2.CC_STAT_AREA]
        cw = stats[i, cv2.CC_STAT_WIDTH]
        ch = stats[i, cv2.CC_STAT_HEIGHT]
        if cw <= 0 or ch <= 0:
            continue
        ratio = max(cw, ch) / min(cw, ch)
        fill = area / (cw * ch)
        if ratio > 12 or (ratio > 6 and fill < 0.25) or area < 8 or (fill < 0.12 and area < h * w * 0.02):
            mask[labels == i] = 0

    return cv2.bitwise_not(cv2.bitwise_and(inv, inv, mask=mask))


def recognize(path):
    """预处理 → 去线 → Tesseract多模式投票 → 输出结果"""
    # 读取
    img = cv2.imread(path)
    if img is None:
        print(f"❌ 找不到图片: {path}")
        return
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 小图放大
    h, w = gray.shape
    if h < 64:
        s = 64 / h
        gray = cv2.resize(gray, (max(int(w * s), 24), 64), interpolation=cv2.INTER_CUBIC)

    # 去噪 + 增强
    gray = cv2.bilateralFilter(gray, 5, 16, 16)
    gray = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray)

    # 二值化（OTSU + 自适应兜底）
    t, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    if t < 60:
        bs = max(9, min(h, w) // 6) | 1
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, bs, 4)

    # 去干扰线
    binary = remove_lines(binary)

    # 笔画修复
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, k)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, k)

    # 裁剪文字区域
    pts = cv2.findNonZero(cv2.bitwise_not(binary))
    if pts is not None:
        x, y, rw, rh = cv2.boundingRect(pts)
        x = max(x - 6, 0)
        y = max(y - 6, 0)
        x2 = min(x + rw + 12, binary.shape[1])
        y2 = min(y + rh + 12, binary.shape[0])
        binary = binary[y:y2, x:x2]

    # 等比缩放到标准高度
    ch, cw = binary.shape
    if ch > 0 and cw > 0:
        scale = min(64 / ch, 4.0)
        binary = cv2.resize(binary, (max(int(cw * scale), 16), int(ch * scale)),
                            interpolation=cv2.INTER_CUBIC)
    binary = cv2.copyMakeBorder(binary, 12, 12, 12, 12, cv2.BORDER_CONSTANT, value=255)

    # 多 PSM 识别 + 投票
    candidates = []
    for psm in ["10", "8", "7", "6"]:
        try:
            data = pytesseract.image_to_data(binary, lang="chi_sim",
                                             config=f"--psm {psm}",
                                             output_type=pytesseract.Output.DICT)
            for i, txt in enumerate(data["text"]):
                txt = txt.strip()
                if txt and len(txt) <= 4:
                    conf = float(data["conf"][i]) / 100.0 if data["conf"][i] != "-1" else 0.0
                    if conf > 0.05:
                        candidates.append({"text": txt, "confidence": conf})
        except Exception:
            pass

    if not candidates:
        print("⚠️ 未识别到文字")
        return

    # 多PSM一致加权
    from collections import Counter
    mc, n = Counter(c["text"] for c in candidates).most_common(1)[0]
    if n >= 2:
        for c in candidates:
            if c["text"] == mc:
                c["confidence"] = min(c["confidence"] + 0.20, 1.0)

    # 排序取最佳
    candidates.sort(key=lambda x: x["confidence"], reverse=True)
    best = candidates[0]

    return best["text"]


def main():
    arr = []
    split_grid("img.webp","tu",3,3)
    for file in os.listdir("tu"):
        txt = recognize(f"./tu/{file}")
        arr.append({str(file.split(".")[0]): txt})

    return arr

if __name__ == "__main__":
    arr = main()
    print(arr)
