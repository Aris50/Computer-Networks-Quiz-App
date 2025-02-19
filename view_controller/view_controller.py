from controller.controller import Controller
import random
import time
import threading

# TODO: handle user input errors
class Bcolors:
    CORRECT = '\033[92m'
    INCORRECT = '\033[91m'
    NORMAL = '\033[0m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    ORANGE = '\033[33m'

class View:
    def __init__(self):
        self.__controller = Controller()
        self.__remaining_time = 0
        self.__lock = threading.Lock()

    #Prints all the questions on the screen
    def print_all_questions(self):
        questions = list(self.__controller.get_data().values())
        for i in range(len(questions)):
            print(f"{i+1}: {questions[i]}")

    @staticmethod
    def ask_user_to_play_again():
        answer="n/a"
        while answer not in ["y", "n"]:
            answer = input("\nDo you want to play again? (y/n):\n>>")
            if answer == "y":
                print("Restarting the game...")
                for i in range (3):
                    print("...")
                    time.sleep(1)
                return True
            elif answer == "n":
                print("Bye!")
                return False
            else:
                print(Bcolors.INCORRECT + "Invalid input. Please enter y or n." + Bcolors.NORMAL)

    def countdown(self):
        while self.__remaining_time > 0:
            with self.__lock:
                self.__remaining_time -= 1
            time.sleep(1)

    def start_countdown(self):
        countdown_thread = threading.Thread(target=self.countdown,)
        countdown_thread.start()

    def print_time_left(self):
        print(Bcolors.ORANGE + f"Time left: {(int(self.__remaining_time / 60))} minutes and {self.__remaining_time % 60} seconds" + Bcolors.NORMAL)

    # Function to help the user revise ad have a chance to check for their mistakes
    def revision(self):
        wrong_questions = self.__controller.get_wrong_questions()
        ans="n/a"
        # Handle correctly wrong input
        while ans not in ["y", "n"]:
            ans = input("Do you want to revise your wrong answers? (y/n): ")
            if ans == "y":
                for key,value in wrong_questions.items():
                    print("\n" + f"{value['label_nr']}" +". "+f"{value['question']}")
                    print(f"Your answer: {value['user_answer']}")
                    print(f"Correct answer: {value['correct']}")
            elif ans != "n":
                print(Bcolors.INCORRECT+"Invalid input. Please enter y or n."+Bcolors.NORMAL)

    # Prints the welcome message that the user sees on the console when they first open the app
    @staticmethod
    def print_welcome_message():
        # self.print_all_questions()
        rules = "Welcome to the Computer Networks Quiz!\n\n>> You will be asked a series of multiple choice question, and you must answer them correctly. \n>> Write in lowercase all the corresponding letters of the answers you think are correct\n>> "+Bcolors.BLUE+"You WILL get points for partially correct results!\n"+Bcolors.NORMAL
        print(rules)

    def answer_question_view(self,current_question, i, number):
        # Print the question
        print("\n" + str(i+1) + "/" + str(number) + ". " + current_question['question'])

        # Print the answers
        answers = current_question['answers']
        for j in range(len(answers)):
            print(f"{chr(j + 97)}) {answers[j]}")

        # Get user input
        user_answer = input(">> ")

        # Evaluate user answer
        # Case 1: the answer is completely correct
        if user_answer == current_question['correct']:
            print(Bcolors.CORRECT + "CORRECT!" + Bcolors.NORMAL)
            self.__controller.update_score("correct", user_answer, current_question['correct'])
        # Case 2: A-> the answer is partially correct or B-> the answer is incorrect
        else:
            # Prepare to add this question to a wrong questions dictionary that can be checked at the end by the user
            wrong_question = current_question.copy()
            wrong_question['user_answer'] = user_answer
            wrong_question['label_nr'] = str(i+1)
            self.__controller.add_wrong_question(wrong_question)
            # Check if the question is in case A or B
            partially_correct = Controller.check_if_partially_correct(user_answer, current_question['correct'])
            # A) the answer is partially correct
            if partially_correct:
                print(Bcolors.ORANGE + "PARTLY CORRECT!" + Bcolors.NORMAL)
                print(f"The correct answer was {current_question['correct']}.")
                self.__controller.update_score("partly", user_answer, current_question['correct'])
            # B) the answer is incorrect
            else:
                print(Bcolors.INCORRECT + "INCORRECT!" + Bcolors.NORMAL)
                print(f"The correct answer was {current_question['correct']}")

    #This is the main function that runs the app
    def run(self):
        self.print_welcome_message()

        # Initialise all the available questions
        questions = self.__controller.get_data()

        # Start the main application
        while True:
            # Ask the user how many questions they want to answer
            number = input("How many questions do you want to answer?(write all if you want to answer all questions): ")

            # Prepare the number of questions. Make sure the input is a valid number
            if number != "all":
                while not number.isdigit() or int(number) <= 0:
                    print(Bcolors.INCORRECT+"Please enter a valid number"+Bcolors.NORMAL)
                    number = input("How many questions do you want to answer?(write all if you want to answer all questions): ")
                number = int(number)
            else:
                number = self.__controller.get_number_of_questions()

            # Set the timer and start the countdown
            self.__remaining_time  = number*60
            self.start_countdown()

            # We keep in valid_id_list al the ids of the questions that were not asked yet
            valid_id_list = self.__controller.get_all_ids()

            # We start using the questions one by one, until the user answers the desired number of questions
            for i in range(number):
                # Get a random question id and remove it from the valid id's, using random
                question_id = random.choice(valid_id_list)
                valid_id_list.remove(question_id)

                # Let the user answer the question
                current_question = questions[question_id]
                self.answer_question_view(current_question, i, number)

                # If we are not at the last question, we print the score, as usual.
                # If we are, we print the average because the game is over, and we proceed to give the user his grade
                if i != number-1 and self.__remaining_time:
                    print("Your current score is " + Bcolors.BLUE + str(self.__controller.get_score()) + "/" + str(number) + Bcolors.NORMAL)
                else:
                    print("\n\n-----------------------------------")
                    if self.__remaining_time==0:
                        print("TIME IS UP!")
                    print("Your final score is " + Bcolors.BLUE + str(
                        self.__controller.calculate_grade(number)) + "%"+ Bcolors.NORMAL)
                    print("-----------------------------------\n")
                    print(f"You had: {int(self.__remaining_time/60)} minutes and {self.__remaining_time%60} seconds left.")
                    print(Bcolors.CORRECT+"Thank you for playing!"+Bcolors.NORMAL)
                    # We make sure we reset the program here
                    break

                # If we have get to an empty list and the for loop is still going:
                # it means that all the questions were asked exactly once, and the number of questions that the user entered is not yet finished.
                # In this case, we restart and add all the id's again
                if not valid_id_list:
                    valid_id_list = self.__controller.get_all_ids()

                # Print how much time the user has left.
                self.print_time_left()


            # Allow the user to review his mistakes if he so desires
            self.revision()

            # Ask the user if they want to play again, if they do we need to reset the score
            if not self.ask_user_to_play_again():
                self.__remaining_time=0
                break
            else:
                self.__controller.reset_score()



