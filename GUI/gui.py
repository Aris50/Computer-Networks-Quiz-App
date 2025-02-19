import tkinter
from controller.controller import Controller
from tkinter import *
import random

class GUI:
    def __init__(self):
        self.__controller = Controller()

        # Declare the window attribute, set the welcoming label
        self.__window = tkinter.Tk()
        self.__label = tkinter.Label(self.__window, text="Welcome to the Quiz App", font=("Arial", 24), width=50, height=5, fg="black")
        self.__label.place(x=400, y=10)
        self.__label.configure(bg="#f5f5f5")  # Very white-ish background

        # Set window
        self.__window.geometry("1400x800")
        self.__window.title("Computer Networks: Quiz-App")
        self.__window.configure(bg="#f5f5f5")  # Very white-ish background

        # Set the app icon
        self.__icon = PhotoImage(file='iconimg.png')
        self.__window.iconphoto(True, self.__icon)

        # Create a listbox for questions
        self.__question_listbox = Listbox(self.__window, bg="#f5f5f5", font=("Arial", 12), width=50, height=20, fg="black")
        self.__question_listbox.place(x=10, y=10)

        # Add items to the question Listbox
        data = self.__controller.get_data()
        questions = list(data.values())
        random.shuffle(questions)
        for question in questions:
            self.__question_listbox.insert(END, question['question'])

        # Create a frame for answer checkboxes
        self.__answer_frame = Frame(self.__window, bg="#f5f5f5")
        self.__answer_frame.place(x=500, y=10)

        # Function to update answer checkboxes
        def update_answers(event):
            for widget in self.__answer_frame.winfo_children():
                widget.destroy()
            selected_index = self.__question_listbox.curselection()
            if selected_index:
                selected_question = questions[selected_index[0]]
                answers = selected_question['answers']
                for answer in answers:
                    var = IntVar()
                    Checkbutton(self.__answer_frame, text=answer, variable=var, bg="#f5f5f5", font=("Arial", 12), fg="black").pack(anchor=W)

        # Bind the selection event to the update_answers function
        self.__question_listbox.bind('<<ListboxSelect>>', update_answers)

    def run(self):
        self.__window.mainloop()