# 📈 Stock Market Prediction Web App

This is a full-stack web application that predicts the next-day closing price of major **stocks** using machine learning (Random Forest). It features a sleek modern frontend with a live prediction UI and a Flask-based backend trained on historical data.

---

## 🚀 Features

- ✅ Predict next-day closing price for top stocks like AAPL, MSFT, GOOGL, AMZN, and TSLA
- ✅ Dual API fallback: uses `yfinance` first, then `Alpha Vantage` if needed
- ✅ Trains and serves ML models using Random Forest Regressor
- ✅ Displays predicted price and model accuracy
- ✅ Interactive prediction page with Chart.js graphs
- ✅ Frontend built with glassmorphism UI in HTML/CSS/JS
- ✅ Modular backend using Flask Blueprints and Controllers

---

## 🧠 Tech Stack

| Layer      | Technologies |
|------------|--------------|
| Frontend   | HTML, CSS, JavaScript, Chart.js |
| Backend    | Python, Flask, Flask-CORS       |
| ML Models  | Scikit-learn, RandomForest, joblib |
| Data APIs  | Yahoo Finance (via yfinance), Alpha Vantage |
| Dev Tools  | VS Code, Live Server, Postman (optional) |

---

## 📁 Project Structure

```
Stock Market Prediction/
│
├── backend/
│   ├── app.py
│   ├── controllers/
│   │   └── predict_controller.py
│   ├── routes/
│   │   └── predict_routes.py
│   ├── utils/
│   │   ├── data_fetch.py
│   │   └── __init__.py
│   ├── ml_model/
│   │   ├── train_model.py
│   │   ├── predict.py
│   │   ├── models/
│   │   │   ├── AAPL_model.pkl
│   │   │   └── AAPL_scaler.pkl
│
├── frontend/
│   ├── index.html
│   ├── predict.html
│   ├── about.html
│   ├── contact.html
│   ├── style.css
│   └── stock.js
│
└── README.md
```

---

## 🔢 Model Training & Accuracy

- Features used: `Close`, `High-Low`, `SMA_5`, `EMA_20`, `RSI`
- Model: `RandomForestRegressor`
- Accuracy metric: `R² Score` printed during training
- Training data span: ~10 years from Yahoo Finance or Alpha Vantage

---

## ⚙️ How to Run the Project

### 1. Clone the Repo & Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` not available, manually install:

```bash
pip install flask flask-cors yfinance alpha_vantage scikit-learn pandas numpy joblib
```

### 2. Add Your API Key

Open `backend/utils/data_fetch.py` and paste your Alpha Vantage API key:

```python
ALPHA_VANTAGE_API_KEY = 'YOUR_API_KEY'
```

### 3. Train Models

```bash
cd backend
python3 -m ml_model.train_model
```

### 4. Start Flask API Server

```bash
cd backend
python3 app.py
```

### 5. Open Frontend in Browser

Use Live Server on `predict.html` or simply open in browser.

---

## 💬 Sample Prediction Output

```json
{
  "symbol": "AAPL",
  "predicted_price": 213.33,
  "accuracy": 99.88,
  "status": "success"
}
```

---

## 📬 Contact & Credits

- 💻 Developed by: Sankalp Rana
- 🌐 GitHub: [github.com/sankalprana](https://github.com/sankalprana)
- 📍 University: Chitkara, India

---

## 📦 Notes

- Do **not** commit `.pkl` files or API keys to GitHub
- Always retrain the model after major feature or data changes