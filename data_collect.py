import pandas as pd
import gspread as gs 
import os
import pathlib

#functions to pull data from g-sheets

path = pathlib.Path().resolve()

def get_sheet_data(url,sheet_name):
    sh = gc.open_by_url(url)
    ws = sh.worksheet(sheet_name)
    df = pd.DataFrame(ws.get_all_records())
    return df

if __name__ == "__main__":
    pwd_path= os.path.dirname(os.path.abspath(__file__))
    myfile = os.path.join(pwd_path, 'google_secrets.json')

    startup_df_list = ['df_startup_DO_limits','df_startup_EO_limits','df_startup_DO_risk','df_startup_EO_risk','df_startup_RoL']
    startup_csv_list = [x.strip('df_') for x in startup_df_list]

    sme_df_list = ['df_sme_PI_limits','df_sme_DO_limits','df_sme_cyber_limits','df_sme_PI_RoL',
                    'df_sme_cyber_RoL','df_sme_DO_RoL','df_sme_industry_dict']
    sme_csv_list = [x.strip('df_') for x in sme_df_list]

    gc = gs.service_account(filename=myfile)
    
    for df,parquet in zip(startup_df_list,startup_csv_list):
        df = get_sheet_data('https://docs.google.com/spreadsheets/d/1qhnjWeHugVGcxiBbEJg0BRa_fDTbRTB9p1W94eXugQY/edit#gid=0',parquet)
        df.to_parquet(f'{path}/Data/{parquet}.parquet')
    
    for df,parquet in zip(sme_df_list,sme_csv_list):
        df = get_sheet_data('https://docs.google.com/spreadsheets/d/1qhnjWeHugVGcxiBbEJg0BRa_fDTbRTB9p1W94eXugQY/edit#gid=0',parquet)
        df.to_parquet(f'{path}/Data/{parquet}.parquet')