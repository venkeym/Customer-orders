import streamlit as st

import pandas as pd

import snowflake.connector

 

SNOWFLAKE_USER = 'bkeloth'

SNOWFLAKE_PASSWORD = 'Bansi@2022'

SNOWFLAKE_ACCOUNT = 'anblickspartner.east-us-2.azure'

SNOWFLAKE_DATABASE = 'DBT_PRACTICE_DB'

SNOWFLAKE_WAREHOUSE = 'POC_DATAHUB_GX_WH'

SNOWFLAKE_ROLE = 'SYSADMIN'

 

# Streamlit app

def main():

    st.title('Streamlit Snowflake Connection')

 

    # Create Snowflake connection

    conn = snowflake.connector.connect(

        user=SNOWFLAKE_USER,

        password=SNOWFLAKE_PASSWORD,

        account=SNOWFLAKE_ACCOUNT,

        warehouse=SNOWFLAKE_WAREHOUSE,

        database=SNOWFLAKE_DATABASE,

        role = SNOWFLAKE_ROLE

    )

 

 

 

    query = "SELECT DISTINCT FIRST_NAME FROM MAIN.CUSTOMERS"

    v_cur = conn.cursor()

    results = v_cur.execute(query)

    vendor_names = [result[0] for result in results]

 

    option = st.selectbox('Choose Vendor Name', vendor_names)

    st.write('You selected:', option)

   

    v_sql = f"SELECT First_name, Number_of_orders FROM MAIN.CUSTOMERS WHERE FIRST_NAME = '{option}'"

    query = v_sql

    v_cur = conn.cursor()

    results = v_cur.execute(query).fetchall()

 

    df = pd.DataFrame(results, columns=["First_name", "Number_of_orders"])

    edited_df = st.data_editor(df, on_change=lambda: None)

    st.session_state.data_editor = edited_df

    favorite_command = st.session_state.data_editor.loc[

        st.session_state.data_editor["First_name"] == option

    ]["Number_of_orders"].iloc[0]

 

    #edited_df = st.data_editor(df, column_config={"First_name": "Streamlit_Command", "Number_of_orders": "Number of Orders"})

    #st.data_editor(df, key="data_editor")

    st.write("Here's the session state:")

    st.write(st.session_state["data_editor"])

    st.write("Saving values...")

    edited_df.to_csv("data.csv")

 

    # Write the edited values to the database

    sql = f"UPDATE MAIN.CUSTOMERS SET Number_of_orders = '{favorite_command}' WHERE FIRST_NAME = '{option}'"

    v_cur.execute(sql)

    conn.commit()

    st.write("Values saved!")

    conn.close()

 

if __name__ == '__main__':

    main()