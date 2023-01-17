FROM python:3.11
LABEL maintainer="Jarvis"
RUN pip install --upgrade pip
COPY requirements.txt ./
# 自行建立更新清單 不要使用快取目錄(會下載最新版本的套件)
RUN pip install --no-cache-dir -r requirements.txt