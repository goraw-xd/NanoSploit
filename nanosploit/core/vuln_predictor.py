"""
vuln_predictor.py
ML model for predicting future vulnerabilities in IoT/embedded devices.
"""

import os
import json
import logging
from typing import List, Dict, Any

try:
    import joblib
    import numpy as np
except ImportError:
    joblib = None
    np = None
    logging.warning("ML libraries not installed. VulnPredictor will run in mock mode.")

class VulnPredictor:
    """
    Predicts potential vulnerabilities in firmware images using ML models.
    Supports training, prediction, and feature extraction.
    """
    def __init__(self, model_path=None):
        self.model_path = model_path or "vuln_predictor_model.pkl"
        self.model = None
        self.features = ["buffer_overflow", "command_injection", "crypto_weakness", "hardcoded_key", "weak_rng"]
        self._load_model()
        logging.basicConfig(filename="vuln_predictor.log", level=logging.INFO)

    def _load_model(self):
        if joblib and os.path.isfile(self.model_path):
            self.model = joblib.load(self.model_path)
            logging.info(f"Loaded ML model from {self.model_path}")
        else:
            self.model = None
            logging.info("No ML model found. Using mock predictor.")

    def train(self, training_data: List[Dict[str, Any]], labels: List[int]):
        """
        Train the ML model on firmware features and vulnerability labels.
        Args:
            training_data (list): List of feature dicts for firmware samples.
            labels (list): List of vulnerability labels (0=safe, 1=vulnerable).
        """
        if not joblib or not np:
            logging.warning("ML libraries not available. Training is mocked.")
            return "[MOCK] Training completed."
        X = self._extract_features_batch(training_data)
        y = np.array(labels)
        from sklearn.ensemble import RandomForestClassifier
        clf = RandomForestClassifier(n_estimators=100)
        clf.fit(X, y)
        joblib.dump(clf, self.model_path)
        self.model = clf
        logging.info("Model trained and saved.")
        return "Training completed."

    def predict(self, firmware_image: str) -> Dict[str, Any]:
        """
        Predict potential vulnerabilities in the given firmware image.
        Args:
            firmware_image (str): Path to firmware image file.
        Returns:
            dict: Prediction results, including vulnerability types and risk score.
        """
        features = self._extract_features(firmware_image)
        if self.model and joblib and np:
            X = np.array([features])
            pred = self.model.predict(X)[0]
            proba = self.model.predict_proba(X)[0]
            result = {
                "vulnerable": bool(pred),
                "risk_score": float(max(proba)),
                "features": dict(zip(self.features, features))
            }
        else:
            # Mock prediction logic
            result = {
                "vulnerable": True,
                "risk_score": 0.85,
                "features": dict(zip(self.features, features)),
                "note": "Mock prediction. Install scikit-learn, joblib, numpy for real ML."
            }
        logging.info(f"Prediction for {firmware_image}: {result}")
        return result

    def _extract_features(self, firmware_image: str) -> List[int]:
        """
        Extract features from firmware image for ML prediction.
        Args:
            firmware_image (str): Path to firmware image file.
        Returns:
            list: Feature vector (mocked or real).
        """
        # In a real implementation, use binwalk, radare2, yara, etc.
        # Here, we mock feature extraction
        if not os.path.isfile(firmware_image):
            logging.warning(f"Firmware image not found: {firmware_image}")
            return [0, 0, 0, 0, 0]
        # Mock: pretend we found some features
        return [1, 1, 0, 1, 0]

    def _extract_features_batch(self, firmware_list: List[Dict[str, Any]]) -> Any:
        """
        Extract features for a batch of firmware samples.
        Args:
            firmware_list (list): List of firmware feature dicts.
        Returns:
            np.ndarray: Feature matrix for ML training.
        """
        if not np:
            return firmware_list
        # Mock: convert dicts to feature vectors
        X = []
        for fw in firmware_list:
            X.append([fw.get(f, 0) for f in self.features])
        return np.array(X)

    def explain(self, firmware_image: str) -> str:
        """
        Provide an explanation of the prediction for the firmware image.
        Args:
            firmware_image (str): Path to firmware image file.
        Returns:
            str: Explanation of prediction.
        """
        result = self.predict(firmware_image)
        explanation = f"Firmware: {firmware_image}\n"
        explanation += f"Vulnerable: {result['vulnerable']}\n"
        explanation += f"Risk Score: {result['risk_score']}\n"
        explanation += "Feature Analysis:\n"
        for k, v in result["features"].items():
            explanation += f"  {k}: {v}\n"
        if "note" in result:
            explanation += f"Note: {result['note']}\n"
        logging.info(f"Explanation for {firmware_image}: {explanation}")
        return explanation

    def save_prediction(self, firmware_image: str, output_path: str = None):
        """
        Save prediction results to a JSON file.
        Args:
            firmware_image (str): Path to firmware image file.
            output_path (str): Path to output JSON file.
        """
        result = self.predict(firmware_image)
        if not output_path:
            output_path = firmware_image + ".vuln.json"
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)
        logging.info(f"Saved prediction to {output_path}")
        return output_path
