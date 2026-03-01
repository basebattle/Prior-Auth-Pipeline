import httpx
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import asyncio

class NPILookupResult(BaseModel):
    npi: str
    status: str                    # "A" (active), "D" (deactivated)
    provider_name: str
    credential: Optional[str]      # MD, DO, NP, etc.
    specialty: Optional[str]       # Primary taxonomy description
    taxonomy_code: Optional[str]   # e.g., "207X00000X" for Orthopedic Surgery
    address_city: Optional[str]
    address_state: Optional[str]
    last_updated: Optional[str]

async def lookup_npi(npi: str) -> Optional[NPILookupResult]:
    """Query NPPES registry for NPI details."""
    url = "https://npiregistry.cms.hhs.gov/api/"
    params = {"number": npi, "version": "2.1"}
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("result_count", 0) == 0:
                return None
            
            result = data["results"][0]
            basic = result.get("basic", {})
            taxonomies = result.get("taxonomies", [])
            primary_taxonomy = next((t for t in taxonomies if t.get("primary")), taxonomies[0]) if taxonomies else {}

            return NPILookupResult(
                npi=str(result["number"]),
                status="A" if str(result.get("enumeration_type")) else "U",
                provider_name=f"{basic.get('first_name', '')} {basic.get('last_name', '')}".strip(),
                credential=basic.get("credential"),
                specialty=primary_taxonomy.get("desc"),
                taxonomy_code=primary_taxonomy.get("code"),
                address_city=result.get("practiceLocations", [{}])[0].get("city"),
                address_state=result.get("practiceLocations", [{}])[0].get("state"),
                last_updated=result.get("last_updated_epoch")
            )
    except Exception as e:
        # Log error or return none - for now return None to handle as tool failure
        return None

def sync_lookup_npi(npi: str) -> Optional[NPILookupResult]:
    """Synchronous wrapper for lookup_npi."""
    try:
        return asyncio.run(lookup_npi(npi))
    except (RuntimeError, Exception):
        # Handle cases where the event loop is already running
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return None
        return asyncio.run(lookup_npi(npi))
