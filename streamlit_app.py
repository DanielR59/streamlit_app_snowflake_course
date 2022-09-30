
import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

def get_frutyvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    #streamlit.text(fruityvice_response.json())
    # write your own comment -what does the next line do? 
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    # write your own comment - what does this do?
    return fruityvice_normalized


my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
streamlit.title("My Parents New Healty Diner")

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocker Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast' )

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)
#New Section
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get infromation")
  else:

    streamlit.dataframe(get_frutyvice_data(fruit_choice))
       
    streamlit.write('The user entered ', fruit_choice)
except URLError as e:
    streamlit.error()  




#streamlit.text("Hello from Snowflake:")
streamlit.header("The fruit load list contains:")

def get_fruit_list():
    with my_cnx.cursor() as my_cur:
        #my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
        my_cur.execute("SELECT * FROM fruit_load_list")
        my_data_rows = my_cur.fetchall()
        return my_data_rows
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("INSERT INTO fruit_load_list values ('"+ new_fruit + "')")
        return 'Thanks for adding ', new_fruit
    
new_fruit_choice = streamlit.text_input('What fruit would you add?')
if streamlit.button('Add a fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    streamlit.text(insert_row_snowflake(new_fruit_choice))
    my_cnx.close()




