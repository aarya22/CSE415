"""
Aman Arya
aarya22@uw.edu
1535134
CSE 415

A conversational agent modeled on Dennis, the repressed anarcho-syndacalist peasant
from Monty Python's Holy Grail.
"""

import string, random

# setting some defaults
MEMORY = {'possession': 'swords', 'think': 'exploting the workers', 'request': 'gathering filth', 'id': 'king', 'feel': 'outdated imperialist dogma'}

# boolean for cycling
x = True

def introduce():
    return 'I\'m Dennis the 37 year old repressed Peasant, that\'s my name. \nNot like you would bother to find out, you automatically treat me \nas an inferior. I live in an anarcho-syndacalist commune, and the \nexecutive officer for the week is aarya22@uw.edu.\n'


def agentName():
    return 'Dennis'


def respond(the_input):

    # Basic string processing
    global x
    x = not x
    exclude = set(string.punctuation)
    the_input = ''.join(c for c in the_input if c not in exclude)  # remove punctuation
    wordlist = the_input.split(' ')
    wordlist = [k.lower() for k in wordlist]  # lowercase all words in input
    # Mapped wordlist
    mapped_wordlist = you_me_map(wordlist)

    if 'hi' in wordlist or 'hello' in wordlist or 'hey' in wordlist:
        # Response to greeting
        if x:
            return "I already gave an introduction damn it!"
        else:
            return "We\'ve been over this already. I\'m Dennis the 37 year old peasant!"
    if wordlist[0] == '':
        # Response if no response given
        if x:
            return "Oh now we see the silence inherent in the system! \n" + punt()
        else:
            return "Not willin\' to engage in discourse eh. Typical imperialist tactic... \n" + punt()
    if wordlist[0:2] == ['i', 'am']:
        # Response to identity of other
        MEMORY['id'] = stringify(mapped_wordlist[2:])
        if x:
            return 'An\' how did you become a ' + \
                   stringify(mapped_wordlist[2:]) + '? By oppressing the workers? \n' + punt()
        else:
            return 'So a ' + \
                   stringify(mapped_wordlist[2:]) + \
                   '. \nWell I certainly didn\'t vote for you! \n' + punt()
    if 'please' in wordlist:
        # Response to asking nicely
        return "Asking nicely won\'t work either! I\'m privy to your tricks! \n" + punt()
    if 'where' in wordlist:
        # Response about where Dennis lives
        return 'I live in an anarcho-syndacalist commune where we each take turns to be a sort of executive officer for the week \nbut all the decisions of that officer have to be ratified at a special bi-weekly meeting by a simple majority in the case of purely internal affairs \nbut by a two thirds majority in the case of external ones.'
    if wpred(wordlist[0]):
        # Response to any questions asked of Dennis
        if x:
            return 'Your interrogation will never work on me, capitalist dog! \n' + punt()
        else:
            return 'Oh ho ho! I\'ll be asking the questions here! \n' + punt()
    if 'have' in wordlist or 'had' in wordlist or 'has' in wordlist or 'my' in wordlist:
        # Response to anything about possessions
        if 'have' in wordlist:
            idx = wordlist.index('have')
        elif 'had' in wordlist:
            idx = wordlist.index('had')
        elif 'has' in wordlist:
            idx = wordlist.index('has')
        else:
            idx = wordlist.index('my')
        MEMORY['possession'] = stringify(mapped_wordlist[idx+1:])
        if x:
            return 'You know what? That\'s exactly the problem. Private property! \nJust another way the capitalists keep the workers down an\' perpetuatin\' \nthe cycle of class conflict!'
        else:
            return 'Have you now? Probably got ' + MEMORY['possession'] + ' from exploitin\' the workers!'
    if wordlist[0:2] == ['i', 'feel']:
        # Response to anything about what the other feels
        MEMORY['feel'] = stringify(mapped_wordlist[2:])
        if x:
            return 'Feel? I didn\'t know that dogs could feel ' + \
                   stringify(
                       mapped_wordlist[2:]) + '! Where was this feeling when you were busy exploitin\' the working class? \n' + punt()
        else:
            return 'Oh really? What about the way you feel about your outdated imperialist dogma? \n' + punt()
    if 'because' in wordlist:
        # Response to any justifications
        if x:
            return 'Don\'t justify your capitalist greed to me! I know all about it already! \n' + punt()
        else:
            return 'Oh sure sure... probably what you tell yourself at night to keep the nightmares \n of exploited children begging for mercy away'
    if 'yes' in wordlist or 'ok' in wordlist or 'yeah' in wordlist:
        # Response to agreeing with Dennis
        if x:
            return 'Agreeing with me? I\'shocked that you\'re capable of reason! \n' + punt()
        else:
            return 'What? What are you getting at? \n' + punt()
    if wordlist[0] == 'you':
        # Response to characterization of Dennis
        MEMORY['insult'] = stringify(mapped_wordlist[1:])
        if x:
            return "Help, help I\'m being oppressed! Come see the insults inherent in the system! \n" + punt()
        else:
            return "I object to you automatically treating me like an inferior \n" + punt()
    if wordlist[0:2] == ['can', 'you'] or wordlist[0:2] == ['could', 'you'] or 'please' in wordlist:
        # Response to requesting something from Dennis
        MEMORY['request'] = stringify(mapped_wordlist[2:])
        return "We already went over this. I\'m not going to " + stringify(mapped_wordlist[2:]) + " just so you can get fat off of my hard work! \n" + punt()
    if verbp(wordlist[0]) or dpred(wordlist[0]):
        # Response to telling Dennis to do something
        if x:
            return "Not simply satisfied with the legions you probably already have under your command eh? You want me to work for you now too? \n" + punt()
        else:
            return "What? So you make me slave away while you get rich off the disparity of what I produce and what you sell it for? \n" + punt()
    if wordlist[0:3] == ['do', 'you', 'think']:
        # Response to what Dennis thinks about anything
        MEMORY['think'] = stringify(mapped_wordlist[3:])
        return "Do I think " + stringify(mapped_wordlist[3:]) + "? No of course not, We're living in a dictatorship. ..... \n A self-perpetuating autocracy in which the working classes are ravaged by the greed of pigs like you!"
    if 'workers' in wordlist or 'worker' in wordlist:
        # Response to mentioning workers
        return "Thinkin\' about the workers now eh? Only when its beneficial to your wealth!"
    if 'government' in wordlist:
        # Response to mentioning government
        return "Government huh! We\'re living in a dictatorship, a self perpetuating autocracy that persists \n through active suppression of the proleteriat!"
    if 'class' in wordlist:
        # Response to mentioning class
        return "Class, don\'t blame me for bringing class into this! You\'re the one who brought it up now!"
    if 'system' in wordlist:
        # Response to mentioning system
        return "Ah the system, probably going to show me the violence inherent in the system now!"
    if 'power' in wordlist:
        # Response to mentioning power
        return "Listen supreme executive power has to be derived from a mandate from the masses! Not from some farcical aquatic ceremonies!"
    if 'water' in wordlist or 'aquatic' in wordlist:
        # Response to mentioning water or aquatic
        return "Bet you\'re a big fan of farcical aquatic ceremonies."
    if 'woman' in wordlist or 'girl' in wordlist or 'lady' in wordlist or 'female' in wordlist:
        # Response to being called a female
        return "Man damn it! I\'m a 37 year old man! Not that you would bother to find out"
    if 'no' in wordlist or 'not' in wordlist:
        # Response to a negatory statement
        if x:
            return "You disagree? Obviously the system is incapable of participating in dialogue! \n" + punt()
        else:
            return "Well! A challenge eh? Explain your reasoning at once imperialist dog! \n" + punt()

    return(punt())


CASE_MAP = {'i': 'you', 'I': 'you', 'me': 'you', 'you': 'me',
            'my': 'your', 'your': 'my',
            'yours': 'mine', 'mine': 'yours', 'am': 'are'}

def punt():
    PUNTS = ['Listen I don\'t know how you got ' + MEMORY['possession'] + ' but strange women lying aroun\' in ponds \n distributing ' + MEMORY['possession'] + ' is no basis for a system of government!',
             'Justify why you think ' + MEMORY['think'] + ' is alright.',
             'Why did you make ' + MEMORY['request'] + ' a priority? Exhaustin\' your worker supply already?',
             'So you\'re a ' + MEMORY['id'] + '? Got that from exploitin\' the workers did ya? Listen, supreme executive power comes \n from a mandate from the masses, not some farcical ceremony!',
             'Explain why you feel you\'re entitled to ' + MEMORY['feel'] + ' while you actively suppress feelings of dissent from the \n worker population you exploit on a daily basis!',
             'See if I mean, if I went around sayin\' I was an empereror just because some moistened bink had \n lobbed a scimitar at me they\'d put me away!']
    return random.choice(PUNTS)


def stringify(wordlist):
    # Adds spaces between words in wordlist
    return ' '.join(wordlist)


def you_me(w):
    # Changes a word from 1st to 2nd person or vice-versa.
    try:
        result = CASE_MAP[w]
    except KeyError:
        result = w
    return result


def you_me_map(wordlist):
    # Applies YOU-ME to a whole sentence or phrase.
    return [you_me(w) for w in wordlist]


def wpred(w):
    # Returns True if w is one of the question words.
    return w in ['when', 'why', 'where', 'how', 'what']


def dpred(w):
    # Returns True if w is an auxiliary verb.
    return w in ['do', 'can', 'should', 'would']


def verbp(w):
    # Returns True if w is one of these known verbs.
    return (w in ['go', 'have', 'be', 'try', 'eat', 'take', 'help',
                  'make', 'get', 'jump', 'write', 'type', 'fill',
                  'put', 'turn', 'compute', 'think', 'drink',
                  'blink', 'crash', 'crunch', 'add', 'work', 'see', 'hear'])

if __name__ == '__main__':
    print(introduce())
    while True:
        the_input = input('TYPE HERE:>> ')
        if the_input == 'bye':
            break
        print(respond(the_input))

