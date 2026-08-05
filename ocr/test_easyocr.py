import cv2
import easyocr

def preprocess_image(file_path):
    # 1. 이미지 읽기
    img = cv2.imread(file_path)
    
    # 2. 해상도 2배 확대 (얇은 글씨 보존)
    img_resized = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # 3. 흑백 변환
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    
    return gray

# ==========================================
# EasyOCR 초기화 및 실행
# ==========================================

# 1. Reader 객체 생성 (한국어 'ko', 영어 'en' 지원)
print("EasyOCR 모델을 불러오는 중입니다... (최초 실행 시 다운로드 소요)")
reader = easyocr.Reader(['ko', 'en'], gpu=False)

# 테스트할 이미지 경로
input_path = "test_images/3-1.jpg"  

# ==========================================
# [1] 원본 이미지 OCR 실행
# ==========================================
print("\n[1/2] 원본 이미지 OCR 분석 중...")
# EasyOCR은 이미지 파일 경로를 직접 입력받을 수도 있습니다.
original_results = reader.readtext(input_path, detail=1)

print("\n===== 원본 OCR =====")
for bbox, text, conf in original_results:
    print(f"{text} : {conf:.2f}")


# ==========================================
# [2] 전처리 이미지 OCR 실행
# ==========================================
print("\n[2/2] 전처리 이미지 생성 및 OCR 분석 중...")
processed_img = preprocess_image(input_path)
processed_results = reader.readtext(processed_img, detail=1)

print("\n===== 전처리 OCR =====")
for bbox, text, conf in processed_results:
    print(f"{text} : {conf:.2f}")