import re

def calculate_text_quality_score(text: str) -> float:
    """
    대용량 텍스트에서도 리스트를 생성하지 않고 빠르게 유효성 점수를 계산합니다.
    """
    if not text or not text.strip():
        return 0.0
    
    total_chars = len(text)
    
    # re.findall 대신 re.finditer와 제너레이터를 사용하여 메모리 할당 최소화
    pattern = re.compile(r'[가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9\s.,?!~\-_\(\)\[\]\'"]')
    valid_count = sum(1 for _ in pattern.finditer(text))
    
    score = valid_count / total_chars
    return round(score, 4)