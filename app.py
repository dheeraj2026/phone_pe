import streamlit as st
import sqlite3
import pandas as pd

# Connect to SQLite DB
conn = sqlite3.connect("../db/phonepe.db")

st.title("📊 PhonePe Transactions Dashboard")

# Dropdown to select year
years = pd.read_sql_query("SELECT DISTINCT year FROM aggregated_transaction ORDER BY year", conn)
selected_year = st.selectbox("Select Year", years["year"])

# Show total amount
query_total = "SELECT SUM(amount) AS total_amount FROM aggregated_transaction WHERE year = ?"
total_amount = pd.read_sql_query(query_total, conn, params=[selected_year])
st.metric("Total Transaction Amount", f"₹ {total_amount.iloc[0]['total_amount']:.2f}")

# Show by transaction type
query_type = """
SELECT transaction_type, SUM(amount) AS amount
FROM aggregated_transaction
WHERE year = ?
GROUP BY transaction_type
"""
df_type = pd.read_sql_query(query_type, conn, params=[selected_year])
st.bar_chart(df_type.set_index("transaction_type"))

conn.close()
