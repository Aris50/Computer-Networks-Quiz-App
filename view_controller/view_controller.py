from controller.controller import Controller
import random

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

    #Prints all the questions on the screen
    def print_all_questions(self):
        questions = list(self.__controller.get_data().values())
        for i in range(len(questions)):
            print(f"{i+1}: {questions[i]}")

    # Prints the welcome message that the user sees on the console when they first open the app
    @staticmethod
    def print_welcome_message():
        # self.print_all_questions()
        rules = "Welcome to the Computer Networks Quiz!\n\n>> You will be asked a series of multiple choice question, and you must answer them correctly. \n>> Write in lowercase all the corresponding letters of the answers you think are correct\n>> "+Bcolors.BLUE+"You WILL get points for partially correct results!\n"+Bcolors.NORMAL
        print(rules)

    def answer_question_view(self,current_question, i):
        # Print the question
        print("\n" + str(i+1) + ". " + current_question['question'])

        # Print the answers
        answers = current_question['answers']
        for i in range(len(answers)):
            print(f"{chr(i + 97)}) {answers[i]}")

        # Get user input
        user_answer = input(">> ")

        # Evaluate user answer
        # Case 1: the answer is completely correct
        if user_answer == current_question['correct']:
            print(Bcolors.CORRECT + "CORRECT!" + Bcolors.NORMAL)
            self.__controller.update_score("correct", user_answer, current_question['correct'])
        # Case 2: A-> the answer is partially correct or B-> the answer is incorrect
        else:
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

            # Prepare the number of questions.
            if number != "all":
                number = int(number)
            else:
                number = self.__controller.get_number_of_questions()

            # We keep in valid_id_list al the ids of the questions that were not asked yet
            valid_id_list = self.__controller.get_all_ids()

            # We start using the questions one by one, until the user answers the desired number of questions
            for i in range(number):
                # Get a random question id and remove it from the valid id's, using random
                question_id = random.choice(valid_id_list)
                valid_id_list.remove(question_id)

                # Let the user answer the question
                current_question = questions[question_id]
                self.answer_question_view(current_question, i)

                # If we are not at the last question, we print the score, as usual.
                # If we are, we print the average because the game is over, and we proceed to give the user his grade
                if i != number-1:
                    print("Your current score is " + Bcolors.BLUE + str(self.__controller.get_score()) + "/" + str(number) + Bcolors.NORMAL)
                else:
                    print("Your final score is " + Bcolors.BLUE + str(
                        self.__controller.calculate_grade(number)) + "%"+ Bcolors.NORMAL)
                    print(Bcolors.CORRECT+"Thank you for playing!"+Bcolors.NORMAL)

                # If we have get to an empty list and the for loop is still going:
                # it means that all the questions were asked exactly once, and the number of questions that the user entered is not yet finished.
                # In this case, we restart and add all the id's again
                if not valid_id_list:
                    valid_id_list = self.__controller.get_all_ids()



