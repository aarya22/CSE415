'''
PartII.py
Aman Arya, CSE 415, Autumn 2017, University of Washington
Instructor:  S. Tanimoto.
Assignment 2 Part II.  ISA Hierarchy Manipulation
Extra credit (Cycle detection and processing) implemented and working.
'''

from re import *  # Loads the regular expression module.
from collections import defaultdict

ISA = defaultdict(list)
INCLUDES = defaultdict(list)
ARTICLES = defaultdict(str)


def reset():
    global ISA, INCLUDES, ARTICLES, HAS
    ISA = defaultdict(list)
    INCLUDES = defaultdict(list)
    ARTICLES = defaultdict(str)


def store_isa_fact(category1, category2):
    'Stores one fact of the form A BIRD IS AN ANIMAL'
    # That is, a member of CATEGORY1 is a member of CATEGORY2
    ISA[category1].append(category2)
    INCLUDES[category2].append(category1)


def get_isa_list(category1):
    'Retrieves any existing list of things that CATEGORY1 is a'
    return ISA[category1]


def get_includes_list(category1):
    'Retrieves any existing list of things that CATEGORY1 includes'
    return INCLUDES[category1]


def isa_test1(category1, category2):
    'Returns True if category 2 is (directly) on the list for category 1.'
    return get_isa_list(category1).__contains__(category2)


def isa_test(category1, category2, depth_limit=10):
    'Returns True if category 1 is a subset of category 2 within depth_limit levels'
    if category1 == category2: return True
    if isa_test1(category1, category2): return True
    if depth_limit < 2: return False
    for intermediate_category in get_isa_list(category1):
        if isa_test(intermediate_category, category2, depth_limit - 1):
            return True
    return False


def store_article(noun, article):
    'Saves the article (in lower-case) associated with a noun.'
    ARTICLES[noun] = article.lower()


def get_article(noun):
    'Returns the article associated with the noun, or if none, the empty string.'
    return ARTICLES[noun]


def get_all_hasa(category):
    global ISA
    hasa = []
    for k in ISA.keys():
        if isa_test(k, category) and k != category:
            hasa.append(k)
    return hasa


def get_all_isa(category, l, visited=None):
    if visited is None:
        visited = set()
    visited.add(category)
    o = get_isa_list(category)
    if len(o) != 0:
        l.append(o)
        for k in o:
            if k not in visited:
                get_all_isa(k, l, visited=visited)
    return l

def know(x):
    'Returns information about x'
    s = x[1:-2]
    isa = get_all_isa(s, l=[])
    a1 = get_article(s).capitalize()

    for i in isa[0]:
        if isa_test1(s, i):
            a2 = get_article(s)
            print(a1 + ' ' + str(s) + ' is ' + a2 + ' ' + i + '; you told me that directly.\n')

    for j in isa[1:]:
        for l in j:
            a2 = get_article(l)
            print(a1 + ' ' + str(s) + ' is ' + a2 + ' ' + l + ', because ' + report_chain(s, l) + '\n')

    hasa = get_all_hasa(s)
    #print(hasa)
    for k in hasa:
        a2 = get_article(k)
        print(a1 + ' ' + str(s) + ' is something more general than ' + a2 + ' ' + str(k) + ', because ' + report_chain(k, s) + '\n')

    print('That\'s all I know about ' + x[:-1] + '.')



def linneus():
    'The main loop; it gets and processes user input, until "bye".'
    print('This is Linneus.  Please tell me "ISA" facts and ask questions.')
    print('For example, you could tell me "An ant is an insect."')
    print('Type \'test\' to run tests.')
    while True:
        info = input('Enter an ISA fact, or "bye" here: ')
        if info == 'bye': return 'Goodbye now!'
        if info == 'test':
            test()
        else:
            process(info)


# Some regular expressions used to parse the user sentences:
assertion_pattern = compile(r"^(a|an|A|An)\s+([-\w]+)\s+is\s+(a|an)\s+([-\w]+)(\.|\!)*$", IGNORECASE)
query_pattern = compile(r"^is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)
what_pattern = compile(r"^What\s+is\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)
why_pattern = compile(r"^Why\s+is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)


def process(info):
    'Handles the user sentence, matching and responding.'
    result_match_object = assertion_pattern.match(info)
    if result_match_object != None:
        items = result_match_object.groups()
        store_article(items[1], items[0])
        store_article(items[3], items[2])
        store_isa_fact(items[1], items[3])
        print("I understand.")
        return
    result_match_object = query_pattern.match(info)
    if result_match_object != None:
        items = result_match_object.groups()
        answer = isa_test(items[1], items[3])
        if answer:
            print("Yes, it is.")
        else:
            print("No, as far as I have been informed, it is not.")
        return
    result_match_object = what_pattern.match(info)
    if result_match_object != None:
        items = result_match_object.groups()
        supersets = get_isa_list(items[1])
        if supersets != []:
            first = supersets[0]
            a1 = get_article(items[1]).capitalize()
            a2 = get_article(first)
            print(a1 + " " + items[1] + " is " + a2 + " " + first + ".")
            return
        else:
            subsets = get_includes_list(items[1])
            if subsets != []:
                first = subsets[0]
                a1 = get_article(items[1]).capitalize()
                a2 = get_article(first)
                print(a1 + " " + items[1] + " is something more general than " + a2 + " " + first + ".")
                return
            else:
                print("I don't know.")
        return
    result_match_object = why_pattern.match(info)
    if result_match_object != None:
        items = result_match_object.groups()
        if not isa_test(items[1], items[3]):
            print("But that's not true, as far as I know!")
        else:
            answer_why(items[1], items[3])
        return

    x = info.split(' ')
    if x[0] == 'Tell' or x[0] == 'tell':
        know(x[6])
        return
    print("I do not understand.  You entered: ")
    print(info)


def answer_why(x, y):
    'Handles the answering of a Why question.'
    if x == y:
        print("Because they are identical.")
        return
    if isa_test1(x, y):
        print("Because you told me that.")
        return
    print("Because " + report_chain(x, y))
    return


from functools import reduce


def report_chain(x, y):
    'Returns a phrase that describes a chain of facts.'
    chain = find_chain(x, y)
    if len(chain) > 1:
        all_but_last = chain[0:-1]
        last_link = chain[-1]
        main_phrase = reduce(lambda x, y: x + y, map(report_link, all_but_last))
        last_phrase = "and " + report_link(last_link)
        new_last_phrase = last_phrase[0:-2] + '.'
        return main_phrase + new_last_phrase
    else:
        phrase = list(report_link(chain[0]))
        phrase[-2] = '.'

        return ''.join(phrase)

def report_link(link):
    'Returns a phrase that describes one fact.'
    x = link[0]
    y = link[1]
    a1 = get_article(x)
    a2 = get_article(y)
    return a1 + " " + x + " is " + a2 + " " + y + ", "


def find_chain(x, z):
    'Returns a list of lists, which each sublist representing a link.'
    if isa_test1(x, z):
        return [[x, z]]
    else:
        for y in get_isa_list(x):
            if isa_test(y, z):
                temp = find_chain(y, z)
                temp.insert(0, [x, y])
                return temp


def test():
    CASE1 = [
        ("A turtle is a reptile.", None),
        ("A turtle is a shelled-creature.", None),
        ("A reptile is an animal.", None),
        ("An animal is a thing.", None),
        ("Is a turtle a reptile.", ["Yes, it is."]),
        ("Is a turtle an animal.", ["Yes, it is."]),
        ("What is a turtle?", ["A turtle is a reptile."]),
        ("Why is a turtle an animal?", ["Because a turtle is a reptile, and a reptile is an animal."]),
        ("Why is an animal a reptile?", ["But that's not true, as far as I know!"]),
        ("Tell me what you know about \'turtle\', with justification.", [
            "A turtle is a reptile; you told me that directly.",
            "A turtle is a shelled-creature; you told me that directly.",
            "A turtle is an animal, because a turtle is a reptile and a reptile is an animal.",
            "A turtle is a thing, because a turtle is a reptile, a reptile is an animal, and an animal is a thing.",
            "That's all I know about \'turtle\'."]),
    ]

    CASE2 = [
        ("A BugsBunny is a cartoon.", None),
        ("A DaffyDuck is a cartoon.", None),
        ("A BugsBunny is a rabbit.", None),
        ("A DaffyDuck is a duck.", None),
        ("A duck is a bird.", None),
        ("A bird is an animal", None),
        ("A rabbit is a mammal.", None),
        ("A mammal is an animal.", None),
        ("Is a BugsBunny an animal?", ["Yes, it is."]),
        ("Is a DaffyDuck a rabbit?", ["No, as far as I have been informed, it is not."]),
        ("Tell me what you know about \'DaffyDuck\', with justification.", [
            "A DaffyDuck is a cartoon; you told me that directly.",
            "A DaffyDuck is a duck; you told me that directly.",
            "A DaffyDuck is a bird, because a DaffyDuck is a duck and a duck is a bird",
            "A DaffyDuck is an animal, because a DaffyDuck is a duck, a duck is a bird, and a bird is an animal.",
            "That's all I know about \'DaffyDuck\'."]),
        ("Tell me what you know about \'rabbit\', with justification.", [
            "A rabbit is a mammal; you told me that directly.",
            "A rabbit is an animal, because a rabbit is a mammal and a mammal is an animal.",
            "A rabbit is something more general than a BugsBunny, because a BugsBunny is a rabbit.",
            "That's all I know about \'rabbit\'."]),
    ]

    TESTS = [CASE2]

    import sys
    import io
    old_stdout = sys.stdout
    new_stdout = io.StringIO()

    for i, case in enumerate(TESTS):
        print("======== TEST %d =========" % i)
        reset()
        for inp, out in case:
            print("         INPUT: %s" % inp)
            sys.stdout = new_stdout
            process(inp)
            sys.stdout = old_stdout
            lines = [x.strip() for x in new_stdout.getvalue().split("\n") if x.strip()]
            new_stdout = io.StringIO()
            if out is not None:
                for l in lines:
                    print("   YOUR OUTPUT: %s" % l)
                for l in out:
                    print("CORRECT OUTPUT: %s" % l)
                print("")
        print("")


#linneus()
test()
