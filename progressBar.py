import json
import time

import requests
import streamlit as st


def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception as e:
        return e


def main():
    st.set_page_config(page_title="ETL MANAGER", page_icon="🤖")
    st.title("Start ETL")
    session = requests.Session()
    with st.form("api key form"):
        index = st.text_input("Enter Lambda api key")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("Lambda Fired")
            data = fetch(session, index)
            st.json(data, expanded=True)
            if data:
                st.write(data)
                # remove the print data after 30 seconds
    st.title("Get ETL Progress")
    session = requests.Session()
    with st.form("url_form"):
        index = st.text_input("Enter URL")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("Result")
            data = fetch(session, index)
            st.json(data, expanded=True)
            if data:
                etl_progress = st.progress(0)
                while data["status"] != "STOPPED" or data["status"] != "FAILED":
                    data = fetch(session, index)
                    etl_progress.progress(int(data["progress"]))
                    st.write(int(data["progress"]))
                    st.write(data["status"])
                    time.sleep(30)
            else:
                st.error("Error")


if __name__ == "__main__":
    main()
