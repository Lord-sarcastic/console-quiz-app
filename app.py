import json
import random

NUMBER_OF_QUESTIONS = 20

QUESTIONS_FILE = 'questions.json'

STATE_FILE = 'app_state.json'

WELCOME_MESSAGE = f"""
Hi, there! This is a quiz application with {NUMBER_OF_QUESTIONS} questions.
Four options are available for each. Reply each question with the letter of the options:
a, b, c or d.

You can cancel the quiz at anytime with CTRL + C/D and continue from where you stop.
"""

PROMPT = f"""
Press 's' to start or 'c' to cancel.
"""

END_MESSAGE = f"""
Thanks for completing the quiz, your results are as follows:
"""

class Question:
    def __init__(self, question: str, index: int, options: tuple, answer: str) -> None:
        options_dict = {}
        
        self.question = question
        self.index = index
        self.options = [*options, answer]
        random.shuffle(self.options)
        self.answer = self.options.index(answer)
    
    def check_answer(self, answer_index):
        return self.answer == answer_index
    
    def show_question(self):
        question_details = f"""
        Question: {self.question}
        Pick an option:
            a. {self.options[0]}
            b. {self.options[1]}
            c. {self.options[2]}
            d. {self.options[3]}
        """

        print(question_details)
    
    def show_correct_option(self):
        index_to_option = {
            '0': 'a',
            '1': 'b',
            '2': 'c',
            '3': 'd'
        }
        print(f"""
        Correct option is:
            {index_to_option[str(self.answer)]} {self.options[self.answer]}
        """)

def load_file(file_name):
    '''
    Loads contents of a json file and returns it as valid Python
    '''

    with open(file_name, 'r') as f:
        content = json.load(f)

    return content

def dump_to_file(file_name, content, state='WRITE'):
    '''
    Writes content `content` to `file_name`
    '''

    file_state = {
        'WRITE': 'w',
        'READ': 'r',
        'APPEND': 'a'
    }

    with open(file_name, file_state.get(state, file_state['APPEND'])) as f:
        json.dump(content, f)

def validate_state(state):
    '''
    Checks if `state` contains questions
    '''

    return bool(state['question_order'])

def reset_state():
    '''
    Sets state to initial values
    '''

    state = {
        "current_score": 0,
        "question_order": [],
        "current_question": 0
    }
    dump_to_file(STATE_FILE, state)

def process_prompt_response(response):
    '''
    Validates response of user to generic prompts
    '''

    ACTIONS = {
        's': ask_questions,
        'c': exit,
        'o': 'REPEAT'
    }

    return ACTIONS.get(response.lower(), ACTIONS['o'])

def proceed_prompt():
    '''
    Displays welcome message and proceeds into actions
    '''

    print(WELCOME_MESSAGE)
    response = None
    while not response:
        user_answer = input(PROMPT).strip()
        action = process_prompt_response(user_answer)
        if isinstance(action, str):
            print("Invalid option")
            response = None
        else:
            response = True
    action()

def get_questions():
    '''
    Retrieves selected questions from file or loads from state. Returns
    selected questions and dict of questions with index-based keys
    '''

    state = load_file(STATE_FILE)
    loaded_questions = load_file(QUESTIONS_FILE)
    structured_questions = {}

    for (index, question) in enumerate(loaded_questions):
        structured_questions[f'{index + 1}'] = question

    if validate_state(state):
        state_questions = state['question_order']
        questions = state_questions[
            state_questions.index(
                state['current_question']
            ):
        ]
    else:
        question_indexes = list(range(1, len(loaded_questions) + 1))
        random.shuffle(question_indexes)
        questions = question_indexes[:NUMBER_OF_QUESTIONS]
    
    return questions, structured_questions

def load_questions_into_class(questions_index, structured_questions):
    '''
    Instantiates class with loaded questions
    '''

    packaged_questions = []
    for index in questions_index:
        question = structured_questions[f'{index}']
        question_class = Question(
            question=question['question'],
            index=index,
            options=(
                question['other_1'],
                question['other_2'],
                question['other_3'],
            ),
            answer=question['correct']
        )
        packaged_questions.append(question_class)
    
    return packaged_questions

def process_option(option):
    '''
    Process response given by user to respond to questions
    '''

    allowed_options = ['a', 'b', 'c', 'd']
    index = None
    exists = option.lower() in allowed_options
    
    if exists:
        index = allowed_options.index(option)

    return (exists, index)
   
def prompt_question(question: Question) -> bool:
    '''
    Handles asking process of each question
    '''

    CORRECT = "Correct! :)"
    WRONG = "Wrong! :("
    question.show_question()
    response = input("Enter option: ").strip()
    processed_resonse = process_option(response)

    while not processed_resonse[0]:
        print("Invalid option")
        response = input("Enter option: ").strip()
        processed_resonse = process_option(response)
    
    correct = question.check_answer(processed_resonse[1])
    if correct:
        print(CORRECT)
    else:
        print(WRONG)
        question.show_correct_option()
    
    return correct

def ask_questions() -> None:
    '''
    Main app driver, drives the question asking process
    '''

    state = load_file(STATE_FILE)
    questions_unruly = get_questions()
    state['question_order'] = questions_unruly[0]
    questions = load_questions_into_class(*questions_unruly)
    for question in questions:
        state['current_question'] = question.index
        dump_to_file(STATE_FILE, state)
        print(f"Question {state['question_order'].index(question.index)}")
        score = prompt_question(question)
        state['current_score'] += int(score)
        dump_to_file(STATE_FILE, state)
        print(f"You have {state['current_score']} points")
    
    print(END_MESSAGE)
    print(f"Score: {score}/{NUMBER_OF_QUESTIONS}")
    
def play_quiz():
    '''
    Initilizes quiz play
    '''

    proceed_prompt(PROMPT)
    ask_questions()

if __name__ == '__main__':
    play_quiz()