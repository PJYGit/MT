# --------------------------
# Name: Jiayao Pang ID: 194174300
# CP460 (Fall 2019)
# Midterm Student Utilities File
# --------------------------

# -----------------------------------------------
# Remember to change the name of the file to:
#               utilities.py
# Delete this box after changing the file name
# ----------------------------------------------

# ----------------------------------------------
# You can not add any library other than these:
import math
import string
import random


# ----------------------------------------------

# -----------------------------------------------------------
# Parameters:   fileName (string)
# Return:       contents (string)
# Description:  Utility function to read contents of a file
#               Can be used to read plaintext or ciphertext
# -----------------------------------------------------------
def file_to_text(fileName):
    inFile = open(fileName, 'r', encoding=" ISO-8859-15")
    contents = inFile.read()
    inFile.close()
    return contents


# -----------------------------------------------------------
# Parameters:   None
# Return:       baseString (str)
# Description:  Returns base string for substitution cipher
# -----------------------------------------------------------
def get_baseString():
    # generate alphabet
    alphabet = ''.join([chr(ord('a') + i) for i in range(26)])
    symbols = """.,; #"?'!:-"""  # generate punctuations
    return alphabet + symbols


# -----------------------------------------------------------
# Parameters:   key (str)
# Return:       key (str)
# Description:  Utility function for Substitution cipher
#               Exchanges '#' wiht '\n' and vice versa
# -----------------------------------------------------------
def adjust_key(key):
    if '#' in key:
        newLineIndx = key.index('#')
        key = key[:newLineIndx] + '\n' + key[newLineIndx + 1:]
    else:
        newLineIndx = key.index('\n')
        key = key[:newLineIndx] + '#' + key[newLineIndx + 1:]
    return key


# -------------------------------------------------------------------------------------
# Parameters:   ciphertext (str)
#               baseString (str)
# Return:       None
# Description:  A debugging tool for substitution cipher
# ---------------------------------------------------------------------------------------
def debug_substitution(ciphertext, baseString):
    subString = ['-' for i in range(len(baseString))]
    plaintext = ['-' for i in range(len(ciphertext))]
    print('Ciphertext:')
    print(ciphertext[:200])
    print()
    command = input('Debug Mode: Enter Command: ')
    description = input('Description: ')
    print()

    while command != 'end':
        subChar = command[8].lower()
        baseChar = command[15].lower()

        if subChar == '#':
            subChar = '\n'
        if baseChar == '#':
            baseChar = '\n'

        if baseChar in baseString:
            indx = baseString.index(baseChar)
            subString[indx] = subChar
        else:
            print('(Error): Base Character does not exist!\n')

        print('Base:', end='')
        for i in range(len(baseString)):
            if baseString[i] == '\n':
                print('# ', end='')
            else:
                print('{} '.format(baseString[i]), end='')
        print()
        print('Sub :', end='')
        for i in range(len(subString)):
            if subString[i] == '\n':
                print('# ', end='')
            else:
                print('{} '.format(subString[i]), end='')
        print('\n')

        print('ciphertext:')
        print(ciphertext[201:500])  # <---- you can edit this if you need to show more text
        for i in range(len(plaintext)):
            if ciphertext[i].lower() == subChar:
                if subChar == '#' or subChar == '\n':
                    plaintext[i] == '\n'
                else:
                    plaintext[i] = baseChar
        print('plaintext :')
        print("".join(plaintext[201:500]))  # <---- you can edit this if you need to show more text
        print('\n_______________________________________\n')
        command = input('Enter Command: ')
        description = input('Description: ')
        print()
    return


# you can add any utility functions as you like


# -----------------------------------------------------------------------------
# Parameters:   text (string)
#               size (int)
# Return:       list of strings
# Description:  Break a given string into strings of given size
#               Result is provided in a list
# ------------------------------------------------------------------------------
def text_to_blocks(text, size):
    blocks = list()
    element = ''
    for char in text:
        if len(element) == size:
            blocks.append(element)
            element = ''
        element += char
    # do not forget the last block whose size is not equal to 'size'
    if len(element) != 0:
        blocks.append(element)

    return blocks


# -------------------------------------------------------------------------------------
# Parameters:   blocks: list of strings
# Return:       baskets: list of strings
# Description:  Assume all blocks have same size = n (other than last block)
#               Create n baskets
#               In basket[i] put character #i from each block
# ---------------------------------------------------------------------------------------
def blocks_to_baskets(blocks):
    # your code here
    # init the list to store string types
    empty = ''
    baskets = [empty] * len(blocks[0])

    for c in range(len(blocks[0])):
        for element in blocks:
            if c < len(element):
                baskets[c] += element[c]

    return baskets


# -----------------------------------------------------------
# Parameters:   dictFile (string): filename
# Return:       list of words (list)
# Description:  Reads a given dictionary file
#               dictionary file is assumed to be formatted: each word in a separate line
#               Returns a list of strings, each pertaining to a dictionary word
# -----------------------------------------------------------
def load_dictionary(dictFile):
    inFile = open(dictFile, 'r', encoding=" ISO-8859-15")
    dictList = inFile.readlines()
    i = 0
    for word in dictList:
        dictList[i] = word.strip('\n')
        i += 1
    inFile.close()
    return dictList


# -------------------------------------------------------------------
# Parameters:   text (string)
# Return:       list of words (list)
# Description:  Reads a given text
#               Each word is saved as an element in a list.
#               Returns a list of strings, each pertaining to a word in file
#               Gets rid of all punctuation at the start and at the end
# -------------------------------------------------------------------
def text_to_words(text):
    wordList = []
    lines = text.split('\n')
    for line in lines:
        line = line.strip('\n')
        line = line.split(' ')
        for i in range(len(line)):
            if line[i] != '':
                line[i] = line[i].strip(string.punctuation)
                wordList += [line[i]]
    return wordList


# -----------------------------------------------------------
# Parameters:   text (string)
#               dictFile (string): dictionary file
# Return:       (#matches, #mismatches)
# Description:  Reads a given text, checks if each word appears in dictionary
#               Returns a tuple of number of matches and number of mismatches.
#               Words are compared in lowercase.
# -----------------------------------------------------------
def analyze_text(text, dictFile):
    dictList = load_dictionary(dictFile)
    wordList = text_to_words(text)
    matches = 0
    mismatches = 0
    for word in wordList:
        if word.lower() in dictList:
            matches += 1
        else:
            mismatches += 1
    return (matches, mismatches)


# -----------------------------------------------------------
# Parameters:   text (string)
#               dictFile (string): dictionary file
#               threshold (float): number between 0 to 1
# Return:       True/False
# Description:  Check if a given file is a plaintext
#               If #matches/#words >= threshold --> True
#                   otherwise --> False
#               If invalid threshold given, default is 0.9
#               An empty string is assumed to be non-plaintext.
# -----------------------------------------------------------
def is_plaintext(text, dictFile, threshold):
    if text == '':
        return False
    result = analyze_text(text, dictFile)
    percentage = result[0] / (result[0] + result[1])
    if threshold < 0 or threshold > 1:
        threshold = 0.9
    if percentage >= threshold:
        return True
    return False


# -----------------------------------------------------------
# Parameters:   None
# Return:       squqre (list of strings)
# Description:  Constructs Vigenere square as list of strings
#               element 1 = "abcde...xyz"
#               element 2 = "bcde...xyza" (1 shift to left)
# -----------------------------------------------------------
def get_vigenereSquare():
    alphabet = get_lower()
    return [shift_string(alphabet, i, 'l') for i in range(26)]


# -----------------------------------------------------------
# Parameters:   None
# Return:       alphabet (string)
# Description:  Return a string of lower case alphabet
# -----------------------------------------------------------
def get_lower():
    return "".join([chr(ord('a') + i) for i in range(26)])


# -------------------------------------------------------------------
# Parameters:   s (string): input string
#               n (int): number of shifts
#               d (str): direction ('l' or 'r')
# Return:       s (after applying shift
# Description:  Shift a given string by n shifts (circular shift)
#               as specified by direction, l = left, r= right
#               if n is negative, multiply by 1 and change direction
# -------------------------------------------------------------------
def shift_string(s, n, d):
    if d != 'r' and d != 'l':
        print('Error (shift_string): invalid direction')
        return ''
    if n < 0:
        n = n * -1
        d = 'l' if d == 'r' else 'r'
    n = n % len(s)
    if s == '' or n == 0:
        return s

    s = s[n:] + s[:n] if d == 'l' else s[-1 * n:] + s[:-1 * n]

    return s


# -----------------------------------------------------------
# Parameters:   text (str)
# Return:       list: wordCount
# Description:  Count frequency of letters in a given text
#               Returns a list, first element is count of 'a'
#               Counts both 'a' and 'A' as one character
# -----------------------------------------------------------
def get_charCount(text):
    return [text.count(chr(97 + i)) + text.count(chr(65 + i)) for i in range(26)]


# -----------------------------------
# Parameters:   text (string)
# Return:       modifiedText (string)
# Description:  Removes all non-alpha characters from the given string
#               Returns a string of only alpha characters upper case
# -----------------------------------
def remove_nonalpha(text):
    # your code here
    modifiedText = ''
    for char in text:
        if char.isalpha():
            modifiedText += char

    return modifiedText


# ----------------------------------------------------------------
# Parameters:   ciphertext(string)
# Return:       I (float): Index of Coincidence
# Description:  Computes and returns the index of coincidence
#               for a given text
# ----------------------------------------------------------------
def get_indexOfCoin(ciphertext):
    # your code here
    ciphertext = remove_nonalpha(ciphertext)
    length = len(ciphertext)
    # make sure 'divided by 0' error would not occur
    if length < 2:
        return 0
    countList = get_charCount(ciphertext)

    # calculate the sum
    sum = 0
    for charCount in countList:
        sum += charCount * (charCount - 1)
    # use the formula to get the final result
    I = sum / (length * (length - 1))

    return I


# ----------------------------------------------------------------
# Parameters:   ciphertext(string)
# Return:       key length (int)
# Description:  Uses Friedman's test to compute key length
#               returns key length rounded to nearest integer
# ---------------------------------------------------------------
def getKeyL_friedman(ciphertext):
    # your code here
    I = get_indexOfCoin(ciphertext)
    k = round((0.068 - 1 / 26) / (I - 1 / 26))
    return k


# ----------------------------------------------------------------
# Parameters:   ciphertext(string)
# Return:       key length (int)
# Description:  Uses the Ciphertext Shift method to compute key length
#               Attempts key lengths 1 to 20
# ---------------------------------------------------------------
def getKeyL_shift(ciphertext):
    # your code here
    resultList = list()

    for i in range(1, 21):
        sum = 0
        counter = 0
        for char in ciphertext[i:]:
            # add 1 if it matches
            if char == ciphertext[counter]:
                sum += 1
            counter += 1
        resultList.append(sum)

    # get the index and add 1
    k = resultList.index(max(resultList)) + 1

    return k


# -------------------------------------------------------------------------------------
# Parameters:   plaintext(string)
#               key: (shifts,direction) (int,str)
# Return:       ciphertext (string)
# Description:  Encryption using Shfit Cipher (Monoalphabetic Substitituion)
#               The alphabet is shfited as many as "shifts" using given direction
#               Non alpha characters --> no substitution
#               Valid direction = 'l' or 'r'
#               Algorithm preserves case of the characters
# ---------------------------------------------------------------------------------------
def e_shift(plaintext, key):
    alphabet = get_lower()

    shifts, direction = key
    if shifts < 0:
        shifts *= -1
        direction = 'l' if key[1] == 'r' else 'r'
    shifts = key[0] % 26
    shifts = shifts if key[1] == 'l' else 26 - shifts

    ciphertext = ''
    for char in plaintext:
        if char.lower() in alphabet:
            plainIndx = alphabet.index(char.lower())
            cipherIndx = (plainIndx + shifts) % 26
            cipherChar = alphabet[cipherIndx]
            ciphertext += cipherChar.upper() if char.isupper() else cipherChar
        else:
            ciphertext += char
    return ciphertext


# -------------------------------------------------------------------------------------
# Parameters:   ciphertext(string)
#               key: (shifts,direction) (int,str)
# Return:       ciphertext (string)
# Description:  Decryption using Shfit Cipher (Monoalphabetic Substitituion)
#               The alphabet is shfited as many as "shifts" using given direction
#               Non alpha characters --> no substitution
#               Valid direction = 'l' or 'r'
#               Algorithm preserves case of the characters
#               Trick: Encrypt using same #shifts but the other direction
# ---------------------------------------------------------------------------------------
def d_shift(ciphertext, key):
    direction = 'l' if key[1] == 'r' else 'r'
    return e_shift(ciphertext, (key[0], direction))


# -----------------------------------------------------------
# Parameters:   None
# Return:       list
# Description:  Return a list with English language letter frequencies
#               first element is frequency of 'a'
# -----------------------------------------------------------
def get_freqTable():
    freqTable = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
                 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
                 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
                 0.00978, 0.0236, 0.0015, 0.01974, 0.00074]
    return freqTable


# -----------------------------------------------------------
# Parameters:   text (string)
# Return:       double
# Description:  Calculates the Chi-squared statistics
#               chiSquared = for i=0(a) to i=25(z):
#                               sum( Ci - Ei)^2 / Ei
#               Ci is count of character i in text
#               Ei is expected count of character i in English text
#               Note: Chi-Squared statistics uses counts not frequencies
# -----------------------------------------------------------
def get_chiSquared(text):
    freqTable = get_freqTable()
    charCount = get_charCount(text)

    result = 0
    for i in range(26):
        Ci = charCount[i]
        Ei = freqTable[i] * len(text)
        result += ((Ci - Ei) ** 2) / Ei
    return result


# -----------------------------------
# Parameters:   text (string)
# Return:       nonalphaList (2D List)
# Description:  Analyzes a given string
#               Returns a list of non-alpha characters along with their positions
#               Format: [[char1, pos1],[char2,post2],...]
#               Example: get_nonalpha('I have 3 cents.') -->
#                   [[' ', 1], [' ', 6], ['3', 7], [' ', 8], ['.', 14]]
# -----------------------------------
def get_nonalpha(text):
    # your code here
    nonalphaList = list()
    counter = 0
    for char in text:
        if char.isalpha() is False:
            nonalphaList.append((char, counter))
        counter += 1

    return nonalphaList


# -------------------------------------------------------------------
# Parameters:   text (string)
# Return:       list of words (list)
# Description:  Reads a given text
#               Each word is saved as an element in a list.
#               Returns a list of strings, each pertaining to a word in file
#               Gets rid of all punctuation at the start and at the end
# -------------------------------------------------------------------
def text_to_words(text):
    wordList = []
    lines = text.split('\n')
    for line in lines:
        line = line.strip('\n')
        line = line.split(' ')
        for i in range(len(line)):
            if line[i] != '':
                line[i] = line[i].strip(string.punctuation)
                wordList += [line[i]]
    return wordList


# -----------------------------------
# Parameters:   text (str)
#               2D list: [[char1,pos1], [char2,pos2],...]
# Return:       modifiedText (string)
# Description:  inserts a list of nonalpha characters in the positions
# -----------------------------------
def insert_nonalpha(text, nonAlpha):
    # your code here
    modifiedText = text

    counter = 0
    for l in nonAlpha:
        # using [:] to handle strings
        temp1 = modifiedText[:l[1]]
        temp2 = modifiedText[l[1]:]
        modifiedText = temp1 + l[0] + temp2
        counter += 1

    return modifiedText


def get_shiftStringList():
    atbash_lower = ''
    regular_lower = get_lower()
    for c in regular_lower:
        atbash_lower += regular_lower[ord('z') - ord(c)]
    regular_upper = regular_lower.upper()
    atbash_upper = atbash_lower.upper()

    shiftList = list()
    shiftList.append(regular_upper + regular_lower)
    shiftList.append(regular_upper + atbash_lower)
    shiftList.append(atbash_upper + regular_lower)
    shiftList.append(atbash_upper + atbash_lower)

    shiftList.append(regular_lower + regular_upper)
    shiftList.append(regular_lower + atbash_upper)
    shiftList.append(atbash_lower + regular_upper)
    shiftList.append(atbash_lower + atbash_upper)

    return shiftList


c = file_to_text('ciphertext_Jiayao_Pang_q3.txt')

'''
charCount = get_charCount(remove_nonalpha(c))
print(charCount)
length = len(remove_nonalpha(c))

counter = 0
for char in charCount:
    charCount[counter] = round(float(char / length), 4)
    counter += 1

print(charCount)
print(get_freqTable())

wordList = text_to_words(c.replace('!', ' '))
single = list()

for word in wordList:
    if len(word) == 1 and word not in single:
        single.append(word)
print(single)
'''
debug_substitution(c, get_baseString())
