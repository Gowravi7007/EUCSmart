{
  "rewrites": [
    { "source": "/(.*)", "destination": "api/api.py" }
  ]
}
from flask import Flask, request, jsonify
import hashlib
import numpy as np
from scipy.spatial import distance
import os

app = Flask(__name__)

# --- AI CONFIGURATION ---
# Note: In a serverless environment, generating this on every request is slow.
# For your hackathon demo, we'll keep it, but in production, load a pre-computed matrix.
baseline_data = np.random.normal(size=(100, 3)) 
baseline_mean = np.mean(baseline_data, axis=0)
covariance_matrix = np.cov(baseline_data, rowvar=False)
# Add a tiny bit of noise to diagonal to prevent Singular Matrix errors
inv_covariance = np.linalg.inv(covariance_matrix + np.eye(3) * 1e-6)

def calculate_anomaly_score(telemetry_vector):
    """Calculates Mahalanobis Distance for AI Anomaly Detection."""
    dist = distance.mahalanobis(telemetry_vector, baseline_mean, inv_covariance)
    return dist

# --- API ENDPOINTS ---

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "SecureChain AI API is Online"}), 200

@app.route('/api/verify-ota', methods=['POST'])
def verify_ota():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400

    firmware_binary = data.get('binary_string', '').encode()
    provided_hash = data.get('hash')
    telemetry = data.get('telemetry') 

    # 1. Integrity Check (SHA-256)
    computed_hash = hashlib.sha256(firmware_binary).hexdigest()
    if computed_hash != provided_hash:
        return jsonify({
            "status": "REJECTED", 
            "reason": "Hash Mismatch",
            "computed": computed_hash,
            "provided": provided_hash
        }), 400

    # 2. AI Anomaly Scan
    try:
        # Convert telemetry list to numpy array
        tel_array = np.array(telemetry).astype(float)
        anomaly_score = calculate_anomaly_score(tel_array)
        
        # Threshold: 3.0 is standard for Mahalanobis anomalies
        risk_level = "HIGH" if anomaly_score > 3.0 else "LOW"
        
        return jsonify({
            "status": "SUCCESS" if risk_level == "LOW" else "QUARANTINED",
            "integrity": "VERIFIED",
            "anomaly_score": round(float(anomaly_score), 4),
            "risk_level": risk_level
        })
    except Exception as e:
        return jsonify({"status": "ERROR", "reason": str(e)}), 500

# IMPORTANT: Remove app.run() for Vercel. 
# Vercel looks for the 'app' object automatically.
