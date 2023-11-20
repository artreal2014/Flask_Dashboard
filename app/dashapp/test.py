import datetime 
#import calendar
import pandas as pd
import helper 
import numpy as np

datasource_dir = 'D:/Works/Projects/r.hr_larkdashboard/app/dashapp/datasource'

df_bu = pd.read_excel(f"{datasource_dir}/bipo_bu.xlsx")
df_department = pd.read_excel(f"{datasource_dir}/bipo_department.xlsx")        
df_company = pd.read_excel(f"{datasource_dir}/bipo_company.xlsx")
df_country = pd.read_excel(f"{datasource_dir}/bipo_country.xlsx")
df_contract = pd.read_excel(f"{datasource_dir}/bipo_contracttype.xlsx")
df_staff = pd.read_excel(f"{datasource_dir}/bipo_staff.xlsx")

today = datetime.datetime.now() 
year_now = today.year 
month_now = today.month
today = datetime.datetime(year_now, month_now, today.day)
period = 6
num_month = int(period) #convert to int
last_date_list = helper.last_day_of_month_dates(num_month) #last day of months in a list


import plotly.express as px

fig = px.colors.diverging.swatches_continuous()
fig.show()

if 0==1:
    #test the datetime stamp
    df_generated = pd.read_excel(f"{datasource_dir}/datetime_generated.xlsx")
    datetime_generated = df_generated['Date Generated'][0].to_pydatetime()

    print (datetime_generated)
    print (type(datetime_generated))

if 0==1:
    #test the histogram bins
    df_staff=df_staff[df_staff['Active']=='Y']
    df_age = df_staff
    df_age['Age'] = df_age['Age'].apply(lambda x: int(int(x)/100))  #convert age to int
    bin=[*range(20, 60, 5)] #create bin edges 20-25, 25-30, 30-35, 35-40, 40-45, 45-50, 50-55, 55-60
    print (bin)
    counts, bins = np.histogram(df_age['Age'], bins=bin)
    percent = counts/len(df_age['Age'])*100
    print (bins)
    print (counts)

    new_bins = []
    for b in bins:
        b_text = str(b) + '-' + str(b+4)
        new_bins.append(b_text)
    new_bins.pop()
    new_bins.append("55+")
    print (new_bins)


if 0==1:
    #test the headcount calculation 
    records = []
    for last_date in last_date_list: 
        df_staff1 = df_staff[ df_staff['DateJoin']<=last_date] #join before last day
        df_staff2 = df_staff1[ df_staff1['DateResign'].isna()]     #active staff
        df_staff3 = df_staff1[ df_staff1['DateResign']>last_date]  #exit after last day
        df_staff4 = pd.concat([df_staff2, df_staff3])           #active + exit>last day

        df_staff4 = df_staff4[['EmployeeCode']].groupby('EmployeeCode').first().reset_index() #only take unique employee code
        record = {
            'Month': last_date.strftime('%y/%m'),
            'HeadCount': len(df_staff4)
        }
        records.append(record)

    df = pd.DataFrame.from_records(records)
    df = df.sort_values(by=['Month']).reset_index(drop=True)

    df.to_excel(f"{datasource_dir}/bipo_staff_headcount_debug.xlsx", index=False)