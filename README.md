# 411170337 賴昱豪
# 411170375 侯冠宇
# 412170566 莊哲瑋
# 410170562 吳秉謙

# 衛教查詢系統 - Flask 專案說明文件

本專案為小組期末專題之最小可行性產品 (MVP)，使用 Flask 框架開發，並透過 Docker 進行環境管理，確保專案可以在不同電腦上快速重現。

## 專題主題說明
* **主題名稱**：衛教查詢系統
* **簡單描述**：提供使用者便捷的醫療與健康教育資訊查詢介面，協助推廣健康知識。

---

## 環境開發工具
* **虛擬環境管理**：Docker / Docker Compose
* **後端框架**：Flask
* **前端樣板**：Jinja2 (HTML/CSS)

---

## 專案啟動步驟

請確保您的電腦已安裝 [Docker](https://www.docker.com/products/docker-desktop/) 與 Docker Compose。

### 1. 啟動 Docker 容器
在專案根目錄（包含 `docker-compose.yml` 的資料夾）開啟終端機 (Terminal/CMD)，輸入以下指令：

```bash
docker-compose up --build
