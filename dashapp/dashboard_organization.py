from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from .mydash import * #access DataStore and MyDash
from  flask_login import login_required
from .helper import * #access first_day_of_month_dates and last_day_of_month_dates
import numpy as np 

# define tab org structure 
# <-- each tab have it's own rendering structure
@login_required
def render_orgstructure (dash_module: MyDash):
    # get data
    ds = dash_module.datasource 
    
    dropdown = {'BU': 'BU', 'CountryCode': 'CountryCode', 'DepartmentCode':'DepartmentCode', 'Track':'Track', 'Gender':'Gender'}

    dropdown_bu = {'ALL': 'All'} #value: lable
    dropdown_bu.update(dict(zip(ds.df_bu['BUCode'], ds.df_bu['BU']))) # { value: lable} for dropdown
    
    dropdown_department = {'ALL': 'All'} #value: lable
    dropdown_department = dict(zip(ds.df_department['DepartmentCode'], ds.df_department['DepartmentName']))

    dropdown_country = {'ALL': 'All'}
    dropdown_country.update(dict(zip(ds.df_country['CountryCode'], ds.df_country['CountryName'])))

    dropdown_contract = dict(zip(ds.df_contract['ContractCode'], ds.df_contract['ContractName']))

    #prepare content
    tabcontent_orgstructure = dbc.Container([
        dbc.Row(
            dbc.Col([
                html.H1("Organization Structure", className='text-center text-primary mb-4'), 
                f"Data refreshed on {ds.datetime_generated.strftime('%Y-%m-%d %H:%M')}" 
                ], xs=12, sm=12, md=12, lg=12, xl=12
            ),
        ),
        dbc.Card([
            dbc.CardHeader("Filters:"),
            dbc.CardBody([
                dbc.Row([        
                    dbc.Col([
                        html.Header("Filter BU:", className='text-left text-primary'), 
                        dcc.Dropdown(options=dropdown_bu, value='ALL', id='dropdown-1-bu',
                                    persistence=True, persistence_type='local')
                        ], xs=12, sm=12, md=12, lg=3, xl=3
                    ),
                    dbc.Col([
                        html.Header("Filter Country:", className='text-left text-primary'), 
                        dcc.Dropdown(options=dropdown_country, value='ALL', id='dropdown-1-country',
                                    persistence=True, persistence_type='local')
                        ], xs=12, sm=12, md=12, lg=3, xl=3
                    ),
                    dbc.Col([
                        html.Header("Filter Department:", className='text-left text-primary'), 
                        dcc.Dropdown(options=dropdown_department, value=ds.df_department['DepartmentCode'].to_list(), 
                                    multi=True, id='dropdown-1-department',
                                    persistence=True, persistence_type='local')
                        ], xs=12, sm=12, md=12, lg=9, xl=9
                    ),
                    dbc.Col([
                        html.Header("Filter Contract Type:", className='text-left text-primary'), 
                        dcc.Dropdown(options=dropdown_contract, value=ds.df_contract['ContractCode'].to_list(), 
                                    multi=True, id='dropdown-1-contract',
                                    persistence=True, persistence_type='local')
                        ], xs=12, sm=12, md=12, lg=9, xl=9
                    ) 
                ], justify='left'), 
            ]),
        ]), 
        dbc.Card([
            dbc.CardHeader("Commonly Used Chart:"),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H1("", className="card-title", style = {'textAlign': 'center'}, id='card-1-headcount',),
                                html.P("Latest headcount after filtering", className="card-text", style = {'textAlign': 'center'}),
                            ],),
                        ])
                    ], xs=12, sm=12, md=3, lg=3, xl=3)
                ], justify='left'), 
                dbc.Row([
                    dbc.Col([dcc.Graph(id='figure-1-bu')], xs=12, sm=12, md=6, lg=6, xl=6),
                    dbc.Col([dcc.Graph(id='figure-1-country')], xs=12, sm=12, md=6, lg=6, xl=6),
                ], justify='left'), 
                dbc.Row([
                    dbc.Col([dcc.Graph(id='figure-1-department')], xs=12, sm=12, md=6, lg=6, xl=6),
                    dbc.Col([dcc.Graph(id='figure-1-track')], xs=12, sm=12, md=6, lg=6, xl=6),
                ], justify='left'), 
                dbc.Row([
                    dbc.Col([dcc.Graph(id='figure-1-ptrack')], xs=12, sm=12, md=6, lg=6, xl=6),
                    dbc.Col([dcc.Graph(id='figure-1-mtrack')], xs=12, sm=12, md=6, lg=6, xl=6),
                ], justify='left'), 
                dbc.Row([
                    dbc.Col([dcc.Graph(id='figure-1-age')], xs=12, sm=12, md=6, lg=6, xl=6),
                    dbc.Col([dcc.Graph(id='figure-1-yearservice')], xs=12, sm=12, md=6, lg=6, xl=6),
                ], justify='left'), 
                dbc.Row([
                    dbc.Col([dcc.Graph(id='figure-1-gender')], xs=12, sm=12, md=6, lg=6, xl=6),
                    dbc.Col([dcc.Graph(id='figure-1-contracttype')], xs=12, sm=12, md=6, lg=6, xl=6),
                ], justify='left'), 
            ])            
        ]), 
        dbc.Card([
            dbc.CardHeader("Explore Different Break-Downs::"),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Row([
                            html.Header("Level 1 Breakdown:", className='text-left text-primary'), 
                            dcc.Dropdown(options=dropdown, value="BU", id='dropdown-1-1', 
                                        persistence=True, persistence_type='local'),
                            ]
                        ),
                        dbc.Row([
                            html.Header("Level 2 Breakdown:", className='text-left text-primary'), 
                            dcc.Dropdown(options=dropdown, value="CountryCode", id='dropdown-1-2', 
                                        persistence=True, persistence_type='local'),
                            ]
                        ),
                        dbc.Row([
                            html.Header("Level 3 Breakdown:", className='text-left text-primary'), 
                            dcc.Dropdown(options=dropdown, value="Track", id='dropdown-1-3', 
                                        persistence=True, persistence_type='local'),
                            ]
                        ),
                        dbc.Row([
                            html.Header("Level 4 Breakdown:", className='text-left text-primary'), 
                            dcc.Dropdown(options=dropdown, value="Gender", id='dropdown-1-4', 
                                        persistence=True, persistence_type='local'),
                            ]
                        ),

                    ], xs=12, sm=12, md=3, lg=3, xl=3),
                    dbc.Col([dcc.Graph(id='figure-1-burst')], xs=12, sm=12, md=9, lg=9, xl=9, align='center'),
                ], justify='left'), # head count at the end of the month
            ])
        ]), 
    ])
    return tabcontent_orgstructure

# add several call backs
def add_callback_orgstructure(dash_module: MyDash):
    # call back 1: on sunburst chart
    @dash_module.callback(
        [Output('figure-1-burst', 'figure')],
        [
            Input('dropdown-1-bu', 'value'),
            Input('dropdown-1-country', 'value'),
            Input('dropdown-1-department', 'value'),
            Input('dropdown-1-contract', 'value'),
            Input('dropdown-1-1', 'value'),
            Input('dropdown-1-2', 'value'),
            Input('dropdown-1-3', 'value'),
            Input('dropdown-1-4', 'value'),
        ]
    )
    def update_orgstructure(bucode, countrycode, departmentcode, contractcode, 
                            dropdown1, dropdown2, dropdown3, dropdown4):
        df_staff = dash_module.datasource.df_staff.copy() #retrieve dataframe
        df_staff = df_staff[df_staff['Active'] == 'Y'] #filter by status
        
        #filters
        if bucode != 'ALL':
            df_staff = df_staff[df_staff['BU'] == bucode] #filter by bu code
        if countrycode != 'ALL':
            df_staff = df_staff[df_staff['CountryCode'] == countrycode] #filter by country code
        df_staff = df_staff[df_staff['DepartmentCode'].isin(departmentcode)] #filter by department code
        df_staff= df_staff[df_staff['ContractType'].isin(contractcode)] #filter by contract type

        # figure 1: headcount by org structure
        # group rule = [dropdown1, dropdown2, dropdown3, dropdown4]
        group_rule = [dropdown1]
        if dropdown2 != None and dropdown2 not in group_rule:
            group_rule.append(dropdown2)
        if dropdown3 != None and dropdown3 not in group_rule:
            group_rule.append(dropdown3)
        if dropdown4 != None and dropdown4 not in group_rule:
            group_rule.append(dropdown4)

        df_group = df_staff.groupby(group_rule)['EmployeeCode'].count().reset_index()
        df_group = df_group.rename(columns={'EmployeeCode': 'Count'})
        df_group['Total'] = 'Total'
        
        title = f"Headcount by {'>'.join(group_rule)}"
        path = ['Total'] + group_rule 
        fig = px.sunburst(df_group, path=path, values='Count', title=title)
        fig.update_traces(
            textinfo="label+percent parent",
            hovertemplate='<b>%{id}</b> <br>HeadCount: %{value} <br>Percent in Parent: %{percentParent:.2%} <br>Percent in Total: %{percentRoot:.2%} <extra></extra>'
        )
        fig.update_layout(margin=dict(t=30, b=20, l=20, r=20)) #size of the sunburst chart, decrease the margin to increase the size
        return [fig]
    
    # call back 2: on commonly used chart, only affected by filters
    @dash_module.callback(
    [   
        Output('card-1-headcount', 'children'),
        Output('figure-1-bu', 'figure'), 
        Output('figure-1-country', 'figure'),
        Output('figure-1-department', 'figure'),
        Output('figure-1-track', 'figure'),
        Output('figure-1-ptrack', 'figure'),
        Output('figure-1-mtrack', 'figure'),
        Output('figure-1-age', 'figure'),
        Output('figure-1-yearservice', 'figure'),
        Output('figure-1-gender', 'figure'),
        Output('figure-1-contracttype', 'figure')
    ],
    [
        Input('dropdown-1-bu', 'value'),
        Input('dropdown-1-country', 'value'),
        Input('dropdown-1-department', 'value'),
        Input('dropdown-1-contract', 'value')
    ]
    )
    def update_orgastrcture_commoncharts(bucode, countrycode, departmentcode, contractcode):
        df_staff = dash_module.datasource.df_staff.copy() #retrieve dataframe
        df_staff = df_staff[df_staff['Active'] == 'Y'] #filter by status
        #df_staff['JobTrack'] = df_staff['JobLevel'].str[0:1] # P, M, A
        
        #filters
        if bucode != 'ALL':
            df_staff = df_staff[df_staff['BU'] == bucode] #filter by bu code
        if countrycode != 'ALL':
            df_staff = df_staff[df_staff['CountryCode'] == countrycode] #filter by country code
        df_staff = df_staff[df_staff['DepartmentCode'].isin(departmentcode)] #filter by department code
        df_staff= df_staff[df_staff['ContractType'].isin(contractcode)] #filter by contract type

        # card-1-headcount
        hc = df_staff['EmployeeCode'].count()
        hc = str(hc) #convert to string

        # figure-1-bu 
        df_bu = df_staff.groupby(['BU'])['EmployeeCode'].count().reset_index()
        df_bu = df_bu.rename(columns={'EmployeeCode': 'Count'})
        title1 = "Headcount by BU"
        fig1 = px.pie(df_bu, values='Count', names='BU', title=title1, hole=0.3) 
        fig1.update_traces(textposition='auto', textinfo='percent+value+label')

        # figure-1-country, 
        df_country = df_staff.groupby(['CountryCode'])['EmployeeCode'].count().reset_index()
        df_country = df_country.rename(columns={'EmployeeCode': 'Count'})
        title2 = "Headcount by Country"
        fig2 = px.pie(df_country, values='Count', names='CountryCode', title=title2, hole=0.3) 
        fig2.update_traces(textposition='auto', textinfo='percent')

        # figure-1-department
        df_dpt = df_staff.groupby(['DepartmentCode'])['EmployeeCode'].count().reset_index()
        df_dpt = df_dpt.rename(columns={'EmployeeCode': 'Count'})
        title3 = "Headcount by Department"
        fig3 = px.pie(df_dpt, values='Count', names='DepartmentCode', title=title3, hole=0.3) 
        fig3.update_traces(textposition='auto', textinfo='percent')

        # figure-1-track
        df_track = df_staff.groupby(['Track', 'JobLevel'])['EmployeeCode'].count().reset_index()
        df_track = df_track.rename(columns={'EmployeeCode': 'Count'})

        title4 = "Headcount by Job Track"
        fig4 = px.pie(df_track, values='Count', names='Track', title=title4, hole=0.3) 
        fig4.update_traces(textposition='auto', textinfo='label+percent')
        
        # figure-1-ptrack
        df_ptrack = df_staff[df_staff['Track']=="P"]
        df_ptrack = df_ptrack.groupby(['JobLevel'])['EmployeeCode'].count().reset_index()
        df_ptrack = df_ptrack.rename(columns={'EmployeeCode': 'Count'})
        df_ptrack['Percent'] = df_ptrack['Count'] / df_ptrack['Count'].sum()
        df_ptrack['Percent'] = df_ptrack['Percent'].apply(lambda x: '{:.1%}'.format(x)) #format into percentage 
        title5 = "Headcount by Job Level (Professional Track)"
        fig5 = px.bar(df_ptrack, x='JobLevel', y='Count', title=title5,
                      hover_data=['Count', 'Percent'], 
                      category_orders={"JobLevel": ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10", "P11"]})
        fig5.update_layout(hovermode="x unified")

        # figure-1-mtrack
        df_mtrack = df_staff[df_staff['Track']=="M"]
        df_mtrack = df_mtrack.groupby(['JobLevel'])['EmployeeCode'].count().reset_index()
        df_mtrack = df_mtrack.rename(columns={'EmployeeCode': 'Count'})
        df_mtrack['Percent'] = df_mtrack['Count'] / df_mtrack['Count'].sum()
        df_mtrack['Percent'] = df_mtrack['Percent'].apply(lambda x: '{:.1%}'.format(x)) #format into percentage 
        title6 = "Headcount by Job Level (Management Track)"
        fig6 = px.bar(df_mtrack, x='JobLevel', y='Count', title=title6,
                      hover_data=['Count', 'Percent'], 
                      category_orders={"JobLevel": ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11"]})
        fig6.update_layout(hovermode="x unified")
        
        # figure-1-age
        df_age = df_staff
        df_age['Age'] = df_age['Age'].apply(lambda x: int(int(x)/100))
        bin=[*range(20, 60, 5)] #create bin edges 20-25, 25-30, 30-35, 35-40, 40-45, 45-50, 50-55, 55-60
        counts, bins = np.histogram(df_age['Age'], bins=bin)
        percents = counts/len(df_age['Age'])*100
        # new bin for display purpose
        new_bins = []
        for b in bins:
            b_text = str(b) + '-' + str(b+4)
            new_bins.append(b_text)
        new_bins.pop()
        new_bins.pop()
        new_bins.append("55+")

        df_age1 = pd.DataFrame({'Age': new_bins, 'Count': counts, 'Percent': percents})
        df_age1['Percent'] = df_age1['Percent'].apply(lambda x: '{:.1%}'.format(x)) #format into percentage
        title7 = "Headcount by Age"
        fig7 = px.bar(df_age1, x='Age', y='Count', title=title7,
                      hover_data=['Count', 'Percent'])
        fig7.update_layout(hovermode="x unified")

        # figure-1-yearservice
        df_yos = df_staff
        df_yos['YearService'] = df_age['ServiceLength'].apply(lambda x: int(int(x)/100))
        df_yos = df_yos.groupby(['YearService'])['EmployeeCode'].count().reset_index()
        df_yos = df_yos.rename(columns={'EmployeeCode': 'Count'})
        df_yos['Percent'] = df_yos['Count'] / df_yos['Count'].sum()
        df_yos['Percent'] = df_yos['Percent'].apply(lambda x: '{:.1%}'.format(x)) #format into percentage 
        title8 = "Headcount by Year of Service"
        fig8 = px.bar(df_yos, x='YearService', y='Count', title=title8,
                      hover_data=['Count', 'Percent'])
        fig8.update_layout(hovermode="x unified")

        #figure-1-gender
        df_gender = df_staff
        df_gender = df_gender.groupby(['Gender'])['EmployeeCode'].count().reset_index()
        df_gender = df_gender.rename(columns={'EmployeeCode': 'Count'})
        title9 = "Headcount by Gender"
        fig9 = px.pie(df_gender, names='Gender', values='Count', title=title9, hole=0.3)
        fig9.update_traces(textposition='auto', textinfo='percent')


        #Output('figure-1-contracttype', 'figure')
        df_contract = df_staff
        df_contract = df_contract.groupby(['ContractType'])['EmployeeCode'].count().reset_index()
        df_contract = df_contract.rename(columns={'EmployeeCode': 'Count'})
        title10 = "Headcount by Type of Contract"
        fig10 = px.pie(df_contract, names='ContractType', values='Count', title=title10, hole=0.3)
        fig10.update_traces(textposition='auto', textinfo='percent')        

        return [hc, fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10]