import streamlit as st

# Data provided by the user, structured in a dictionary for easy access.
# This acts as a simple database for the app.
FINANCIAL_DATA = {
    "Total assets": {
        "Total assets for the U.K. were approximately (2024)": "$357 million",
        "Total assets for the U.K. were approximately (2022)": "$352 million",
        "Total assets for the U.K. were approximately (2020)": "$369 million",
    },
    "Closing share price": {
        "message": "(metric not found)"
    },
    "Employees": {
        "employees of the Firm until July (2021)": "$2,023 million",
        "employees of the Firm until July (2019)": "$2 million",
    }
}

def main():
    """
    Main function to run the Streamlit application.
    """
    # Set the title of the Streamlit app page.
    st.title("Financial Data Q&A")

    # Create a sidebar for user input.
    st.sidebar.header("Select a Metric")

    # Create a list of available metrics (modes) from the data dictionary keys.
    modes = list(FINANCIAL_DATA.keys())

    # Create a selectbox in the sidebar for the user to choose a metric.
    selected_mode = st.sidebar.selectbox(
        "Choose the data you want to see:",
        modes
    )

    # Display the selected metric as a subheader in the main area.
    st.subheader(f"Data for: {selected_mode}")

    # Retrieve the data corresponding to the user's selection.
    data_to_display = FINANCIAL_DATA.get(selected_mode, {})

    # Check if the selected metric has a special 'message' (like 'metric not found').
    if "message" in data_to_display:
        st.warning(data_to_display["message"])
    # If it's regular data, display it.
    else:
        # Check if there is any data to show.
        if data_to_display:
            # Iterate through the questions and answers and display them.
            for question, answer in data_to_display.items():
                st.markdown(f"- **{question}:** {answer}")
        else:
            # Handle the unlikely case where a metric exists but has no data.
            st.info("No data available for this metric.")

if __name__ == "__main__":
    main()
