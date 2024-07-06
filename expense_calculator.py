import streamlit as st
import pandas as pd
import altair as alt
from io import BytesIO
import base64

# Title of the app
st.title("Monthly Expense Calculator")

# Function to calculate total expenses
def calculate_total_expenses(expenses):
    return sum(expenses.values())

# Input total salary
total_salary = st.number_input("Enter your total salary:", min_value=1)

# Main expense categories
expense_categories = ["Housing", "Transportation", "Food", "Health", "Personal Care", "Entertainment", "Investment", "Miscellaneous"]

# Dictionary to store user inputs
user_expenses = {}

st.markdown('## Categories')
# Create two columns for expense inputs
col1, col2 = st.columns(2)

# Get user inputs for each category in separate columns
with col1:
    for category in expense_categories[:4]:
        user_expenses[category] = st.number_input(f"{category}:", min_value=0)

with col2:
    for category in expense_categories[4:]:
        user_expenses[category] = st.number_input(f"{category}:", min_value=0)

# Calculate total expenses
total_expenses = calculate_total_expenses(user_expenses)

# Calculate remaining balance
remaining_balance = total_salary - total_expenses

# Determine if savings are more than 40% of total salary
savings_percentage = (remaining_balance / total_salary) * 100

# Create two columns for the forms
form_col1, form_col2 = st.columns(2)

# Display summary in a form
with form_col1.form(key='summary_form'):
    st.header("Summary")
    st.write(f"**Total Salary:** ${total_salary:.2f}", unsafe_allow_html=True)
    st.write(f"**Total Expenses:** ${total_expenses:.2f}", unsafe_allow_html=True)
    st.write(f"**Remaining Balance:** ${remaining_balance:.2f}", unsafe_allow_html=True)
    
    if savings_percentage > 40:
        st.success("Congratulations! Your savings are more than 40% of your total salary.", icon='✅')
    elif 0 < savings_percentage <= 40:
        st.warning("You need to take care of your expenses ASAP.", icon='🚨')
    elif savings_percentage < 0:
        st.error("Worst expense management", icon="⚠️")
        
    st.form_submit_button("Submit")

# Display breakdown of expenses in a form with different fonts
with form_col2.form(key='breakdown_form'):
    st.header("Expense Breakdown")
    for category in expense_categories:
        st.markdown(f"<h4 style='font-family:Arial; font-size:16px;'>{category}: ${user_expenses[category]:.2f}</h4>", unsafe_allow_html=True)
    
    # Generate CSV download link
    csv_expenses = pd.DataFrame(user_expenses.items(), columns=['Expense', 'Amount'])
    csv_expenses_str = csv_expenses.to_csv(index=False)
    csv_expenses_encoded = base64.b64encode(csv_expenses_str.encode()).decode()
    href = f'<a href="data:file/csv;base64,{csv_expenses_encoded}" download="expenses.csv">Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)
    
    st.form_submit_button("Submit")

st.markdown(''' 
            <style>
            .st-emotion-cache-19rxjzo.ef3psqc7
            { 
                visibility: hidden;           
            }
            </style>
            ''', unsafe_allow_html=True)

# Display bar chart of expenses
st.header("Expenses Bar Chart")

expenses_df = pd.DataFrame(user_expenses.items(), columns=['Expense', 'Amount'])
bar_chart = alt.Chart(expenses_df).mark_bar().encode(
    x='Expense',
    y='Amount',
    color=alt.condition(
        alt.datum.Amount > 0,
        alt.value('green'),  # The positive color
        alt.value('red')  # The negative color
    )
).properties(
    width=600,
    height=400
)
chart = st.altair_chart(bar_chart, use_container_width=True)
