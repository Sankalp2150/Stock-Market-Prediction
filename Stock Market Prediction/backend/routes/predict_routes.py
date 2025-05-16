from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from controllers.predict_controller import predict_price
from ml_model.predict import load_model_and_predict, get_historical_comparison_data
import math

# Define a Blueprint for prediction routes
predict_bp = Blueprint("predict_bp", __name__)

@predict_bp.route("/predict", methods=["POST"])
@cross_origin()
def predict():
    """
    Handle POST requests to predict stock prices based on the provided symbol.
    Expects JSON data with a 'symbol' key.
    Returns JSON response with prediction results or error messages.
    """
    data = request.get_json()
    symbol = data.get("symbol")

    if not symbol:
        return jsonify({
            "status": "error",
            "message": "Symbol is required"
        }), 400

    try:
        result = predict_price(symbol)

        # Check if prediction returned an error
        if "error" in result:
            return jsonify({
                "status": "error",
                "message": result["error"]
            }), 500

        historical_data = get_historical_comparison_data(symbol)

        return jsonify({
            "status": "success",
            "symbol": symbol,
            "predicted_price": round(float(result["predicted_price"]), 2),
            "accuracy": round(float(result["accuracy"]), 2) if result["accuracy"] and not math.isnan(result["accuracy"]) else 0.0,
            "chart": historical_data
        })

    except Exception as e:
        print(f"[ERROR] Prediction failed for symbol '{symbol}': {e}")
        return jsonify({
            "status": "error",
            "message": f"Prediction failed: {str(e)}"
        }), 500