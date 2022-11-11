import pandas as pd
import streamlit as st
import pathlib


st.markdown("# Startup Limits Calculator 🎈")

df_list = ['df_startup_DO_limits','df_startup_EO_limits','df_startup_DO_risk','df_startup_EO_risk','df_startup_RoL']

csv_list = [x.strip('df_') for x in df_list]

path = pathlib.Path().resolve()

df_DO_limits = pd.read_parquet(f'{path}/Data/startup_DO_limits.parquet')
df_EO_limits = pd.read_parquet(f'{path}/Data/startup_EO_limits.parquet')

df_DO_risk = pd.read_parquet(f'{path}/Data/startup_DO_risk.parquet')
df_EO_risk = pd.read_parquet(f'{path}/Data/startup_EO_risk.parquet')

df_RoL = pd.read_parquet(f'{path}/Data/startup_RoL.parquet').set_axis(['Product', 1, 2, 3, 4, 5], axis=1, inplace=False)

founding_list = df_DO_limits.iloc[: , 1:].columns

left_column, right_column = st.columns(2)

formattedList = ['$'+ member for member in founding_list]

with left_column:
    st.selectbox('Insert the product that you are limiting',df_RoL['Product'].unique(),key = 'product')
    st.selectbox('Insert here founding of the Company', founding_list, key='founding',help='The value that the company raised on their current round')

with right_column:
    st.selectbox('Insert the company type',df_DO_limits['Type'].unique(), key = 'type')
    st.selectbox('Insert the company industry',df_DO_risk['Industry'].unique(), key = 'industry')

session_product = st.session_state.product
session_founding = st.session_state.founding
session_type = st.session_state.type
session_industry = st.session_state.industry 


if st.button('Calculate Limits, Risk and Premium'):
    if session_product == 'D&O':
        limits = df_DO_limits.query('Type == @session_type')[st.session_state.founding].iloc[0]
        risk = df_DO_risk.query('Industry == @session_industry')[session_type].iloc[0]
        RoL = df_RoL.query('Product == @session_product')[risk].iloc[0]
        premium = limits*(RoL/100)

    elif session_product == 'E&O':
        limits = df_EO_limits.query('Type == @session_type')[st.session_state.founding].iloc[0]
        risk = df_EO_risk.query('Industry == @session_industry')[session_type].iloc[0]
        RoL = df_RoL.query('Product == @session_product')[risk].iloc[0]
        premium = limits*(RoL/100)

    elif session_product == 'CYBER':
        limits = df_EO_limits.query('Type == @session_type')[st.session_state.founding].iloc[0]
        risk = df_EO_risk.query('Industry == @session_industry')[session_type].iloc[0]
        RoL = df_RoL.query('Product == @session_product')[risk].iloc[0]
        premium = float(limits*(RoL/100))
    
    st.write(f'Limits: '+'$'+format(limits,',.2f'))
    st.write(f'Risk: {risk}')
    st.write(f'RoL: '+'{:. 0%}'. format(RoL))
    st.write(f'Premium: '+'$'+format(premium,',.2f'))
