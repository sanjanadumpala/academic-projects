# Basic Dynamic Programming Sequence Alignment Algorithm
import sys
import re
import time

import psutil


# Function to validate a correct input
def checkinput(string):
    if (string.isalpha()):
        pattern = r'[^ACGT]'
        if (re.search(pattern, string)):
            sys.exit('Error! Base string should contain only A, C, G, T, but {string} was recevied'.format(
                string=string))
        else:
            return 'Base'
    else:
        try:
            index = int(string)
        except:
            sys.exit('Error! Expected a numerical index, but "{string}" was given'.format(
                string=string))
        else:
            return index


# Function to generate the strings (strings[0] = X, strings[1] = Y)
def string_generator(input_file):
    strings = list()
    base_strings = list()
    lengths = list()

    for line in input_file:
        # Removing the newline character
        line = line.split()[0]

        check_result = checkinput(line)

        if (check_result == 'Base'):
            strings.append(line)
            base_strings.append(line)
            lengths.append(0)

        else:
            lengths[-1] += 1
            index = check_result
            string = strings[-1]
            strings[-1] = string[:index+1] + string + string[index+1:]

    # Validating the generation of strings
    lengths = [2 ** lengths[i] * len(base_strings[i]) for i in (0, 1)]
    if (len(strings[0]) != lengths[0] or len(strings[1]) != lengths[1]):
        sys.exit('Program Error in generation of strings!')

    # returning the strings
    return strings[0], strings[1]


# Function to find the similarity between two strings
def string_similarity(X, Y, delta, alpha):
    m = len(X)
    n = len(Y)

    scores = [[0] * (n+1) for _ in range(m+1)]

    # Initialization
    score = 0
    for x_position in range(m+1):
        scores[x_position][0] = score
        score += delta

    score = 0
    for y_position in range(n+1):
        scores[0][y_position] = score
        score += delta

    # Filling the scores table
    for x_position in range(1, m+1):
        for y_position in range(1, n+1):
            scores[x_position][y_position] = min(scores[x_position-1][y_position] + delta,
                                                 scores[x_position][y_position-1] + delta,
                                                 scores[x_position-1][y_position-1] + alpha[X[x_position-1]][Y[y_position-1]])

    return scores


# Function to find the alignment between two strings
def string_alignment(X, Y, delta, alpha):
    X_align = str()
    Y_align = str()

    # Calculating the string similarity scores using DP
    scores = string_similarity(X, Y, delta, alpha)

    # Top-Down Pass to find the string alignments
    x_position = len(X)
    y_position = len(Y)

    while not (x_position == 0 and y_position == 0):
        # Add gaps for remaining length of the longer string and break the while
        if (x_position == 0):
            X_align = '_' * y_position + X_align
            Y_align = Y[:y_position] + Y_align
            break
        elif (y_position == 0):
            X_align = X[:x_position] + X_align
            Y_align = '_' * x_position + Y_align
            break

        X_add = Y_add = '_'

        # Pair Xm and Yn characters
        if ((alpha[X[x_position-1]][Y[y_position-1]] + scores[x_position-1][y_position-1]) == scores[x_position][y_position]):
            X_add = X[x_position-1]
            Y_add = Y[y_position-1]
            x_position -= 1
            y_position -= 1

        # Add a gap corresponding to Xm
        elif (delta + scores[x_position-1][y_position] == scores[x_position][y_position]):
            X_add = X[x_position-1]
            x_position -= 1

        # Add a gap corresponding to Yn
        elif (delta + scores[x_position][y_position-1] == scores[x_position][y_position]):
            Y_add = Y[y_position-1]
            y_position -= 1

        X_align = X_add + X_align
        Y_align = Y_add + Y_align

    return scores[len(X)][len(Y)], X_align, Y_align


# Function to measure memory usage
def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed


# main method
if __name__ == '__main__':

    # Start measuring memory
    startMemory = process_memory()

    # Fetching the input and output files
    if (len(sys.argv) != 3):
        sys.exit('Error! 2 parameters required, but {count} were given'.format(
            count=(len(sys.argv)-1)))

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Reading the input file
    try:
        i_f = open(input_file, 'r')
    except:
        sys.exit(
            'Error! {filepath} - Input file not found'.format(filepath=input_file))

    try:
        o_f = open(output_file, 'w')
    except:
        sys.exit(
            'Error! {filepath} - Path not found'.format(filepath=output_file))

    X, Y = string_generator(i_f)

    # Defining alpha and delta values
    delta = 30
    alpha = {'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
             'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
             'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
             'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0}}

    # Start measuring time
    start_time = time.time()
    
    # Run Algorithm
    score, X_align, Y_align = string_alignment(X, Y, delta, alpha)

    # End measuring time
    end_time = time.time()

    # End measuring memory
    endMemory = process_memory()

    # Calculate time and memory usage
    time_taken = (end_time - start_time)*1000
    mem_taken = endMemory - startMemory

    # Write to the file
    original_stdout = sys.stdout
    sys.stdout = o_f
    print(score, X_align, Y_align, time_taken, mem_taken, sep="\n")
    sys.stdout = original_stdout
