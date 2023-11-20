#import dash 
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .mydash import * #access DataStore and MyDash
import datetime
from  flask_login import login_required
from .helper import * #access first_day_of_month_dates and last_day_of_month_dates

# define tab turn over 
# <-- each tab have it's own rendering structure
@login_required
def render_turnover (dash_module: MyDash):
    # get data
    ds = dash_module.datasource 
    
    dropdown_bu = {'ALL': 'All'} #key:value
    dropdown_bu.update(dict(zip(ds.df_bu['BUCode'], ds.df_bu['BU']))) # { value: lable} for dropdown
    dropdown_bu2 = dict(zip(ds.df_bu['BUCode'], ds.df_bu['BU']))


    dropdown_department = dict(zip(ds.df_department['DepartmentCode'], ds.df_department['DepartmentName']))

    dropdown_country = {'ALL': 'All'}
    dropdown_country.update(dict(zip(ds.df_country['CountryCode'], ds.df_country['CountryName'])))

    dropdown_contract = dict(zip(ds.df_contract['ContractCode'], ds.df_contract['ContractName']))

    dropdown_period = {'6': '6-Month', '12': '12-Month', '18': '18-Month', '24': '24-Month'}

    #prepare content
    tabcontent_turnover = dbc.Container([
        # Turnover  
        dbc.Row(
            dbc.Col([
                html.H1("Turnover", className='text-center text-primary mb-4'), 
                f"Data refreshed on {ds.datetime_generated.strftime('%Y-%m-%d %H:%M')}" 
                ], xs=12, sm=12, md=12, lg=12, xl=12
            ),
        ),
        dbc.Card([
            dbc.CardHeader("Filters:"),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Header("Business Unit:", className='text-left text-primary'), 
                        dcc.Dropdown(options=dropdown_bu, value="ALL", id='dropdown-2-1-bu', 
                                    persistence=True, persistence_type='local'),
                        ], xs=12, sm=12, md=3, lg=3, xl=3
                    ),
                    dbc.Col([
                        html.Header("Country:", className='text-left text-primary'), 
                        dcc.Dropdown(options=dropdown_country, value="ALL", id='dropdown-2-1-country',
                                    persistence=True, persistence_type='local'),                             
                        ], xs=12, sm=12, md=3, lg=3, xl=3
                    ),
                    dbc.Col([
                        html.Header("Month to Lookback:", className='text-left text-primary'),
                        dcc.Dropdown(options=dropdown_period, value="12", 
                                    multi=False, id='dropdown-2-1-peroid',
                                    persistence=True, persistence_type='local')

                        ], xs=12, sm=12, md=3, lg=3, xl=3
                    )
                ]),
                dbc.Row([
                    dbc.Col([
                        html.Header("Department:", className='text-left text-primary'), 
                        dcc.Dropdown(options=dropdown_department, value=ds.df_department['DepartmentCode'].to_list(),
                                    multi=True, id='dropdown-2-1-department',
                                    persistence=True, persistence_type='local')
                        ], xs=12, sm=12, md=12, lg=12, xl=12
                    )
                ], justify='center'),
                dbc.Row([
                    dbc.Col([
                        html.Header("Contract Type:", className='text-left text-primary'), 
                        dcc.Dropdown(options=dropdown_contract, value=ds.df_contract['ContractCode'].to_list(), 
                                    multi=True, id='dropdown-2-1-contract',
                                    persistence=True, persistence_type='local')
                        ], xs=12, sm=12, md=12, lg=12, xl=12
                    ) 
                ], justify='center'),  # Horizontal:start,center,end,between,around
            ]), 
        ]),
        dbc.Card([
            dbc.CardHeader("Charts:"),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([dcc.Graph(id='figure-new-exit')], width = 12)
                ], justify='center'), #new hire and exit during the month
                dbc.Row([
                   dbc.Col([dcc.Graph(id='figure-attrition-rate')], width = 12)
                ], justify='center') #new hire and exit during the month
            ])
        ]),

    ], fluid=True)
    return tabcontent_turnover


def add_callback_turnover(dash_module: MyDash):
    # first callback, update figure1, exit/join chart
    @dash_module.callback(
        [
            Output('figure-new-exit', 'figure'),
            Output('figure-attrition-rate', 'figure')
        ],
        Input('dropdown-2-1-bu', 'value'),
        Input('dropdown-2-1-department', 'value'),
        Input('dropdown-2-1-country', 'value'),
        Input('dropdown-2-1-contract', 'value'),
        Input('dropdown-2-1-peroid', 'value')
    )
    def update_turnover(bucode, departmentcode, countrycode, contractcode, period):        
        df_staff = dash_module.datasource.df_staff.copy() #retrieve dataframe
        df_staff_all = dash_module.datasource.df_staff.copy() #retrieve dataframe

        #filters
        if bucode != "ALL":
            df_staff = df_staff[df_staff['BU'] == bucode]

        if countrycode != "ALL":
            df_staff = df_staff[df_staff['CountryCode'] == countrycode]
            df_staff_all = df_staff_all[df_staff_all['CountryCode'] == countrycode]

        df_staff = df_staff[df_staff['DepartmentCode'].isin(departmentcode)]
        df_staff_all = df_staff_all[df_staff_all['DepartmentCode'].isin(departmentcode)]

        df_staff = df_staff[df_staff['ContractType'].isin(contractcode)]
        df_staff_all = df_staff_all[df_staff_all['ContractType'].isin(contractcode)]

        today = datetime.datetime.now() 
        year_now = today.year 
        month_now = today.month
        today = datetime.datetime(year_now, month_now, today.day)

        num_month = int(period) #convert to int
        last_date_list = last_day_of_month_dates(num_month) #last day of months in a list

        #Figure: create hire / exit bar chart
        # count new/exit staff in the month 
        # if join date between 1st and last day of the month, she is counted as new hire
        # if exit date between 1st and last day of the month, she is counted as exit
        # Head count f- count staff at the EOD of last day of the month 
        # As long as the staff is in on last day of the month, she is counted as headcount. 
        # Even if she only join on day 31, she is still counted.
        # If Staff left the BU before/on the last day of the month, she is excluded from the count.
        # Even if she only left on day 31, she is still excluded. Cut of is End of Day, last day of the month
        #create hire and exit figure
        records = []
        for last_date in last_date_list: 
            first_date = last_date.replace(day=1) #first day of a month 

            df_join = df_staff[df_staff['DateJoin']<=last_date] 
            df_join = df_join[df_join['DateJoin']>=first_date]

            df_exit = df_staff[df_staff['DateResign']<=last_date]
            df_exit = df_exit[df_exit['DateResign']>=first_date]
            #df_exit = df_exit[['EmployeeCode']].groupby('EmployeeCode').first().reset_index() #only take unique employee code
            #print(df_exit.columns)

            df_exit_vol = df_exit[ ~df_exit['ExitType'].isin(["Involuntary"]) | df_exit['ExitType'].isna() ]
            df_exit_invol = df_exit[ df_exit['ExitType'].isin(["Involuntary"]) ] 

            df_hc1 = df_staff[ df_staff['DateJoin']<=last_date] #join before last day
            df_hc2 = df_hc1[ df_hc1['DateResign'].isna()]       #active staff even now
            df_hc3 = df_hc1[ df_hc1['DateResign']>last_date]    #exit after last day
            df_hc = pd.concat([df_hc2, df_hc3])                 #active + exit>last day
            df_hc = df_hc.drop_duplicates(subset=['EmployeeCode'], keep='first') #only take unique employee code

            record = {
                'Month': last_date.strftime('%y/%m'),
                'StaffJoined': len(df_join),
                #'StaffExit': -len(df_exit),
                'StaffExit_Voluntary': -len(df_exit_vol), 
                'StaffExit_Involuntary': -len(df_exit_invol),
                'HeadCount': len(df_hc)     #headcount at the end of the month
            }
            records.append(record)
        df1 = pd.DataFrame.from_records(records)
        df1 = df1.sort_values(by=['Month']).reset_index(drop=True)
        
        figure1 = make_subplots(specs=[[{"secondary_y": True}]])    #a plot with two y axis
        figure1.add_trace(
            go.Bar(x=df1['Month'], y=df1['StaffJoined'], name="New Join"),
            secondary_y=False,
        )
        '''
        figure1.add_trace(
            go.Bar(x=df1['Month'], y=df1['StaffExit'], name="Exit"),
            secondary_y=False,
        )
        '''
        figure1.add_trace(
            go.Bar(x=df1['Month'], y=df1['StaffExit_Voluntary'], marker={'color': 'lightsalmon'}, name="Voluntary Exit"),
            secondary_y=False,
        )
        figure1.add_trace(
            go.Bar(x=df1['Month'], y=df1['StaffExit_Involuntary'], marker={'color': 'indianred'}, name="Involuntary Exit"),
            secondary_y=False,
        )
        figure1.add_trace(
            go.Scatter(x=df1['Month'], y=df1['HeadCount'],  mode='lines+markers', marker={'color': 'green', 'size': 12}, name='HeadCount'),  #headcount at the end of the month
            secondary_y = True #plot on secondary y axis
        )

        figure1.update_layout(
            barmode='relative',
            title_text=f'Headcount, Hire and Exit of the Month<br><sup>Headcount captured after the last day of each month</sup>',
            hovermode="x unified"
        )
        figure1.update_yaxes(title_text="Join/Exit", secondary_y=False)
        figure1.update_yaxes(title_text="HeadCount (End of Month)", secondary_y=True)
        
        #Figure 2: create attrition rate chart
        # BU specific attrition rate
        df_att = df1.copy()
        df_att['BU'] = bucode
        #df_att['AttritionRate'] = -df_att['StaffExit']/df_att['HeadCount']
        df_att['AttritionRate'] = -(df_att['StaffExit_Voluntary']+df_att['StaffExit_Involuntary'])/df_att['HeadCount']
        df_att=df_att[['Month', 'BU', 'AttritionRate']]
        # Total attrition rate, ignore BU
        if bucode != "ALL": # if BU select is NOT ALL, then add ALL to the df.
            for last_date in last_date_list:
                first_date = last_date.replace(day=1) #first day of a month 

                df_exit = df_staff_all[df_staff_all['DateResign']<=last_date]
                df_exit = df_exit[df_exit['DateResign']>=first_date]

                df_hc1 = df_staff_all[ df_staff_all['DateJoin']<=last_date] #join before last day
                df_hc2 = df_hc1[ df_hc1['DateResign'].isna()]       #active staff even now
                df_hc3 = df_hc1[ df_hc1['DateResign']>last_date]    #exit after last day
                df_hc = pd.concat([df_hc2, df_hc3])                 #active + exit>last day
                # Total attrition rate
                df_temp_all = pd.DataFrame(
                    [(last_date.strftime('%y/%m'), 'ALL', len(df_exit)/len(df_hc))],
                    columns=('Month', 'BU', 'AttritionRate')
                )
                df_att = pd.concat([df_att, df_temp_all]) #concat to df attrition

        df_att = df_att.sort_values(by=['BU', 'Month']).reset_index(drop=True)

        figure2 = go.Figure()
        for bu in df_att['BU'].unique():
            figure2.add_trace(
                go.Scatter(x=df_att[df_att['BU']==bu]['Month'], y=df_att[df_att['BU']==bu]['AttritionRate'], 
                           mode='lines+markers', marker={'size': 12}, name=bu))
        
        figure2.update_layout(
            yaxis_tickformat = '.1%',
            yaxis_range=[0, 0.1],
            title_text='Attrition Rate of the Month (Exit/HeadCount at End of Month)',
            hovermode="x unified")

        # return 
        return [figure1, figure2]
