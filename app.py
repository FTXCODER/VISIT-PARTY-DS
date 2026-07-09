# import streamlit as st
# import gspread
# from google.oauth2.service_account import Credentials
# from datetime import datetime

# # ----------------------------------------------------
# # PAGE SETTINGS
# # ----------------------------------------------------

# st.set_page_config(
#     page_title="Sales Entry",
#     page_icon="📋",
#     layout="centered"
# )

# # ----------------------------------------------------
# # GOOGLE SHEET SETTINGS
# # ----------------------------------------------------

# SPREADSHEET_ID = "1gZ6XzgJ1_HRv99bOTzOD6VFnitksQY6C3LS5iWm0ajo"

# SCOPES = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive",
# ]

# # Read Service Account from Streamlit Secrets
# creds = Credentials.from_service_account_info(
#     st.secrets["gcp_service_account"],
#     scopes=SCOPES
# )

# client = gspread.authorize(creds)

# spreadsheet = client.open_by_key(SPREADSHEET_ID)

# ds_sheet = spreadsheet.worksheet("DS")
# member_sheet = spreadsheet.worksheet("MEMBER NAME")

# # ----------------------------------------------------
# # LOAD MEMBER LIST
# # ----------------------------------------------------

# try:
#     members = member_sheet.col_values(1)

#     if len(members) > 0:
#         members = members[1:]      # Remove Header

# except:
#     members = []

# # ----------------------------------------------------
# # TITLE
# # ----------------------------------------------------

# st.title("📋 Daily Sales Entry")

# st.write("Fill the details below")

# st.divider()

# # ----------------------------------------------------
# # MEMBER
# # ----------------------------------------------------

# selected_member = st.selectbox(
#     "Select Member",
#     [""] + members
# )

# manual_member = st.text_input(
#     "Or Type New Member"
# )

# # ----------------------------------------------------
# # DATE
# # ----------------------------------------------------

# visit_date = st.date_input(
#     "Date",
#     value=datetime.today()
# )

# # ----------------------------------------------------
# # PARTY
# # ----------------------------------------------------

# party = st.text_input(
#     "Visit Party Name"
# )

# # ----------------------------------------------------
# # PCS
# # ----------------------------------------------------

# pcs = st.number_input(
#     "Order In PCS",
#     min_value=0,
#     step=1
# )

# # ----------------------------------------------------
# # VALUE
# # ----------------------------------------------------

# value = st.number_input(
#     "Approx Value",
#     # min_value=0.0,
#     # step=100.0
#     min_value=0.0,
#     value=0.0,
#     step=1.0,
#     format="%g"
# )

# st.write("")

# # ----------------------------------------------------
# # SAVE BUTTON
# # ----------------------------------------------------

# if st.button("💾 SAVE", use_container_width=True):

#     # Final Member Name
#     member = manual_member.strip()

#     if member == "":
#         member = selected_member

#     # Validation

#     if member == "":
#         st.error("Please Select or Enter Member Name")
#         st.stop()

#     if party.strip() == "":
#         st.error("Please Enter Visit Party Name")
#         st.stop()

#     formatted_date = visit_date.strftime("%d-%b-%Y")

#     data = [
#         member,
#         formatted_date,
#         party.strip(),
#         pcs,
#         value
#     ]

#     ds_sheet.append_row(data, value_input_option="USER_ENTERED")

#     st.success("✅ Data Saved Successfully!")

#     st.balloons()






import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# ----------------------------------------------------
# PAGE SETTINGS
# ----------------------------------------------------

st.set_page_config(
    page_title="Sales Entry",
    page_icon="📋",
    layout="centered"
)

# ----------------------------------------------------
# GOOGLE SHEET SETTINGS
# ----------------------------------------------------

SPREADSHEET_ID = "1gZ6XzgJ1_HRv99bOTzOD6VFnitksQY6C3LS5iWm0ajo"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES
)

client = gspread.authorize(creds)

spreadsheet = client.open_by_key(SPREADSHEET_ID)

ds_sheet = spreadsheet.worksheet("DS")
member_sheet = spreadsheet.worksheet("MEMBER NAME")

# ----------------------------------------------------
# LOAD MEMBER LIST
# ----------------------------------------------------

try:
    members = member_sheet.col_values(1)

    if len(members) > 0:
        members = members[1:]  # Remove header

except:
    members = []

# ----------------------------------------------------
# TITLE
# ----------------------------------------------------

st.title("📋 B2B Sales Daily Entry form")
st.write("Fill the details below")
st.divider()

# ----------------------------------------------------
# FORM
# ----------------------------------------------------

with st.form("sales_form", clear_on_submit=True):

    selected_member = st.selectbox(
        "Select Member",
        [""] + members
    )

    manual_member = st.text_input(
        "Or Type New Member"
    )

    visit_date = st.date_input(
        "Date",
        value=datetime.today()
    )

    party = st.text_input(
        "Visit Party Name"
    )

    pcs = st.number_input(
        "Order In PCS",
        min_value=0,
        step=1
    )

    value = st.number_input(
        "Approx Value",
        min_value=0.0,
        value=0.0,
        step=1.0,
        format="%g"
    )

    submitted = st.form_submit_button(
        "💾 SAVE",
        use_container_width=True
    )

# ----------------------------------------------------
# SAVE DATA
# ----------------------------------------------------

if submitted:

    member = manual_member.strip()

    if member == "":
        member = selected_member

    if member == "":
        st.error("Please Select or Enter Member Name")
        st.stop()

    if party.strip() == "":
        st.error("Please Enter Visit Party Name")
        st.stop()

    formatted_date = visit_date.strftime("%d-%b-%Y")

    row = [
        member,
        formatted_date,
        party.strip(),
        pcs,
        value
    ]

    ds_sheet.append_row(
        row,
        value_input_option="USER_ENTERED"
    )

    st.success("✅ Data Saved Successfully!")

    st.balloons()
