# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    # base case
    if len(sequence) <= 1:
        return list(sequence)
    
    # recursive case
    else:
        first_letter = sequence[0]
        permutations = get_permutations(sequence[1:])
        perm_result = []
        for item in permutations:
            for i in range(len(item) + 1):
                perm_result.append(item[:i] + first_letter + item[i:])
        return perm_result
    
    # for recursive case, think about how to move from sequence - 1 to sequence
    # Example: we have 'ab' as sequence[1:], get_permutations should give us ['ab','ba']
    # For each of the elements, we add sequence[0] to all possible positions
    
    # tried this video to understand recursion: https://www.youtube.com/watch?v=ngCos392W4w&ab_channel=Reducible

sequence = 'abc'
print(get_permutations(sequence))

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))

#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    pass #delete this line and replace with your code here

