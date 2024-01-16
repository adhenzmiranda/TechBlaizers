import tkinter as tk
from html import unescape
import random
from tkinter import font
import requests
import customtkinter as ctk

class App(tk.Tk):
    def __init__(self, title):
        """
        Initializes the object with a given title.

        Parameters:
            title (str): The title of the object.

        Returns:
            None
        """
        super().__init__()
        self.styles = Styles()
        self.title(title)
        self.configure(bg='#4E55FF')
        self.score = 0
        self.startmenu = StartTriviaMenu(self, self.styles)
        self.resizable(False, False)
        self.iconbitmap('Images/logo/logo-ico.ico')
        self.mainloop()
    def reset_app(self):
        """
        Reset the app by destroying all widgets.

        Parameters:
            None
        
        Returns:
            None

        Pseudocode:
            1. Loop through each widget in the app's children
            2. Destroy the widget
        """
        for widget in self.winfo_children():
            widget.destroy()

class Styles:
    def __init__(self):
        """
        Initializes the class and sets the initial values for the instance variables.

        Parameters:
            self (object): The instance of the class.
        
        Returns:
            None
        """
        self.h1 = font.Font(family='DFMaruGothic StdN W7', size=35, weight='bold')
        self.p = font.Font(family='DFMaruGothic StdN W7', size=20)
        # Tech Trivia
        self.logo = tk.PhotoImage(file='Images/logo/logo-main.png')
        self.logo_small = tk.PhotoImage(file='Images/logo/logo-small.png')

class StartTriviaMenu(tk.Frame):
    def __init__(self, parent, styles):  
        """
        Initializes the object with the given parent widget and styles.

        Parameters:
            parent (Widget): The parent widget.
            styles (Styles): The styles object.

        Returns:
            None
        """
        super().__init__(parent)
        self.styles = styles
        self.h1 = self.styles.h1
        self.p = self.styles.p
        self.logo = self.styles.logo
        self.configure(bg='#4E55FF')
        self.grid(row=0, sticky='ew')
        self.create_widgets()

    def create_widgets(self):
        """
        Creates and configures the widgets for the GUI.

        Returns:
            None
        """
        # Frame
        main_frame = tk.Frame(self, bg='#4E55FF')
        main_frame.columnconfigure(0, weight=1)
        main_frame.grid(row=0)
        
        # Logo Image
        # Label
        tk.Label(
            main_frame,
            font=self.h1,
            compound='top',
            image=self.logo,
            text='TechBlaizer',
            bg='#4E55FF',
            fg='#fff'
        ).grid(
            row=0,
            pady=5,
        )

        tk.Label(
            main_frame,
            font=self.p,
            text='A Tech and Science\nTrivia Game',
            bg='#4E55FF',
            fg='#fff'
        ).grid(
            row=1,
        )

        ctk.CTkButton(
            main_frame,
            text='Start',
            corner_radius=10,
            fg_color='#F46146',
            font=('DFMaruGothic StdN W7', 20),
            hover_color=('#F46146', '#DC573F'),
            command=self.startapp
        ).grid(
            pady=10,
            row=2
        )

    def startapp(self):
        """
        Start the app by hiding the current grid and creating a new instance of the MainTriviaMenu class.

        Parameters:
            None

        Returns:
            None
        """
        self.grid_forget()
        self.mainmenu = MainTriviaMenu(self.master, self.styles, self.master.score)

class MainTriviaMenu(tk.Frame):
    def __init__(self, parent, styles, score):
        """
        Initializes an instance of the class.

        Args:
            parent: The parent widget.
            styles: The styles used for the widgets.
            score: The score value.

        Returns:
            None.
        """
        super().__init__(parent)
        self.styles = styles
        self.p = self.styles.p
        self.score = score
        self.grid(row=0, sticky='ew')
        self.create_widgets()

    def create_widgets(self):
        """
        Creates and configures the widgets for the user interface of the application.

        Parameters:
        - None

        Returns:
        - None
        """
        main_frame = tk.Frame(self, bg='#4E55FF')
        main_frame.columnconfigure(0, weight=1)

        main_frame.grid(row=0, column=0, sticky='ew')
        
        tk.Label(
            main_frame,
            font=self.styles.p,
            text='Select Difficulty',
            bg='#4E55FF',
            fg='#fff'
        ).grid(
            row=0,
            pady=5,
            sticky='ew'
        )
        self.diff = ctk.CTkComboBox(
            main_frame,
            font=('DFMaruGothic StdN W7', 20),
            values=[
                'Easy',
                'Medium',
                'Hard'
            ],
            width=300
        )
        self.diff.grid(
            row=1,
            pady=5,
            sticky='ew',
            ipady = 5
        )

        tk.Label(
            main_frame,
            font=self.styles.p,
            text='Select Category',
            bg='#4E55FF',
            fg='#fff'
        ).grid(
            row=2,
            sticky='ew'
        )

        self.category = ctk.CTkComboBox(
            main_frame,
            font=('DDFMaruGothic StdN W7', 20),
            values=[
                'Science: Computers',
                'Science: Gadgets',
                'Science: Nature',
                'Science: Mathematics',
                'Science: Geography'
            ],
            width=300
        )
        self.category.grid(
            row=3,
            sticky='ew',
            ipady = 5
        )

        ctk.CTkButton(
            main_frame,
            text='Start',
            corner_radius=10,
            fg_color='#F46146',
            font=('DDFMaruGothic StdN W7', 20),
            hover_color=('#F46146', '#DC573F'),
            command=self.startquiz
        ).grid(
            row=4,
            pady=10,
        )

    def startquiz(self):
        """
        Starts the quiz by retrieving quiz questions from an API based on the selected category and difficulty level.

        Parameters:
            self (Quiz): The Quiz object.
        
        Returns:
            None
        """
        # dictionary

        # convert combobox string to lowercase
        diff_link = self.diff.get()
        print(diff_link)
        diff_link = diff_link.lower()  # Updated line
        print(diff_link)

        category_dict = {
            "Science: Computers": 18,
            "Science: Gadgets": 30,
            "Science: Nature": 17,
            "Science: Mathematics": 19,
            "Science: Geography": 22
        }
        self.selected_subject = self.category.get()
        print(self.selected_subject)
        category_id = category_dict[self.selected_subject]

        api_url = f'https://opentdb.com/api.php?amount=5&category={category_id}&difficulty={diff_link}&type=multiple'
        print(api_url)
        quiz_json_url = requests.get(api_url)
        print(quiz_json_url.status_code)
        self.mainmenu = Question_1(self.master, self.styles, quiz_json_url, self.score, self.selected_subject)
        self.grid_forget()

class Question_1(tk.Frame):
    def __init__(self, parent, styles, quiz_json_url, score, selected_subject):
        """
        Initializes the object of the class.

        Parameters:
        - parent: The parent widget.
        - styles: A dictionary of styles.
        - quiz_json_url: The URL of the quiz JSON.
        - score: The current score.
        - selected_subject: The selected subject.

        Returns:
        None
        """
        super().__init__(parent)
        self.grid(row=0, sticky='ew')
        self.styles = styles
        self.quiz_json_url = quiz_json_url
        self.score = score
        self.selected_subject= selected_subject
        self.create_widgets()

    def create_widgets(self):
        # Frames
        main_frame = tk.Frame(self, bg='#4E55FF')
        main_frame.grid(row=0, column=0, sticky='ew')

        left_frame = tk.Frame(main_frame, bg='#4E55FF')
        left_frame.grid(row=1, column=0, sticky='ew')
        right_frame = tk.Frame(main_frame, bg='#4E55FF')
        right_frame.grid(row=1, column=1, sticky='ew')
        bottom_frame = tk.Frame(main_frame, bg='#4E55FF')
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky='ew')


        # JSON file
        quiz_data = self.quiz_json_url.json()
        question = unescape(quiz_data['results'][0]['question'])

        # Subject Title
        category_label = tk.Label(
            main_frame,
            image=self.styles.logo_small,
            compound='top',
            font=self.styles.p,
            text=f'Category: {self.selected_subject}',
            bg='#4E55FF',
            fg='#fff',
            anchor='center'
        )
        category_label.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=5,
            sticky='ew'
        )

        # Question
        tk.Label(
            left_frame,
            font=self.styles.p,
            text=question,
            bg='#4E55FF',
            fg='#fff',
            wraplength=400,
            anchor='w'
        ).grid(
            row=0,
            columnspan=2,
            pady=5,
            sticky='ew'
        )

        correct_answer = unescape(quiz_data['results'][0]['correct_answer'])
        print(correct_answer)
        incorrect_answers = [unescape(answer) for answer in quiz_data['results'][0]['incorrect_answers']]
        print(incorrect_answers)

        # Combine the correct and incorrect answers into one list
        answer_choices = [correct_answer] + incorrect_answers
        print(answer_choices)

        # Shuffle the answer choices
        random.shuffle(answer_choices)

        grid_index = 0
        for choice in answer_choices:
            ctk.CTkButton(
                right_frame,
                text=choice,
                command=lambda choice=choice: self.check_answer(choice, correct_answer, main_frame, right_frame),
                font=('DDFMaruGothic StdN W7', 20),
                fg_color='#F46146',
                hover_color=('#F46146', '#DC573F'),
                corner_radius=10
            ).grid(
                row=grid_index,  # Use grid_index directly for the row
                column=0,  # Set the column to 0
                pady=5,
                padx=5,
                sticky='ew',
                ipadx=5,
                ipady=10,
            )
            grid_index += 1

    def check_answer(self, selected_choice, correct_answer, main_frame, right_frame):
        for button in right_frame.winfo_children():
            if isinstance(button, ctk.CTkButton):
                button.configure(state=tk.DISABLED)
        if selected_choice == correct_answer:
            self.score += 1
            print(self.score)
            tk.Label(
                main_frame,
                bg='#4E55FF',
                fg='#fff',
                font=self.styles.p,
                text=f'Correct! it is indeed {correct_answer}!',
                wraplength=400
            ).grid(
                row=4,
                columnspan=2,
                sticky='ew'
            )

            ctk.CTkButton(
                main_frame,
                text='Next',
                command=self.next_q,
                bg_color='#4E55FF',
                font=('DDFMaruGothic StdN W7', 20),
                fg_color='#F46146',
                hover_color=('#F46146', '#DC573F'),
                corner_radius=10
            ).grid(
                row=5,
                columnspan=2,
                pady=5,
                
            )
        else:
            tk.Label(
                main_frame,
                bg='#4E55FF',
                fg='#fff',
                font=self.styles.p,
                text=f'Incorrect! The correct answer is:  {correct_answer}!',
                wraplength=400
            ).grid(
                row=4,
                columnspan=2
            )
            ctk.CTkButton(
                main_frame,
                text='Next',
                command=self.next_q,
                bg_color='#4E55FF',
                font=('DDFMaruGothic StdN W7', 20),
                fg_color='#F46146',
                hover_color=('#F46146', '#DC573F'),
                corner_radius=10
            ).grid(
                row=5,
                columnspan=2,
                pady=5,
            )
            # self.next_q()

    def next_q(self):
        self.question_2 = Question_2(self.master, self.styles, self.quiz_json_url, self.score, self.selected_subject)
        self.grid_forget()

class Question_2(tk.Frame):
    def __init__(self, parent, styles, quiz_json_url, score, selected_subject):
        super().__init__(parent)
        self.grid(row=0, sticky='ew')
        self.styles = styles
        self.quiz_json_url = quiz_json_url
        self.score = score
        self.selected_subject= selected_subject
        self.create_widgets()

    def create_widgets(self):
        # Frames
        main_frame = tk.Frame(self, bg='#4E55FF')
        main_frame.grid(row=0, column=0, sticky='ew')

        left_frame = tk.Frame(main_frame, bg='#4E55FF')
        left_frame.grid(row=1, column=0, sticky='ew')
        right_frame = tk.Frame(main_frame, bg='#4E55FF')
        right_frame.grid(row=1, column=1, sticky='ew')
        bottom_frame = tk.Frame(main_frame, bg='#4E55FF')
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky='ew')


        # JSON file
        quiz_data = self.quiz_json_url.json()
        question = unescape(quiz_data['results'][1]['question'])

        # Subject Title
        category_label = tk.Label(
            main_frame,
            image=self.styles.logo_small,
            compound='top',
            font=self.styles.p,
            text=f'Category: {self.selected_subject}',
            bg='#4E55FF',
            fg='#fff',
            anchor='center'
        )
        category_label.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=5,
            sticky='ew'
        )

        # Question
        tk.Label(
            left_frame,
            font=self.styles.p,
            text=question,
            bg='#4E55FF',
            fg='#fff',
            wraplength=400,
            anchor='w'
        ).grid(
            row=0,
            columnspan=2,
            pady=5,
            sticky='ew'
        )

        correct_answer = unescape(quiz_data['results'][1]['correct_answer'])
        print(correct_answer)
        incorrect_answers = [unescape(answer) for answer in quiz_data['results'][1]['incorrect_answers']]
        print(incorrect_answers)

        # Combine the correct and incorrect answers into one list
        answer_choices = [correct_answer] + incorrect_answers
        print(answer_choices)

        # Shuffle the answer choices
        random.shuffle(answer_choices)

        grid_index = 0
        for choice in answer_choices:
            ctk.CTkButton(
                right_frame,
                text=choice,
                command=lambda choice=choice: self.check_answer(choice, correct_answer, main_frame, right_frame),
                font=('DDFMaruGothic StdN W7', 20),
                fg_color='#F46146',
                hover_color=('#F46146', '#DC573F'),
                corner_radius=10
            ).grid(
                row=grid_index,  # Use grid_index directly for the row
                column=0,  # Set the column to 0
                pady=5,
                padx=5,
                sticky='ew',
                ipadx=5,
                ipady=10,
            )
            grid_index += 1

    def check_answer(self, selected_choice, correct_answer, main_frame, right_frame):
        for button in right_frame.winfo_children():
            if isinstance(button, ctk.CTkButton):
                button.configure(state=tk.DISABLED)
        if selected_choice == correct_answer:
            self.score += 1
            print(self.score)
            tk.Label(
                main_frame,
                bg='#4E55FF',
                fg='#fff',
                font=self.styles.p,
                text=f'Correct! it is indeed {correct_answer}!',
                wraplength=400
            ).grid(
                row=4,
                columnspan=2,
                sticky='ew'
            )

            ctk.CTkButton(
                main_frame,
                text='Next',
                command=self.next_q,
                bg_color='#4E55FF',
                font=('DDFMaruGothic StdN W7', 20),
                fg_color='#F46146',
                hover_color=('#F46146', '#DC573F'),
                corner_radius=10
            ).grid(
                row=5,
                columnspan=2,
                pady=5,
            )
        else:
            tk.Label(
                main_frame,
                bg='#4E55FF',
                fg='#fff',
                font=self.styles.p,
                text=f'Incorrect! The correct answer is:  {correct_answer}!',
                wraplength=400
            ).grid(
                row=4,
                columnspan=2
            )
            ctk.CTkButton(
                main_frame,
                text='Next',
                command=self.next_q,  # Use self.next_q instead of next_q
                bg_color='#4E55FF',
                font=('DDFMaruGothic StdN W7', 20),
                fg_color='#F46146',
                hover_color=('#F46146', '#DC573F'),
                corner_radius=10
            ).grid(
                row=5,
                columnspan=2,
                pady=5,
            )
            # self.next_q()

    def next_q(self):
        self.question_3 = Question_3(self.master, self.styles, self.quiz_json_url, self.score, self.selected_subject)
        self.grid_forget()
class Question_3(tk.Frame):
    def __init__(self, parent, styles, quiz_json_url, score, selected_subject):
        super().__init__(parent)
        self.grid(row=0, sticky='ew')
        self.styles = styles
        self.quiz_json_url = quiz_json_url
        self.score = score
        self.selected_subject= selected_subject
        self.create_widgets()

    def create_widgets(self):
        # Frames
        main_frame = tk.Frame(self, bg='#4E55FF')
        main_frame.grid(row=0, column=0, sticky='ew')

        left_frame = tk.Frame(main_frame, bg='#4E55FF')
        left_frame.grid(row=1, column=0, sticky='ew')
        right_frame = tk.Frame(main_frame, bg='#4E55FF')
        right_frame.grid(row=1, column=1, sticky='ew')
        bottom_frame = tk.Frame(main_frame, bg='#4E55FF')
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky='ew')


        # JSON file
        quiz_data = self.quiz_json_url.json()
        question = unescape(quiz_data['results'][2]['question'])

        # Subject Title
        category_label = tk.Label(
            main_frame,
            image=self.styles.logo_small,
            compound='top',
            font=self.styles.p,
            text=f'Category: {self.selected_subject}',
            bg='#4E55FF',
            fg='#fff',
            anchor='center'
        )
        category_label.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=5,
            sticky='ew'
        )

        # Question
        tk.Label(
            left_frame,
            font=self.styles.p,
            text=question,
            bg='#4E55FF',
            fg='#fff',
            wraplength=400,
            anchor='w'
        ).grid(
            row=0,
            columnspan=2,
            pady=5,
            sticky='ew'
        )

        correct_answer = unescape(quiz_data['results'][2]['correct_answer'])
        print(correct_answer)
        incorrect_answers = [unescape(answer) for answer in quiz_data['results'][2]['incorrect_answers']]
        print(incorrect_answers)

        # Combine the correct and incorrect answers into one list
        answer_choices = [correct_answer] + incorrect_answers
        print(answer_choices)

        # Shuffle the answer choices
        random.shuffle(answer_choices)

        grid_index = 0
        for choice in answer_choices:
            ctk.CTkButton(
                right_frame,
                text=choice,
                command=lambda choice=choice: self.check_answer(choice, correct_answer, main_frame, right_frame),
                font=('DDFMaruGothic StdN W7', 20),
                fg_color='#F46146',
                hover_color=('#F46146', '#DC573F'),
                corner_radius=10
            ).grid(
                row=grid_index,  # Use grid_index directly for the row
                column=0,  # Set the column to 0
                pady=5,
                padx=5,
                sticky='ew',
                ipadx=5,
                ipady=10,
            )
            grid_index += 1

    def check_answer(self, selected_choice, correct_answer, main_frame, right_frame):
        for button in right_frame.winfo_children():
            if isinstance(button, ctk.CTkButton):
                button.configure(state=tk.DISABLED)
        if selected_choice == correct_answer:
            self.score += 1
            print(self.score)
            tk.Label(
                main_frame,
                bg='#4E55FF',
                fg='#fff',
                font=self.styles.p,
                text=f'Correct! it is indeed {correct_answer}!',
                wraplength=400
            ).grid(
                row=4,
                columnspan=2,
                sticky='ew'
            )

            ctk.CTkButton(
                main_frame,
                text='Next',
                command=self.next_q,
                bg_color='#4E55FF',
                font=('DDFMaruGothic StdN W7', 20),
                fg_color='#F46146',
                hover_color=('#F46146', '#DC573F'),
                corner_radius=10
            ).grid(
                row=5,
                columnspan=2,
                pady=5,
            )
        else:
            tk.Label(
                main_frame,
                bg='#4E55FF',
                fg='#fff',
                font=self.styles.p,
                text=f'Incorrect! The correct answer is:  {correct_answer}!',
                wraplength=400
            ).grid(
                row=4,
                columnspan=2
            )
            ctk.CTkButton(
                main_frame,
                text='Next',
                command=self.next_q,  # Use self.next_q instead of next_q
                bg_color='#4E55FF',
                font=('DDFMaruGothic StdN W7', 20),
                fg_color='#F46146',
                hover_color=('#F46146', '#DC573F'),
                corner_radius=10
            ).grid(
                row=5,
                columnspan=2,
                pady=5,
            )
            # self.next_q()

    def next_q(self):
        self.question_4 = Question_4(self.master, self.styles, self.quiz_json_url, self.score, self.selected_subject)
        self.grid_forget()
class Question_4(tk.Frame):
    def __init__(self, parent, styles, quiz_json_url, score, selected_subject):
        super().__init__(parent)
        self.grid(row=0, sticky='ew')
        self.styles = styles
        self.quiz_json_url = quiz_json_url
        self.score = score
        self.selected_subject= selected_subject
        self.create_widgets()

    def create_widgets(self):
        # Frames
        main_frame = tk.Frame(self, bg='#4E55FF')
        main_frame.grid(row=0, column=0, sticky='ew')

        left_frame = tk.Frame(main_frame, bg='#4E55FF')
        left_frame.grid(row=1, column=0, sticky='ew')
        right_frame = tk.Frame(main_frame, bg='#4E55FF')
        right_frame.grid(row=1, column=1, sticky='ew')
        bottom_frame = tk.Frame(main_frame, bg='#4E55FF')
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky='ew')


        # JSON file
        quiz_data = self.quiz_json_url.json()
        question = unescape(quiz_data['results'][3]['question'])

        # Subject Title
        category_label = tk.Label(
            main_frame,
            image=self.styles.logo_small,
            compound='top',
            font=self.styles.p,
            text=f'Category: {self.selected_subject}',
            bg='#4E55FF',
            fg='#fff',
            anchor='center'
        )
        category_label.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=5,
            sticky='ew'
        )

        # Question
        tk.Label(
            left_frame,
            font=self.styles.p,
            text=question,
            bg='#4E55FF',
            fg='#fff',
            wraplength=400,
            anchor='w'
        ).grid(
            row=0,
            columnspan=2,
            pady=5,
            sticky='ew'
        )

        correct_answer = unescape(quiz_data['results'][3]['correct_answer'])
        print(correct_answer)
        incorrect_answers = [unescape(answer) for answer in quiz_data['results'][3]['incorrect_answers']]
        print(incorrect_answers)

        # Combine the correct and incorrect answers into one list
        answer_choices = [correct_answer] + incorrect_answers
        print(answer_choices)

        # Shuffle the answer choices
        random.shuffle(answer_choices)

        grid_index = 0
        for choice in answer_choices:
            ctk.CTkButton(
                right_frame,
                text=choice,
                command=lambda choice=choice: self.check_answer(choice, correct_answer, main_frame, right_frame),
                font=('DDFMaruGothic StdN W7', 20),
                fg_color='#F46146',
                hover_color=('#F46146', '#DC573F'),
                corner_radius=10
            ).grid(
                row=grid_index,  # Use grid_index directly for the row
                column=0,  # Set the column to 0
                pady=5,
                padx=5,
                sticky='ew',
                ipadx=5,
                ipady=10,
            )
            grid_index += 1

    def check_answer(self, selected_choice, correct_answer, main_frame, right_frame):
        for button in right_frame.winfo_children():
            if isinstance(button, ctk.CTkButton):
                button.configure(state=tk.DISABLED)
        if selected_choice == correct_answer:
            self.score += 1
            print(self.score)
            tk.Label(
                main_frame,
                bg='#4E55FF',
                fg='#fff',
                font=self.styles.p,
                text=f'Correct! it is indeed {correct_answer}!',
                wraplength=400
            ).grid(
                row=4,
                columnspan=2,
                sticky='ew'
            )

            ctk.CTkButton(
                main_frame,
                text='Next',
                command=self.next_q,
                bg_color='#4E55FF',
                font=('DDFMaruGothic StdN W7', 20),
                fg_color='#F46146',
                hover_color=('#F46146', '#DC573F'),
                corner_radius=10
            ).grid(
                row=5,
                columnspan=2,
                pady=5,
            )
        else:
            tk.Label(
                main_frame,
                bg='#4E55FF',
                fg='#fff',
                font=self.styles.p,
                text=f'Incorrect! The correct answer is:  {correct_answer}!',
                wraplength=400
            ).grid(
                row=4,
                columnspan=2
            )
            ctk.CTkButton(
                main_frame,
                text='Next',
                command=self.next_q,  # Use self.next_q instead of next_q
                bg_color='#4E55FF',
                font=('DDFMaruGothic StdN W7', 20),
                fg_color='#F46146',
                hover_color=('#F46146', '#DC573F'),
                corner_radius=10
            ).grid(
                row=5,
                columnspan=2,
                pady=5,
            )
            # self.next_q()

    def next_q(self):
        self.question_5 = Question_5(self.master, self.styles, self.quiz_json_url, self.score, self.selected_subject)
        self.grid_forget()
class Question_5(tk.Frame):
    def __init__(self, parent, styles, quiz_json_url, score, selected_subject):
        super().__init__(parent)
        self.grid(row=0, sticky='ew')
        self.styles = styles
        self.quiz_json_url = quiz_json_url
        self.score = score
        self.selected_subject= selected_subject
        self.create_widgets()

    def create_widgets(self):
        # Frames
        main_frame = tk.Frame(self, bg='#4E55FF')
        main_frame.grid(row=0, column=0, sticky='ew')

        left_frame = tk.Frame(main_frame, bg='#4E55FF')
        left_frame.grid(row=1, column=0, sticky='ew')
        right_frame = tk.Frame(main_frame, bg='#4E55FF')
        right_frame.grid(row=1, column=1, sticky='ew')
        bottom_frame = tk.Frame(main_frame, bg='#4E55FF')
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky='ew')


        # JSON file
        quiz_data = self.quiz_json_url.json()
        question = unescape(quiz_data['results'][4]['question'])

        # Subject Title
        category_label = tk.Label(
            main_frame,
            image=self.styles.logo_small,
            compound='top',
            font=self.styles.p,
            text=f'Category: {self.selected_subject}',
            bg='#4E55FF',
            fg='#fff',
            anchor='center'
        )
        category_label.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=5,
            sticky='ew'
        )

        # Question
        tk.Label(
            left_frame,
            font=self.styles.p,
            text=question,
            bg='#4E55FF',
            fg='#fff',
            wraplength=400,
            anchor='w'
        ).grid(
            row=0,
            columnspan=2,
            pady=5,
            sticky='ew'
        )

        correct_answer = unescape(quiz_data['results'][4]['correct_answer'])
        print(correct_answer)
        incorrect_answers = [unescape(answer) for answer in quiz_data['results'][4]['incorrect_answers']]
        print(incorrect_answers)

        # Combine the correct and incorrect answers into one list
        answer_choices = [correct_answer] + incorrect_answers
        print(answer_choices)

        # Shuffle the answer choices
        random.shuffle(answer_choices)

        grid_index = 0
        for choice in answer_choices:
            ctk.CTkButton(
                right_frame,
                text=choice,
                command=lambda choice=choice: self.check_answer(choice, correct_answer, main_frame, right_frame),
                font=('DDFMaruGothic StdN W7', 20),
                fg_color='#F46146',
                hover_color=('#F46146', '#DC573F'),
                corner_radius=10
            ).grid(
                row=grid_index,  # Use grid_index directly for the row
                column=0,  # Set the column to 0
                pady=5,
                padx=5,
                sticky='ew',
                ipadx=5,
                ipady=10,
            )
            grid_index += 1

    def check_answer(self, selected_choice, correct_answer, main_frame, right_frame):
        for button in right_frame.winfo_children():
            if isinstance(button, ctk.CTkButton):
                button.configure(state=tk.DISABLED)
        if selected_choice == correct_answer:
            self.score += 1
            print(self.score)
            tk.Label(
                main_frame,
                bg='#4E55FF',
                fg='#fff',
                font=self.styles.p,
                text=f'Correct! it is indeed {correct_answer}!',
                wraplength=400
            ).grid(
                row=4,
                columnspan=2,
                sticky='ew'
            )

            ctk.CTkButton(
                main_frame,
                text='Next',
                command=self.next_q,
                bg_color='#4E55FF',
                font=('DDFMaruGothic StdN W7', 20),
                fg_color='#F46146',
                hover_color=('#F46146', '#DC573F'),
                corner_radius=10
            ).grid(
                row=5,
                columnspan=2,
                pady=5,
            )
        else:
            tk.Label(
                main_frame,
                bg='#4E55FF',
                fg='#fff',
                font=self.styles.p,
                text=f'Incorrect! The correct answer is:  {correct_answer}!',
                wraplength=400
            ).grid(
                row=4,
                columnspan=2
            )
            ctk.CTkButton(
                main_frame,
                text='Next',
                command=self.next_q,  # Use self.next_q instead of next_q
                bg_color='#4E55FF',
                font=('DDFMaruGothic StdN W7', 20),
                fg_color='#F46146',
                hover_color=('#F46146', '#DC573F'),
                corner_radius=10
            ).grid(
                row=5,
                columnspan=2,
                pady=5,
            )
            # self.next_q()

    def next_q(self):
        self.final = Final(self.master, self.styles, self.quiz_json_url, self.score)
        self.grid_forget()

class Final(tk.Frame):
    def __init__(self, parent, styles, quiz_json_url, score):
        super().__init__(parent)
        self.grid(row=0, sticky='ew')
        self.styles = styles
        self.quiz_json_url = quiz_json_url
        self.score = score
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self, bg='#4E55FF')
        main_frame.grid(row=0, column=0, sticky='ew')

        if self.score == 0 or self.score == 1 or self.score == 2:
            tk.Label(
                main_frame,
                image=self.styles.logo_small,
                compound='top',
                bg='#4E55FF',
                fg='#fff',
                font=self.styles.p,
                text=f'You got {self.score} out of 5.\n It\'s okay! Just Try again!',
            ).grid(
                row=0,
                columnspan=2,
                pady=5,
                sticky='ew'
            )
            ctk.CTkButton(
                main_frame,
                text='Play Again',
                command=self.play_again,
                bg_color='#4E55FF',
                font=('DDFMaruGothic StdN W7', 20),
                fg_color='#F46146',
                hover_color=('#F46146', '#DC573F'),
            ).grid(
                row=1,
                columnspan=2,
                pady=5,
            )
        else:
            tk.Label(
                main_frame,
                image=self.styles.logo_small,
                compound='top',
                bg='#4E55FF',
                fg='#fff',
                font=self.styles.p,
                text=f'You got {self.score} out of 5.\n Congrats!\n You\'re a trivia master!\nYou wanna go again?',
            ).grid(
                row=0,
                columnspan = 2,
                pady=5,
                sticky='ew'
            )
            ctk.CTkButton(
                main_frame,
                text='Play Again',
                command=self.play_again,
                bg_color='#4E55FF',
                font=('DDFMaruGothic StdN W7', 20),
                fg_color='#F46146',
                hover_color=('#F46146', '#DC573F'),
            ).grid(
                row=1,
                columnspan = 2,
                pady=5,
            )

    def play_again(self):
        self.grid_forget()
        self.startmenu = MainTriviaMenu(self.master, self.styles, self.master.score)

App('Trivia Game App')