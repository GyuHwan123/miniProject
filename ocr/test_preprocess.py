import cv2
from preprocess import preprocess_image


input_path = "test_images/3-1.jpg"

output = preprocess_image(input_path)


cv2.imwrite(
    "processed_student.png",
    output
)

print("전처리 완료")