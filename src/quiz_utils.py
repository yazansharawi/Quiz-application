import random

def get_randomized_options(options):
    if not options:
        return None, None

    correct_answer = options[0]
    random.shuffle(options)
    correct_answer_index = options.index(correct_answer)
    return options, correct_answer_index