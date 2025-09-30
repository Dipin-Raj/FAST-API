import streamlit as st
import requests
from datetime import date
import os

# FastAPI base URL - Read from environment variable for deployment, with a local fallback
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

st.title("🏥 HMS Patient Management")

# --- Create Patient --- 
st.header("Add New Patient")
with st.form("new_patient_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    date_of_birth = st.date_input("Date of Birth", min_value=date(1900, 1, 1), max_value=date.today())
    phone_number = st.text_input("Phone Number (Optional)")
    address = st.text_input("Address (Optional)")
    submitted = st.form_submit_button("Add Patient")

    if submitted:
        patient_data = {
            "name": name,
            "email": email,
            "date_of_birth": date_of_birth.isoformat(),
            "phone_number": phone_number if phone_number else None,
            "address": address if address else None,
        }
        try:
            response = requests.post(f"{FASTAPI_URL}/patients/", json=patient_data)
            if response.status_code == 200:
                st.success("Patient added successfully!")
                st.json(response.json())
            else:
                st.error(f"Error adding patient: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI. Make sure it's running at http://localhost:8000")

st.markdown("---")

# --- View Patients --- 
st.header("View All Patients")
if st.button("Refresh Patients List"):
    try:
        response = requests.get(f"{FASTAPI_URL}/patients/")
        if response.status_code == 200:
            patients = response.json()
            if patients:
                st.dataframe(patients)
            else:
                st.info("No patients found.")
        else:
            st.error(f"Error fetching patients: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to FastAPI. Make sure it's running at http://localhost:8000")

st.markdown("---")

# --- Update Patient --- 
st.header("Update Patient")
with st.form("update_patient_form"):
    update_id = st.number_input("Patient ID to Update", min_value=1, step=1)
    update_name = st.text_input("New Name (leave blank to keep current)")
    update_email = st.text_input("New Email (leave blank to keep current)")
    update_dob = st.date_input("New Date of Birth (leave as default to keep current)", value=None)
    update_phone = st.text_input("New Phone Number (leave blank to keep current)")
    update_address = st.text_input("New Address (leave blank to keep current)")
    update_submitted = st.form_submit_button("Update Patient")

    if update_submitted and update_id:
        update_data = {}
        if update_name: update_data["name"] = update_name
        if update_email: update_data["email"] = update_email
        if update_dob: update_data["date_of_birth"] = update_dob.isoformat()
        if update_phone: update_data["phone_number"] = update_phone
        if update_address: update_data["address"] = update_address

        if update_data:
            try:
                response = requests.put(f"{FASTAPI_URL}/patients/{update_id}", json=update_data)
                if response.status_code == 200:
                    st.success(f"Patient {update_id} updated successfully!")
                    st.json(response.json())
                elif response.status_code == 404:
                    st.error(f"Patient {update_id} not found.")
                else:
                    st.error(f"Error updating patient: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to FastAPI. Make sure it's running at http://localhost:8000")
        else:
            st.warning("No fields provided for update.")

st.markdown("---")

# --- Delete Patient --- 
st.header("Delete Patient")
with st.form("delete_patient_form"):
    delete_id = st.number_input("Patient ID to Delete", min_value=1, step=1)
    delete_submitted = st.form_submit_button("Delete Patient")

    if delete_submitted and delete_id:
        try:
            response = requests.delete(f"{FASTAPI_URL}/patients/{delete_id}")
            if response.status_code == 200:
                st.success(f"Patient {delete_id} deleted successfully!")
            elif response.status_code == 404:
                st.error(f"Patient {delete_id} not found.")
            else:
                st.error(f"Error deleting patient: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI. Make sure it's running at http://localhost:8000")

st.markdown("---")

# --- Database Schema Management ---
st.header("🗄️ Database Schema Management")

# Display Current Schema
st.subheader("Current Database Schema")
if st.button("Fetch Schema"):
    try:
        response = requests.get(f"{FASTAPI_URL}/db/schema")
        if response.status_code == 200:
            schema_data = response.json()
            if schema_data:
                st.json(schema_data)
            else:
                st.info("No schema information found.")
        else:
            st.error(f"Error fetching schema: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to FastAPI. Make sure it's running at http://localhost:8000")

st.markdown("### Alembic Migrations")
st.warning("**Advanced Use:** If you get a 'table already exists' error, your database is out of sync. Use 'Stamp Database' to mark all migrations as applied without running them.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Fetch Alembic History"):
        try:
            response = requests.get(f"{FASTAPI_URL}/alembic/history")
            if response.status_code == 200:
                st.code(response.json().get("stdout", "No history found."))
            else:
                st.error(f"Error fetching history: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI.")

with col2:
    if st.button("Upgrade Database (head)"):
        try:
            response = requests.post(f"{FASTAPI_URL}/alembic/upgrade")
            if response.status_code == 200:
                st.success("Database upgraded successfully!")
                st.code(response.json().get("stdout", ""))
            else:
                st.error(f"Error upgrading database: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI.")

with col3:
    if st.button("Downgrade Database (-1)"):
        try:
            response = requests.post(f"{FASTAPI_URL}/alembic/downgrade")
            if response.status_code == 200:
                st.success("Database downgraded successfully!")
                st.code(response.json().get("stdout", ""))
            else:
                st.error(f"Error downgrading database: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI.")
            
with col4:
    if st.button("Stamp Database (head)"):
        try:
            response = requests.post(f"{FASTAPI_URL}/alembic/stamp")
            if response.status_code == 200:
                st.success("Database stamped successfully!")
                st.code(response.json().get("stdout", ""))
            else:
                st.error(f"Error stamping database: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI.")

st.markdown("### Generate New Migration")
with st.form("generate_migration_form"):
    migration_message = st.text_input("Migration Message", "Add new column to patients table")
    generate_submitted = st.form_submit_button("Generate Migration Script")

    if generate_submitted:
        try:
            response = requests.post(f"{FASTAPI_URL}/alembic/revision", json={"message": migration_message})
            if response.status_code == 200:
                st.success("Migration script generated!")
                st.code(response.json().get("stdout", ""))
                st.info("Remember to manually edit app/models.py to define your new column(s) before generating a migration.")
            else:
                st.error(f"Error generating migration: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI.")
