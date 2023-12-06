FROM python:3.10-slim

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

COPY ./apps ./apps
COPY ["./requirements.txt","./"]
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

CMD ["python", "apps/main.py"]