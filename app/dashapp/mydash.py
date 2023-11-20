import dash 
import pandas as pd
import dotenv
import os
import datetime 
# Load environment variable parameters in the .env file
dotenv.load_dotenv(dotenv.find_dotenv())
datasource_dir = os.getenv('DATASOURCE_DIR')

# this module to manage data reading from data store
class DataSource():

    df_bu: pd.DataFrame
    df_department: pd.DataFrame
    df_company: pd.DataFrame
    df_country: pd.DataFrame
    #df_assignment: pd.DataFrame
    df_staff:pd.DataFrame
    datetime_generated: datetime.datetime

    def __init__(self):
        self.df_bu = pd.read_excel(f"{datasource_dir}/bipo_bu.xlsx")
        self.df_department = pd.read_excel(f"{datasource_dir}/bipo_department.xlsx")        
        self.df_company = pd.read_excel(f"{datasource_dir}/bipo_company.xlsx")
        self.df_country = pd.read_excel(f"{datasource_dir}/bipo_country.xlsx")
        self.df_contract = pd.read_excel(f"{datasource_dir}/bipo_contracttype.xlsx")
        self.df_staff = pd.read_excel(f"{datasource_dir}/bipo_staff.xlsx")
        
        df_generated = pd.read_excel(f"{datasource_dir}/datetime_generated.xlsx")
        self.datetime_generated = df_generated['Date Generated'][0].to_pydatetime()

    @staticmethod
    def reload_bu(): 
        pass    

    @staticmethod
    def get_available_indicators(df) -> list:
        return df['Indicator Name'].unique()

# extend Dash class with new datasource as new member viarables
class MyDash(dash.Dash):
    datasource: DataSource
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.datasource = DataSource() #add datasource 