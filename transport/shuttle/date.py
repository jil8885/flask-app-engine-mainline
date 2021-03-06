import os
import json
from datetime import datetime

from workalendar.asia import SouthKorea

from common.config import korea_timezone

cal = SouthKorea()


def is_semester(date_to_know=None):
    if not date_to_know:
        date_to_know = datetime.now(tz=korea_timezone)
    # 학기중, 계절학기, 방학 중인지 구별 코드
    # json 파일 로드
    current_dir = os.path.dirname(os.path.abspath(__file__))
    date_url = f'{current_dir}/timetable/date.json'
    with open(date_url, 'r') as raw_json:
        result = json.load(raw_json)
    term_result = -1
    for key in [x for x in list(result.keys()) if x not in ['holiday', 'halt']]:
        for term in result[key]:
            start_time = datetime.strptime(term['start'], "%m/%d/%Y").replace(tzinfo=korea_timezone)
            end_time = datetime.strptime(term['end'], "%m/%d/%Y").replace(tzinfo=korea_timezone)
            start_time = start_time.replace(year=date_to_know.year)
            end_time = end_time.replace(year=date_to_know.year)
            if end_time > start_time and start_time <= date_to_know < end_time:
                term_result = key
                break
            elif end_time < start_time:
                end_time = end_time.replace(date_to_know.year + 1)
                if start_time <= date_to_know < end_time:
                    term_result = key
                    break
        if term_result != -1:
            break

    # 운행 중지 일자
    for stop_date in result['halt']:
        halt_date = datetime.strptime(stop_date, "%m/%d/%Y")
        if (date_to_know.month, date_to_know.day) == (halt_date.month, halt_date.day):
            term_result = 'halt'

    # 평일/주말 구분
    if date_to_know.weekday() in [5, 6] or not cal.is_working_day(date_to_know):
        day = 'weekend'
    else:
        day = 'week'

    # 공휴일 구분
    for holiday_date in result['holiday']:
        holiday_date = datetime.strptime(holiday_date, "%m/%d/%Y")
        if (date_to_know.month, date_to_know.day) == (holiday_date.month, holiday_date.day):
            day = 'weekend'

    return term_result, day


def which_weekday():
    date_to_know = datetime.now(tz=korea_timezone)
    # 평일/주말 구분
    if date_to_know.weekday() == 5:
        day = 'sat'
    elif date_to_know.weekday() == 6 or not cal.is_working_day(date_to_know):
        day = 'sun'
    else:
        day = 'weekdays'
    return day
