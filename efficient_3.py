import sys
import gc
import time

import psutil
from basic_3 import string_generator, string_alignment as basic_string_alignment


# Function to find the similarity between two strings - Memory Efficient
def string_similarity(X, Y, delta, alpha):
    m = len(X)
    n = len(Y)

    # Declaration
    prev_score = [0] * (n+1)

    # Initialization (First Column - prev score)
    score = 0
    for y_position in range(n+1):
        prev_score[y_position] = score
        score += delta

    # Calculating similarity score using DP
    curr_score = None
    for x_position in range(1, m+1):
        curr_score = [0] * (n+1)
        curr_score[0] = prev_score[0] + delta
        for y_position in range(1, n+1):
            curr_score[y_position] = min(curr_score[y_position-1] + delta,
                                         prev_score[y_position] + delta,
                                         prev_score[y_position-1] + alpha[X[x_position-1]][Y[y_position-1]])

        prev_score = curr_score

        # Garbage Collection
        gc.collect()

    return curr_score


# Function to find the alignment between two strings
def string_alignment(X, Y, delta, alpha):
    m = len(X)
    n = len(Y)

    # Recursion Termination Condition
    # Both strings are empty (very similar)
    if (len(X) == 0 and len(Y) == 0):
        return (0, X, Y)

    # Adding gaps for string X corresponding to Y(longer string)
    elif (len(X) == 0):
        return (len(Y) * delta, '_' * len(Y), Y)

    # Adding gaps for string Y corresponding to X(longer string)
    elif (len(Y) == 0):
        return (len(X) * delta, X, '_' * len(X))

    # Pairing up Xm and Yn character
    elif (len(X) == 1 and len(Y) == 1):
        return (alpha[X[0]][Y[0]], X, Y)

    # Finding the alignment of character X with string Y
    # For this case, both the memory efficient and the basic algorithm take the similar amount of memory
    elif (len(X) == 1):
        return basic_string_alignment(X, Y, delta, alpha)

    # Divide Step
    # Splitting X intp X_l and X_r
    X_l, X_r = X[:m//2], X[m//2:]

    # Finding the best split for Y
    left_score = string_similarity(X_l, Y, delta, alpha)
    right_score = string_similarity(X_r[::-1], Y[::-1], delta, alpha)

    # Considering k = 0 to be the best split for Y
    min_split_index = 0
    min_split_score = left_score[0] + right_score[n]

    for k in range(n+1):
        split_score = left_score[k] + right_score[n-k]
        if (split_score < min_split_score):
            min_split_score = split_score
            min_split_index = k

    # Recursive Step
    _, X_l_align, Y_l_align = string_alignment(
        X_l, Y[:min_split_index], delta, alpha)
    _, X_r_align, Y_r_align = string_alignment(
        X_r, Y[min_split_index:], delta, alpha)

    # Conquer Step
    return (min_split_score, X_l_align + X_r_align, Y_l_align + Y_r_align)


# Function to measure memory usage
def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed


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
