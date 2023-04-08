import const.char as char
from random import randint

class PasswordGenerator:
    def __init__(self, lower, upper, number, specialChar, maxPwdSize) :
        self.lower = lower
        self.upper = upper
        self.number = number
        self.specialChar = specialChar
        self.maxPwdSize = maxPwdSize

    """ Disable or enable lower case char """
    def enableLower(self):
        self.lower = True
    def disableLower(self):
        self.lower = False

    """ Disable or enable upper case char """
    def enableUpper(self):
        self.upper = True
    def disableLower(self):
        self.upper = False

    """ Disable or enable number char """
    def enableNumber(self):
        self.number = True
    def disableNumber(self):
        self.number = False

    """ Disable or enable special char """
    def enableSpecialChar(self):
        self.specialChar = True
    def disableSpecialChar(self):
        self.specialChar = False

    """ Return a string with all the accepted char """
    def getAllAcceptedChar(self):
        result = ""
        if (self.lower):
            result += char.LOWER_ALPHABET
        if (self.upper):
            result += char.UPPER_ALPHABET
        if (self.number):
            result += char.NUMBER
        if (self.specialChar):
            result += char.SPECIAL_CHARACTER
        return result


    """ Return a random password """
    def generatePassword(self):
        password = ""
        for i in range (self.maxPwdSize):
            password += self.getAllAcceptedChar()[randint(0, len(self.getAllAcceptedChar())-1)]
        #print(password)
        return password