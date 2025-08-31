from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState

from models.llms import response_model

from tools.retriever import create_retriever_tool_from_docs
from tools.crawl import crawl_data
from tools.preprocess import clean_text, splitter


urls = [
    "https://nongnghiepsofa.com/7-loai-benh-hai-tren-cay-lua/",
    "https://daithanhtech.com/top-5-cac-loai-benh-o-cay-lua-va-cach-phong-tru-hieu-qua-nam-2024/",
    "https://taydojsc.com.vn/benh-vi-khuan-tren-lua/",

    "https://nongnghiepsofa.com/cac-loai-benh-do-nam-gay-ra-tren-cay-sau-rieng/",
    "https://tincay.com/6-benh-thuong-gap-tren-cay-sau-rieng/",
    "https://taydojsc.com.vn/cach-dieu-tri-benh-dom-rong-tren-cay-sau-rieng/"

]

# Crawl
docs = crawl_data(urls)
print(f"Đã crawl {len(docs)} trang")

# Clean
cleaned_docs = clean_text(docs)

# Split
chunks = splitter(cleaned_docs)
print(f"Đã tạo {len(chunks)} chunk")

# Create retriever tool
retriever_tool_instance = create_retriever_tool_from_docs(chunks)


def generate_query_or_respond(state: MessagesState):
    """Call the model to generate a response based on the current state. Given
    the question, it will decide to retrieve using the retriever tool, or simply respond to the user.
    """

    # Thêm system message mạnh mẽ hơn
    system_prompt = """Bạn là một chuyên gia tư vấn nông nghiệp. Khi người dùng hỏi về:
    - Bệnh cây trồng (lúa, ngô, rau củ...)
    - Sâu bệnh hại
    - Phương pháp phòng trừ
    - Kỹ thuật canh tác
    - Giống cây trồng
    - Bất kỳ câu hỏi nông nghiệp nào

    BẮT BUỘC phải sử dụng retriever tool để tìm kiếm thông tin chính xác từ cơ sở dữ liệu trước khi trả lời.

    CHỈ trả lời trực tiếp khi:
    - Người dùng chào hỏi
    - Câu hỏi không liên quan đến nông nghiệp
    - Người dùng cảm ơn

    Với câu hỏi "một số loại bệnh ở cây lúa" - PHẢI sử dụng tool để tìm kiếm."""

    messages = [SystemMessage(content=system_prompt)] + state["messages"]

    response = (
        response_model
        .bind_tools([retriever_tool_instance])
        .invoke(messages)
    )
    return {"messages": [response]}
