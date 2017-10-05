"""
Aman Arya

Assignment 1 Part A
"""


def three_x_cubed_plus_7(x):
    return 3 * x ** 3 + 7


def mystery_code(text):
    i = 0
    new = list(text)
    for c in text:
        if c.isalpha():
            if c.islower():
                if ord(c) >= ord('a') and ord(c) < ord('h'):
                    new[i] = chr(ord(c) - 13)
                else:
                    new[i] = chr(ord(c) - 39)
            else:
                new[i] = chr(ord(c)+25)
        else:
            new[i] = c
        i += 1

    text = ''.join(new)
    return text


def pair_off(l):
    return [l[i:i + 2] for i in range(0, len(l), 2)]


def past_tense(st):
    n = []
    vowels = ['a', 'e', 'i', 'o', 'u']
    for s in st:
        s = s.lower()
        if s == 'have':
            s = 'had'
        elif s == 'be':
            s = 'was'
        elif s == 'eat':
            s = 'ate'
        elif s == 'go':
            s = 'went'
        elif s.endswith('e'):
            s += 'd'
        elif s.endswith('y') and s[-2] not in vowels:
            new = list(s)
            new[-1] = 'i'
            s = ''.join(new)
            s += 'ed'
        elif s[-2] in vowels and s[-3] not in vowels and s[-1] not in vowels and s[-1] != 'y' and s[-1] != 'w':
            c = s[-1]
            s += c + 'ed'
        else:
            s += 'ed'


        n.append(s)

    return n


if __name__ == '__main__':
    print("Examples for three x cubed plus 7: ")
    print("With 2: " + str(three_x_cubed_plus_7(2)))
    print("With 22: " + str(three_x_cubed_plus_7(22)))
    print("With 10000000: " + str(three_x_cubed_plus_7(10000000)) + "\n")
    print("Examples of mystery code: ")
    print("With original example: " + str(mystery_code("abc Iz th1s Secure? n0, no, 9!")))
    print("With \"One by land, two by sea\": " + str(mystery_code(("One by land, two by sea"))))
    print("With \"Les sanglots longs Des violons De l\'automne Blessent mon coeur D'une langueur Monotone.\": " + str(mystery_code("Les sanglots longs Des violons De l\'automne Blessent mon coeur D'une langueur Monotone.\n")))
    print("Examples with pair-off: ")
    print("With original example: " + str(pair_off([2, 5, 1.5, 100, 3, 8, 7, 1, 1, 0, -2])))
    print("With [22]: " + str(pair_off([22])))
    print("With Golomb\'s sequence [1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8]: " + str(pair_off([1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8,])) + "\n")
    print("Examples with past tense: ")
    print("With original example: " + str(past_tense(['program', 'debug', 'execute', 'crash', 'repeat', 'eat'])))
    print("With ['have', 'be', 'try', 'blink', 'crash', 'crunch', 'add']: " + str(past_tense(['have', 'be', 'try', 'blink', 'crash', 'crunch', 'add'])))
    print("With ['want', 'go', 'laugh', 'cry', 'smile', 'subtract', 'multiply', 'smooth']: " + str(past_tense(['want', 'go', 'laugh', 'cry', 'smile', 'subtract', 'multiply', 'smooth'])))
    print(pair_off([]))
