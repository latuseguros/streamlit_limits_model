import pandas as pd
import streamlit as st

st.markdown("# SME Limits Calculator 🎈")

df_list = ['df_sme_PI_limits','df_sme_DO_limits','df_sme_cyber_limits','sme_PI_RoL','sme_cyber_RoL','sme_DO_RoL']

csv_list = [x.strip('df_') for x in df_list]

path = '/Users/hdnovak/Documents/Latu/Models/limits_model'

df_DO_limits = pd.read_parquet(f'{path}/Data/sme_DO_limits.parquet')
df_PI_limits = pd.read_parquet(f'{path}/Data/sme_PI_limits.parquet')
df_cyber_limits = pd.read_parquet(f'{path}/Data/sme_PI_limits.parquet')

df_DO_RoL = pd.read_parquet(f'{path}/Data/sme_DO_RoL.parquet')
df_PI_RoL = pd.read_parquet(f'{path}/Data/sme_PI_RoL.parquet')
df_cyber_RoL = pd.read_parquet(f'{path}/Data/sme_cyber_RoL.parquet')

revenue_list = df_DO_limits.iloc[: , 1:].columns

st.selectbox('Insert the product that you are limiting',['PI','D&O','Cyber'],key = 'product')

left_column, right_column = st.columns(2)

with left_column:
    st.selectbox('Insert here revenue of the Company', revenue_list, key='revenue',help='The value that the company raised as yearly revenue')

session_product = st.session_state.product
session_revenue = st.session_state.revenue

if session_product == 'PI':
    with right_column:
        st.selectbox('Insert the company industry', df_PI_limits['Industry'].unique(), key = 'industry')
else:
    with right_column:
        st.selectbox('Insert the company industry', df_DO_limits['Industry'].unique(), key = 'industry')

session_industry = st.session_state.industry 


if st.button('Calculate Limits, Risk and Premium'):
    if session_product == 'PI':
        limits = df_PI_limits.query('Industry == @session_industry')[session_revenue].iloc[0]
        RoL = df_PI_RoL.query('Industry == @session_industry')[session_revenue].iloc[0]
        premium = limits*RoL

    elif session_product == 'D&O':
        limits = df_DO_limits.query('Industry == @session_industry')[session_revenue].iloc[0]
        RoL = df_DO_RoL.query('Industry == @session_industry')[session_revenue].iloc[0]
        premium = limits*RoL

    elif session_product == 'CYBER':
        limits = df_cyber_limits.query('Industry == @session_industry')[session_revenue].iloc[0]
        RoL = df_cyber_RoL.query('Industry == @session_industry')[session_revenue].iloc[0]
        premium = limits*RoL
    
    st.write(f'Limits: {limits}')
    st.write(f'RoL: {RoL}')
    st.write(f'Premium: {premium}')
