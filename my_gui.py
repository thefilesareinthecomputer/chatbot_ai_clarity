# my_gui.py

import tkinter as tk
import requests

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
    app.mainloop()
