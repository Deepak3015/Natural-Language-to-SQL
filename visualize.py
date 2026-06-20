import streamlit as st
import pandas as pd

def visualize(df):

    if df.empty:
        st.warning("No Data Found!!")

        return
    
    if len(df) == 1 and  len(df.columns) == 1:
        value = df.iloc[0,0]
        if isinstance(value,int,float):
            value = round(value,2)
        st.metric(label = df.column[0],value=value)
        return
    
    if len(df.columns) == 2:
        first_column = df.columns[0]
        numeric_columns = df.select_dtypes(include="number").columns
        ignored_columns = ["id","customer_id","product_id","order_id","review_id","employee _id","payment_id","shipment_id"]
        if(len(numeric_columns)==1 and first_column.lower() not in ignored_columns):
            chart_df = df.set_index(first_column)
            st.subheader("📊 Visualization")
            st.bar_chart(chart_df)
        return
    
    if ("date" in first_column.lower() or "month" in first_column.lower() or "year" in first_column.lower()):
        numeric_columns = df.select_dtypes(include = "number").columns
        if len(numeric_columns) >= 1:
            chart_df = df.set_index(first_column)
            st.subheader("📈 Trend")
            st.line_chart(chart_df)
            return
        
    st.dataframe(df,hide_index = True,use_container_width = True)