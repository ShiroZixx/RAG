import re

from langchain_core.messages import BaseMessage
import os
from graph.workflow import graph
from vision.vision_analyzer import analyze_plant_disease, extract_disease_name


def clean_and_split(text: str) -> list:

    lines = []
    for line in text.strip().split("\n"):
        line = re.sub(r"^[\s\-–•]+", "", line).strip()
        if line:
            lines.append(line)

    if len(lines) == 1 and ("." in lines[0] or ";" in lines[0]):
        sentence_parts = re.split(r"[.;]\s*", lines[0])
        lines = [s.strip() for s in sentence_parts if s.strip()]

    return lines


def parse_structured_disease_info(text: str) -> dict:
    result = {
        "name": "",
        "symptoms": [],
        "description": [],
        "treatment": []
    }

    name_match = re.search(r"1\.\s*Tên bệnh\s*:\s*(.+?)\n", text)
    symptoms_match = re.search(r"2\.\s*Triệu chứng chính\s*:\s*((?:.|\n)+?)\n3\.", text)
    description_match = re.search(r"3\.\s*Nguyên nhân gây bệnh\s*:\s*((?:.|\n)+?)\n4\.", text)
    treatment_match = re.search(r"4\.\s*Biện pháp phòng chống\s*:\s*((?:.|\n)+)", text)

    if name_match:
        result["name"] = name_match.group(1).strip()

    if symptoms_match:
        result["symptoms"] = clean_and_split(symptoms_match.group(1))

    if description_match:
        result["description"] = clean_and_split(description_match.group(1))

    if treatment_match:
        result["treatment"] = clean_and_split(treatment_match.group(1))

    return result

def main(user_input: str):
    print("CHẨN ĐOÁN & TRA CỨU BỆNH CÂY\n")
    user_input = user_input

    if os.path.exists(user_input) and user_input.lower().endswith((".jpg", ".png", ".jpeg")):
        # Trường hợp người dùng nhập ảnh
        print("Phân tích ảnh bằng mô hình Gemini Vision...")
        vision_response = analyze_plant_disease(user_input, 'trieu_chung.txt')
        print("Phân tích từ ảnh:")
        print(vision_response)

        # Trích tên bệnh từ phản hồi của vlm
        disease_name = extract_disease_name(vision_response)

        if not disease_name:
            print("\n Không nhận diện được tên bệnh từ ảnh.")
            return

        print(f"\n Truy vấn thông tin về bệnh: {disease_name}")
        question = f"{disease_name} là gì và cách điều trị?"

    else:
        # Trường hợp người dùng nhập văn bản
        question = user_input

    full_answer = ""
    # Gửi vào Agentic RAG workflow
    for chunk in graph.stream({"messages": [{"role": "user", "content": question}]}):
        for node, update in chunk.items():
            print(f"\n🔁 Node: {node}")
            message = update["messages"][-1]
            if isinstance(message, BaseMessage):
                full_answer += message.content + "\n"
            else:
                full_answer += str(message) + "\n"

    disease_info = parse_structured_disease_info(full_answer)

    return disease_info






