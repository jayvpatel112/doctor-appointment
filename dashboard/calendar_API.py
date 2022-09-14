# from decouple import config
from google.oauth2 import service_account
import googleapiclient.discovery
from datetime import timedelta
from datetime import datetime

CAL_ID = ''
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = './calenderdj-959ee3d67168.json'

print(SERVICE_ACCOUNT_FILE)

def test_calendar(appointment_date, appointment_start_time, appointment_end_time):
    print("RUNNING TEST_CALENDAR()")

    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

    # CREATE A NEW EVENT
    date_format_str = '%Y-%m-%d %H:%M:%S'
    time_start_str = f"{appointment_date} {appointment_start_time}" #"2022-09-14 14:15:00"
    start_time = datetime.strptime(time_start_str, date_format_str)

    time_end_str = f"{appointment_date} {appointment_end_time}"
    end_time = datetime.strptime(time_end_str, date_format_str)

    new_event = {
                    "summary": "eventTitle",
                    "start": {"dateTime": start_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
                    "end": {"dateTime": end_time.isoformat(), 'timeZone': 'Asia/Kolkata',},
                }

    service.events().insert(calendarId=CAL_ID, body=new_event).execute()
    print('Event created')

 # GET ALL EXISTING EVENTS
    events_result = service.events().list(calendarId=CAL_ID, maxResults=2500).execute()
    events = events_result.get('items', [])

    # LOG THEM ALL OUT IN DEV TOOLS CONSOLE
    for e in events:

        print(e)

    #uncomment the following lines to delete each existing item in the calendar
    #event_id = e['id']
        # service.events().delete(calendarId=CAL_ID, eventId=event_id).execute()


    return events
