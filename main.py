# main.py

from flask import Flask, render_template, request
import tensorflow as tf
import nltk
import tensorflow_datasets as tfds
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os
import openpyxl
import csv
import tkinter as tk
import requests

app = Flask(__name__)
nltk.download("popular")
datasets = tfds.load("imdb_reviews", as_supervised=True)
pd.options.display.max_rows = 10
pd.options.display.float_format = "{:.1f}".format
sns.set()

def get_sentiments(review):
    # your code here
    sentiment = tf.constant([[1.0, 0.0]])
    return sentiment

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process_text", methods=["POST"])
def process_text():
    try:
        user_input = request.form["user-input"]
    except KeyError:
        return "BadRequestKeyError: user-input field not found in the request form"
    # rest of the code to process the user's input and return a response

directories = ['data_files/purchases', 'data_files/sales', 'data_files/variances']

def create_dataframe(directories):
    dataframes = []
    for directory in directories:
        for filename in os.listdir(directory):
            if filename.endswith(".xlsx"):
                file_path = os.path.join(directory, filename)
                df = pd.read_excel(file_path)
                dataframes.append(df)
    return pd.concat(dataframes)

df = create_dataframe(directories)


# gui

class ChatInterface(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Clarity Chatbot")

        # create chat window
        self.chat_window = tk.Text(self, height=20, width=50)
        self.chat_window.pack(pady=10)

        # create input field
        self.entry_field = tk.Entry(self, width=50)
        self.entry_field.pack(pady=10)
        self.entry_field.focus()

        # bind the enter key to the send_message method
        self.entry_field.bind("<Return>", self.send_message)

    def send_message(self, event=None):
        user_input = self.entry_field.get()

        # insert user's message into the chat window
        self.chat_window.insert(tk.END, "You: " + user_input + "\n")

        # clear the input field
        self.entry_field.delete(0, tk.END)

        # get response from chatbot and insert it into the chat window
        chatbot_response = self.get_response(user_input)
        self.chat_window.insert(tk.END, "Clarity: " + chatbot_response + "\n")

    def get_response(self, user_input):
        # make a request to the Flask app to get a response from the chatbot
        response = requests.get(f"http://localhost:5000/query?msg={user_input}")
        return response.text
  
if __name__ == "__main__":
    app = ChatInterface()
    app.run()
    app.mainloop()
