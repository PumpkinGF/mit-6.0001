# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

# ## END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        # getter
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        # getter
        return self.valid_words.copy()

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        self.shift_dict = {} # expect:{'A':'B','B':'C', ... 'a':'b','b':'c', ...}
        upper_letters = string.ascii_uppercase
        lower_letters = string.ascii_lowercase
        
        # shift for upper and lower, respectively
        for a in upper_letters: # 对upper_letters中每个字符（如'A'），找到位置，移动shift位，变成shift_dict中key 'A'对应的value
            upper_position = upper_letters.index(a)
            upper_shift_position = upper_position + shift
            if upper_shift_position > 25: # 注意是25不是26
                upper_shift_position -= 26
            self.shift_dict[a] = upper_letters[upper_shift_position]
            
        for b in lower_letters: # 对lower一样
            lower_position = lower_letters.index(b)
            lower_shift_position = lower_position + shift
            if lower_shift_position > 25:
                lower_shift_position -= 26
            self.shift_dict[b] = lower_letters[lower_shift_position]        
        
        return self.shift_dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        output_str = ''
        
        # call build_shift_dict(self, shift)
        shift_letter = self.build_shift_dict(shift)
        
        for letter in self.message_text:
            if letter in shift_letter.keys(): # if letter in 52, shift; otherwise, remain the same
                letter = shift_letter[letter]
                
            output_str += letter
        
        return output_str

# +
# test shift_dict
shift = 2

shift_dict = {} # expect:{'A':'B','B':'C', ... 'a':'b','b':'c', ...}
upper_letters = string.ascii_uppercase
lower_letters = string.ascii_lowercase

for a in upper_letters:
    upper_position = upper_letters.index(a)
    upper_shift_position = upper_position + shift
    if upper_shift_position > 25:
        upper_shift_position -= 26
    shift_dict[a] = upper_letters[upper_shift_position]

# print(shift_dict)
# -

# test apply_shift
a = Message('abc')
b = a.apply_shift(2)
print(b)


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        # from Style Guide #7: make use of inheritance (data attributes from parent class) as much as possible
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        
        num_words = []
        for s in range(26): # for every shift (1 - 26), 用apply_shift（output: 移位后的string）
            decrypt_output = self.apply_shift(s)
            decrypt_boolean = []
            for i in decrypt_output.split(): # 对每个单词，用is_word，返回true/false串
                decrypt_boolean.append(is_word(word_list, i))
            num_words.append(sum(decrypt_boolean))# 计算每个shift的true数量，返回一个数值，append到一个list（起始需要一个空list）
        max_shift = num_words.index(max(num_words)) # 找到最大true数量对应的shift值
        decrypt_mess = self.apply_shift(max_shift) # 找到对应的decrypted message
        return max_shift, decrypt_mess # 塞到一个tuple里面，return

# CiphertextMessage结构
        # for every shift (1 - 26), 用apply_shift（output: 移位后的string）
            # 对每个单词，用is_word，返回true/false串
            # 计算每个shift的true数量，返回一个数值，append到一个list（起始需要一个空list）
        # 找到最大true数量对应的shift值
        # 找到对应的decrypted message
        # 塞到一个tuple里面，return

if __name__ == '__main__':
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())
    ciphertext = CiphertextMessage('jgnnq') 
    print('Expected Output:', (24, 'hello')) 
    print('Actual Output:', ciphertext.decrypt_message())

#    #Example test case (PlaintextMessage)
#    plaintext = PlaintextMessage('hello', 2)
#    print('Expected Output: jgnnq')
#    print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    #Example test case (CiphertextMessage)
#    ciphertext = CiphertextMessage('jgnnq')
#    print('Expected Output:', (24, 'hello'))
#    print('Actual Output:', ciphertext.decrypt_message())

    #TODO: WRITE YOUR TEST CASES HERE

    #TODO: best shift value and unencrypted story 
    
    pass #delete this line and replace with your code here
