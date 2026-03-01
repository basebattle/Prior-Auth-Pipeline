import time
from typing import Dict, Any

class OCRProcessor:
    """Simulated OCR Processor for clinical documents."""
    
    def process_document(self, file_bytes: bytes, file_name: str) -> str:
        """Extract text from PDF/Image. 
        In production, this would use Tesseract, AWS Textract, or Google Document AI.
        """
        # Mock processing time
        time.sleep(1.5)
        
        # Simulated extraction based on filename or dummy content
        if "imaging" in file_name.lower():
            return "MRI Right Knee: Grade IV joint space narrowing, large osteophytes, subchondral sclerosis."
        elif "pt_notes" in file_name.lower():
            return "Physical Therapy Summary: Completed 12 sessions. Pain remains 8/10. Strengthening exercises failed to improve function."
        else:
            return "Extracted clinical text from document: Patient reports chronic knee pain for 2 years. Failed NSAIDs."

# instance for tool use
ocr_tool = OCRProcessor()
