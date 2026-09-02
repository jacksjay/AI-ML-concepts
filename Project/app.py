
import streamlit as st
import requests

# Set the base URL of our FastAPI server. 
BASE_URL = "http://127.0.0.1:8001"

# Set the main title of the web page
st.title(" AI Patient Management System")

# Create 5 distinct tabs to organize our UI neatly
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "View All", "Sort Data", "Search Patient", "Add Patient", "Update/Delete"
])


# TAB 1: VIEW ALL PATIENTS (/view)
with tab1:
    st.header("All Patients Database")
    
    # Create a button. When clicked, it returns True and runs the code block below
    if st.button("Fetch All Patients"):
        
        response = requests.get(f"{BASE_URL}/view")
        
        
        if response.status_code == 200:
            # Convert the JSON text response into a Python list/dictionary
            patients = response.json()
            # If the list is not empty, display it as a interactive table
            if patients:
                st.dataframe(patients)
            else:
                st.info("No patients found. Please add some!")
        else:
            # If it fails, show a red error box with the backend's error message
            st.error(f"Error: {response.text}")



# TAB 2: SORT PATIENTS (/sort)
with tab2:
    st.header("Sort Patients")
    
    # Create two dropdown menus for the user to pick sorting options
    # The first item in the list is the default value
    sort_by = st.selectbox("Sort by attribute:", ["height", "weight", "age", "gender"])
    order = st.selectbox("Order:", ["asc", "desc"])
    
    if st.button("Sort Data"):
        # We pass query parameters using the 'params' dictionary in the requests library
        # This builds the URL: /sort?sort_by=height&order=asc
        query_parameters = {"sort_by": sort_by, "order": order}
        response = requests.get(f"{BASE_URL}/sort", params=query_parameters)
        
        if response.status_code == 200:
            st.dataframe(response.json())
        else:
            st.error(f"Error: {response.text}")



# TAB 3: SEARCH SPECIFIC PATIENT (/patient/{id})
with tab3:
    st.header("Find a Patient")
    
    # Text input box for the user to type the ID
    search_id = st.text_input("Enter Patient ID to search (e.g., P001)")
    
    if st.button("Search"):
        # Ensure the user didn't leave the box blank
        if search_id:
            # Build the dynamic URL (e.g., /patient/P001)
            response = requests.get(f"{BASE_URL}/patient/{search_id}")
            
            if response.status_code == 200:
                # Display the single patient dictionary as a clean JSON block on screen
                st.json(response.json())
            elif response.status_code == 404:
                st.warning("Patient not found in the database.")
            else:
                st.error(f"Error: {response.text}")
        else:
            st.warning("Please enter an ID first.")



# TAB 4: CREATE PATIENT (/create)
with tab4:
    st.header("Register New Patient")
    
    # st.form bundles all inputs together so the page doesn't refresh on every keystroke
    with st.form("create_form"):
        # Split the form into two side-by-side columns
        col1, col2 = st.columns(2)
        
        with col1:
            p_id = st.text_input("Patient ID (e.g., P001)")
            p_name = st.text_input("Full Name")
            p_city = st.text_input("City")
            p_gender = st.selectbox("Gender", ["male", "female", "other"])
            
        with col2:
            p_age = st.number_input("Age", min_value=0, max_value=120)
            p_height = st.number_input("Height (meters)", min_value=0.5, max_value=3.0, value=1.75)
            p_weight = st.number_input("Weight (kg)", min_value=2.0, max_value=300.0, value=70.0)
            
        # The submit button for the form
        submitted = st.form_submit_button("Save Patient")
        
        # If the user clicks submit, build the data payload
        if submitted:
            payload = {
                "id": p_id, "name": p_name, "city": p_city, "age": p_age,
                "gender": p_gender, "height": p_height, "weight": p_weight
            }
            
            # Send the payload to the backend using a POST request
            response = requests.post(f"{BASE_URL}/create", json=payload)
            
            
            if response.status_code in [200, 201]:
                st.success(f"Patient {p_name} added successfully!")
            else:
                st.error(f"Failed to create: {response.text}")



# TAB 5: UPDATE & DELETE (/edit/{id} & /delete/{id})
with tab5:
    st.header("Update or Delete Patient")
    
    # Provide a warning because deletes are permanent
    st.warning("Warning: Deleting a patient cannot be undone.")
    
    # We need the ID for either updating or deleting
    target_id = st.text_input("Enter Patient ID to modify/delete")
    
    # Delete Section
    # We put the delete button directly in the tab (not in a form)
    if st.button("Delete Patient", type="primary"): # type="primary" makes the button red/accent colored
        if target_id:
            # Send a DELETE HTTP request
            response = requests.delete(f"{BASE_URL}/delete/{target_id}")
            if response.status_code == 200:
                st.success("Patient deleted successfully!")
            else:
                st.error(f"Error: {response.text}")
        else:
            st.error("Please provide a Patient ID.")

    st.markdown("---") # Adds a horizontal dividing line
    
    # Update Section
    st.subheader("Update Details")
    st.write("Fill in ONLY the fields you want to change. Leave others blank or at 0.")
    
    with st.form("update_form"):
        u_name = st.text_input("New Name (leave blank to skip)")
        u_city = st.text_input("New City (leave blank to skip)")
        u_age = st.number_input("New Age (0 to skip)", min_value=0, max_value=120, value=0)
        
        update_submitted = st.form_submit_button("Update Patient")
        
        if update_submitted:
            if target_id:
                # We only add fields to the payload if the user actually typed something
                update_payload = {}
                if u_name: update_payload["name"] = u_name
                if u_city: update_payload["city"] = u_city
                if u_age > 0: update_payload["age"] = u_age
                
                if update_payload:
                    # Send a PUT request to update the database
                    response = requests.put(f"{BASE_URL}/edit/{target_id}", json=update_payload)
                    if response.status_code == 200:
                        st.success("Patient updated successfully!")
                    else:
                        st.error(f"Error: {response.text}")
                else:
                    st.warning("No new data provided to update.")
            else:
                st.error("Please provide a Patient ID at the top.")