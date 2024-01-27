import streamlit as st
import numpy as np
import pandas as pd
import random
import string
from datetime import datetime

st.title("Stock Records")
st.markdown('1. In here you can check and make transactions for stock in and stock out.')
st.markdown('2. Be sure to fill all the transaction needed.')
st.markdown('3. Refresh page to see the records updated.')

def load_data(file):
    excel_file = pd.ExcelFile(file)
    return excel_file

excel_file_record = load_data("RECORD.xlsx")
excel_file_data = load_data("SIMULATION.xlsx")

st.write("## Records:")
df_record = pd.read_excel(excel_file_record, sheet_name="RECORD")
df_data = pd.read_excel(excel_file_data, sheet_name="Copy of DATA")

st.dataframe(df_record)
#st.dataframe(df_data)

# Show details of records
label_department = df_data['DEPARTMENT'].unique()
label_department = np.c_[label_department, [1,2,3,4,5,6]]



selected_row_index = st.number_input("Enter the row index to update:", min_value=0, max_value=len(df_data)-1, step=1)

st.write("### Details")
st.write('Department ID : ', df_data.at[selected_row_index, "DEPT ID"])
st.write('Department : ', df_data.at[selected_row_index, "DEPARTMENT"])
st.write('Item Detail : ', df_data.at[selected_row_index, "ITEM DETAILS"])
st.write('Item Code : ', df_data.at[selected_row_index, "ITEM CODE"])
st.write('Unit : ', df_data.at[selected_row_index, "UNIT"])
st.write('Current Stock : ', df_data.at[selected_row_index, "CURRENT STOCK"])

stock = st.number_input("How many stocks are in or out?: ", step=1, min_value=0)
used_by = st.multiselect('Used by department:', label_department[:, 0], max_selections=1) 


if len(used_by) > 0:
    index = 0
    for x in label_department[:, 0]:    
        index += 1
        if x == used_by[0]:
            key_value = index

characters = string.digits + string.ascii_lowercase
record_generator = ''.join(random.choice(characters) for _ in range(8))
data_generator = ''.join(random.choice(characters) for _ in range(8))

if st.button('Stock in'):
    index = 0
    for x in label_department[:, 0]:    
        index += 1
        if x == used_by[0]:
            key_value = index
    
    add_stock = df_data.at[selected_row_index, "CURRENT STOCK"] + stock
    
    new_record = {
            'RECORD ID' : record_generator,
            'TIMESTAMP' : datetime.now(),
            'DEPT ID' : df_data.at[selected_row_index, "DEPT ID"],
            'DATAID' : data_generator,
            'USED BY DEPARTMENT' : key_value,
            'ITEM DETAILS' : df_data.at[selected_row_index, "ITEM DETAILS"],  
            'ITEM CODE' : df_data.at[selected_row_index, "ITEM CODE"], 
            'CURRENT STOCK' : df_data.at[selected_row_index, "CURRENT STOCK"], 
            'IN QTY' : stock,
            'OUT QTY' : 0,
            'IMAGE' : None,
            'REMARK PI NUMBER' : None
        }
    
    df_record.loc[len(df_record)] = new_record
    with pd.ExcelWriter("RECORD.xlsx", engine="openpyxl", mode="w") as writer:
        df_record.to_excel(writer, sheet_name="RECORD", index=False)
    
    df_data.at[selected_row_index, "CURRENT STOCK"] = add_stock
    with pd.ExcelWriter("SIMULATION.xlsx", engine="openpyxl", mode="w") as writer:
        df_data.to_excel(writer, sheet_name="Copy of DATA", index=False)
    
    st.warning("Record added successfully!")

if st.button('Stock out'):
    
    if stock > df_data.at[selected_row_index, "CURRENT STOCK"]:
        st.success("Error, stock out is more then current stock!")
    
    else:
        index = 0
        for x in label_department[:, 0]:    
            index += 1
            if x == used_by[0]:
                key_value = index
        
        minus_stock = df_data.at[selected_row_index, "CURRENT STOCK"] - stock
        
        new_record = {
                'RECORD ID' : record_generator,
                'TIMESTAMP' : datetime.now(),
                'DEPT ID' : df_data.at[selected_row_index, "DEPT ID"],
                'DATAID' : data_generator,
                'USED BY DEPARTMENT' : key_value,
                'ITEM DETAILS' : df_data.at[selected_row_index, "ITEM DETAILS"],  
                'ITEM CODE' : df_data.at[selected_row_index, "ITEM CODE"], 
                'CURRENT STOCK' : df_data.at[selected_row_index, "CURRENT STOCK"], 
                'IN QTY' : 0,
                'OUT QTY' : stock,
                'IMAGE' : None,
                'REMARK PI NUMBER' : None
            }
        
        df_record.loc[len(df_record)] = new_record
        with pd.ExcelWriter("RECORD.xlsx", engine="openpyxl", mode="w") as writer:
            df_record.to_excel(writer, sheet_name="RECORD", index=False)
        
        df_data.at[selected_row_index, "CURRENT STOCK"] = minus_stock
        with pd.ExcelWriter("SIMULATION.xlsx", engine="openpyxl", mode="w") as writer:
            df_data.to_excel(writer, sheet_name="Copy of DATA", index=False)
            
        st.success("Record added successfully!")