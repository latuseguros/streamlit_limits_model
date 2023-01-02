import pandas as pd
import streamlit as st
import pathlib

st.markdown("# SME Limits Calculator 🎈")

path = pathlib.Path().resolve()

df_DO_limits = pd.read_csv(f'{path}/Data/sme_DO_limits.csv')
df_PI_limits = pd.read_csv(f'{path}/Data/sme_PI_limits.csv')
df_cyber_limits = pd.read_csv(f'{path}/Data/sme_PI_limits.csv')

revenue_list = df_DO_limits.iloc[: , 1:].columns

st.selectbox('Insert the product that you are limiting',['PI','D&O','Cyber'],key = 'product')

left_column, right_column = st.columns(2)

with left_column:
    st.selectbox('Insert here revenue of the Company', revenue_list, key='revenue',help='The value that the company raised as yearly revenue')

with right_column:
    st.selectbox('Insert the company industry', df_PI_limits['TYPE'].unique(), key = 'industry')

session_product = st.session_state.product
session_revenue = st.session_state.revenue
session_industry = st.session_state.industry 


if st.button('Calculate Limits, Risk and Premium'):
    if session_product == 'PI':
        limits = df_PI_limits.query('TYPE == @session_industry')[session_revenue].iloc[0]

    elif session_product == 'D&O':
        limits = df_DO_limits.query('TYPE == @session_industry')[session_revenue].iloc[0]

    elif session_product == 'CYBER':
        limits = df_cyber_limits.query('TYPE == @session_industry')[session_revenue].iloc[0]
    
    st.write(f'Limits (in USD): '+'$'+format(limits,',.2f'))
