import streamlit as st
import pandas as pd
import json
from nltk.chat.util import Chat, reflections

st.set_page_config(page_title="AI File Chatbot", layout="wide")

st.sidebar.title("Navigation")
app_mode = st.sidebar.radio(
    "Select an option",
    ["Upload File", "Chatbot", "Data Mapping", "Visualization", "Error Reporting"],
)
if app_mode == "Upload File":
    st.title("File Upload and Preview")
    uploaded_file = st.file_uploader("Upload your file (CSV, JSON, or XML)", type=["csv", "json", "xml"])

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            st.write("Preview of Uploaded File:")
            st.dataframe(df)
        elif uploaded_file.name.endswith(".json"):
            data = json.load(uploaded_file)
            st.write("Preview of Uploaded JSON File:")
            st.json(data)

        elif uploaded_file.name.endswith(".xml"):
            st.write("XML Preview (static example):")
            st.code("<root><data>Sample XML Content</data></root>")

        else:
            st.error("Unsupported file format!")
elif app_mode == "Chatbot":
    st.title("AI Chatbot")
    st.write("Ask questions about your file or general queries.")

    static_data = pd.DataFrame({
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "Salary": [50000, 60000, 70000]
    })
    st.write("Static Data Used for Chatbot:")
    st.dataframe(static_data)
    chatbot_pairs = [
        (r"What is the salary of (.*)?", 
         lambda matches: f"The salary of {matches[0]} is {static_data.loc[static_data['Name'] == matches[0], 'Salary'].values[0] if matches[0] in static_data['Name'].values else 'not found in the data.'}"),
        (r"How many people are in the data?", 
         lambda _: f"There are {len(static_data)} people in the dataset."),
        (r"What is the average age?", 
         lambda _: f"The average age is {static_data['Age'].mean()} years."),
        (r"(.*)", 
         lambda matches: "Sorry, I don't understand your question.")
    ]
    chatbot = Chat(chatbot_pairs, reflections)

    user_query = st.text_input("Enter your query:")
    if st.button("Ask Chatbot"):
        if user_query.strip():
            response = chatbot.respond(user_query)
            st.success(f"Chatbot Response: {response}")
        else:
            st.warning("Please enter a query.")
elif app_mode == "Data Mapping":
    st.title("Data Mapping Simulation")
    st.write("Simulate mapping of source fields to target fields.")

    source_fields = ["Name", "Age", "Salary"]
    target_fields = ["Full Name", "Years", "Income"]

    mapping = {}
    for field in source_fields:
        mapping[field] = st.selectbox(f"Map '{field}' to:", target_fields, key=field)

    st.write("Current Mappings:")
    st.json(mapping)

elif app_mode == "Visualization":
    st.title("Data Visualization")
    st.write("Visualize uploaded file data (static example).")
    df = pd.DataFrame({
        "Category": ["A", "B", "C", "D"],
        "Values": [10, 20, 15, 30],
    })

    st.bar_chart(df.set_index("Category"))

elif app_mode == "Error Reporting":
    st.title("Error Reporting")
    st.write("Simulated error report for invalid data.")
    errors = [
        {"Row": 2, "Column": "Age", "Error": "Invalid value (negative number)"},
        {"Row": 5, "Column": "Salary", "Error": "Missing value"},
    ]

    st.write("Error Log:")
    st.table(errors)

    st.write("Generate Report:")
    if st.button("Download Report"):
        error_df = pd.DataFrame(errors)
        error_df.to_csv("error_report.csv", index=False)
        st.success("Error report generated: error_report.csv")
