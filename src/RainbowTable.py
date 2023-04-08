import hashlib
import random

class RainbowTable:
    def __init__(self, hashAlgorithm, allAcceptedChar, nbReduce, maxPwdSize) :
        self.hashAlgorithm = hashAlgorithm
        self.allAcceptedChar = allAcceptedChar
        self.nbReduce = nbReduce
        self.maxPwdSize = maxPwdSize

    """" Return a string with all accepted char """
    def getAllAcceptedChar(self) :
        return self.allAcceptedChar

    """" Return the hashed plain text """
    def hash(self, plainText):
        if (self.hashAlgorithm == 0 or self.hashAlgorithm == 1):
            plainText = plainText.encode('utf-8')
            if (self.hashAlgorithm == 0):
                return hashlib.sha1(plainText).hexdigest()
            elif (self.hashAlgorithm == 1):
                return hashlib.md5(plainText).hexdigest()
        elif (self.hashAlgorithm == 2):
            result, tmp = "", 5381 
            primeNumbers = [5, 61, 11, 1]
            choosen = random.choice(primeNumbers)
            for i in plainText:
                tmp = (((tmp * (2**choosen)) + tmp) + ord(i))
            result =  str((tmp))[:11]
            return result

    """" Return a plain text from a part of hash """
    def reduce_base(self, hashedText, color):
        reduced_text = ""
        if isinstance(hashedText[1],int) == True:
            length = hashedText[1] % (self.maxPwdSize- self.minPwdSize + 1) - self.minPwdSize
        else:
            length = ord(hashedText[1]) % (self.maxPwdSize- self.minPwdSize + 1) - self.minPwdSize
        for i in range (-length):
            if (type((hashedText[((color + i) % len(hashedText))])))== str:
                reduced_text += self.getAllAcceptedChar()[ord(hashedText[((color + i) % len(hashedText))]) % len(self.getAllAcceptedChar())]
            else :
                reduced_text += self.getAllAcceptedChar()[(hashedText[((color + i) % len(hashedText))]) % len(self.getAllAcceptedChar())]
        return reduced_text

    """
    only accepts hexadecimal hashes in input
    returns reduced password in string type of fixed length
    fixed length is self.maxPwdSize
    """
    def reduce_old(self, hashedtext, color):
        reduced_text = ""
        pwd_length = self.maxPwdSize
        charset = self.getAllAcceptedChar()
        for letter in range(pwd_length):
            new_letter_index_hex = hashedtext[(color + letter) % len(hashedtext)] #choosing a hexnumber in hash
            new_letter_index = int(new_letter_index_hex, 16) #convert hex to int
            reduced_text += charset[new_letter_index % len(charset)] #new letter appended to the to-be returned string
        return reduced_text
    
    def reduce(self, hashedtext, color):
        pwd_length = self.maxPwdSize
        charset = self.getAllAcceptedChar()
        hash_obj = hashlib.sha256(hashedtext.encode())
        hash_bytes = hash_obj.digest()
        combined_bytes = hash_bytes + color.to_bytes(4, byteorder="big")
        reduced_text = ""
        while len(reduced_text) < pwd_length:
            hash_obj = hashlib.sha256(combined_bytes)
            hash_bytes = hash_obj.digest()
            combined_bytes = hash_bytes + color.to_bytes(4, byteorder="big")
            hash_int = int.from_bytes(hash_bytes, byteorder="big")
            index = hash_int % len(charset)
            reduced_text += charset[index]
        return reduced_text

