import json
class Repository:
    def __init__(self):
        with open('questions.json', 'r') as file:
            # Get the data from the file
            data = json.load(file)

        # Create a dictionary with the id of the question as the key
        self.__data = {str(question['id']): question for question in data}
        # Keep track of the next available ID so id's do not repeat
        self.__next_available_id = len(data)
        # Keep track of your score
        self.__score = 0
        # Store the wrong questions so we can show them at the end if the user so desires
        self.__wrong_questions = {}


    def get_data(self):
        return self.__data #.copy()

    def set_data(self, new_data):
        self.__data = new_data
        self.log_data()

    def get_keys(self):
        return self.__data.keys()

    def set_keys(self, new_keys):
        self.__data = {key: self.__data[key] for key in new_keys}
        self.log_data()

    def add_question(self, new_question):
        # Give the new question a unique ID
        next_id = str(self.__next_available_id)
        new_question['id'] = next_id
        self.__next_available_id+=1
        self.__data[next_id] = new_question
        self.log_data()

    def remove_question(self, question_id):
        if question_id in self.__data:
            del self.__data[question_id]
            self.log_data()

    def get_number_of_questions(self):
        return len(self.__data)

    def log_data(self):
        with open('questions.json', 'w') as file:
            json.dump(list(self.__data.values()), file, indent=4)

    def increment_score(self):
        self.__score+=1

    def get_score(self):
        return self.__score

    def reset_score(self):
        self.__score = 0

    def add_partial_score(self, partial_score):
        self.__score+=partial_score

    def add_wrong_question(self, question):
        self.__wrong_questions[question['id']] = question

    def reset_wrong_questions(self):
        self.__wrong_questions = {}

    def get_wrong_questions(self):
        return self.__wrong_questions.copy()







