import json
class Repository:
    def __init__(self):
        with open('safety.json', 'r') as file:
            # Get the data from the file
            data = json.load(file)

        with open('question_status.json', 'r') as file:
            # Get the data from the file
            questions_status = json.load(file)

        # Create a dictionary with the id of the question as the key, and with the right prefixes:
        # 1) Prefix the questions (because we take them from safety and they don't have prefixes, so we make them)
        for question in data:
            Repository.set_question_prefix(question)
        # 2a) Create the dictionary with all data
        self.__data = {question['id']: question for question in data}
        # 2b) Save the prefixing
        self.log_data('questions.json', self.__data)

        # Create smaller dictionaries with all the separate types of questions
        self.__tf_questions = {key: self.__data[key] for key in self.__data.keys() if self.__data[key]['id'][:2] == 'tf'}
        self.__mcs_questions = {key: self.__data[key] for key in self.__data.keys() if self.__data[key]['id'][:3] == 'mcs'}
        self.__mcm_questions = {key: self.__data[key] for key in self.__data.keys() if self.__data[key]['id'][:3] == 'mcm'}
        self.__fr_questions = {key: self.__data[key] for key in self.__data.keys() if self.__data[key]['id'][:2] == 'fr'}

        # Create a dictionary with the id as a key and the status of the question as the value
        self.__question_status = {question['id']: question for question in questions_status}

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

    #TODO: Also modify the other question types, and the question_status
    def add_question(self, new_question):
        # Give the new question a unique ID
        next_id = str(self.__next_available_id)
        new_question['id'] = next_id
        Repository.set_question_prefix(new_question)
        self.__next_available_id+=1
        self.__data[next_id] = new_question
        #self.log_data('questions.json')

    #TODO: Also modify the other question types, and the question_status
    def remove_question(self, question_id):
        if question_id in self.__data.keys():
            del self.__data[question_id]
            #self.log_data('questions.json')

    def get_number_of_questions(self):
        return len(self.__data)

    @staticmethod
    def log_data(file_name, data):
        with open(file_name, 'w') as file:
            json.dump(list(data.values()), file, indent=4)

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

    def update_answer_status(self, question_id, status):
        if status:
             self.__question_status[question_id]['answered_correctly'] += 1
        else:
            self.__question_status[question_id]['answered_wrong'] += 1
        self.log_data('question_status.json', self.__question_status)

    def get_answer_status(self, question_id):
        return self.__question_status[question_id]

    def reset_question_status(self):
        for key in self.__question_status.keys():
            self.__question_status[key]['answered_correctly'] = 0
            self.__question_status[key]['answered_wrong'] = 0
        self.log_data('question_status.json', self.__question_status)

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







