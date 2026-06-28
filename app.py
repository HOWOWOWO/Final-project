from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

import requests
import pandas as pd

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ==================== ORM Models ====================

class ETFBasicInfo(db.Model):
    __tablename__ = 'etf_basic_info'
    id = db.Column(db.Integer, primary_key=True)
    etf_code = db.Column(db.String(10), unique=True, nullable=False)
    etf_name = db.Column(db.String(50), nullable=False)
    fund_size = db.Column(db.Float)
    listing_date = db.Column(db.Date)

class ETFHoldings(db.Model):
    __tablename__ = 'etf_holdings'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    stock_code = db.Column(db.String(10), nullable=False)
    stock_name = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Float, nullable=False)

class ETFTransactionSummary(db.Model):
    __tablename__ = 'etf_transaction_summary'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)
    open_price = db.Column(db.Float)
    high_price = db.Column(db.Float)
    low_price = db.Column(db.Float)
    close_price = db.Column(db.Float)
    volume = db.Column(db.BigInteger)

with app.app_context():
    db.create_all()

# ==================== Routes ====================

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/time-sales")
def get_time_sales_api():
    url = "https://query1.finance.yahoo.com/v8/finance/chart/0050.TW"
    params = {
        "range": "1d",
        "interval": "1m", # 獲取每分鐘的 Tick 彙整
        "includeTimestamps": "true"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            return jsonify({"status": "error", "message": "無法取得 Yahoo 資料"}), response.status_code
            
        data = response.json()
        result = data['chart']['result'][0]
        timestamps = result.get('timestamp', [])
        indicators = result['indicators']['quote'][0]
        
        # 取得前一日收盤價 (用來計算當前 Tick 的漲跌)
        meta = result.get('meta', {})
        previous_close = meta.get('chartPreviousClose', 0)

        data_list = []
        for i in range(len(timestamps)):
            close_price = indicators['close'][i]
            volume = indicators['volume'][i]
            
            # 排除無效交易點
            if close_price is None:
                continue
                
            # 1. 時間格式化 (時:分)
            t_str = pd.to_datetime(timestamps[i], unit='s').tz_localize('UTC').tz_convert('Asia/Taipei').strftime('%H:%M')
            
            # 2. 計算漲跌
            change = round(close_price - previous_close, 2)
            if change > 0:
                change_str = f"▲ {change}"
                direction = "up"
            elif change < 0:
                change_str = f"▼ {abs(change)}"
                direction = "down"
            else:
                change_str = "0.00"
                direction = "stay"
                
            # 3. 換算成台股習慣的「張數」 (Yahoo 原始資料是股數，除以 1000 變張數)
            sheets = int(volume / 1000) if volume else 0

            data_list.append({
                "time": t_str,
                "price": round(close_price, 2),
                "change": change_str,
                "direction": direction, # 供前端判斷顏色
                "sheets": sheets
            })

        # 最新時間排在最上面
        data_list.reverse()
        return jsonify({"status": "success", "data": data_list})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/charts")
def charts():
    return render_template("charts.html")

@app.route("/analysis")
def analysis():
    return render_template("analysis.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)