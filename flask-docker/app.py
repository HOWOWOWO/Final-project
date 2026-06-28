from flask import Flask, render_template
import requests
from datetime import datetime

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


@app.route("/etf")
def etf_menu():
    etf_items = [
        {
            "title": "歷年股利",
            "url": "/etf/dividend",
            "description": "顯示 0050 歷年配息與除息資料。"
        },
        {
            "title": "現金殖利率",
            "url": "/etf/yield",
            "description": "觀察 0050 現金股利與殖利率變化。"
        },
        {
            "title": "成分股",
            "url": "/etf/constituent",
            "description": "顯示 0050 ETF 主要持股與產業分布。"
        },
        {
            "title": "淨值及折溢價",
            "url": "/etf/premium",
            "description": "比較 0050 市價、淨值與折溢價。"
        },
        {
            "title": "基本資料",
            "url": "/etf/basic",
            "description": "介紹 0050 的基金名稱、代號、追蹤指數與交易資訊。"
        },
        {
            "title": "TWSE 0050 每日行情",
            "url": "/twse_0050",
            "description": "從證交所資料讀取 0050 的開盤價、最高價、最低價、收盤價與成交量。"
        },
        {
            "title": "Yahoo 0050 資料",
            "url": "/yahoo_0050",
            "description": "整理 Yahoo 股市中的 0050 基本資料、持股分析與成交彙整連結。"
        },
    ]

    return render_template("etf_menu.html", etf_items=etf_items)


@app.route("/twse_0050")
def twse_0050():
    stock_no = "0050"

    # 自動抓目前月份，例如 2026 年 6 月會變成 20260601
    today = datetime.today()
    query_date = today.strftime("%Y%m01")

    url = "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY"

    params = {
        "date": query_date,
        "stockNo": stock_no,
        "response": "json"
    }

    headers_request = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers_request,
            timeout=10
        )

        data = response.json()

        if data.get("stat") == "OK" and len(data.get("data", [])) > 0:
            latest = data["data"][-1]

            rows = [
                ["股票代號", stock_no],
                ["股票名稱", "元大台灣50"],
                ["日期", latest[0]],
                ["成交量", latest[1]],
                ["開盤價", latest[3]],
                ["最高價", latest[4]],
                ["最低價", latest[5]],
                ["收盤價", latest[6]],
            ]

        else:
            rows = [
                ["錯誤", "查不到 0050 的資料，可能今天還沒有交易資料。"]
            ]

    except Exception as e:
        rows = [
            ["錯誤", str(e)]
        ]

    return render_template(
        "etf_table.html",
        title="0050 每日行情資料",
        headers=["項目", "內容"],
        rows=rows
    )


@app.route("/yahoo_0050")
def yahoo_0050():
    yahoo_items = [
        {
            "title": "Yahoo 0050 基本資料",
            "url": "https://tw.stock.yahoo.com/quote/0050.TW/profile",
            "description": "查看 0050 的基金基本資料。"
        },
        {
            "title": "Yahoo 0050 持股分析",
            "url": "https://tw.stock.yahoo.com/quote/0050.TW/holding",
            "description": "查看 0050 的持股組成與比例。"
        },
        {
            "title": "Yahoo 0050 成交彙整",
            "url": "https://tw.stock.yahoo.com/quote/0050.TW/time-sales",
            "description": "查看 0050 的成交明細與即時交易資訊。"
        },
    ]

    return render_template("yahoo_0050.html", yahoo_items=yahoo_items)


@app.route("/etf/dividend")
def etf_dividend():
    rows = [
        ["2026", "1.00", "2026/01/22", "2026/02/11", "1.39%"],
        ["2025", "3.06", "2025/01、2025/07", "分兩次發放", "2.06%"],
        ["2024", "4.00", "2024/01、2024/07", "分兩次發放", "2.79%"],
        ["2023", "4.50", "2023/01、2023/07", "分兩次發放", "3.64%"],
    ]

    return render_template(
        "etf_table.html",
        title="0050 歷年股利",
        headers=["年度", "年股利", "除息日", "發放日", "年殖利率"],
        rows=rows
    )


@app.route("/etf/yield")
def etf_yield():
    rows = [
        ["2026", "1.00", "約 1.39%", "觀察中"],
        ["2025", "3.06", "約 2.06%", "股利較穩定"],
        ["2024", "4.00", "約 2.79%", "殖利率提高"],
        ["2023", "4.50", "約 3.64%", "配息表現較高"],
    ]

    return render_template(
        "etf_table.html",
        title="0050 現金殖利率",
        headers=["年度", "年股利", "年殖利率", "說明"],
        rows=rows
    )


@app.route("/etf/constituent")
def etf_constituent():
    rows = [
        ["2330", "台積電", "半導體", "約 58.26%"],
        ["2454", "聯發科", "IC 設計", "約 6.42%"],
        ["2308", "台達電", "電子零組件", "約 4.81%"],
        ["2317", "鴻海", "電子製造", "前五大成分股"],
        ["3711", "日月光投控", "半導體封測", "前五大成分股"],
    ]

    return render_template(
        "etf_table.html",
        title="0050 成分股",
        headers=["股票代號", "股票名稱", "產業類別", "持股比例"],
        rows=rows
    )


@app.route("/etf/premium")
def etf_premium():
    rows = [
        ["2026/06/26", "103.10", "102.98", "0.12", "0.12%"],
        ["2026/06/25", "107.20", "106.70", "0.50", "0.47%"],
        ["2026/06/24", "107.15", "106.26", "0.89", "0.84%"],
        ["2026/06/23", "110.10", "109.68", "0.42", "0.38%"],
    ]

    return render_template(
        "etf_table.html",
        title="0050 淨值及折溢價",
        headers=["日期", "市價", "淨值", "折溢價", "折溢價%"],
        rows=rows
    )


@app.route("/etf/basic")
def etf_basic():
    rows = [
        ["ETF 名稱", "元大台灣50"],
        ["股票代號", "0050"],
        ["追蹤指數", "臺灣50指數"],
        ["投資特色", "分散投資台灣大型權值股"],
        ["適合族群", "長期投資、穩健型投資人"],
    ]

    return render_template(
        "etf_table.html",
        title="0050 基本資料",
        headers=["項目", "內容"],
        rows=rows
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)