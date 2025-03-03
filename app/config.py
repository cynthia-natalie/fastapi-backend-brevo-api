import os
from dotenv import load_dotenv

load_dotenv() # Load .env file

class Settings: # Default if not set
    BREVO_API_KEY: str = os.getenv("BREVO_API_KEY", "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")
    START_DATE: str = os.getenv("START_DATE", "2025-02-14")
    END_DATE: str = os.getenv("END_DATE", "2025-02-21")
    LOG_FILE: str = os.getenv("LOG_FILE", "output.csv")

settings = Settings()