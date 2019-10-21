# --------------------------
# Name: Jiayao Pang ID: 19417430
# CP460 (Fall 2019)
# Midterm Student Solution File
# --------------------------

# ----------------------------------------------
# You can not add any library other than these:
import math
import string
import random
import utilities


# ----------------------------------------------

# ---------------------------------
#           Q0: Matching         #
# ---------------------------------
# -------------------------------------------------------
#                   EDIT THIS FILE
# change this function such that it makes the proper matching
# Also provide your description of how you found the matching. 
# -------------------------------------------------------
def match_files():
    # Files related to vigenere cipher
    cipher1 = 'ciphertext_Jiayao_Pang_q4.txt'  # <--- change this
    plain1 = 'plaintext_Jiayao_Pang_q4.txt'  # <--- change this
    vigenereFiles = [plain1, cipher1]
    print('The Vigenere ciphertext file is:', cipher1)
    print('I found that the above file is a vigenere cipher by noticing that\n'
          'the text seems just like a random text. And it does not match the\n'
          'features of other 3 ways of encryption. The punctuations in this\n'
          'text is normal and there are not too many upper alphabets. It also\n'
          'does not end with letter q.')  # <--- complete this
    print()

    # Files related to substitution cipher
    cipher2 = 'ciphertext_Jiayao_Pang_q3.txt'  # <--- change this
    plain2 = 'plaintext_Jiayao_Pang_q3.txt'  # <--- change this
    subFiles = [plain2, cipher2]
    print('The Substitution ciphertext file is:', cipher2)
    print('I found that the above file is a substitution cipher by noticing that\n'
          'There are few new line characters which means that the new line characters\n'
          'are most likely substituted by other characters')  # <--- complete this
    print()

    # Files related to xshift cipher
    cipher3 = 'ciphertext_Jiayao_Pang_q2.txt'  # <--- change this
    plain3 = 'plaintext_Jiayao_Pang_q2.txt'  # <--- change this
    xshiftFiles = [plain3, cipher3]
    print('The xshift ciphertext file is:', cipher3)
    print('I found that the above file is an xshift cipher by noticing that\n'
          'there are so many upper alphabets in the cipher which suits the way\n'
          'of xshift encryption where the shiftString is constructed with half\n'
          'upper alphabets and half lower alphabets.')  # <--- complete this
    print()

    # Files related to xcrypt cipher
    cipher4 = 'ciphertext_Jiayao_Pang_q1.txt'  # <--- change this
    plain4 = 'plaintext_Jiayao_Pang_q1.txt'  # <--- change this
    xcryptFiles = [plain4, cipher4]
    print('The xcrypt ciphertext file is:', cipher4)
    print('I found that the above file is an xcrypt cipher by noticing that\n'
          'the text ends with q. Then I traced back from the last letter of \n'
          'the cipher and it is obvious that there are several letter q and the\n'
          'distance between every 2 successive q is all the same.')  # <--- complete this
    print()

    return [vigenereFiles, subFiles, xshiftFiles, xcryptFiles]


# ---------------------------------
#         Q1: Vigenere           #
# ---------------------------------

# -----------------------------------------------------------
# Parameters:   plaintext(string)
#               key (str): a phrase
# Return:       ciphertext (string)
# Description:  Enryption using Vigenere Cipher (Q1)
# -----------------------------------------------------------
def e_vigenere(plaintext, key):
    # your code here
    ciphertext = ''
    square = utilities.get_vigenereSquare()
    length = len(key)
    counter = 0

    # use the letter from key to encrypt not the plaintext itself
    # use mod function to make it recursive
    for char in plaintext:
        if char.lower() in square[0]:
            plainIndex = square[0].index(char.lower())
            keyIndex = square[0].index(key[counter % length].lower())
            cipherChar = square[keyIndex][plainIndex]
            ciphertext += cipherChar.upper() if char.isupper() else cipherChar
            counter += 1
            counter %= length
        else:
            ciphertext += char
    return ciphertext


# -----------------------------------------------------------
# Parameters:   ciphertext(string)
#               key (str): a phrase
# Return:       ciphertext (string)
# Description:  Decryption using Vigenere Cipher (Q1)
# -----------------------------------------------------------
def d_vigenere(ciphertext, key):
    # your code here
    plaintext = ''
    square = utilities.get_vigenereSquare()
    length = len(key)

    # use the letter from key to decrypt
    # use mod function to make it recursive
    counter = 0
    for char in ciphertext:
        if char.lower() in square[0]:
            keyIndex = square[0].index(key[counter % length].lower())
            counter += 1
            counter %= length
            plainIndex = 0
            for i in range(26):
                if square[i][keyIndex] == char.lower():
                    plainIndex = i
                    break

            plainChar = square[0][plainIndex]

            plaintext += plainChar.upper() if char.isupper() else plainChar

        else:
            plaintext += char
    return plaintext


# -----------------------------------------------------------
# Parameters:   ciphertext(string)
# Return:       key,plaintext
# Description:  Cryptanlysis of Vigenere Cipher (Q1)
# -----------------------------------------------------------
def cryptanalysis_vigenere(ciphertext):
    # yoru code here
    FriedmanL = utilities.getKeyL_friedman(ciphertext)
    ShiftL = utilities.getKeyL_shift(ciphertext)
    non_alpha = utilities.get_nonalpha(ciphertext)

    if ShiftL != 1:
        # try every possible size
        start = min(FriedmanL, ShiftL)
        if start >= 3:
            start -= 1
        end = max(FriedmanL, ShiftL) + 2
        modified = utilities.remove_nonalpha(ciphertext)
        for size in range(start, end):
            plaintext = ''
            shiftList = []
            blocks = utilities.text_to_blocks(modified, size)
            baskets = utilities.blocks_to_baskets(blocks)

            for element in baskets:
                # get the list of chi_squared for every shift
                chiList = [round(utilities.get_chiSquared(utilities.d_shift(element, (i, 'l'))), 4)
                           for i in range(26)]

                shiftList.append(chiList.index(min(chiList)))

            for i in range(len(baskets)):
                baskets[i] = utilities.d_shift(baskets[i], (shiftList[i], 'l'))

            result = utilities.blocks_to_baskets(baskets)
            for e in result:
                plaintext += e

            plaintext = utilities.insert_nonalpha(plaintext, non_alpha)

            if utilities.is_plaintext(plaintext, 'engmix.txt', 0.90):
                plain = utilities.remove_nonalpha(plaintext)[:size]
                key = ''
                v_square = utilities.get_vigenereSquare()
                counter = 0
                for pChar in plain:
                    pIndex = v_square[0].index(pChar)
                    kIndex = v_square[pIndex].index(blocks[0][counter])
                    counter += 1
                    key += v_square[0][kIndex]

                return key, plaintext

    key = 0
    plaintext = ''

    return key, plaintext


def comments_q1():
    print('Comments:')
    print('How I found the key length:\n'
          'I used getKeyL_friedman(ciphertext) and getKeyL_shift(ciphertext)\n'
          'to get the approximate range of the length.\n'
          'Then I made the range guessed larger to make sure I will not miss the correct length\n'
          'Next, I used the range to make a loop :\n'
          '    1st: text_to_blocks\n'
          '    2nd: blocks_to_baskets\n'
          '    3rd: try 26 times of d_shift() for every basket and get the chi_square list\n'
          '    4th: select the minimum chi_square value and its index is the shift length\n'
          '         after this step, we got the shift length of every basket'
          '    5th: then it is easy for me to construct the plaintext\n'
          '    6th: with using is_plaintext(), I will know if this length is right\n'
          '    7th: if the key length is wrong, then try next key length until I got the right answer')
    print('How I found the keyword: \n'
          'After I got the right plaintext and the key length, and I have got the ciphertext already.\n'
          'Then it is easy for me to find the key according to the vegenere square.')
    return


# ---------------------------------
#   Q2: Substitution Cipher      #
# ---------------------------------
# -------------------------------------------------------
# Parameters:   plaintext(str)
#               key: subString (str)
# Return:       ciphertext (string)
# Description:  Encryption using substitution (Q2)
# -------------------------------------------------------
def e_substitution(plaintext, key):
    # your code here
    ciphertext = ''
    plaintext = plaintext.replace('\n', '#')
    key = utilities.adjust_key(key)
    baseString = utilities.get_baseString()

    for plainChar in plaintext:
        upperFlag = True if plainChar.isupper() else False
        plainChar = plainChar.lower()

        if plainChar in baseString:
            Index = baseString.index(plainChar)
            cipherChar = key[Index]
            cipherChar = cipherChar.upper() if upperFlag else cipherChar

        else:
            cipherChar = plainChar

        ciphertext += cipherChar

    ciphertext = ciphertext.replace('#', '\n')

    return ciphertext


# -----------------------------------------
# Parametes:    ciphertext (str)
#               key: subString (str)
# Return:       plaintext (str)
# Description:  Decryption using substitution (Q2)
# -----------------------------------------
def d_substitution(ciphertext, key):
    # your code here
    plaintext = ''
    ciphertext = ciphertext.replace('\n', '#')
    key = utilities.adjust_key(key)
    baseString = utilities.get_baseString()

    for cipherChar in ciphertext:
        upperFlag = True if cipherChar.isupper() else False
        cipherChar = cipherChar.lower()

        if cipherChar in key:
            Index = key.index(cipherChar)
            plainChar = baseString[Index]
            plainChar = plainChar.upper() if upperFlag else plainChar

        else:
            plainChar = cipherChar

        plaintext += plainChar

    plaintext = plaintext.replace('#', '\n')

    return plaintext


def cryptanalysis_substitution(ciphertext):
    key = '''yhribekafszmpxwojductnvlgq!-#;". '?,:'''  # <--- change this line with your key
    key = utilities.adjust_key(key)  # <--- keep this line
    # add lines to decrypt the ciphertext
    # remember to write your plaintext to file
    return key, plaintext


def comments_q2():
    print('Comments:')
    print('See Qutaiba_Albluwi_sub_log.txt file')  # <----- edit this
    return


# ---------------------------------
#           Q3: Xshift           #
# ---------------------------------

# -----------------------------------------
# Parametes:    plaintext (str)
#               key: (shiftString,shifts)
# Return:       ciphertext (str)
# Description:  Encryption using Xshift Cipher
# -----------------------------------------
def e_xshift(plaintext, key):
    # your code here
    baseString = key[0]
    subString = utilities.shift_string(key[0], int(key[1]), 'l')
    ciphertext = ''

    for plainChar in plaintext:
        if plainChar in subString:
            Index = baseString.index(plainChar)
            cipherChar = subString[Index]
        else:
            cipherChar = plainChar

        ciphertext += cipherChar

    return ciphertext


# -----------------------------------------
# Parametes:    ciphertext (str)
#               key: (shiftString,shifts)
# Return:       plaintext (str)
# Description:  Decryption using Xshift Cipher
# -----------------------------------------
def d_xshift(ciphertext, key):
    # your code here
    baseString = key[0]
    subString = utilities.shift_string(key[0], int(key[1]), 'l')
    plaintext = ''

    for cipherChar in ciphertext:
        if cipherChar in baseString:
            Index = subString.index(cipherChar)
            plainChar = baseString[Index]
        else:
            plainChar = cipherChar

        plaintext += plainChar

    return plaintext


# -----------------------------------------
# Parametes:    ciphertext (str)
# Return:       key,plaintext
# Description:  Cryptanalysis of  Xshift Cipher
# -----------------------------------------
def cryptanalysis_xshift(ciphertext):
    # your code here
    wordList = utilities.text_to_words(ciphertext)
    single = list()

    for word in wordList:
        if len(word) == 1 and word not in single:
            single.append(word)

    shiftStringList = utilities.get_shiftStringList()

    for s in single:
        for shiftString in shiftStringList:
            now_c = shiftString.index(s)
            ori_c = shiftString.index('I')
            dis = now_c - ori_c if now_c > ori_c else now_c - ori_c + 52
            plaintext = d_xshift(ciphertext, (shiftString, dis))

            if utilities.is_plaintext(plaintext, 'engmix.txt', 0.90):
                return (shiftString, dis), plaintext

    key = ('', 0)
    plaintext = ''

    return key, plaintext


def comments_q3():
    print('Comments:')
    print('Brute-force space is: 16 <--- This means most likely, I will break the cipher after\n'
          'trying up to 16 times')
    print('Explain here your brute-force design\n'
          'Most likely, the word I and the word a will appear in every English text. So: \n'
          '    1st: text_to_words(ciphertext)\n'
          '    2nd: find every different word whose length is one and store them to the list named single\n'
          '    3rd: for every letter in single, try the 8 different kinds of shiftString to get each shift length\n'
          '    4th: use the shift length to d_xshift() and then use is_plaintext() to detect if the length is right\n'
          '    Until I got the right key.')
    return


# ---------------------------------
#           Q4: Xcrypt           #
# ---------------------------------
# -------------------------------------------------------
# Parameters:   plaintext(string)
#               key (int)
# Return:       ciphertext (string)
# Description:  Encryption using xcrypt (Q4)
# -------------------------------------------------------
def e_xcrypt(plaintext, key):
    # your code here
    ciphertext = ''

    blocks = utilities.text_to_blocks(plaintext, int(key))
    while len(blocks[-1]) != int(key):
        blocks[-1] += 'q'

    baskets = utilities.blocks_to_baskets(blocks)

    for basket in baskets:
        ciphertext += basket

    return ciphertext


# -------------------------------------------------------
# Parameters:   ciphertext(string)
#               key (int)
# Return:       plaintext (string)
# Description:  Decryption using xcrypt (Q4)
# -------------------------------------------------------
def d_xcrypt(ciphertext, key):
    # your code here
    plaintext = ''
    size = int(math.ceil(len(ciphertext) / key))

    blocks = utilities.text_to_blocks(ciphertext, size)
    baskets = utilities.blocks_to_baskets(blocks)

    for basket in baskets:
        plaintext += basket

    while plaintext[-1] == 'q':
        plaintext = plaintext[:-1]

    return plaintext


# -------------------------------------------------------
# Parameters:   ciphertext(string)
# Return:       key (int),plaintext (str)
# Description:  cryptanalysis of xcrypt (Q4)
# -------------------------------------------------------
def cryptanalysis_xcrypt(ciphertext):
    # your code here
    if ciphertext[-1] == 'q':
        lastIndex = ciphertext.rfind('q')
        Index = ciphertext.rfind('q', 0, lastIndex)

        possibleKey = len(ciphertext) / (lastIndex - Index)

        plaintext = d_xcrypt(ciphertext, possibleKey)
        if utilities.is_plaintext(plaintext, 'engmix.txt', 0.90):
            return int(possibleKey), plaintext

    found = False
    for i in range(1, 501):
        plaintext = d_xcrypt(ciphertext, i)
        if utilities.is_plaintext(plaintext, 'engmix.txt', 0.90):
            found = True
            break

    if found is False:
        return 0, ''

    return i, plaintext


# -------------------------------------------------------
# Parameters:   None
# Return:       None
# Description:  Your comments on Q4 solution
# -------------------------------------------------------
def comments_q4():
    print('My Comments:')
    print('Used threshold is: ', 0.90)
    print('Cryptanalysis Method: \n'
          'First of all, I find out the distance between the last 2 letters q.\n'
          'And then I guess: \n'
          '    possibleKey = len(ciphertext) / distance.\n'
          'Next, I use the possibleKey to d_xcrypt() and use is_plaintext() to see if it is successful'
          'If successful, return. Else, try real brute-force.')
    return


'''
p = utilities.file_to_text('ciphertext_Jiayao_Pang_q1.txt')
c = d_xcrypt(p, 147)
print(c)
f = open('plaintext_Jiayao_Pang_q1.txt', 'w')
f.write(c)
f.close()

print(cryptanalysis_xshift(p))

print(utilities.getKeyL_friedman(p))
print(utilities.getKeyL_shift(p))



# p = 'THISTERMISEASY'
# c = e_xcrypt(p, 82)
# print(e_xcrypt(p, 82))
# c = e_vigenere(p, 'disposition')
# print(d_vigenere(c, 'disposition'))

print(cryptanalysis_xcrypt(p))
'''
