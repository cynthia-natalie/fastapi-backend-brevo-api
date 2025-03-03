import csv
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from app.config import settings
from app.logger import logger

def fetch_email_logs():
    all_events = []
    limit = 5000
    offset = 0

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = settings.BREVO_API_KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    while True:
        try:
            response = api_instance.get_email_event_report(
                limit=limit, offset=offset, start_date=settings.START_DATE, end_date=settings.END_DATE
            )
            if not response.events:
                break  

            all_events.extend(response.events)
            offset += limit

        except ApiException as e:
            logger.error(f"Error fetching logs: {e}")
            return []

    return all_events

def write_logs_to_csv(events, output_file=settings.LOG_FILE):
    columns = ["recipient", "message_id", "date", "event", "link", "ip_address"]
    
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        for event in events:
            writer.writerow({
                "recipient": event.email,
                "message_id": event.message_id,
                "date": event._date,
                "event": event.event,
                "link": getattr(event, "link", ""),
                "ip_address": getattr(event, "ip", ""),
            })

    logger.info(f"Logs exported to {output_file}")
    return output_file
