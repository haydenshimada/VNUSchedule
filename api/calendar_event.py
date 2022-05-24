from datetime import date, timedelta

event_list = []


# returns a list of events from a list of subjects
def create_event_list(subject_list):
    for subject in subject_list:
        print(subject)

        # convert subject data to appropriate data used in creating event
        title = subject.name
        description = subject.classCode
        date = get_date(subject.date)
        start_time = str(int(subject.start) + 6) + ':00:00'
        end_time = str(int(subject.end) + 7) + ':00:00'
        location = subject.where

        # create an event from converted data
        event_body = {
            "summary": title,  # title of event
            "location": location,
            "description": description,
            "end": {
                # "dateTime": "2022-05-04T22:00:00",
                "dateTime": date + 'T' + end_time,
                "timeZone": "Asia/Ho_Chi_Minh"
            },
            "start": {
                # "dateTime": "2022-05-04T21:00:00",
                "dateTime": date + 'T' + start_time,
                "timeZone": "Asia/Ho_Chi_Minh"
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 10},
                ],
            },
            'recurrence': [
                'RRULE:FREQ=WEEKLY',
            ],
        }

        event_list.append(event_body)


# arg `weekday`: a str. eg: T3
# returns a string representation of `weekday` 
# in current week. eg: 2022-05-24
def get_date(weekday):
    return str(date.today() - timedelta(days=date.today().weekday() % 7) + timedelta(int(weekday[1]) - 2))
