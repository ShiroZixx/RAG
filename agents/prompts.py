GRADE_PROMPT = """
    Bạn là một chuyên gia đánh giá độ liên quan của tài liệu với câu hỏi về các loại cây trông của người dùng.

    Tài liệu được truy xuất: 
    {context}

    Câu hỏi của người dùng: {question}

    Nếu tài liệu chứa từ khóa hoặc ý nghĩa ngữ nghĩa liên quan đến câu hỏi, hãy đánh giá là có liên quan.
    Chú ý cụ thể câu hỏi liên quan đến loại cây nào tránh nhầm lẫn các loại cây
    Đưa ra điểm số nhị phân 'yes' hoặc 'no' để chỉ ra liệu tài liệu có liên quan đến câu hỏi hay không.
    """

REWRITE_PROMPT = """
    Hãy xem xét câu hỏi đầu vào và cố gắng hiểu ý định ngữ nghĩa cơ bản.

    Câu hỏi ban đầu:
    {question}

    Hãy viết lại câu hỏi để tìm kiếm hiệu quả hơn, tập trung vào:
    - Tên bệnh cụ thể trên loại cây nào
    - Triệu chứng rõ ràng
    - Loại cây trồng
    - Biện pháp phòng chống

    Câu hỏi được cải thiện:
    """

GENERATE_PROMPT = """

    - Bạn là chuyên gia về bệnh hại cây trồng (cụ thể là cây lúa hoặc cây sầu riêng) với nhiều năm kinh nghiệm.
    
    - Bạn sẽ cung cấp thông tin về cây lúa hoặc cây sầu riêng cho người dùng
    
    - Hãy trả lời câu hỏi một cách chính xác với những thông tin tham khảo
  
    - Dùng dấu gạch đầu dòng nếu có nhiều ý
    
    - Đưa thẳng thông tin không cần những câu chào không cần thiết
    
    - Hãy trả lời theo cấu trúc sau:
            1. Tên bệnh: 
            2. Triệu chứng chính:
            3. Nguyên nhân gây bệnh: 
            4. Biện pháp phòng chống:
    
    - Câu hỏi: {question}
    - Thông tin tham khảo: {context}

    Trả lời:
    """
