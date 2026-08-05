# model_manager.py
import gc
import torch
import easyocr
from paddleocr import PaddleOCR

_current_model_type = None
_current_model_instance = None

def get_ocr_engine(model_type: str):
    global _current_model_type, _current_model_instance
    
    # 1. 이미 메모리에 올려둔 모델이 동일하면 재사용 (0초 소요, 속도 극대화)
    if _current_model_type == model_type and _current_model_instance is not None:
        return _current_model_instance
        
    # 2. 다른 모델이 메모리에 있으면 이전 모델만 정교하게 해제
    if _current_model_instance is not None:
        del _current_model_instance
        _current_model_instance = None
        _current_model_type = None
        
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    # 3. 신규 모델 할당 및 상주
    if model_type == "easyocr":
        _current_model_instance = easyocr.Reader(['ko', 'en'], gpu=True)
    elif model_type == "paddleocr":
        _current_model_instance = PaddleOCR(use_angle_cls=True, lang='korean', use_gpu=True)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    _current_model_type = model_type
    return _current_model_instance