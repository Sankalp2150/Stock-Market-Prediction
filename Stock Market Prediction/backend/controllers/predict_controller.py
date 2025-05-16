import os
import sys

# Ensure predict.py from ml_model can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml_model'))

from predict import load_model_and_predict

def predict_price(symbol):
    try:
        result = load_model_and_predict(symbol)
        return result
    except Exception as e:
        # Return an error dictionary for the route to handle gracefully
        return {"error": str(e)}