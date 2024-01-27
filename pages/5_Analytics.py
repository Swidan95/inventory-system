import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.title("Analytics")

def load_data(file):
    excel_file = pd.ExcelFile(file)
    return excel_file

excel_file_record = load_data("RECORD.xlsx")
excel_file_data = load_data("SIMULATION.xlsx")
df_record = pd.read_excel(excel_file_record, sheet_name="RECORD")
df_data = pd.read_excel(excel_file_data, sheet_name="Copy of DATA")

# Basic statistics
st.subheader("Basic Statistics")
st.write(f"Total Items: {len(df_data)}")
st.write(f"Total Records: {len(df_record)}")
st.write(f"Total Department: {len(df_data['DEPARTMENT'].unique())}")
st.write(f"Total Transactions: {len(df_record)}")

#st.subheader("Number of items for each department")
tag = df_data.groupby(by=["DEPARTMENT"]).count()[["ITEM DETAILS"]].sort_values(by="ITEM DETAILS")
tag_count = tag.rename(columns={'ITEM DETAILS':'Count'})
fig_count = px.bar(
    tag_count,
    x = 'Count',
    y = tag.index,
    title="<b>Number of items for each department</b>"
)
#st.plotly_chart(fig_count)

#st.subheader("Number of Current Stock for each department")
stock_tag = df_data.groupby(by=['DEPARTMENT']).sum()['CURRENT STOCK']
fig_stock = px.bar(
    stock_tag,
    x = ['CURRENT STOCK'],
    y = stock_tag.index,
    title="<b>Number of Current Stock for each department</b>"
)
#st.plotly_chart(fig_stock)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_count, use_container_width=True)
right_column.plotly_chart(fig_stock, use_container_width=True)