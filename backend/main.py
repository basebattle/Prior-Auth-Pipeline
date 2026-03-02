from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys
import uuid
from pathlib import Path

# Add backend to path so we can import services
backend_path = Path(__file__).resolve().parent
sys.path.append(str(backend_path))

from services.pa_service import pa_service
from data.schemas import PARequestInput
from data.synthetic_generator import generate_scenarios

app = FastAPI(title="Priora-Pipeline API")

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Priora-Pipeline API Operational"}

@app.get("/api/scenarios")
def get_random_scenarios(count: int = 1):
    """Fetch randomized sample PA cases."""
    return generate_scenarios(count)

@app.post("/api/submit")
async def submit_pa_request(request: PARequestInput, background_tasks: BackgroundTasks):
    """Submit a PA request to the multi-agent pipeline."""
    try:
        print(f"Received PA submission for patient: {request.patient_name}")
        # Create request in DB first and get ID
        request_id = str(uuid.uuid4())
        print(f"Generated UUID: {request_id}")
        
        pa_service.store.create_request(request_id, request.dict())
        print(f"Request {request_id} created in DB")
        
        # Run pipeline in background
        background_tasks.add_task(pa_service.run_pipeline_background, request_id, request)
        print(f"Background task added for {request_id}")
        
        return {"request_id": request_id, "status": "processing"}
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"CRITICAL Submission error: {e}")
        print(error_trace)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/requests")
def list_history(limit: int = 50):
    """Get all past requests."""
    return pa_service.get_all_requests(limit)

@app.get("/api/requests/{request_id}")
def get_request_details(request_id: str):
    """Get full details and generated package for a specific ID."""
    data = pa_service.get_full_request_and_package(request_id)
    if not data:
        raise HTTPException(status_code=404, detail="Request not found")
    return data

@app.post("/api/review/{request_id}")
def update_review_status(request_id: str, action: Dict[str, str]):
    """Update decision after human review."""
    # Logic to update DB status (Approved/Rejected)
    status = action.get("status")
    if status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    pa_service.store.update_request_status(request_id, status)
    return {"status": "updated", "new_status": status}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
