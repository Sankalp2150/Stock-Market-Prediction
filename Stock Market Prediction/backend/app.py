from flask import Flask, jsonify
from flask_cors import CORS
from routes.predict_routes import predict_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Register blueprint
app.register_blueprint(predict_bp)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Stock Market Prediction API is running."})

if __name__ == "__main__":
    app.run(debug=True)