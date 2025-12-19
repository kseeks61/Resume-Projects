import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# Title and Description
st.title("Interactive Data Visualization")
st.write("This app allows you to visualize data with dynamic filters and groupings.")

# Load the dataset
df = pd.read_csv('/Users/kseeks61/Downloads/Data_Vis_Project_Raw.csv')

# Drop unnecessary columns
df = df.drop(["YEAR", "SERIAL", "NHISHID", "PERNUM", "NHISPID", "HHX", "ASTATQCFLAG"], axis=1)

# Create a new column for adult/child distinction
df["Adult/Child"] = df["ASTATFLG"].apply(lambda x: "Adult" if x == 1 else "Child")
df = df.drop(["ASTATFLG", "CSTATFLG"], axis=1)

df["REGION"] = df["REGION"].replace({1: "Northeast", 2: "Midwest", 3: "South", 4: "West"})

df["URBRRL"]= df["URBRRL"].replace({1: "Large Central Metro", 2: "Large Fringe Metro", 3: "Medium and Small Metro", 4: "Nonmetroplitan"})

df["SEX"]= df["SEX"].replace({1: "Male", 2: "Female"})

df["SEXORIEN"] = df["SEXORIEN"].replace({1: "Lesbian/Gay", 2: "Heterosexual", 3: "Bisexual", 4: "Other", 5: "Don't Know"})

df["FAMSTRUCSC"] = df["FAMSTRUCSC"].replace({1: "Single Parent Never Married", 2: "Single Parent Ever Married", 3: "Married Parents Residing In Same Household", 4: "Cohabiting Parents Residing In Same Household", 5: "At Least 1 Non-Parent Residing In Same Household"})

df["RACENEW"] = df["RACENEW"].replace({100: "White", 200: "Black or African American", 300: "American Indian or Alaska Native", 400: "Asian", 500: "Other Race or Multi-Race"})

df["GOTSTAMPFAM"] = df["GOTSTAMPFAM"].replace({10: "No Food Stamps", 20: "Received Food Stamps", 21: "Received Food Stamps Last Year", 22: "Received Food Stamps Last Month"})

df["FSSTAT"] = df["FSSTAT"].replace({1: "Food Secure", 2: "Low Food Security", 3: "Very Low Food Security"})

df["JAILEV"] = df["JAILEV"].replace({1: "No", 2: "Yes", 3: "Separated From Parent Due To Incarceration "})

df["ALCDRUGEV"] = df["ALCDRUGEV"].replace({1: "No", 2: "Yes"})

df["ADLTPUTDOWN"] = df["ADLTPUTDOWN"].replace({1: "No", 2: "Yes"})

df["UNFAIRRACE"] = df["UNFAIRRACE"].replace({1: "No", 2: "Yes"})

df["BEHAVEDIF"] = df["BEHAVEDIF"].replace({1: "No Difficulty", 2: "Some Difficulty", 3: "A Lot of Difficulty", 4: "Cannot Do At All"})

df["MKFRNDIF"] = df["MKFRNDIF"].replace({1: "No Difficulty", 2: "Some Difficulty", 3: "A Lot of Difficulty", 4: "Cannot Do At All"})

df["DEPRESSEV"] = df["DEPRESSEV"].replace({1: "No", 2: "Yes"})

df["DSOCIALP"] = df["DSOCIALP"].replace({1: "No Difficulty", 2: "Some Difficulty", 3: "A Lot of Difficulty", 4: "Cannot Do At All"})

df["DPCOUNSEL"] = df["DPCOUNSEL"].replace({1: "No", 2: "Yes"})

df["ANXIETYEV"] = df["ANXIETYEV"].replace({1: "No", 2: "Yes"})

df["WORFREQ"] = df["WORFREQ"].replace({1: "Daily", 2: "Weekly", 3: "Monthly", 4: "A Few Times A Year", 5: "Never"})

df["WORRX"] = df["WORRX"].replace({1: "No", 2: "Yes"})

df["WORFEELEVL"] = df["WORFEELEVL"].replace({1: "A Lot", 2: "A Little", 3: "Somewhere Between A Little And A Lot"})

df["DEPFREQ"] = df["DEPFREQ"].replace({1: "Daily", 2: "Weekly", 3: "Monthly", 4: "A Few Times A Year", 5: "Never"})

df["DEPFEELEVL"] = df["DEPFEELEVL"].replace({1: "A Lot", 2: "A Little", 3: "Somewhere Between A Little And A Lot"})

df["DEPRX"] = df["DEPRX"].replace({1: "No", 2: "Yes"})

df["SUPPORTCOMM"] = df["SUPPORTCOMM"].replace({1: "No", 2: "Yes"})

df["SATISFIED"] = df["SATISFIED"].replace({13: "Very Satisfied", 21: "Satisfied", 31: "Dissatisfied", 41: "Very Dissatisfied"})

df = df.applymap(lambda x: np.nan if isinstance(x, (int, np.integer)) else x)

# Split into adult and child DataFrames
child_df = df[df['Adult/Child'] == "Child"]
adult_df = df[df['Adult/Child'] == "Adult"]

adult_df['Group'] = 'Adult'
child_df['Group'] = 'Child'

child_df = child_df[["DEPFREQ", "FSSTAT", "RACENEW", "GOTSTAMPFAM", "REGION",
                     "SEX", "URBRRL", "WORFREQ", "ADLTPUTDOWN", "ALCDRUGEV", "BEHAVEDIF",
                     "FAMSTRUCSC", "JAILEV", "MKFRNDIF", "SUPPORTCOMM", "UNFAIRRACE"]]


adult_df = adult_df[["DEPFREQ", "FSSTAT", "RACENEW", "GOTSTAMPFAM", "REGION",
                     "SEX", "URBRRL", "WORFREQ", "DEPRESSEV", "DSOCIALP", "DPCOUNSEL",
                     "ANXIETYEV", "DEPRX", "DEPFEELEVL", "SATISFIED",
                     "SEXORIEN", "WORFEELEVL", "WORRX"]]
# Sidebar for group selection
st.sidebar.header("Filter Options")
group = st.sidebar.selectbox("Select Group:", ["Adult", "Child"], key="group_select")

# Filter the data based on the selected group
filtered_data = adult_df if group == "Adult" else child_df

# Sidebar for chart type selection (single feature or multiple features)
chart_type = st.sidebar.radio(
    "Select Chart Type:",
    ["Single Feature Chart", "Multiple Feature Chart"],
    key="chart_type_select"
)

# Feature selection for single feature chart
if chart_type == "Single Feature Chart":
    selected_feature_1 = st.sidebar.selectbox(
        "Select Feature to Visualize:", filtered_data.columns, key="feature_1_select"
    )

    # Display the filtered DataFrame
    st.write(f"Filtered Data for {group}:")
    st.dataframe(filtered_data)

    # Drop NaN values for the selected feature
    filtered_data = filtered_data.dropna(subset=[selected_feature_1])

    # Generate the bar chart for the selected feature
    try:
        chart_data = filtered_data[selected_feature_1].value_counts().reset_index()
        chart_data.columns = [selected_feature_1, 'Count']

        fig = px.bar(
            chart_data,
            x=selected_feature_1,
            y='Count',
            title=f"{selected_feature_1} Distribution for {group}",
            text='Count',  # Show counts on the bars
            color=selected_feature_1,  # Color bars based on the feature
            category_orders={selected_feature_1: sorted(chart_data[selected_feature_1].unique())}  # Optional: control color order
        )

        # Customize the chart
        fig.update_traces(textposition='outside')
        fig.update_layout(yaxis_title='Count', xaxis_title=selected_feature_1)

        # Display the chart
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error generating chart: {e}")

# Feature selection for multiple feature chart
if chart_type == "Multiple Feature Chart":
    # Allow the user to select two features for grouping
    selected_feature_1 = st.sidebar.selectbox(
        "Select the first feature to group by:", filtered_data.columns, key="feature_1_select_multi"
    )
    selected_feature_2 = st.sidebar.selectbox(
        "Select the second feature to group by:", filtered_data.columns, key="feature_2_select_multi"
    )

    # Checkbox for allowing selection of a specific value from the first feature
    filter_by_value = st.sidebar.checkbox(
        f"Filter by specific value from {selected_feature_1}?", key="filter_by_value_checkbox"
    )

    if filter_by_value:
        # If checkbox is selected, show a selectbox to pick a specific value
        feature_1_values = filtered_data[selected_feature_1].dropna().unique()
        selected_feature_1_value = st.sidebar.selectbox(
            f"Select specific value from {selected_feature_1}:", feature_1_values, key="feature_1_value_select"
        )

        # Filter the data based on the selected value from selected_feature_1
        filtered_data = filtered_data[filtered_data[selected_feature_1] == selected_feature_1_value]
    else:
        # If checkbox is not selected, use the entire dataset
        st.write(f"Showing all data for {selected_feature_1}.")

    # Display the filtered DataFrame
    st.write(f"Filtered Data for {group}:")
    st.dataframe(filtered_data)

    # Drop NaN values for the selected features
    filtered_data = filtered_data.dropna(subset=[selected_feature_1, selected_feature_2])

    # Group the data by both features and calculate the count
    grouped_data = filtered_data.groupby([selected_feature_1, selected_feature_2]).size().reset_index(name="Count")

    # Generate the bar chart for the grouped features
    try:
        fig = px.bar(
            grouped_data,
            x=selected_feature_1,
            y="Count",
            color=selected_feature_2,  # Color bars based on the second feature
            title=f"Distribution of {selected_feature_1} by {selected_feature_2} for {group}",
            labels={selected_feature_1: selected_feature_1, selected_feature_2: selected_feature_2, "Count": "Count"},
            barmode="group",  # Group bars by the second feature
            category_orders={selected_feature_2: sorted(grouped_data[selected_feature_2].unique())}  # Optional: control color order
        )

        # Customize the chart
        fig.update_traces(textposition='outside')
        fig.update_layout(yaxis_title='Count', xaxis_title=selected_feature_1)

        # Display the chart
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error generating chart: {e}")