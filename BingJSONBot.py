import re
import json
from collections import Counter
from string import punctuation
from math import sqrt

# load the data from the json file
try:
    with open("chatbot.json", "r") as file:
        data = json.load(file)
except FileNotFoundError:
    # create an empty dictionary if the file does not exist
    data = {}

def get_words(text):
    """Retrieve the words present in a given string of text.
    The return value is a list of tuples where the first member is a lowercase word,
    and the second member the number of time it is present in the text."""
    words_regexp_string = '(?:\\w+|[' + re.escape(punctuation) + ']+)'
    words_regexp = re.compile(words_regexp_string)
    words_list = words_regexp.findall(text.lower())
    return Counter(words_list).items()

B = 'Hello!'
while True:
    # output bot's message
    print('B: ' + B)
    # ask for user input; if blank line, exit the loop
    H = input('H: ').strip()
    if H == '':
        break
    # store the association between the bot's message words and the user's response
    words = get_words(B)
    words_length = sum([n * len(word) for word, n in words])
    for word, n in words:
        # update the data dictionary with the new associations
        if word not in data:
            data[word] = [[H, n / words_length]]
        else:
            found = False
            for pair in data[word]:
                if pair[0] == H:
                    pair[1] += n / words_length
                    found = True
                    break
            if not found:
                data[word].append([H, n / words_length])
    # find the best answer based on the input
    words = get_words(H)
    if words:
        # get the sentences and weights for each word in the input
        candidates = []
        for word, n in words:
            if word in data:
                candidates.extend([[sentence, weight * n] for sentence, weight in data[word]])
        # calculate the score for each sentence by summing the weights
        scores = {}
        for candidate in candidates:
            if candidate[0] in scores:
                scores[candidate[0]] += candidate[1]
            else:
                scores[candidate[0]] = candidate[1]
        # get the sentence with the highest score
        best_answer = (None, 0)
        for score in scores.items():
            if score[1] > best_answer[1]:
                best_answer = score
        # output the answer or a default message if no answer is found
        B = best_answer[0] or "I don't know what to say."
    else:
        B = "Please say something."

# save the data to the json file
with open("chatbot.json", "w") as file:
    json.dump(data, file)


