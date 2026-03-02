import time
import uuid
import json
import asyncio
import traceback
from typing import Dict, Any, List, Optional
from agent.orchestrator import pa_pipeline
from agent.state import PARequestState
from data.store import PAStore
from config.settings import DB_PATH
from data.schemas import PARequestInput

class PAService:
    """Facade for all PA operations."""
    
    def __init__(self, db_path: str = str(DB_PATH)):
        self.store = PAStore(db_path)
        self.pipeline = pa_pipeline

    async def submit_request(self, request: PARequestInput) -> str:
        """Submit a single PA request for processing (async)."""
        request_id = str(uuid.uuid4())
        state = self._prepare_initial_state(request_id, request)
        try:
            final_state = await self.pipeline.ainvoke(state)
            return self._handle_final_state(request_id, final_state)
        except Exception as e:
            self.store.update_request_status(request_id, "error")
            raise e

    def run_pipeline_background(self, request_id: str, request: PARequestInput):
        """Standard background task for FastAPI."""
        print(f"DEBUG: Starting background pipeline for {request_id}")
        state = self._prepare_initial_state(request_id, request)
        try:
            # Update status to processing
            self.store.update_request_status(request_id, "processing")
            
            # Run graph
            print(f"DEBUG: Invoking pipeline for {request_id}")
            final_state = self.pipeline.invoke(state)
            
            # Handle completion
            print(f"DEBUG: Pipeline finished for {request_id}. Handling final state.")
            self._handle_final_state(request_id, final_state)
        except Exception as e:
            print(f"CRITICAL: Background Pipeline Error [{request_id}]: {e}")
            traceback.print_exc()
            self.store.update_request_status(request_id, "error")

    def submit_request_sync(self, request: PARequestInput) -> str:
        """Submit a single PA request for processing (sync). Better for Streamlit frontend."""
        request_id = str(uuid.uuid4())
        state = self._prepare_initial_state(request_id, request)
        try:
            # LangGraph supports synchronous .invoke()
            final_state = self.pipeline.invoke(state)
            return self._handle_final_state(request_id, final_state)
        except Exception as e:
            self.store.update_request_status(request_id, "error")
            raise e

    def _prepare_initial_state(self, request_id: str, request: PARequestInput) -> PARequestState:
        # Check if already in store, if not create
        if not self.store.get_request(request_id):
            req_dict = request.model_dump() if hasattr(request, 'model_dump') else request.dict()
            self.store.create_request(request_id, req_dict)
        
        return {
            "request_id": request_id,
            "patient_id": request.patient_id,
            "patient_name": request.patient_name,
            "patient_dob": request.patient_dob,
            "payer_name": request.payer_name,
            "procedure_code": request.procedure_code,
            "diagnosis_codes": request.diagnosis_codes,
            "requesting_provider_npi": request.requesting_provider_npi,
            "clinical_notes": request.clinical_notes,
            "urgency": request.urgency,
            "current_agent": "triage",
            "iteration_count": 0,
            "pipeline_status": "in_progress",
            "processing_start_time": time.time(),
            "agent_timings": {}
        }

    def _handle_final_state(self, request_id: str, final_state: Dict[str, Any]) -> str:
        pa_package = final_state.get("pa_package")
        if pa_package:
            # If it's a Pydantic model, convert to dict
            package_dict = pa_package.model_dump() if hasattr(pa_package, 'model_dump') else pa_package
            self.store.save_package(request_id, package_dict)
        else:
            self.store.update_request_status(request_id, "error")
        return request_id

    def get_all_requests(self, limit: int = 50) -> List[Dict[str, Any]]:
        """List all recent requests from database."""
        return self.store.list_requests(limit)

    def get_full_request_and_package(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Get full PA request and its generated package joining two tables."""
        res = self.store.get_request(request_id)
        if not res: return None
        
        package = self.store.get_package(request_id)
        if package:
            res["result_package"] = package
        
        return res

# Shared service instance
pa_service = PAService()
