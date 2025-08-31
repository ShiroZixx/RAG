import streamlit as st
import tempfile

from langchain_core.messages import BaseMessage

from graph.workflow import graph
from vision.vision_analyzer import analyze_plant_disease, extract_disease_name


st.set_page_config(page_title="Chẩn đoán bệnh cây", layout="centered")
st.title("🌾 CHẨN ĐOÁN & TRA CỨU BỆNH CÂY")

tab1, tab2 = st.tabs(["Nhập câu hỏi", "Tải ảnh cây"])

final_question = None

with tab1:
    user_question = st.text_area("Bạn muốn hỏi gì?", placeholder="Ví dụ: Bệnh đạo ôn ở lúa là gì và cách chữa?")
    if st.button("Tra cứu", key="text_query"):
        if user_question.strip():
            final_question = user_question.strip()
        else:
            st.warning("Vui lòng nhập câu hỏi.")

with tab2:
    uploaded_file = st.file_uploader("Tải lên ảnh cây", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Ảnh bạn đã chọn", use_container_width=True)

        if st.button("Phân tích ảnh"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_path = temp_file.name

            with st.spinner("Đang phân tích ảnh..."):
                response = analyze_plant_disease(temp_path)
                st.success("Kết quả phân tích:")
                st.write(response)

                disease_name = extract_disease_name(response)
                if disease_name:
                    st.info(f"Tên bệnh được nhận diện: **{disease_name}**")
                    final_question = f"{disease_name} là gì và cách điều trị?"
                else:
                    st.warning("Không trích được tên bệnh rõ ràng từ ảnh.")

if final_question:
    with st.spinner("Đang truy vấn thông tin..."):
        try:
            for chunk in graph.stream({"messages": [{"role": "user", "content": final_question}]}):
                for node, update in chunk.items():
                    message = update["messages"][-1]
                    print(f"\n Node: {node}")

            st.success("Kết quả tra cứu:")
            if isinstance(message, BaseMessage):
                st.write(message.content)
            else:
                st.write(message)

        except Exception as e:
            st.error(f" Lỗi khi gọi hệ thống RAG: {str(e)}")
else:
    st.info(" Nhập câu hỏi hoặc tải ảnh để tra cứu bệnh cây.")
