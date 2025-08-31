import base64
from langchain_core.messages import HumanMessage
from models.llms import vision_model
import re

def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def analyze_plant_disease(image_path: str,  question: str = "Phân tích tên bệnh của cây trong hình"):
    """
    Phân tích hình ảnh cây để phát hiện bệnh, triệu chứng
    """

    base64_image = encode_image_to_base64(image_path)

    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": f"""
                {question}
                Hãy nhận diện loại bệnh của cây trong ảnh đầu vào theo 2 loại cây là cây lúa hoặc cây sầu riêng 
                1. Cây lúa:
                - Bệnh khô vằn ở lúa
                - Bệnh đạo ôn hại lúa 
                - Bệnh bạc lá trên lúa
                - Bệnh vàng lá ở cây lúa
                - Bệnh đốm sọc
                - Bệnh vàng lùn (lùn xoắn lá)
                
                2. Cây sầu riêng:
                - Bệnh thối trái (nấm trái)
                - Bệnh nứt thân xì mủ
                - Bệnh thán thư
                - Bệnh đốm rong
                - Bệnh nấm hồng
                - Bệnh cháy lá 
                
                Tránh nhầm lẫn giữa: bạc lá & vàng lá, đốm sọc & đạo ôn & khô vằn.
                
                Hãy trả lời theo cấu trúc :
                1. Tên loại cây (nếu xác định được) (Loại cây: )
                2. Chẩn đoán bệnh (Chẩn đoán bệnh: )
                3. Triệu chứng có trong ảnh (Triệu chứng: )

                Trả lời bằng tiếng Việt, ngắn gọn và chính xác.
                không dùng các dấu *
                           
                """

            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            }
        ]
    )

    try:
        response = vision_model.invoke([message])
        return response.content
    except Exception as e:
        return f"Lỗi khi gọi mô hình vision: {str(e)}"

def extract_disease_name(response: str) -> str:
    """
    Tìm tên bệnh từ phần trả lời của Vision model.
    """
    match = re.search(r"(?:Chẩn đoán bệnh)\s*[:\-–]\s*(.+)", response)
    if match:
        return match.group(1).strip()
    return ""
