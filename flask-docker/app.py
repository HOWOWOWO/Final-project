from flask import Flask, render_template

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
    etf_lines = [
        "0050 ETF 持股分布示範資料",
        "資料來源：公開資料整理 / 專題展示用",
        "",
        "股票代號    股票名稱    說明",
        "2330        台積電      台灣大型半導體公司",
        "2317        鴻海        電子製造服務公司",
        "2454        聯發科      IC 設計公司",
        "2308        台達電      電源與電子零組件公司",
        "2412        中華電      電信服務公司",
        "2881        富邦金      金融控股公司",
        "2882        國泰金      金融控股公司",
        "2303        聯電        半導體晶圓代工公司",
        "2891        中信金      金融控股公司",
        "3711        日月光投控  半導體封測公司",
    ]

    return render_template("crawl_0050.html", etf_lines=etf_lines)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)