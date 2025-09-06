"""
api.py
REST/GraphQL API for NanoSploit.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any
import importlib
import logging
import json
import os
from pathlib import Path

from starlette.graphql import GraphQLApp
import graphene

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

app = FastAPI(title="NanoSploit API", description="REST/GraphQL API for IoT/Embedded Exploit Operations", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dynamic import helpers
def dynamic_import(module_path, class_name):
    try:
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except Exception as e:
        logging.error(f"Failed to import {class_name} from {module_path}: {e}")
        return None

# Pydantic models for requests
class PayloadRequest(BaseModel):
    arch: str
    obfuscate: Optional[bool] = False

class FuzzRequest(BaseModel):
    firmware: str
    auto_harness: Optional[bool] = False

class ProtocolRequest(BaseModel):
    protocol: str
    target: str
    attack: str

class HILRequest(BaseModel):
    payload: str
    chip: str

class PredictRequest(BaseModel):
    firmware: str

class ModuleRequest(BaseModel):
    module: str
    action: str
    target: str
    params: Optional[Dict[str, Any]] = None

class ScenarioRequest(BaseModel):
    scenario_file: str
    run: Optional[bool] = False

class ReplayRequest(BaseModel):
    chain_file: str

class BlueTeamRequest(BaseModel):
    drill_file: str
    report: Optional[str] = None

class ReportRequest(BaseModel):
    type: str
    source: str

# REST Endpoints
@app.post("/core/payload")
def generate_payload(req: PayloadRequest):
    PayloadGenerator = dynamic_import("nanosploit.core.payload_generator", "PayloadGenerator")
    if not PayloadGenerator:
        raise HTTPException(status_code=500, detail="PayloadGenerator not available")
    pg = PayloadGenerator()
    payload = pg.generate(req.arch, obfuscate=req.obfuscate)
    out_path = f"output/payload_{req.arch}.bin"
    Path("output").mkdir(exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(payload)
    return {"status": "success", "output": out_path}

@app.post("/core/fuzz")
def fuzz_firmware(req: FuzzRequest):
    FirmwareFuzzer = dynamic_import("nanosploit.core.firmware_fuzzer", "FirmwareFuzzer")
    if not FirmwareFuzzer:
        raise HTTPException(status_code=500, detail="FirmwareFuzzer not available")
    ff = FirmwareFuzzer()
    results = ff.fuzz(req.firmware, auto_harness=req.auto_harness)
    return {"status": "success", "results": results}

@app.post("/core/protocol")
def protocol_abuse(req: ProtocolRequest):
    ProtocolAbuseSimulator = dynamic_import("nanosploit.core.protocol_abuse", "ProtocolAbuseSimulator")
    if not ProtocolAbuseSimulator:
        raise HTTPException(status_code=500, detail="ProtocolAbuseSimulator not available")
    pas = ProtocolAbuseSimulator()
    result = pas.simulate(req.protocol, req.target, req.attack)
    return {"status": "success", "result": result}

@app.post("/core/hil")
def hil_emulation(req: HILRequest):
    HILEmulator = dynamic_import("nanosploit.core.hil_emulator", "HILEmulator")
    if not HILEmulator:
        raise HTTPException(status_code=500, detail="HILEmulator not available")
    hil = HILEmulator()
    score = hil.run(req.payload, req.chip)
    return {"status": "success", "risk_score": score}

@app.post("/core/predict")
def vuln_predict(req: PredictRequest):
    VulnPredictor = dynamic_import("nanosploit.core.vuln_predictor", "VulnPredictor")
    if not VulnPredictor:
        raise HTTPException(status_code=500, detail="VulnPredictor not available")
    vp = VulnPredictor()
    prediction = vp.predict(req.firmware)
    return {"status": "success", "prediction": prediction}

@app.post("/module/run")
def run_module(req: ModuleRequest):
    mod_map = {
        "medical_iot": ("nanosploit.modules.medical_iot", "MedicalIoTModule"),
        "smart_city": ("nanosploit.modules.smart_city", "SmartCityModule"),
        "automotive": ("nanosploit.modules.automotive", "AutomotiveModule"),
        "consumer_iot": ("nanosploit.modules.consumer_iot", "ConsumerIoTModule"),
        "industrial_iot": ("nanosploit.modules.industrial_iot", "IndustrialIoTModule"),
    }
    if req.module not in mod_map:
        raise HTTPException(status_code=400, detail="Unknown module")
    module_path, class_name = mod_map[req.module]
    ModuleClass = dynamic_import(module_path, class_name)
    if not ModuleClass:
        raise HTTPException(status_code=500, detail="Module not available")
    mod = ModuleClass()
    params = req.params or {}
    if req.action == "scan":
        result = mod.scan(req.target, **params)
    elif req.action == "exploit":
        result = mod.exploit(req.target, **params)
    elif req.action == "report":
        result = mod.report(req.target, **params)
    else:
        result = {"error": "Unknown action"}
    return {"status": "success", "result": result}

@app.post("/ops/scenario")
def scenario_builder(req: ScenarioRequest):
    ScenarioBuilder = dynamic_import("nanosploit.ops.scenario_builder", "ScenarioBuilder")
    if not ScenarioBuilder:
        raise HTTPException(status_code=500, detail="ScenarioBuilder not available")
    sb = ScenarioBuilder()
    scenario = sb.load(req.scenario_file)
    if req.run:
        results = sb.run(scenario)
        return {"status": "success", "results": results}
    return {"status": "success", "scenario": scenario}

@app.post("/ops/replay")
def attack_replay(req: ReplayRequest):
    AttackReplay = dynamic_import("nanosploit.ops.attack_replay", "AttackReplay")
    if not AttackReplay:
        raise HTTPException(status_code=500, detail="AttackReplay not available")
    ar = AttackReplay()
    chain = ar.load(req.chain_file)
    results = ar.replay(chain)
    return {"status": "success", "results": results}

@app.post("/ops/blueteam")
def blueteam_sim(req: BlueTeamRequest):
    BlueTeamSim = dynamic_import("nanosploit.ops.blueteam_sim", "BlueTeamSim")
    if not BlueTeamSim:
        raise HTTPException(status_code=500, detail="BlueTeamSim not available")
    bt = BlueTeamSim()
    drill = bt.load_drill(req.drill_file)
    report = bt.run_drill(drill)
    if req.report:
        with open(req.report, "w") as f:
            json.dump(report, f, indent=2)
    return {"status": "success", "report": report}

@app.post("/report")
def reporting(req: ReportRequest):
    try:
        with open(req.source, "r") as f:
            data = json.load(f)
        if req.type == "json":
            return JSONResponse(content=data)
        elif req.type == "log":
            return {"log": data.get("log", [])}
        elif req.type == "summary":
            return {"summary": data.get("summary", "No summary available.")}
        else:
            raise HTTPException(status_code=400, detail="Unknown report type")
    except Exception as e:
        logging.error(f"Failed to generate report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# GraphQL Schema
class PayloadType(graphene.ObjectType):
    output = graphene.String()
    status = graphene.String()

class Query(graphene.ObjectType):
    payload = graphene.Field(PayloadType, arch=graphene.String(), obfuscate=graphene.Boolean())
    def resolve_payload(self, info, arch, obfuscate=False):
        PayloadGenerator = dynamic_import("nanosploit.core.payload_generator", "PayloadGenerator")
        if not PayloadGenerator:
            return PayloadType(status="error", output="PayloadGenerator not available")
        pg = PayloadGenerator()
        payload = pg.generate(arch, obfuscate=obfuscate)
        out_path = f"output/payload_{arch}.bin"
        Path("output").mkdir(exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(payload)
        return PayloadType(status="success", output=out_path)

    # Add more GraphQL fields for fuzz, protocol, modules, ops, etc.

schema = graphene.Schema(query=Query)
app.add_route("/graphql", GraphQLApp(schema=schema))

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}
