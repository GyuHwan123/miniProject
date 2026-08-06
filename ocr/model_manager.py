# model_manager.py
import os
os.environ["FLAGS_allocator_strategy"] = "naive_best_fit"
os.environ["FLAGS_fraction_of_gpu_memory_to_use"] = "0.3"

import numpy as np
from paddleocr import PaddleOCR
import easyocr

class ModelManager:
    _paddle_engine = None
    _easy_engine = None

    @classmethod
    def get_paddle(cls):
        if cls._paddle_engine is None:
            cls._paddle_engine = PaddleOCR(
                use_angle_cls=True,
                lang="korean",
                det_limit_side_len=1280,
                det_db_unclip_ratio=1.8,
                use_gpu=True,
                show_log=False,
                enable_mkldnn=False
            )
            # Warm-up
            dummy = np.zeros((100, 100, 3), dtype=np.uint8)
            cls._paddle_engine.ocr(dummy, cls=True)
            print("=== PaddleOCR Loaded & Warmed up ===")
        return cls._paddle_engine

    @classmethod
    def get_easyocr(cls):
        if cls._easy_engine is None:
            # EasyOCR 인스턴스 1회만 생성
            cls._easy_engine = easyocr.Reader(['ko', 'en'], gpu=True)
            # Warm-up
            dummy = np.zeros((100, 100, 3), dtype=np.uint8)
            cls._easy_engine.readtext(dummy)
            print("=== EasyOCR Loaded & Warmed up ===")
        return cls._easy_engine