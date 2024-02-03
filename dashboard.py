import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from PIL import Image
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
from joblib import load


def regression_plot(data):
    model = load('model.joblib')
    input_data = load('input_data.joblib')

    y = data['price']
    y_pred = model.predict(input_data)

    fig, ax = plt.subplots(figsize=(10, 6))
    plt.scatter(y, y_pred)
    ax.set_xlabel('Predicted prices')
    ax.set_ylabel('Real prices')
    ax.set_title('Predicted vs real prices')
    plt.plot([min(y), max(y)], [min(y_pred), max(y_pred)], color='red')
    st.pyplot(fig)


def regression_visualisation(col):
    model = load('model.joblib')
    input_data = load('input_data.joblib')

    predicted_prices = model.predict(input_data)
    carat_values = input_data[col]

    fig, ax = plt.subplots(figsize=(10, 6))
    plt.scatter(carat_values, predicted_prices, label='Model Prediction')
    ax.set_xlabel(capitalize(col))
    ax.set_ylabel('Predicted price')
    ax.set_title(f'The impact of {col} on the predicted price')
    plt.legend()
    st.pyplot(fig)

def show_qualities_by_attribute(data, attribute, value, what):
    filtered_data = data[data[attribute] == value]
    min_val = filtered_data[what].min()
    max_val = filtered_data[what].max()
    median = round(filtered_data[what].median(), 2)
    mean = round(filtered_data[what].mean(), 2)

    st.write(f"Minimum {what} in Diamonds with {value} {attribute} is {min_val}")
    st.write(f"Maximum {what} in Diamonds with {value} {attribute} is {max_val}")
    st.write(f"Median {what} in Diamonds with {value} {attribute} is {median}")
    st.write(f"Avarage {what} in Diamonds with {value} {attribute} is {mean}")

def welcome(data):
    st.header("Welcome to the diamonds data dashboard!")
    st.text("Here you can explore the data concerning data about diamonds and its qualities.")
    st.text("Take a look at the data we are dealing with.")
    st.write(data)

def capitalize(string):
    return string[0].upper() + string[1:]

def display_medians(data, cols):
    for col in cols:
        median = data[col].median()
        st.text(f"{capitalize(col)} median is: {median}")

def display_avarages(data, cols):
    for col in cols:
        avg = round(data[col].mean(), 3)
        st.text(f"{capitalize(col)} avarage is: {avg}")

def pie_chart(data, column, title):
    labels = data[column].value_counts().index
    values = data[column].value_counts().values
    fig = go.Figure(go.Pie(labels=labels, values=values, name=column))
    fig.update_layout(title_text=title)
    return fig

def attribute_with_slider(data, column, title):
    st.header(title)
    min_value = data[column].min()
    max_value = data[column].max()
    value = st.slider(f"See how many diamonds have value of {column} equal or bigger", min_value, max_value)
    count = data[data[column] >= value].shape[0]
    st.info(f"{count} diamonds have value of {column} equal or bigger then {value}")

st.set_page_config(layout = "wide")

st.title(":gem: Diamonds data analysis :gem:")
st.header("Author: Agata Załęska")

path = './'
data = pd.read_csv(f"{path}/clean_data.csv")
columns = data.columns.tolist()
columns_no_price = columns.remove('price')

selected = option_menu(
    menu_title=None,
    options=['Home', 'Data distribution', 'Price and other variables', 'Regresison model'],
    icons=['gem', 'bar-chart', 'cash-coin', 'graph-up-arrow'],
    menu_icon='cast',
    default_index=0,
    orientation='horizontal'
)

if selected == "Home":
    welcome(data)
    st.header("Take a look at the diamonds numeric atributes!")
    numeric_cols = ['carat', 'x dimension', 'y dimension', 'z dimension', 'depth', 'price']
    non_numeric_columns = ["cut", "color", "clarity", "table"]
    choice = st.radio("Display each numeric attribute's", ("Nothing", "Avarage", "Median"))

    if choice == "Avarage":
        display_avarages(data, numeric_cols)
    if choice == "Median":
        display_medians(data, numeric_cols)

    for col in numeric_cols:
        attribute_with_slider(data, col, f"{capitalize(col)} :sparkles:")

    st.header("See some statistic in chosen diamonds cathegories!")
    cat = st.selectbox("pick cathegory", non_numeric_columns)
    value = st.selectbox("pick the value", data[cat].unique())
    var = st.selectbox("pick variable to display", numeric_cols)
    show_qualities_by_attribute(data, cat, value, var)



if selected == "Data distribution":
    st.header("Lets take a look at the variables and their values")
    st.text("Some diamonds characteristics can be divided into categories.")
    st.text("The cut, color and quality are categorical variables.")
    st.text("Their distribution can be nicely observed on pie charts.")

    non_numeric_columns = ["cut", "color", "clarity", "table"]
    non_numeric_capital = [capitalize(c) for c in non_numeric_columns]
    display = st.multiselect("What would you like to see?", non_numeric_capital)

    for i, name in enumerate(non_numeric_capital):
        col_name = non_numeric_columns[i]
        if name in display:
            st.plotly_chart(pie_chart(data, col_name, f"{name} Distribution"))

    st.header("Display histogram with distribution of any variable")
    var = st.selectbox("pick variable", columns)
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.histplot(x=data[var], bins=30)
    ax.set_title(f'{var} distribution')
    ax.set_xlabel(str(var))
    ax.set_ylabel('number of occurences')

    st.pyplot(fig)

if selected == "Price and other variables":
    st.header("Select the variable to show how the price depends on it")
    var = st.selectbox("variable", columns)

    fig, ax = plt.subplots(figsize=(10, 6))
    plt.scatter(data[var], data['price'], alpha=0.6)
    ax.set_title(f"how the diamond's price depends on its {var}")
    ax.set_xlabel(str(var))
    ax.set_ylabel('price')
    plt.grid(True)

    st.pyplot(fig)

if selected == "Regresison model":
    st.header("See the linear regression visualisation")
    regression_plot(data)
    st.markdown('### How does carat impact on the predicted price?')
    regression_visualisation('carat')
    st.markdown('### How does x dimension impact on the predicted price?')
    regression_visualisation('x dimension')
