from repository.repository import Repository

class Controller:
    def __init__(self):
        self.__repo = Repository()

    def get_data(self):
        return self.__repo.get_data()

    def set_data(self, new_data):
        self.__repo.set_data(new_data)

    def add_question(self, new_question):
        self.__repo.add_question(new_question)

    def get_number_of_questions(self):
        return self.__repo.get_number_of_questions()

    def get_all_ids(self):
        # Return a list with all the id's of all the question
        every_id = list(self.__repo.get_keys())
        return every_id

    def calculate_grade(self,  number_of_questions):
        #We compute the average, and we return it with exactly two decimals
        score = self.__repo.get_score()
        grade = score / number_of_questions * 100
        return round(grade,2)

    def update_score(self, status, user_answer, correct_answer):
        if status == "correct":
            self.__repo.increment_score()
        elif status == "partly":
            self.__repo.add_partial_score(Controller.calculate_partial_score(user_answer, correct_answer))

    def get_score(self):
        return self.__repo.get_score()

    # We check to see if any of the user answers are in the correct answers AND IMPORTANT NOTICE HERE:
    # Since only questions with choices can be partially correct, we need to check that
    # the question answer is made out of letters a,b,c,d,e. There are some questions where you have to reply with numbers, ip addresses etc.
    # If you got them wrong, then they are for sure not partially correct, but rather incorrect
    @staticmethod
    def check_if_partially_correct(user_answer, correct_answer):
        return any(element1 in element2 or element2 in element1 for element1 in user_answer for element2 in correct_answer) and (all(element.isalpha() for element in correct_answer))

    @staticmethod
    # One wrong answers cancels out one right answer
    def calculate_partial_score(user_answer, correct_answer):
        correct_user_answers=0
        wrong_user_answers=0
        for answer in user_answer:
            if answer in correct_answer:
                correct_user_answers+=1
            else:
                wrong_user_answers+=1
        # Cancelling out
        final = correct_user_answers - wrong_user_answers

        #If there are uncanceled right answers, we return the score (with 2 decimals only)
        if final:
            return round(1 / len(correct_answer) * final, 2)
        return 0









