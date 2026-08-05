import cv2
import numpy as np

def preprocess_image(file_path):
    # 1. 이미지 읽기
    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2. 텍스트 덩어리 영역 추출을 위한 임시 이진화
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # 픽셀 좌표 모으기 및 최소 면적 사각형 계산
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    
    # OpenCV 버전에 따른 각도 정규화 (-45도 ~ 45도 사이로 맞춤)
    if angle > 45:
        angle = angle - 90
    elif angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
        
    # 3. ⭐️ 스마트 기울기 보정 (핵심 안전장치)
    # 각도가 0.5도 ~ 15도 사이일 때만 '삐뚤어지게 찍힌 사진'으로 간주하고 회전
    if 0.5 < abs(angle) < 15:
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        img = cv2.warpAffine(
            img, M, (w, h), 
            flags=cv2.INTER_CUBIC, 
            borderMode=cv2.BORDER_REPLICATE
        )

    # 4. 해상도 2배 확대 (작은 글씨와 표 실선 보존)
    img_resized = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # 5. 최종 흑백화
    final_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

    
    
    return final_gray