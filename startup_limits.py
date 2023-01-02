import pandas as pd
import streamlit as st
import pathlib


st.markdown("# Startup Limits Calculator 🎈")

path = pathlib.Path().resolve()

df_DO_limits = pd.read_csv(f'{path}/Data/startup_DO_limits.csv')
df_EO_limits = pd.read_csv(f'{path}/Data/startup_EO_limits.csv')
df_cyber_limits = pd.read_csv(f'{path}/Data/startup_cyber_limits.csv')

founding_list = df_DO_limits.iloc[: , 1:].columns

left_column, right_column = st.columns(2)

formattedList = ['$'+ member for member in founding_list]

st.selectbox('Insert the product that you are limiting',['PI','D&O','Cyber'],key = 'product')

with left_column:
    st.selectbox('Insert here founding of the Company', founding_list, key='founding',help='The value that the company raised on their current round')

with right_column:
    st.selectbox('Insert the company industry',df_DO_limits['TYPE'].unique(), key = 'industry')

session_product = st.session_state.product
session_founding = st.session_state.founding
session_industry = st.session_state.industry

if st.button('Calculate Limits, Risk and Premium'):
    if session_product == 'D&O':
        limits = df_DO_limits.query('TYPE == @session_industry')[session_founding].iloc[0]

    elif session_product == 'PI':
        limits = df_EO_limits.query('TYPE == @session_industry')[session_founding].iloc[0]

    elif session_product == 'Cyber':
        limits = df_cyber_limits.query('TYPE == @session_industry')[session_founding].iloc[0]
    
    st.write(f'Limits: '+'USD '+format(limits,',.2f'))
