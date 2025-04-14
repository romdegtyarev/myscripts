#!/usr/bin/env python3

import sys
from icalendar import Calendar
from datetime import datetime
import pytz

TZ_1 = pytz.timezone("Asia/Novosibirsk")
TZ_2 = pytz.timezone("Europe/Moscow")

RENAME_MAP = {
    "Sprint Qualification": "Квалификация к спринту",
    "Sprint Race": "Спринт",
    "Practice 1": "Первая сессия свободных заездов",
    "Practice 2": "Первая сессия свободных заездов",
    "Practice 3": "Первая сессия свободных заездов",
    "Qualifying": "Квалификация",
    "Race": "Гонка"
}

def rename_summary(summary):
    for key, value in RENAME_MAP.items():
        if key.lower() in summary.lower():
            return value
    return summary

def parse_ics(file_path):
    with open(file_path, 'rb') as f:
        cal = Calendar.from_ical(f.read())

    events = []
    for component in cal.walk():
        if component.name == "VEVENT":
            summary = component.get('summary')
            dtstart = component.get('dtstart').dt
            dtend = component.get('dtend').dt
            location = component.get('location')
            description = component.get('description')
            summary = rename_summary(summary)

            if isinstance(dtstart, datetime):
                dtstart_utc = dtstart.astimezone(pytz.utc)
                dtstart_tz1 = dtstart.astimezone(TZ_1)
                dtstart_tz2 = dtstart.astimezone(TZ_2)
            else:
                dtstart_utc = datetime.combine(dtstart, datetime.min.time()).astimezone(pytz.utc)
                dtstart_tz1 = dtstart_utc.astimezone(TZ_1)
                dtstart_tz2 = dtstart_utc.astimezone(TZ_2)

            if isinstance(dtend, datetime):
                dtend_utc = dtend.astimezone(pytz.utc)
                dtend_tz1 = dtend.astimezone(TZ_1)
                dtend_tz2 = dtend.astimezone(TZ_2)
            else:
                dtend_utc = datetime.combine(dtend, datetime.min.time()).astimezone(pytz.utc)
                dtend_tz1 = dtend_utc.astimezone(TZ_1)
                dtend_tz2 = dtend_utc.astimezone(TZ_2)

            events.append({
                'summary': summary,
                'start_utc': dtstart_utc,
                'end_utc': dtend_utc,
                'start_tz1': dtstart_tz1,
                'end_tz1': dtend_tz1,
                'start_tz2': dtstart_tz2,
                'end_tz2': dtend_tz2,
                'location': location,
                'description': description
            })

    events.sort(key=lambda e: e['start_utc'])
    return events

def print_events(events):
    print("📆 События, отсортированные по времени и сгруппированные по месту:\n")

    last_location = None
    for i, event in enumerate(events, 1):
        loc = event['location']
        if loc != last_location:
            print(f"\n📍 Место: {loc}")
            last_location = loc

        print(f"  ▪ Событие: {event['summary']}")
        print(f"     🕒 Начало UTC:   {event['start_utc'].strftime('%Y-%m-%d %H:%M')} UTC")
        print(f"     🕒 Начало {TZ_1.zone}: {event['start_tz1'].strftime('%Y-%m-%d %H:%M %Z')}")
        print(f"     🕒 Начало {TZ_2.zone}: {event['start_tz2'].strftime('%Y-%m-%d %H:%M %Z')}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python icsparser.py <path-to-ics.ics>")
        sys.exit(1)

    file_path = sys.argv[1]
    events = parse_ics(file_path)
    print_events(events)
