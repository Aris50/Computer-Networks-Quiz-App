import json
class Repository:
    def __init__(self):
        with open('safety.json', 'r') as file:
            # Get the data from the file
            data = json.load(file)

        # Create a dictionary with the id of the question as the key, and with the right prefixes:
        # 1) Prefix the questions
        for question in data:
            Repository.set_question_prefix(question)
        # 2) Create the dictionary with all data
        self.__data = {question['id']: question for question in data}
        self.log_data('questions.json')

        # Create smaller dictionaries with all the separate types of questions
        self.__tf_questions = {key: self.__data[key] for key in self.__data.keys() if self.__data[key]['id'][:2] == 'tf'}
        self.__mcs_questions = {key: self.__data[key] for key in self.__data.keys() if self.__data[key]['id'][:3] == 'mcs'}
        self.__mcm_questions = {key: self.__data[key] for key in self.__data.keys() if self.__data[key]['id'][:3] == 'mcm'}
        self.__fr_questions = {key: self.__data[key] for key in self.__data.keys() if self.__data[key]['id'][:2] == 'fr'}

        # Keep track of the next available ID so id's do not repeat
        self.__next_available_id = len(data)
        # Keep track of your score
        self.__score = 0
        # Store the wrong questions so we can show them at the end if the user so desires
        self.__wrong_questions = {}




    def get_data(self):
        return self.__data.copy()

    def get_tf_questions(self):
        return self.__tf_questions.copy()

    def get_mcs_questions(self):
        return self.__mcs_questions.copy()

    def get_mcm_questions(self):
        return self.__mcm_questions.copy()

    def get_fr_questions(self):
        return self.__fr_questions.copy()

    def get_tf_questions_ids(self):
        return self.__tf_questions.keys()

    def get_mcs_questions_ids(self):
        return self.__mcs_questions.keys()

    def get_mcm_questions_ids(self):
        return self.__mcm_questions.keys()

    def get_fr_questions_ids(self):
        return self.__fr_questions.keys()

    def set_data(self, new_data):
        self.__data = new_data
        #self.log_data('questions.json')

    def get_keys(self):
        return self.__data.keys()

    def set_keys(self, new_keys):
        self.__data = {key: self.__data[key] for key in new_keys}
        #self.log_data('questions.json')

    def add_question(self, new_question):
        # Give the new question a unique ID
        next_id = str(self.__next_available_id)
        new_question['id'] = next_id
        Repository.set_question_prefix(new_question)
        self.__next_available_id+=1
        self.__data[next_id] = new_question
        #self.log_data('questions.json')

    def remove_question(self, question_id):
        if question_id in self.__data.keys():
            del self.__data[question_id]
            #self.log_data('questions.json')

    def get_number_of_questions(self):
        return len(self.__data)

    def log_data(self, file_name):
        with open(file_name, 'w') as file:
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

    '''
    fr -> free response
    tf -> true/false
    mcm -> multiple choice, multiple answers
    mcs -> multiple choice, single answer
    '''
    @staticmethod
    def set_question_prefix(question):
        pref = ""
        if not question['answers']:
            pref = "fr"
        elif question['answers'] == ["true", "false"]:
            pref = "tf"
        elif len(question['correct']) > 1:
            pref = "mcm"
        elif len(question['correct']) == 1:
            pref = "mcs"
        question['id'] = pref + str(question['id'])







