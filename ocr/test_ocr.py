from paddleocr import PaddleOCR
from preprocess import preprocess_image
import cv2


ocr = PaddleOCR(
    lang="korean",
    use_angle_cls=True
)


input_path = "test_images/3-3.jpg"


# =====================
# 1. 원본 이미지 OCR
# =====================

print("\n===== 원본 OCR =====")

original_result = ocr.ocr(input_path)


for line in original_result:
    for item in line:
        text = item[1][0]
        score = item[1][1]

        print(text, ":", round(score, 2))


# =====================
# 2. 전처리 이미지 OCR
# =====================

print("\n===== 전처리 OCR =====")


processed = preprocess_image(input_path)


# 임시 저장
cv2.imwrite(
    "processed.png",
    processed
)


processed_result = ocr.ocr(
    "processed.png"
)


for line in processed_result:
    for item in line:
        text = item[1][0]
        score = item[1][1]

        print(text, ":", round(score, 2))