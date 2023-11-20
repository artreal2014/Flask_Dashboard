import datetime
import dateutil.relativedelta

#helper functions

#first day of month in last num_months
def first_day_of_month_dates(num_months):
    today = datetime.datetime.today()  # Get the current date
    first_day = datetime.datetime(today.year, today.month, 1)

    first_day_dates = [first_day]
    for i in range(1, num_months):
        aday = first_day - dateutil.relativedelta.relativedelta(months=i)
        first_day_dates.append(aday)
    return first_day_dates

#last day of month in last num_months
def last_day_of_month_dates(num_months):
    today = datetime.datetime.now()  # Get the current date
    first_day = datetime.datetime(today.year, today.month, 1) + dateutil.relativedelta.relativedelta(months=1)

    first_day_dates = [first_day]
    for i in range(1, num_months):
        aday = first_day - dateutil.relativedelta.relativedelta(months=i)
        first_day_dates.append(aday)

    last_day_dates = []
    for adate in first_day_dates:
        last_day_dates.append(adate - dateutil.relativedelta.relativedelta(days=1))

    return last_day_dates

'''
# Get the last day of the current month and the previous 5 months
months_to_get = 5
date_list = last_day_of_month_dates(months_to_get)
# Print the list of dates
for date in date_list:
    print(date)

date_list = first_day_of_month_dates(months_to_get)
# Print the list of dates
for date in date_list:
    print(date)
'''