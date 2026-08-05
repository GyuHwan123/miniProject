# accuracy.py
from rapidfuzz.distance import Levenshtein
import json
import re
from typing import Optional
from fastapi import UploadFile

async def parse_gt_file(gt_file: Optional[UploadFile]) -> Optional[str]:
    """업로드된 TXT 또는 JSON 파일에서 Ground Truth 텍스트를 추출합니다."""
    if not gt_file:
        return None
    
    content = await gt_file.read()
    ext = gt_file.filename.split(".")[-1].lower()
    
    # 1. TXT 파일 파싱
    if ext == "txt":
        try:
            return content.decode("utf-8").strip()
        except UnicodeDecodeError:
            return content.decode("cp949", errors="ignore").strip()
            
    # 2. JSON 파일 파싱
    elif ext == "json":
        try:
            data = json.loads(content.decode("utf-8"))
            texts = []
            
            # 케이스 A: 파일 전체가 리스트 구조인 경우 [ {annotation.text: "..."}, ... ]
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        # 표준 annotation.text 키 탐색
                        if "annotation.text" in item:
                            texts.append(str(item["annotation.text"]))
                        elif "text" in item:
                            texts.append(str(item["text"]))
                            
            # 케이스 B: 딕셔너리 구조 내부에 리스트나 필드가 있는 경우
            elif isinstance(data, dict):
                # 단일 필드에 텍스트가 있는 경우
                for key in ["text", "gt", "content", "ground_truth", "annotation.text"]:
                    if key in data:
                        texts.append(str(data[key]))                
                # 내부 값들을 돌면서 리스트 형태의 바운딩 박스 데이터 탐색
                for v in data.values():
                    if isinstance(v, list):
                        for item in v:
                            if isinstance(item, dict):
                                if "annotation.text" in item:
                                    texts.append(str(item["annotation.text"]))
                                elif "text" in item:
                                    texts.append(str(item["text"]))
            
            # 흩어져 있던 텍스트 조각들을 하나의 문자열로 결합
            combined_text = "".join(texts)
            return combined_text.strip()
                   
        except Exception as e:
            print(f"JSON GT 파싱 에러: {e}")
            return None
            
    return None
def normalize_text(text: str) -> str:
    """
    OCR 출력물의 줄바꿈(\n)과 공백, 그리고 JSON 조각들의 공백 차이를 
    없애고 순수 문자열 매칭이 가능하도록 정규화합니다.
    """
    if not text:
        return ""
    # 공백, 탭, 줄바꿈 문자(\n, \r)를 모두 제거하여 순수 글자들만 비교
    return re.sub(r'\s+', '', text)

def calculate_cer_accuracy(gt_text: str, pred_text: str) -> dict:
    """Ground Truth(gt_text)와 OCR 추출결과(pred_text)를 비교하여 CER 및 정확도(%) 반환"""
    gt_clean = normalize_text(gt_text)
    pred_clean = normalize_text(pred_text)

    if not gt_clean:
        return {"accuracy_score": 1.0, "accuracy_percentage": "100.0%", "edit_distance": 0}

    # 편집 거리(틀리거나 누락된 글자 수) 산출
    distance = Levenshtein.distance(gt_clean, pred_clean)
    gt_length = len(gt_clean)
    
    cer = distance / gt_length
    accuracy = max(0.0, 1.0 - cer)

    from collections import Counter
    gt_counter = Counter(gt_clean)
    pred_counter = Counter(pred_clean)
    overlap = sum((gt_counter & pred_counter).values())
    char_match_acc = overlap / gt_length if gt_length > 0 else 0.0
    print(f"\n[EVAL DEBUG]")
    print(f"GT 글자 수: {gt_length} | PRED 글자 수: {len(pred_clean)} (차이: {gt_length - len(pred_clean)}자)")
    print(f"Accuracy (순서포함): {accuracy * 100:.2f}%")
    print(f"Char Match Accuracy (순서무관 글자포함률): {char_match_acc * 100:.2f}%\n")
    return {
        "score": round(accuracy, 4),
        "accuracy_percentage": f"{round(accuracy * 100, 2)}%",
        "edit_distance": distance,
        "gt_length": gt_length,
        "cer": round(cer, 4)
    }