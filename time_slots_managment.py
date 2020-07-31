from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import calculations
from config import utc


def process_calendar_instance(title=None, description=None, start_end_time=None, day_num=None, master_email=None,
                              next_week=None, delete=None, calendar_instance_id=None):
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    SCOPES = ['https://www.googleapis.com/auth/calendar']
    store = file.Storage('storage.json')

    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store, flags) \
            if flags else tools.run(flow, store)
    global CAL
    CAL = build('calendar', 'v3', http=creds.authorize(Http()))

    if delete is None:
        data = start_end_time.split('-')
        event = {
            'summary': f'{title}',
            'description': f'{description}',
            'start': {
                'dateTime':
                    f'{calculations.get_date_by_day_number(day_num, next_week).strftime("%Y-%m-%d")}T{data[0]}:{data[1]}:00+0{utc}:00',
            },
            'end': {
                'dateTime':
                    f'{calculations.get_date_by_day_number(day_num, next_week).strftime("%Y-%m-%d")}T{data[2]}:{data[3]}:00+0{utc}:00',
            },
            'attendees': [
                {'email': f'{master_email}'},
            ],
            # 'colorId': f'{random.randint(0,11)}',
        }

        # event = {
        #     'summary': f'{title}',
        #     'description': f'{description}',
        #     'start': {
        #         'dateTime': f'{calculations.get_current_year()}-07-28T10:00:00+03:00',
        #     },
        #     'end': {
        #         'dateTime': f'{calculations.get_current_year()}-07-28T11:20:00+03:00',
        #     }
        # }

        event = CAL.events().insert(calendarId='primary', body=event).execute()

        print('Event created: %s' % (event.get('htmlLink')))
        return event['id']
    else:
        if calendar_instance_id is None:
            print("Calendar instance has been deleted before...")
            return
        event = CAL.events().delete(calendarId='primary', eventId=calendar_instance_id).execute()
        print(event)


