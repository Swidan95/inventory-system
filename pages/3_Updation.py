import streamlit as st
import pandas as pd
import numpy as np

st.title("Updation")
st.markdown('1. In here you can make changes to the data.')
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


label_department = df['DEPARTMENT'].unique()
label_unit = df['UNIT'].unique()
#label_unit
label_department = np.c_[label_department, [1,2,3,4,5,6]]
#label_department    
    
specific_data = df.loc[df['DATAID'] == 22, 'DEPARTMENT']
#specific_data
item = df.at[33, 'ITEM DETAILS']
#item
number = int(df.at[22, 'CURRENT STOCK'])
#number

#array_with_new_column = np.c_[array, new_column]
# Allow user to update data
st.write("## Update Data:")
selected_row_index = st.number_input("Enter the row index to update:", min_value=0, max_value=len(df)-1, step=1)
#if st.button("Edit Data"):
    
updated_value_dept = st.multiselect('Select deparment:', label_department[:, 0], default=df.at[selected_row_index, 'DEPARTMENT'], max_selections=1)

index = 0
for x in label_department[:, 0]:    
    index += 1
    if x == updated_value_dept[0]:
        key_value = index
            

updated_value_item_details = st.text_input('Edit details:', value=df.at[selected_row_index, 'ITEM DETAILS'])
updated_value_item_code = st.text_input('Edit item code:', value=df.at[selected_row_index, 'ITEM CODE'])
updated_value_qty = st.number_input('Edit quantity:', step=1, value=int(df.at[selected_row_index, 'CURRENT STOCK']))
updated_value_unit = st.multiselect('Select Unit:', label_unit, default=df.at[selected_row_index, 'UNIT'], max_selections=1)
    

# Update the dataframe
if st.button("Update Data"):
    df.at[selected_row_index, "DEPT ID"] = key_value
    df.at[selected_row_index, "DEPARTMENT"] = updated_value_dept[0]
    df.at[selected_row_index, "ITEM DETAILS"] = updated_value_item_details
    df.at[selected_row_index, "ITEM CODE"] = updated_value_item_code
    df.at[selected_row_index, "CURRENT STOCK"] = updated_value_qty
    df.at[selected_row_index, "UNIT"] = updated_value_unit[0]
    
    with pd.ExcelWriter("SIMULATION.xlsx", engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, sheet_name="Copy of DATA", index=False)
   
    st.success("Data updated successfully!")

# Save the updated data to Excel
#if st.button("Save Changes"):
#    with pd.ExcelWriter("SIMULATION.xlsx", engine="openpyxl", mode="w") as writer:
#        df.to_excel(writer, sheet_name="Copy of DATA", index=False)
#        st.success("Changes saved to Excel file.")

# Note: Replace "Column_Name" and "your_file.xlsx" with your actual column name and file name.
