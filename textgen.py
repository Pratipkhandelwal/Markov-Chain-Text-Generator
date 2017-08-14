import random
import queue
from collections import defaultdict


def get_next_state(markov_chain, state):
    next_state_items = list(markov_chain[state].items())
    next_states = list(map(lambda x: x[0], next_state_items))
    next_state_counts = list(map(lambda x: x[1], next_state_items))
    total_count = sum(next_state_counts)
    next_state_probabilities = []
    running_total = 0
    for next_state_count in next_state_counts:
        probability = float(next_state_count) / total_count
        running_total += probability
        next_state_probabilities.append(running_total)
    sample = random.random()
    for index, next_state_probability in enumerate(next_state_probabilities):
        if sample <= next_state_probability:
            return next_states[index]
    return None


def tokenise_text_file():
    with open('text', 'r') as file:
        return ' '.join(file).split()


def create_markov_chain(tokens, order):
    if order > len(tokens):
        raise Error('Order greater than number of tokens.')
    markov_chain = defaultdict(lambda: defaultdict(int))
    current_state_queue = queue.Queue()
    for index, token in enumerate(tokens):
        if index < order:
            current_state_queue.put(token)
        elif index < len(tokens):
            current_state = ' '.join(list(current_state_queue.queue))
            current_state_queue.get()
            current_state_queue.put(token)
            next_state = ' '.join(list(current_state_queue.queue))
            markov_chain[current_state][next_state] += 1
    return markov_chain


def generate_text(markov_chain, iterations):
    text = state = random.choice([state for state in markov_chain.keys() if state[0].isupper()])
    for i in range(iterations):
        next_state = get_next_state(markov_chain, state)
        text = '{} {}'.format(text, next_state.split()[-1])
        state = next_state
    return text

if __name__ == '__main__':
    tokens = tokenise_text_file()
    markov_chain = create_markov_chain(tokens, order=2)
    print(generate_text(markov_chain, 50))
