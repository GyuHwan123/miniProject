import cv2
import numpy as np


def preprocess_image(file_path):

    # 이미지 읽기
    img = cv2.imread(file_path)

    # 크기 확대
    img = cv2.resize(
        img,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    # 흑백 변환
    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )


    # 밝은 이미지 어둡게 (감마)
    gamma = 2.5

    table = np.array([
        ((i / 255.0) ** gamma) * 255
        for i in np.arange(256)
    ]).astype("uint8")

    gamma_img = cv2.LUT(
        gray,
        table
    )


    # 대비 강화
    clahe = cv2.createCLAHE(
        clipLimit=3.0,
        tileGridSize=(8,8)
    )

    contrast = clahe.apply(
        gamma_img
    )


    # 노이즈 제거
    denoise = cv2.fastNlMeansDenoising(
        contrast
    )



    # 이진화
    binary = cv2.threshold(
        denoise,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    kernel = np.array([
        [-1,-1,-1],
        [-1, 9,-1],
        [-1,-1,-1]
    ])

    sharp = cv2.filter2D(
        denoise,
        -1,
        kernel
    )

    # 글자 끊김 보완
    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (2,2)
    )

    closed = cv2.morphologyEx(
        binary,
        cv2.MORPH_CLOSE,
        kernel
    )

    # 글자 획 굵게 (Dilation)
    dilated = cv2.dilate(
        closed,
        kernel,
        iterations=2
    )


    return dilated