from pydantic import BaseModel

class ExportLogsResponse(BaseModel):
    message: str
    file_path: str
