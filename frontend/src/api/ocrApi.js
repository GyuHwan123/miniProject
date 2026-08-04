import api from "./axios";

export const uploadOCR = async (files) => {

    // FileUploader에서는 selectedFiles 배열을 넘겨주므로
    // 첫 번째 파일만 사용
    const file = files[0];

    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post(
        "/api/ocr/upload",
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        }
    );

    return response.data;
};