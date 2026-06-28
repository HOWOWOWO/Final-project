# 以 Python 3.11 的輕量版映像檔作為基底
FROM python:3.11-slim

# 把容器內的工作目錄設成 /app
WORKDIR /app

# 安裝 Selenium 需要的 Chromium 瀏覽器與驅動
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# 把 requirements.txt 複製到容器裡
COPY requirements.txt .

# 安裝 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 把目前專案資料夾裡的內容全部複製進容器
COPY . .

# 容器啟動後，自動執行 python app.py
CMD ["python", "app.py"]