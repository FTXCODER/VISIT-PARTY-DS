import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# -----------------------------
# GOOGLE SHEET
# -----------------------------

SPREADSHEET_ID = "1gZ6XzgJ1_HRv99bOTzOD6VFnitksQY6C3LS5iWm0ajo"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_file(
    "service_account.json",
    scopes=SCOPES
)

client = gspread.authorize(credentials)

spreadsheet = client.open_by_key(SPREADSHEET_ID)

ds_sheet = spreadsheet.worksheet("DS")
member_sheet = spreadsheet.worksheet("MEMBER NAME")

# -----------------------------
# MEMBER LIST
# -----------------------------

members = member_sheet.col_values(1)

if members:
    members = members[1:]  # remove header

# -----------------------------
# UI
# -----------------------------

st.set_page_config(
    page_title="Sales Entry",
    page_icon="📋",
    layout="centered"
)

st.title("Sales Entry Form")

st.write("---")

selected_member = st.selectbox(
    "MEMBER",
    [""] + members
)

manual_member = st.text_input(
    "Or Type Member Name"
)

visit_date = st.date_input(
    "DATE",
    value=datetime.today()
)

party = st.text_input(
    "VISIT PARTY NAME"
)

pcs = st.number_input(
    "ORDER IN PCS",
    min_value=0,
    step=1
)

value = st.number_input(
    "APPROX VALUE",
    min_value=0.0,
    step=100.0
)

st.write("")

if st.button("SAVE"):

    member = manual_member.strip() if manual_member.strip() else selected_member

    if member == "":
        st.error("Please select or type MEMBER.")
        st.stop()

    if party.strip() == "":
        st.error("Please enter VISIT PARTY NAME.")
        st.stop()

    formatted_date = visit_date.strftime("%d-%b-%Y")

    row = [
        member,
        formatted_date,
        party,
        pcs,
        value
    ]

    ds_sheet.append_row(row)

    st.success("Data Saved Successfully!")
