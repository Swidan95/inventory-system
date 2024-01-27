import streamlit as st
import pandas as pd
import numpy as np

st.title("Add New Item")
st.markdown('1. In here you can add new items.')
st.markdown('2. Be sure to fill all the information needed.')
st.markdown('3. Refresh page to see the records updated.')

def load_data():
    excel_file = pd.ExcelFile("SIMULATION.xlsx")
    return excel_file

excel_file = load_data()

# Display the current data
st.write("## Current Data:")
df = pd.read_excel(excel_file, sheet_name="Copy of DATA")
st.dataframe(df)


st.write("## Add New Item:")

label_department = df['DEPARTMENT'].unique()
label_unit = df['UNIT'].unique()
label_department = np.c_[label_department, [1,2,3,4,5,6]]

# Allow user to add data
updated_value_dept = st.multiselect('Select department:', label_department[:, 0], max_selections=1)    
updated_value_item_details = st.text_input('Add details:')
updated_value_item_code = st.text_input('Add item code:')
updated_value_qty = st.number_input('Insert quantity:', step=1, min_value=0)
updated_value_unit = st.multiselect('Select Unit:', label_unit, max_selections=1)

# Add data to the dataframe
if len(updated_value_dept) > 0:
    index = 0
    for x in label_department[:, 0]:    
        index += 1
        if x == updated_value_dept[0]:
            key_value = index

if st.button("Add Data"):
    new_data = {
            'DATAID' : len(df)+1,
            'DEPT ID' : index,
            'DEPARTMENT' : updated_value_dept[0],
            'ITEM DETAILS' : updated_value_item_details,
            'ITEM CODE' : updated_value_item_code,
            'CURRENT STOCK' : updated_value_qty,
            'UNIT' : updated_value_unit[0]
        }
    
#    new_data
#    new_row = pd.DataFrame(new_data)
#    new_row
#    df = pd.concat([df, new_row], ignore_index=True)

# Add new row
    df.loc[len(df)] = new_data
    
    with pd.ExcelWriter("SIMULATION.xlsx", engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, sheet_name="Copy of DATA", index=False)
   
    st.success("Data added successfully!")

        