import random

def get_randomized_options(options):
    correct_answer = options[0]
    random.shuffle(options)
    correct_answer_index = options.index(correct_answer)
    return options, correct_answer_index
