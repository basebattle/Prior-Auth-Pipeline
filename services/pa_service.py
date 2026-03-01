import time
import uuid
import json
import asyncio
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
        """Submit a single PA request for processing."""
        request_id = str(uuid.uuid4())
        
        # Save to database initially
        self.store.create_request(request_id, request.dict())
        
        # Initialize internal state
        state = PARequestState(
            request_id=request_id,
            patient_id=request.patient_id,
            patient_name=request.patient_name,
            patient_dob=request.patient_dob,
            payer_name=request.payer_name,
            procedure_code=request.procedure_code,
            diagnosis_codes=request.diagnosis_codes,
            requesting_provider_npi=request.requesting_provider_npi,
            clinical_notes=request.clinical_notes,
            urgency=request.urgency,
            current_agent="triage",
            iteration_count=0,
            pipeline_status="in_progress",
            processing_start_time=time.time(),
            agent_timings={}
        )

        try:
            # Run LangGraph pipeline
            final_state = await self.pipeline.ainvoke(state)
            
            # Extract final package
            pa_package = final_state.get("pa_package")
            if pa_package:
                self.store.save_package(request_id, pa_package.dict())
            else:
                self.store.update_request_status(request_id, "error")

            return request_id

        except Exception as e:
            # Handle error and update status in database
            self.store.update_request_status(request_id, "error")
            print(f"Pipeline error: {e}")
            raise e

    def get_all_requests(self, limit: int = 50) -> List[Dict[str, Any]]:
        """List all recent requests from database."""
        return self.store.list_requests(limit)

    def get_full_request_and_package(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Get full PA request and its generated package if complete."""
        request = self.store.get_request(request_id)
        if not request: return None
        
        # Logic to fetch package if complete
        # (For now we rely on the DB store results)
        return request

# Shared service instance
pa_service = PAService()
