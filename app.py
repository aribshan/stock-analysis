import streamlit as st
st.title("Stock Analyzer")
st.sidebar.header("Navigation")
st.write("Welcome to the Stock Analyzer!")

option = st.sidebar.selectbox("Choose a feature", ["Home", "Stock Search", "Portfolio"])
if option == "Home":
    st.write("Market Overview")
elif option == "Stock Search":
    st.write("Search for a stock")
elif option == "Portfolio":
    st.write("Portfolio Analysis")