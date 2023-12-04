import random

def get_randomized_options(options):
    if not options or len(options) < 1:
        raise ValueError("Options is empty or doesn't have the required number of options")

    correct_answer = options[0]
    random.shuffle(options)
    correct_answer_index = options.index(correct_answer)
    return options, correct_answer_index

