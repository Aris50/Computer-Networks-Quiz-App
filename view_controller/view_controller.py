from controller.controller import Controller
import random
import time
import threading

'''
   fr -> free response
   tf -> true/false
   mcm -> multiple choice, multiple answers
   mcs -> multiple choice, single answer
'''
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
    @staticmethod
    def print_all_questions(questions):
        for i in range(len(questions)):
            print(f"{i+1}: {questions[i]['question']}")
            for j in range(len(questions[i]['answers'])):
                print(f"{chr(j + 97)}) {questions[i]['answers'][j]}")
            #print(f"Correct answer: {questions[i]['correct']}")
        print("\n")

    @staticmethod
    def print_menu():
        print("\n\n" + Bcolors.BLUE+"MAIN MENU"+Bcolors.NORMAL)
        print("1. Start quick quiz")
        print("2. Start practice")
        print("3. Solve questions you struggle with")
        #print("4. Print questions")
        print("0. Exit")

    @staticmethod
    def get_menu_choice():
        choice = input(">>")
        while choice not in ["0", "1", "2", "3"]:
            print(Bcolors.INCORRECT + "Invalid input. Please enter a valid option" + Bcolors.NORMAL)
            choice = input(">>")
        return choice

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
                print("Exiting to main menu...")
                for i in range(3):
                    print("...")
                    time.sleep(1)
                return False
            else:
                print(Bcolors.INCORRECT + "Invalid input. Please enter y or n." + Bcolors.NORMAL)

    def print_score_status(self,number, index):
        if index != number - 1:
            print("Your current score is " + Bcolors.BLUE + str(
                self.__controller.get_score()) + "/" + str(number) + Bcolors.NORMAL)
        else:
            self.show_final_score(number)

    def print_number_of_available_questions(self):
        print("\n\n" + Bcolors.BLUE + "AVAILABLE QUESTIONS IN THE ARCHIVE" + Bcolors.NORMAL)
        print("1. True/False questions: " + str(len(self.__controller.get_tf_questions())))
        print("2. Multiple choice, single answer questions: " + str(len(self.__controller.get_mcs_questions())))
        print("3. Multiple choice, multiple answers questions: " + str(len(self.__controller.get_mcm_questions())))
        print("4. Free response questions: " + str(len(self.__controller.get_fr_questions())))
        print("5. All questions: " + str(len(self.__controller.get_data())))
        print("6. Question you got wrong at least once: " + str(len(self.__controller.gather_troubling_question_from_question_status())) + "\n")

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
            ans = input("Do you want to revise your wrong answers? (y/n): \n>>")
            if ans == "y":
                for key,value in wrong_questions.items():
                    print("\n" + f"{value['label_nr']}" +". "+f"{value['question']}")
                    aux = value['answers']
                    for j in range(len(aux)):
                        print(f"{chr(j + 97)}) {aux[j]}")
                    print(f"Your answer: {value['user_answer']}")
                    print(f"Correct answer: {value['correct']}")
            elif ans != "n":
                print(Bcolors.INCORRECT+"Invalid input. Please enter y or n."+Bcolors.NORMAL)

    def get_desired_number_from_user(self):
        number = input("How many questions do you want to answer?(write all if you want to answer all questions): ")
        # Prepare the number of questions. Make sure the input is a valid number
        if number != "all":
            while not number.isdigit() or int(number) <= 0:
                print(Bcolors.INCORRECT + "Please enter a valid number" + Bcolors.NORMAL)
                number = input(
                    "How many questions do you want to answer?(write all if you want to answer all questions): ")
            number = int(number)
        else:
            number = self.__controller.get_number_of_questions()
        return number

    def show_final_score(self, number):
        print("\n\n-----------------------------------")
        print("Your final score is " + Bcolors.BLUE + str(
            self.__controller.calculate_grade(number)) + "%" + Bcolors.NORMAL)
        print("-----------------------------------\nThank you for playing!\n")

    # Prints the welcome message that the user sees on the console when they first open the app
    @staticmethod
    def print_welcome_message_1():
        # self.print_all_questions()
        rules = "Welcome to the Computer Networks Quiz!\n\n>> You will be asked a series of multiple choice question, and you must answer them correctly. \n>> Write in lowercase all the corresponding letters of the answers you think are correct\n>> "+Bcolors.CORRECT+"You WILL get points for partially correct results!\n"+ Bcolors.NORMAL + ">> " +Bcolors.INCORRECT+"YOU WILL BE TIMED! (1 minute/question). When the time runs out the test is over.\n"+Bcolors.NORMAL+ ">> Do not forget you can say the exit keyword during a question in order to terminate a certain exercise.\n"
        print(rules)

    @staticmethod
    def print_welcome_message_2():
        rules = "Welcome to practice!\n\n>> You enter the type of question you want to answer, and you will get a score.\n>> You will NOT be timed!\n>> Available types (please select a number to continue): \n1) true/false\n2) multiple choice with one answer correct\n3) multiple choice with two answers correct\n4) free-choice answer questions\n"+">>Do not forget you can say the exit keyword during a question in order to terminate a certain exercise.\n"
        print(rules)

    @staticmethod
    def print_welcome_message_3():
        rules="Welcome to the wrong question section! Here you can do the questions you got wrong!\n Above are printed all the questions you got wrong at least once .You will be asked in the order of how many times you got them wrong!.\n"+">>Do not forget you can say the exit keyword during a question in order to terminate a certain exercise.\n"
        print(rules)

    #Let the user select the desired type of questions he wants to practice on
    def get_appropriate_questions(self):
        questions = {}
        valid_id_list = []

        q_type = input("Choose the number of the type of questions you want to practice: ")
        while (not q_type.isdigit()) or (q_type.isdigit() not in range(1, 5)):
            print(Bcolors.INCORRECT + "Unable to identify type. Please try again." + Bcolors.NORMAL)
            q_type = input("Choose the number of the type of questions you want to practice: ")
        print(Bcolors.CORRECT)
        if q_type == "1":
            print("Successfully selected true/false questions.")
            questions = self.__controller.get_tf_questions()
            valid_id_list = self.__controller.get_tf_questions_ids()
        elif q_type == "2":
            print("Successfully selected multiple choice questions with one correct answer.")
            questions = self.__controller.get_mcs_questions()
            valid_id_list = self.__controller.get_mcs_questions_ids()
        elif q_type == "3":
            print("Successfully selected multiple choice questions with two correct answers.")
            questions = self.__controller.get_mcm_questions()
            valid_id_list = self.__controller.get_mcm_questions_ids()
        elif q_type == "4":
            print("Successfully selected free response questions.")
            questions = self.__controller.get_fr_questions()
            valid_id_list = self.__controller.get_fr_questions_ids()
        elif q_type == "5":
            print("Successfully selected all questions.")
            questions = self.__controller.get_data()
            valid_id_list = self.__controller.get_all_ids()
        print(Bcolors.NORMAL)
        return questions, valid_id_list


    def answer_question_view(self,current_question, i, number):
        # Print the question
        question_status = self.__controller.get_answer_status(current_question['id'])
        print("\n" + str(i+1) + "/" + str(number) + ". " + current_question['question'] + "  " + "(c:" + Bcolors.CORRECT +str(question_status['answered_correctly'])+Bcolors.NORMAL + "/w: "+ Bcolors.INCORRECT+str(question_status['answered_wrong']) + Bcolors.NORMAL + ")")

        # Print the answers
        answers = current_question['answers']
        for j in range(len(answers)):
            print(f"{chr(j + 97)}) {answers[j]}")

        # Get user input
        user_answer = input(">> ")
        if user_answer =="exit":
            user_answer=input(Bcolors.INCORRECT+"Are you sure? (y/n): \n>>"+Bcolors.NORMAL)
            if user_answer=="y":
                print(Bcolors.INCORRECT+"----------------------------TERMINATED--------------------------------\n"+Bcolors.NORMAL)
                return False
            else:
                print(Bcolors.CORRECT+"RESUMED\n"+Bcolors.NORMAL)

                # We recall the function to restart the process
                self.answer_question_view(current_question, i, number)

                # In order to stop the recursion, so the function does not execute twice
                return True

        # Evaluate user answer
        # Case 1: the answer is completely correct
        if user_answer == current_question['correct']:
            print(Bcolors.CORRECT + "CORRECT!" + Bcolors.NORMAL)
            self.__controller.update_score("correct", user_answer, current_question['correct'])
            # Update the question status
            self.__controller.update_answer_status(current_question['id'], True)
        # Case 2: A-> the answer is partially correct or B-> the answer is incorrect
        else:
            # Update the question status
            self.__controller.update_answer_status(current_question['id'], False)
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
        # Make sure we return true if the function is completed with success
        return True

    #This is the main function that runs the app
    def run(self):
        # Initialise all the available questions
        self.print_number_of_available_questions()

        while True:
            # Print the menu and let the user choose:
            View.print_menu()
            choice = View.get_menu_choice()

            # 1st choice: Start a random quiz
            if choice == "1":
                questions = self.__controller.get_data()
                self.print_welcome_message_1()
                while True:
                    # Ask the user how many questions they want to answer
                    number = self.get_desired_number_from_user()

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

                        # We check if the user wants to exit or not at every answer check
                        if not self.answer_question_view(current_question, i, number):
                            break

                        # If we are not at the last question, we print the score, as usual.
                        # If we are, we print the average because the game is over, and we proceed to give the user his grade
                        if i != number-1 and self.__remaining_time:
                            print("Your current score is " + Bcolors.BLUE + str(self.__controller.get_score()) + "/" + str(number) + Bcolors.NORMAL)
                        else:
                            self.show_final_score(number)
                            if self.__remaining_time==0:
                                print("TIME IS UP!")
                            print(f"You had: {int(self.__remaining_time/60)} minutes and {self.__remaining_time%60} seconds left.")
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

                    # As the game is over we reset the score and also the wrong questions
                    self.__controller.reset_score()
                    self.__controller.reset_wrong_questions()

                    # The test was timed so we also need to reset the score
                    self.__remaining_time = 0

                    # Ask the user if they want to play again, if they dont we exit to main menu
                    if not self.ask_user_to_play_again():
                        break

            elif choice == "2":
                # We print the welcome message for the practice mode
                View.print_welcome_message_2()

                # We get our required data to start the practice
                questions, valid_id_list = self.get_appropriate_questions()
                while True:
                    # We get the total number of questions from a certain type
                    number = len(valid_id_list)
                    # We start answering all of them
                    for i in range (number):
                        question_id = random.choice(valid_id_list)
                        valid_id_list.remove(question_id)
                        current_question = questions[question_id]

                        # We answer the question, and we print the score at the end of each answer
                        # We check if the user wants to exit or not at every answer check
                        if not self.answer_question_view(current_question, i, number):
                            break
                        self.print_score_status(number, i)

                    # After we finish, we display revision, and ask user if he wants to replay
                    self.revision()

                    # As the game is over, we need the score reset and the wrong questions for revision also
                    self.__controller.reset_score()
                    self.__controller.reset_wrong_questions()

                    if not self.ask_user_to_play_again():
                        break

            elif choice == "3":
                # We get the questions we need, this time we do not need the list of id's
                questions = self.__controller.gather_troubling_question_from_question_status()

                # We print the questions
                View.print_all_questions(questions)

                # We print the welcome message including the rules
                View.print_welcome_message_3()

                # We get the number of questions we need.
                # We set the index so that we can keep track of the number of questions we have answered, because this time we do not use a for loop
                number = len(questions)
                index = -1
                while True:
                    for question in questions:
                        # We manually increase the index of questions
                        index += 1
                        # We check if the user wants to exit or not at every answer check
                        if not self.answer_question_view(question, index, number):
                            break
                        self.print_score_status(number, index)

                    # Give user the capacity to revise his score
                    self.revision()

                    # As the game is over, we need the score reset and the wrong questions for revision also
                    self.__controller.reset_score()
                    self.__controller.reset_wrong_questions()

                    if not self.ask_user_to_play_again():
                        break


            elif choice == "0":
                print(Bcolors.CORRECT+"Thanks for stopping by!"+Bcolors.NORMAL)
                print("Exiting the program...")
                time.sleep(3)
                #exit(0)
                break



