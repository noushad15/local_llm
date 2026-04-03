FROM python:3.11-slim

WORKDIR /local_llm

COPY ../requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ../backend ./backend
COPY ../data ./data
COPY ../scripts ./scripts

CMD ["bash"]
