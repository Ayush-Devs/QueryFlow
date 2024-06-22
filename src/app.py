from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3

import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

prompt = [
    """
    You are an expert in converting English questions to SQL query!
    
    The SQL database has the name GAME and has the following columns - Name,genre,price,offline,single player,ratings,developer
    \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM GAME ;
    \nExample 2 - Tell me all the offline games, 
    the SQL command will be something like this SELECT * FROM GAME 
    where offline="yes"; 
    \nExample 3 - insert "Red Dead Redemption 2","Action-adventure",59,"yes","yes",5,"Rockstar Games", 
    the SQL command will be something like this '''Insert Into GAME values("Red Dead Redemption 2","Action-adventure",59,"yes","yes",5,"Rockstar Games")'''
    \nExample 2 - Tell me all the offline games, 
    the SQL command will be something like this SELECT * FROM GAME 
    where price=0;
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]

st.set_page_config(page_title="QueryFlow")
st.sidebar.header("Gemini App To Retrieve SQL Data")  # Place heading in the sidebar
question = st.sidebar.text_input("Input: ", key="input")  # Place text input in the sidebar
submit = st.sidebar.button("Query")  # Place button in the sidebar

if submit:
    try:
        response = get_gemini_response(question, prompt)
        st.write("Gemini Response:")
        st.write(response)
        if response.lower().startswith("select"):
            results = read_sql_query(response, "game.db")
            st.subheader("SQL Query Results:")
            for row in results:
                st.write(row)
    except Exception as e:
        st.error(f"Error processing query: {str(e)}")
