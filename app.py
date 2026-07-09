import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# -----------------------------
# Google Authentication
# -----------------------------

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "service_account.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)

spreadsheet = client.open("Sales Report")

ds_sheet = spreadsheet.worksheet("DS")
member_sheet = spreadsheet.worksheet("MEMBER NAME")

# -----------------------------
# Load Members
# -----------------------------

members = member_sheet.col_values(1)

members.append("Other")

# -----------------------------
# UI
# -----------------------------

st.set_page_config(
    page_title="DS Entry",
    layout="centered"
)

st.title("DS Entry Form")

selected_member = st.selectbox(
    "Member",
    members
)

member = selected_member

if selected_member == "Other":
    member = st.text_input("Enter Member Name")

today = datetime.today()

date = st.date_input(
    "Date",
    today
)

party = st.text_input("Visit Party Name")

pcs = st.number_input(
    "Order In PCS",
    min_value=0,
    step=1
)

value = st.number_input(
    "Approx Value",
    min_value=0.0,
    step=100.0
)

# -----------------------------
# Save
# -----------------------------

if st.button("SAVE"):

    if member == "":
        st.error("Enter Member Name")

    elif party == "":
        st.error("Enter Party Name")

    else:

        formatted_date = date.strftime("%d-%b-%Y")

        row = [
            member,
            formatted_date,
            party,
            pcs,
            value
        ]

        ds_sheet.append_row(row)

        st.success("Data Saved Successfully")
