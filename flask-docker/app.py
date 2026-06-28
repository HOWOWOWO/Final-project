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


class ETF0050(db.model):
    __tablename__ = 'etf_0050_daily'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)       # 日期
    close_price = db.Column(db.Float, nullable=False)            # 收盤價
    net_value = db.Column(db.Float, nullable=False)              # 淨值
    discount_premium = db.Column(db.Float, nullable=False)       # 折溢價百分比 (%)
    dividend = db.Column(db.Float, default=0.0)                  # 當期股利 (若當天沒發則為0)
    yield_rate = db.Column(db.Float, default=0.0)                # 現金殖利率 (%)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    records = ETF0050.query.order_by(ETF0050.date.desc()).limit(30).all()          # 撈取最新 30 筆歷史資料給前端表格呈現
    return render_template("home.html")

@app.route("/html_tags")
def html_tags():
    return render_template("html_tags.html")

@app.route("/charts")
def charts():
    data = ETF0050.query.order_by(ETF0050.date.asc()).all()
    
    return jsonify({
        "dates": [r.date.strftime('%Y-%m-%d') for r in data],
        "prices": [r.close_price for r in data],
        "net_values": [r.net_value for r in data],
        "discount_premiums": [r.discount_premium for r in data]
    })


@app.route("/analysis")
def analysis():
    return 

    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)