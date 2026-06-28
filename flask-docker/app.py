from flask import Flask, render_template

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/analysis")
def analysis():
    return render_template("analysis.html")


@app.route("/crawl_0050")
def crawl_0050():
    options = Options()

    # Docker 裡面 Chromium 的位置
    options.binary_location = "/usr/bin/chromium"

    # Docker / Render 環境需要這些設定
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)

    try:
        url = "https://www.wantgoo.com/stock/etf/0050/constituent"
        driver.get(url)

        # 等網頁 body 出現
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # 抓整個網頁文字
        page_text = driver.find_element(By.TAG_NAME, "body").text
        lines = page_text.splitlines()

        # 找到 ETF持股分布 這一段
        start_index = 0
        for i, line in enumerate(lines):
            if "ETF持股分布" in line:
                start_index = i
                break

        # 先抓附近 80 行資料
        etf_lines = lines[start_index:start_index + 80]

        return render_template("crawl_0050.html", etf_lines=etf_lines)

    finally:
        driver.quit()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)