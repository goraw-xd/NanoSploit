"""
main.py
NanoSploit Dashboard Backend Entry Point
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import logging
import os

app = FastAPI(title="NanoSploit Dashboard", description="Visualization Front-End for IoT/Embedded Exploit Operations", version="1.0")

# Serve static frontend files (React/Vue build output)
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
if not os.path.exists(frontend_path):
    os.makedirs(frontend_path)
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/", response_class=HTMLResponse)
def index():
    # Placeholder: Serve index.html from frontend
    index_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>NanoSploit Dashboard</h1><p>Frontend not yet implemented.</p>"

@app.get("/api/status")
def status():
    # Example: Return system status, scenario info, etc.
    return {"status": "ok", "message": "NanoSploit Dashboard running."}

@app.get("/api/scenarios")
def list_scenarios():
    # Example: List available scenarios (placeholder)
    scenarios = ["hospital_sim.json", "smart_city_attack.json", "automotive_chain.json"]
    return {"scenarios": scenarios}

@app.get("/api/modules")
def list_modules():
    # Example: List available modules and their status (placeholder)
    modules = [
        {"name": "MedicalIoT", "status": "ready"},
        {"name": "SmartCity", "status": "ready"},
        {"name": "Automotive", "status": "ready"},
        {"name": "ConsumerIoT", "status": "ready"},
        {"name": "IndustrialIoT", "status": "ready"}
    ]
    return {"modules": modules}

@app.get("/api/report/{report_id}")
def get_report(report_id: str):
    # Example: Fetch report by ID (placeholder)
    # In real implementation, fetch from database or file
    sample_reports = {
        "hospital_sim": {"summary": "Hospital simulation completed.", "details": "All pumps patched."},
        "smart_city_attack": {"summary": "Smart city attack chain executed.", "details": "Traffic lights manipulated."}
    }
    return sample_reports.get(report_id, {"error": "Report not found."})

# Add more endpoints for scenario visualization, module control, etc.
