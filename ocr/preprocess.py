import cv2
import numpy as np


def preprocess_image(file_path):

    # 이미지 읽기
    img = cv2.imread(file_path)

    # 크기 확대
    img = cv2.resize(
        img,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    # 흑백 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(
        clipLimit=3.0,
        tileGridSize=(8, 8)
    )

    contrast = clahe.apply(gray)

    # 노이즈 제거
    denoise = cv2.fastNlMeansDenoising(
        gray
    )

    # 이진화
    binary = cv2.threshold(
        denoise,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    return binary