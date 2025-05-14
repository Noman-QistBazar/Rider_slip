import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe
from google.oauth2 import service_account
import streamlit as st
from modules.utils import DATA_FILE

def save_to_google_sheets():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    )
    client = gspread.authorize(credentials)
    spreadsheet = client.open("Rider Slip Data")  # make sure this name matches your sheet

    all_data = pd.read_excel(DATA_FILE, sheet_name=None)
    for sheet_name, df in all_data.items():
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
            worksheet.clear()
        except gspread.exceptions.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="100", cols="20")
        set_with_dataframe(worksheet, df)
