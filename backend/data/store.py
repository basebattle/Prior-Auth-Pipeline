import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

class PAStore:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._initialize_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _initialize_db(self):
        """Create tables if they don't exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # create pa_requests table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pa_requests (
                    id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    patient_name TEXT,
                    patient_dob TEXT,
                    payer_name TEXT NOT NULL,
                    payer_id TEXT,
                    procedure_code TEXT NOT NULL,
                    procedure_description TEXT,
                    diagnosis_codes TEXT NOT NULL,
                    diagnosis_descriptions TEXT,
                    requesting_provider_npi TEXT NOT NULL,
                    requesting_provider_name TEXT,
                    clinical_notes TEXT,
                    urgency TEXT DEFAULT 'standard',
                    pa_type TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    source TEXT DEFAULT 'manual'
                )
            ''')
            
            # create agent_runs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agent_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pa_request_id TEXT NOT NULL REFERENCES pa_requests(id),
                    agent_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    input_summary TEXT,
                    output_summary TEXT,
                    confidence_score REAL,
                    model_used TEXT,
                    tokens_input INTEGER,
                    tokens_output INTEGER,
                    latency_ms INTEGER,
                    iteration_number INTEGER DEFAULT 1,
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # create pa_packages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pa_packages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pa_request_id TEXT NOT NULL REFERENCES pa_requests(id),
                    coverage_determination TEXT,
                    medical_necessity_argument TEXT,
                    supporting_evidence TEXT,
                    documentation_checklist TEXT,
                    npi_verification_result TEXT,
                    confidence_score REAL NOT NULL,
                    risk_factors TEXT,
                    recommended_actions TEXT,
                    package_document TEXT,
                    human_review_status TEXT,
                    human_reviewer_notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()

    def create_request(self, request_id: str, request_data: Dict[str, Any]) -> str:
        """Insert a new PA request into the database."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO pa_requests (
                    id, patient_id, patient_name, patient_dob, payer_name, 
                    procedure_code, diagnosis_codes, requesting_provider_npi, 
                    clinical_notes, urgency, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                request_id,
                request_data.get("patient_id"),
                request_data.get("patient_name"),
                request_data.get("patient_dob"),
                request_data.get("payer_name"),
                request_data.get("procedure_code"),
                json.dumps(request_data.get("diagnosis_codes", [])),
                request_data.get("requesting_provider_npi"),
                request_data.get("clinical_notes"),
                request_data.get("urgency", "standard"),
                "pending"
            ))
            conn.commit()
        return request_id

    def update_request_status(self, request_id: str, status: str, pa_type: Optional[str] = None):
        """Update the status of a request."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if pa_type:
                cursor.execute('UPDATE pa_requests SET status = ?, pa_type = ? WHERE id = ?', (status, pa_type, request_id))
            else:
                cursor.execute('UPDATE pa_requests SET status = ? WHERE id = ?', (status, request_id))
            conn.commit()

    def add_agent_run(self, pa_request_id: str, agent_name: str, run_data: Dict[str, Any]):
        """Log an agent run."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO agent_runs (
                    pa_request_id, agent_name, status, input_summary, 
                    output_summary, confidence_score, model_used, 
                    tokens_input, tokens_output, latency_ms, 
                    iteration_number, error_message
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                pa_request_id,
                agent_name,
                run_data.get("status"),
                run_data.get("input_summary"),
                run_data.get("output_summary"),
                run_data.get("confidence_score"),
                run_data.get("model_used"),
                run_data.get("tokens_input"),
                run_data.get("tokens_output"),
                run_data.get("latency_ms"),
                run_data.get("iteration_number", 1),
                run_data.get("error_message")
            ))
            conn.commit()

    def get_request(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Get a single request."""
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pa_requests WHERE id = ?", (request_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            res = dict(row)
            res["diagnosis_codes"] = json.loads(res["diagnosis_codes"])
            return res
        return None

    def list_requests(self, limit: int = 50) -> List[Dict[str, Any]]:
        """List recent requests."""
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pa_requests ORDER BY created_at DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def save_package(self, request_id: str, package_data: Dict[str, Any]):
        """Save final PA package."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO pa_packages (
                    pa_request_id, coverage_determination, medical_necessity_argument,
                    supporting_evidence, documentation_checklist, npi_verification_result,
                    confidence_score, risk_factors, recommended_actions,
                    package_document, human_review_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                request_id,
                package_data.get("coverage_determination"),
                package_data.get("medical_necessity_argument"),
                json.dumps(package_data.get("supporting_evidence", [])),
                json.dumps(package_data.get("documentation_checklist", [])),
                json.dumps(package_data.get("npi_verification_result", {})),
                package_data.get("confidence_score", 0.0),
                json.dumps(package_data.get("risk_factors", [])),
                json.dumps(package_data.get("recommended_actions", [])),
                package_data.get("package_document"),
                "pending"
            ))
            cursor.execute("UPDATE pa_requests SET status = 'complete', completed_at = CURRENT_TIMESTAMP WHERE id = ?", (request_id,))
            conn.commit()

    def get_package(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Get the generated package for a request."""
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pa_packages WHERE pa_request_id = ?", (request_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            res = dict(row)
            # Parse JSON fields
            for field in ["supporting_evidence", "documentation_checklist", "npi_verification_result", "risk_factors", "recommended_actions"]:
                if field in res and res[field]:
                    try:
                        res[field] = json.loads(res[field])
                    except:
                        res[field] = [] if field != "npi_verification_result" else {}
            return res
        return None
