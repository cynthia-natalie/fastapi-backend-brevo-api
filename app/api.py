from fastapi import APIRouter, Depends
from app.models import ExportLogsResponse
from app.dependencies import get_api_key
from app.logger import logger
from app.services import fetch_email_logs, write_logs_to_csv

# Define API Router (Make sure it's at the top)
router = APIRouter()

@router.get("/export-logs", response_model=ExportLogsResponse, dependencies=[Depends(get_api_key)])
def export_logs():
    logger.info("Export logs endpoint accessed")
    
    logs = fetch_email_logs()
    if not logs:
        return {"message": "No logs available", "file_path": ""}

    file_path = write_logs_to_csv(logs)
    
    return {"message": "Logs successfully exported", "file_path": file_path}
