import sys
import os.path
import string
from os import path

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def error(err):
    print(err)
    sys.exit()

def getIndex(x, tab):
	try:
		return tab.index(x)
	except:
		return -1

def cleanContent(data):
    valid = []
    data = data.split('\n')
    for elem in data:
        elem = elem.split("#")[0].strip()
        if (elem):
            valid.append(elem)
    return valid

def generateFacts(givenFacts):
    facts = [-1] * 26
    j = 1
    while (j < len(givenFacts[0])):
        index = ord(givenFacts[0][j]) - 65
        facts[index] = 1
        j += 1
    return facts

def getRelated(rules, querie):
    i = 0
    related = []
    while (i < len(rules)):
        rule = rules[i].split('>')
        if (querie in rule[1]):
            related.append(rules[i])
        i += 1

    return (related)

def determine(a, b, ope, knownFacts):
    if (a == '0' or a == '1'):
        a = int(a)
    if (b == '0' or b == '1'):
        b = int(b)
    reverseA = False
    reverseB = False
    resultBool = False
    if (a != -1 and a != 0 and a != 1):
        if (a[0] == '!'):
            reverseA = True
            a = a[1]
        a = knownFacts[ord(a) - 65]
    if (b != -1 and b != 0 and b != 1):
        if (b[0] == '!'):
            reverseB = True
            b = b[1]
        b = knownFacts[ord(b) - 65]
    if (reverseA):
        a = not a
    if (reverseB):
        b = not b
    if (ope == '+'):
        if (a == 2 or b == 2):
            resultBool = 2
        else:
            resultBool = (a and b)
    if (ope == '|'):
        resultBool = (a or b)
    if (ope == '^'):
        resultBool = (a ^ b)

    if (resultBool == True):
        return (1)
    if (resultBool == False):
        return (0)
    return (resultBool)

def crunch(rule, facts):
    operators = rule.split()
    if (len(operators) == 1):
        reverse = False
        if (operators[0][0] == '!'):
            reverse = True
            operators[0] = operators[0][1]
            value = facts[ord(operators[0]) - 65]
            return(not value)
        else:
            value = facts[ord(operators[0]) - 65]
            return (value)
    while (len(operators) > 1):
        if ('+' in operators):
            index = getIndex('+', operators)
            operand = operators[index]
            operators[index + 1] = determine(operators[index - 1], operators[index + 1], operand, knownFacts)
            operators.pop(index)
            operators.pop(index - 1)
        elif ('|' in operators):
            index = getIndex('|', operators)
            operand = operators[index]
            operators[index + 1] = determine(operators[index - 1], operators[index + 1], operand, knownFacts)
            operators.pop(index)
            operators.pop(index - 1)
        elif ('^' in operators):
            index = getIndex('^', operators)
            operand = operators[index]
            operators[index + 1] = determine(operators[index - 1], operators[index + 1], operand, knownFacts)
            operators.pop(index)
            operators.pop(index - 1)
        else:
            return (operators[0])

    return(operators[0])

def analyse(rule, facts):
    i = 0
    index = 0
    while (i < len(rule)):
        if (rule[i] == '('):
            index = i
        if (rule[i] == ')'):
            boolean = crunch(rule[index + 1:i], facts)
            rule = rule.replace(rule[index:i + 1], str(boolean))
            index = 0
            i = 0
        i += 1
    if (len(rule) <= 2):
        result = facts[ord(rule[0]) - 65]
    else:
        result = crunch(rule, facts)
    return (result)

def computeComplex(complex, boolean, facts):
    if (complex[2] == '+'):
        if (boolean == True):
            facts[ord(complex[0]) - 65] = 1
            facts[ord(complex[4]) - 65] = 1
        else:
            facts[ord(complex[0]) - 65] = 0
            facts[ord(complex[4]) - 65] = 0
    elif (complex[2] == '|'):
        if (boolean == 1):
            facts[ord(complex[0]) - 65] = 2
            facts[ord(complex[4]) - 65] = 2
        else:
            facts[ord(complex[0]) - 65] = 0
            facts[ord(complex[4]) - 65] = 0
    elif (complex[2] == '^'):
        if (boolean == 1 or boolean == 2):
            facts[ord(complex[0]) - 65] = 2
            facts[ord(complex[4]) - 65] = 2
        else:
            facts[ord(complex[0]) - 65] = 0
            facts[ord(complex[4]) - 65] = 0

    else:
        error('Something is wrong')

    return(facts)

def checkRules(relatedRules, facts, rules, queried, already, givenFacts):
    for rule in relatedRules:
        if (rule in already):
            return (facts, queried, already)
        i = 0
        before = ''
        after = ''
        while (i < len(rule)):
            if (rule[i] == '=' or rule[i] == '<'):
                break
            if (ord(rule[i]) - 65 >= 0 and ord(rule[i]) - 65 <= 26):
                queriedHere = []
                if (rule[i] not in queried):
                    already.append(rule)
                    queriedHere, facts, already = getQuerie(facts, rules, rule[i], queried, already, givenFacts)
                    queried.append(queriedHere)
            before += rule[i]
            i += 1

        after = rule[i:]
        boolean = analyse(before, facts)
        if (after[0] == "="):
            if (len(after[3:]) == 1):
                if (boolean != facts[ord(after[3]) - 65] and boolean == 1):
                    facts[ord(after[3]) - 65] = 1
                    return (facts, queried, already)
                elif (boolean != facts[ord(after[3]) - 65] and boolean == 0):
                    facts[ord(after[3]) - 65] = 0
                elif (boolean != facts[ord(after[3]) - 65] and boolean == 2):
                    facts[ord(after[3]) - 65] = 2
            else:
                if (len(after[3:]) == 2 and after[3] == '!'):
                    facts[ord(after[4]) - 65] = not boolean
                else:
                    facts = computeComplex(after[3:], boolean, facts)
        elif (after[0] == '<'):
            if (len(after[4:]) == 1 and boolean == 1 and boolean != facts[ord(after[4]) - 65]):
                facts[ord(after[4]) - 65] = 1
                return (facts, queried, already)
            elif(len(after[4:]) == 1 and boolean == False and boolean != knownFacts[ord(after[4]) - 65]):
                facts[ord(after[4]) - 65] = 0
            else:
                facts = computeComplex(after[4:], boolean)
    return (facts, queried, already)


def getQuerie(facts, rules, querie, queried, already, givenfacts):
    relatedRules = getRelated(rules, querie)
    queriedHere = []
    if (len(relatedRules) == 0):
        if (querie in givenFacts[0]):
            facts[ord(querie) - 65] = 1
        if (facts[ord(querie) - 65] == -1):
            facts[ord(querie) - 65] = 0
        queriedHere.append(querie)
    else:
        facts, queriedHere, already = checkRules(relatedRules, facts, rules, queried, already, givenFacts)
        queried.append(queriedHere)

    return (queried, facts, already)

if __name__ == '__main__':
    if (path.exists(sys.argv[1])):
        file = open(sys.argv[1])
        data = file.read()
    else:
        error('file doesn\'t exists')
    givenFacts = []
    queries = []
    already = []
    rules = cleanContent(data)
    queried = []
    i = 0
    while (i < len(rules)):
        if (rules[i][0] == '='):
            givenFacts.append(rules[i])
            rules.pop(i)
        if (rules[i][0] == '?'):
            queries.append(rules[i])
            rules.pop(i)
        i += 1

    knownFacts = generateFacts(givenFacts)

    i = 1
    while (i < len(queries[0])):
        queried, facts, already = getQuerie(knownFacts, rules, queries[0][i], queried, already, givenFacts)
        i += 1

    i = 1
    while (i < len(queries[0])):
        value = facts[ord(queries[0][i]) - 65]
        if (value == 1):
            print(bcolors.OKGREEN + '{} is True'.format(queries[0][i]) + bcolors.ENDC)
        elif (value == 0 or value == -1):
            print(bcolors.FAIL + '{} is False'.format(queries[0][i]) + bcolors.ENDC)
        elif (value == 2):
            print(bcolors.WARNING + '{} is Indetermined'.format(queries[0][i]) + bcolors.ENDC)
        i += 1
