# --- Day 16: Ticket Translation ---
# As you're walking to yet another connecting flight, you realize that one of the legs of your re-routed
# trip coming up is on a high-speed train. However, the train ticket you were given is in a language you
# don't understand. You should probably figure out what it says before you get to the train station after
# the next flight.
#
# Unfortunately, you can't actually read the words on the ticket. You can, however, read the numbers, and
# so you figure out the fields these tickets must have and the valid ranges for values in those fields.
#
# You collect the rules for ticket fields, the numbers on your ticket, and the numbers on other nearby
# tickets for the same train service (via the airport security cameras) together into a single document
# you can reference (your puzzle input).
#
# The rules for ticket fields specify a list of fields that exist somewhere on the ticket and the valid
# ranges of values for each field. For example, a rule like class: 1-3 or 5-7 means that one of the fields
# in every ticket is named class and can be any value in the ranges 1-3 or 5-7 (inclusive, such that 3 and
# 5 are both valid in this field, but 4 is not).
#
# Each ticket is represented by a single line of comma-separated values. The values are the numbers on
# the ticket in the order they appear; every ticket has the same format. For example, consider this ticket:
#
# .--------------------------------------------------------.
# | ????: 101    ?????: 102   ??????????: 103     ???: 104 |
# |                                                        |
# | ??: 301  ??: 302             ???????: 303      ??????? |
# | ??: 401  ??: 402           ???? ????: 403    ????????? |
# '--------------------------------------------------------'
# Here, ? represents text in a language you don't understand.
# This ticket might be represented as 101,102,103,104,301,302,303,401,402,403;
# of course, the actual train tickets you're looking at are much more complicated.
# In any case, you've extracted just the numbers in such a way that the first number is always the same specific field,
# the second number is always a different specific field,
# and so on - you just don't know what each position actually means!
#
# Start by determining which tickets are completely invalid; these are tickets
# that contain values which aren't valid for any field. Ignore your ticket for now.
#
# For example, suppose you have the following notes:
#
# class: 1-3 or 5-7
# row: 6-11 or 33-44
# seat: 13-40 or 45-50
#
# your ticket:
# 7,1,14
#
# nearby tickets:
# 7,3,47
# 40,4,50
# 55,2,20
# 38,6,12
# It doesn't matter which position corresponds to which field; you can identify invalid nearby
# tickets by considering only whether tickets contain values that are not valid for any field. In this example,
# the values on the first nearby ticket are all valid for at least one field. This is not true of the other
# three nearby tickets: the values 4, 55, and 12 are are not valid for any field. Adding together all of the
# invalid values produces your ticket scanning error rate: 4 + 55 + 12 = 71.
#
# Consider the validity of the nearby tickets you scanned. What is your ticket scanning error rate?
def isBetween(number, borders):
    return borders[1] >= number >= borders[0]


def checkFieldValidationForRule(number: int, rules: [[int, int]]):
    for rule in rules:
        if isBetween(number, rule):
            return True
    return False


def hasMultipleFields(fields):
    for f in fields:
        if len(fields[f]) > 1:
            return True
    return False


def removeRuleMatches(fields):
    keys = fields.keys()
    while hasMultipleFields(fields):
        for i in keys:
            value = fields[i]
            if len(value) == 1:
                for j in keys:
                    uniqueVal = fields[i][0]
                    if i != j and uniqueVal in fields[j]:
                        fields[j].remove(uniqueVal)
    return fields


class ParsedData:
    rules = {}
    ticket = []
    neighbours = []
    validTickets = []
    invalidTickets = []
    fieldOrder = {}
    mappedTicket = {}

    def __init__(self, rules, ticket, neighbours):
        self.addRule(rules)
        self.addTicket(ticket)
        self.addNeighbours(neighbours)
        self.validateNeighbours()

    def addRule(self, rules):
        for r in rules:
            string = r.split(':')
            rule, values = string[0], [s for s in string[1].split('or')]
            self.rules[rule] = []
            for v in values:
                self.rules[rule] += [[int(x) for x in v.split('-')]]

    def addTicket(self, ticketStr):
        self.ticket = [int(s) for s in ticketStr.split(',')]

    def addNeighbours(self, neighbours):
        for n in neighbours:
            self.neighbours.append([int(s) for s in n.split(',')])

    def validateNeighbours(self):
        invalidTickets = []
        for neighbour in self.neighbours:
            isTicketInvalid = False
            for number in neighbour:
                isNumberValid = self.checkIsNumberValidToRules(number)
                if not isNumberValid:
                    isTicketInvalid = True
            if isTicketInvalid:
                invalidTickets.append(neighbour)
        self.invalidTickets = invalidTickets
        self.validTickets = [self.ticket] + [ticket for ticket in self.neighbours if ticket not in invalidTickets]

    def countInvalidFields(self):
        res = 0
        for neighbour in self.invalidTickets:
            for number in neighbour:
                isNumberValid = self.checkIsNumberValidToRules(number)
                if not isNumberValid:
                    res += number
        return res

    def checkIsNumberValidToRules(self, number):
        isNumberValid = False
        for key in self.rules.keys():
            if isNumberValid:
                break
            rule = self.rules[key]
            if checkFieldValidationForRule(number, rule):
                isNumberValid = True
        return isNumberValid

    # how to check if field accords to a field? Valid tickets can be represented as rectangular matrix.
    # So checking consists of iterating in columns of matrix until there is only one rule left for a column.
    def mapFields(self):
        fields = {}
        for x in range(len(self.ticket)):
            rule = self.getValidRuleForField(x)
            for r in rule:
                if r not in fields.keys():
                    fields[r] = [x]
                else:
                    fields[r].append(x)
        self.fieldOrder = removeRuleMatches(fields)

    def getValidRuleForField(self, fieldPos):
        validRules = []
        for key in self.rules:
            isRuleValid = True
            rule = self.rules[key]
            for ticket in self.validTickets:
                field = ticket[fieldPos]
                if not checkFieldValidationForRule(field, rule):
                    isRuleValid = False
                    break
            if isRuleValid:
                validRules.append(key)
        return validRules

    def mapTicket(self):
        mappedTicket = {}
        for field in self.fieldOrder:
            mappedTicket[field] = self.ticket[self.fieldOrder[field][0]]
        self.mappedTicket = mappedTicket


def parseTicketData(data):
    ticketIndex = data.index('your ticket:') + 1
    neighboursIndex = data.index('nearby tickets:') + 1
    parsedData = ParsedData(data[: ticketIndex - 1], data[ticketIndex], data[neighboursIndex:])
    return parsedData


def partOne(data):
    return data.countInvalidFields()


# --- Part Two ---
# Now that you've identified which tickets contain invalid values,
# discard those tickets entirely. Use the remaining valid tickets to determine which field is which.
#
# Using the valid ranges for each field, determine what order the
# fields appear on the tickets. The order is consistent between all
# tickets: if seat is the third field, it is the third field on every ticket, including your ticket.
#
# For example, suppose you have the following notes:
#
# class: 0-1 or 4-19
# row: 0-5 or 8-19
# seat: 0-13 or 16-19
#
# your ticket:
# 11,12,13
#
# nearby tickets:
# 3,9,18
# 15,1,5
# 5,14,9
# Based on the nearby tickets in the above example,
# the first position must be row, the second position must be class,
# and the third position must be seat; you can conclude that in your
# ticket, class is 12, row is 11, and seat is 13.
#
# Once you work out which field is which, look for the six fields on your
# ticket that start with the word departure. What do you get if you multiply those six values together?


def partTwo(data):
    data.mapFields()
    data.mapTicket()
    res = 1
    for field in data.mappedTicket.keys():
        if 'departure' in field:
            res *= data.mappedTicket[field]
    return res


def task(data):
    data.remove('')
    data = parseTicketData(data)
    print(partOne(data))
    print(partTwo(data))
