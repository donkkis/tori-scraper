from datetime import datetime, timedelta

MONTHS = {
    "tam": 1,
    "hel": 2,
    "maa": 3,
    "huh": 4,
    "tou": 5,
    "kes": 6,
    "hei": 7,
    "elo": 8,
    "syy": 9,
    "lok": 10,
    "mar": 11,
    "jou": 12
}

def get_datetime2(date_string, year_index=datetime.today().year):
    """
    Parse datetime from tori.fi raw datetime string

    returns:
        listing_date: a Python DateTime object 
    """
    time_stamp = date_string.split()

    if time_stamp[0] == "tänään":
        date = datetime.today().day
        month = datetime.today().month
        year = datetime.today().year
    elif time_stamp[0] == "eilen":
        date = (datetime.today() - timedelta(days=1)).day
        month = (datetime.today() - timedelta(days=1)).month
        year = (datetime.today() - timedelta(days=1)).year
    else:
        date = time_stamp[0]
        month = MONTHS[time_stamp[1]]
        year = year_index

    time = time_stamp[-1]

    formatted_time_stamp = f'{date} {month} {year} {time}'
    listing_date = datetime.strptime(formatted_time_stamp, '%d %m %Y %H:%M') 
    return listing_date

# time_stamp_str1 = "tänään 10:22"
# time_stamp_str2 = "eilen 05:22"
# time_stamp_str3 = "4 tou 15:48"

# print(get_datetime2(time_stamp_str1))
# print(get_datetime2(time_stamp_str2))
# print(get_datetime2(time_stamp_str3))
