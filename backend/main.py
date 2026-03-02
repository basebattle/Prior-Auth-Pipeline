from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys
import uuid
import traceback
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
        print(f"DEBUG: Received submission for {request.patient_name}")
        request_id = str(uuid.uuid4())
        
        # Log exactly what we're sending to the store
        req_dict = request.model_dump() if hasattr(request, 'model_dump') else request.dict()
        print(f"DEBUG: Creating request {request_id} in DB")
        pa_service.store.create_request(request_id, req_dict)
        
        # Run pipeline in background
        print(f"DEBUG: Queuing background task for {request_id}")
        background_tasks.add_task(pa_service.run_pipeline_background, request_id, request)
        
        return {"request_id": request_id, "status": "processing"}
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"CRITICAL ERROR in /api/submit: {e}")
        print(error_trace)
        # Use a very safe way to return detail to avoided further errors
        return HTTPException(status_code=500, detail=str(e))

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
