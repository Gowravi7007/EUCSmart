from flask import Flask, request, jsonify
import hashlib
import numpy as np
from scipy.spatial import distance
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

app = Flask(__name__)

# --- AI CONFIGURATION ---
# Example baseline telemetry (e.g., normal speed, engine temp, sensor data)
# In production, load this from your pre-trained dataset
baseline_data = np.random.normal(size=(100, 3)) 
baseline_mean = np.mean(baseline_data, axis=0)
covariance_matrix = np.cov(baseline_data, rowvar=False)
inv_covariance = np.linalg.inv(covariance_matrix)

def calculate_anomaly_score(telemetry_vector):
    """Calculates Mahalanobis Distance for AI Anomaly Detection."""
    dist = distance.mahalanobis(telemetry_vector, baseline_mean, inv_covariance)
    return dist

# --- API ENDPOINTS ---

@app.route('/verify-ota', methods=['POST'])
def verify_ota():
    """
    Verifies firmware integrity (SHA-256) and performs AI Anomaly Scan.
    """
    data = request.get_json()
    
    firmware_binary = data.get('binary_string', '').encode()
    provided_hash = data.get('hash')
    telemetry = data.get('telemetry') # Expecting a list/vector of sensor data

    # 1. Integrity Check (SHA-256)
    computed_hash = hashlib.sha256(firmware_binary).hexdigest()
    if computed_hash != provided_hash:
        return jsonify({"status": "REJECTED", "reason": "Hash Mismatch"}), 400

    # 2. AI Anomaly Scan
    try:
        anomaly_score = calculate_anomaly_score(np.array(telemetry))
        # Threshold for anomaly (example: 3.0)
        risk_level = "HIGH" if anomaly_score > 3.0 else "LOW"
    except Exception as e:
        return jsonify({"status": "ERROR", "reason": str(e)}), 500

    return jsonify({
        "status": "SUCCESS" if risk_level == "LOW" else "QUARANTINED",
        "integrity": "VERIFIED",
        "anomaly_score": round(anomaly_score, 4),
        "risk_level": risk_level
    })

if __name__ == '__main__':
    # Ensure this port matches your Node.js orchestrator configuration
    app.run(port=5000, debug=True)
