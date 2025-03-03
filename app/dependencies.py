from fastapi import HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
import sib_api_v3_sdk
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def validate_brevo_api_key(api_key: str):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = api_key
    api_instance = sib_api_v3_sdk.AccountApi(sib_api_v3_sdk.ApiClient(configuration))

    try:
        api_instance.get_account() 
        return api_key 
    except ApiException as e:
        raise HTTPException(status_code=403, detail="Invalid Brevo API Key")

def get_api_key(api_key: str = Security(api_key_header)):
    return validate_brevo_api_key(api_key)