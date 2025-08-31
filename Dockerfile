FROM python:3.12
LABEL authors="Thang"

WORKDIR /src

COPY tools /src/tools
COPY vision /src/vision
COPY graph /src/graph
COPY Agents /src/Agents
COPY test.py /src/main.py
COPY server.py /src/server.py
COPY requirements.txt /src/requirements.txt

EXPOSE 8888

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8888"]