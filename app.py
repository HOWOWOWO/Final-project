from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from models import db, ETF0050
from dotenv import load_dotenv
import os

import requests

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


app = Flask(__name__)


# 基本資料 (Basic Info) - 通常只有一筆或很少變動
class ETFBasicInfo(db.Model):
    __tablename__ = 'etf_basic_info'
    id = db.Column(db.Integer, primary_key=True)
    etf_code = db.Column(db.String(10), unique=True, nullable=False)  # 0050
    etf_name = db.Column(db.String(50), nullable=False)               # 元大台灣50
    fund_size = db.Column(db.Float)                                   # 基金規模
    listing_date = db.Column(db.Date)                                 # 上市日期

# 持股分析 (Holdings) - 一個日期會對應多個成分股 (如 50 檔)
class ETFHoldings(db.Model):
    __tablename__ = 'etf_holdings'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)                         # 資料日期
    stock_code = db.Column(db.String(10), nullable=False)             # 成分股代號 
    stock_name = db.Column(db.String(50), nullable=False)             # 成分股名稱 
    weight = db.Column(db.Float, nullable=False)                      # 持股權重 (%)

# 成交彙整 (Daily Transactions) - 每日一筆行情
class ETFTransactionSummary(db.Model):
    __tablename__ = 'etf_transaction_summary'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)            # 日期
    open_price = db.Column(db.Float)                                  # 開盤價
    high_price = db.Column(db.Float)                                  # 最高價
    low_price = db.Column(db.Float)                                   # 最低價
    close_price = db.Column(db.Float)                                 # 收盤價
    volume = db.Column(db.BigInteger)                                 # 成交量

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    # 撈取最新一筆成交行情作為首頁摘要
    latest_trade = ETFTransactionSummary.query.order_by(ETFTransactionSummary.date.desc()).first()
    basic_info = ETFBasicInfo.query.filter_by(etf_code='0050').first()
    return render_template("home.html", latest_trade=latest_trade, basic_info=basic_info)


@app.route("/html_tags")
def html_tags():
    return render_template("html_tags.html")


@app.route("/charts")
def charts():
    # 撈取最新 30 筆歷史紀錄供下方的表格呈現
    records = ETFTransactionSummary.query.order_by(ETFTransactionSummary.date.desc()).limit(30).all()
    return render_template("charts.html", records=records)
    

@app.route("/analysis")
def analysis():
    basic_info = ETFBasicInfo.query.filter_by(etf_code='0050').first()
    # 找出最新日期的持股明細
    latest_date = db.session.query(db.func.max(ETFHoldings.date)).scalar()
    holdings = []
    if latest_date:
        holdings = ETFHoldings.query.filter_by(date=latest_date).order_by(ETFHoldings.weight.desc()).all()
    
    return render_template("analysis.html", basic_info=basic_info, holdings=holdings, date=latest_date)

@app.route("/admin")
def admin():
    # 統計基本資料筆數
    basic_status = ETFBasicInfo.query.count()
    
    # 撈取持股分析最新一筆的日期
    latest_holding = db.session.query(db.func.max(ETFHoldings.date)).scalar()
    latest_holding_date = latest_holding.strftime('%Y-%m-%d') if latest_holding else None
    
    # 撈取成交彙整最新一筆的日期
    latest_trade = db.session.query(db.func.max(ETFTransactionSummary.date)).scalar()
    latest_trade_date = latest_trade.strftime('%Y-%m-%d') if latest_trade else None
    
    return render_template(
        "admin.html", 
        basic_status=basic_status, 
        latest_holding_date=latest_holding_date, 
        latest_trade_date=latest_trade_date
    )

@app.route("/api/chart-data")
def chart_data():
    # 提供給 Chart.js 畫圖用的歷史行情數據
    data = ETFTransactionSummary.query.order_by(ETFTransactionSummary.date.asc()).all()
    return jsonify({
        "dates": [r.date.strftime('%Y-%m-%d') for r in data],
        "prices": [r.close_price for r in data],
        "volumes": [r.volume for r in data]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)