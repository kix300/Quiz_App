import tkinter as tk
from tkinter import ttk
import random
import pandas as pd

class QuizApp:
    def __init__(self, root):
        self.good_answers = 0
        self.root = root
        self.root.title("Quiz App")
        self.root.config(bg="#26242f")

        self.question_var = tk.StringVar()
        self.question_label = ttk.Label(root, textvariable=self.question_var, font=("Helvetica", 14), wraplength=500)
        self.question_label.pack(pady=20)
        self.question_label.config(background="#26242f",foreground='white')

        self.options_frame = tk.Frame(root,bg="#26242f",width=10)
        self.options_frame.pack(pady=10)

        self.next_button = tk.Button(root,text="Suivant",bg="#26242f",fg='white',width=10, command=self.next_question)
        self.next_button.pack(pady=20)
     

        self.good_answers = 0
        self.question_counter = 0

        # Load the questions from the Excel file
        self.all_questions_data = self.load_questions_from_excel("quizz.xlsx")
    

        self.used_questions = []
        self.next_question()

    def load_questions_from_excel(self, file_path):
        data = pd.read_excel(file_path)
        questions_data = []
        for _, row in data.iterrows():
            question = row["Question"]
            correct_answer = row["Bonne réponse"]
            wrong_answers = [row["Mauvaise réponse 1"], row["Mauvaise réponse 2"], row["Mauvaise réponse 3"]]
            questions_data.append({"question": question, "reponses":wrong_answers + [correct_answer]  })
        return questions_data
    
    def next_question(self):
        if not self.all_questions_data:
            self.display_result()
            return

        question_data = random.choice(self.all_questions_data)
        self.all_questions_data.remove(question_data)
        self.used_questions.append(question_data)
        self.question_counter += 1

        self.question_var.set(question_data["question"])

        # Display the options for answers
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        for idx, option in enumerate(question_data["reponses"]):
            option_button = tk.Button(self.options_frame, text=option,width=10,bg="#26242f",fg='white', command=lambda o=option: self.check_answer(o, question_data["reponses"][0]))
            option_button.grid(row=idx, column=0, padx=5, pady=5)

    def check_answer(self, selected_answer, correct_answer):
        if selected_answer == correct_answer and self.good_answers <5 :
            self.good_answers += 1
        self.next_question()

    def display_result(self):
        total_questions = self.question_counter
        correct_answers = self.good_answers
        incorrect_answers = total_questions - correct_answers

        result_text = f"Vous avez terminé le quiz !\n\nRésultat : {correct_answers}/{total_questions}\n\nListe des questions incorrectes :"
        for question_data in self.used_questions:
            selected_answer = question_data["reponses"][0]
            correct_answer = question_data["reponses"][0]
            if selected_answer != correct_answer:
                result_text += f"\n\nQuestion : {question_data['question']}\nVotre réponse : {selected_answer}\nRéponse correcte : {correct_answer}"

        self.question_var.set(result_text)
        self.next_button.config(state=tk.DISABLED)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('400x400')
    app = QuizApp(root)
    
    root.mainloop()