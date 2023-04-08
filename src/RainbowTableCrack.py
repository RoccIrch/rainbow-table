import pickle
from src.RainbowTable import RainbowTable
class RainbowTableCrack(RainbowTable):
    def __init__(self, hashToCrack, rbFile):
        self.rainbowSet = pickle.load(open('tables/' + rbFile, 'rb'))
        self.hashToCrack = hashToCrack
        RainbowTable.__init__(self, self.rainbowSet["hashAlgorithm"], self.rainbowSet["allAcceptedChar"], self.rainbowSet["nbReduce"], self.rainbowSet["generatorOptions"])
        self.nbReduce = self.rainbowSet["nbReduce"]
        self.rainbowSet = self.rainbowSet["password"]


    """ cracks a password if found in rainbow tables """
    def findPasswordCrack(self):
        #reversed in order to get better performance on average
        #we try every possible tail hash and then find the head that has the same tail
        for i in reversed(range(self.nbReduce+1)):
            finalhash = self.findTailHash(i)
            if finalhash:
                for tail in finalhash:
                    tableHead = [head for head in self.rainbowSet if self.rainbowSet[head] == tail] #finds all the heads that have the same tail
                    for head in tableHead:
                        solution = self.findPasswordHash(head)
                        if solution != None:#if we did not find a collision
                            return solution
        return None
    """ finds the tail hash of a password"""
    def findTailHash(self,index):
        hashedPwd = self.hashToCrack
        if hashedPwd in self.rainbowSet.values():# hash is already in rainbow table
            return (hashedPwd, 0)
        for i in range(index, self.nbReduce+1):
            plainPwd = self.reduce(hashedPwd, i)
            hashedPwd = self.hash(plainPwd)
            if hashedPwd in self.rainbowSet.values():
                return (hashedPwd, i)
        return False
    
    """ finds the password hash of a password"""
    def findPasswordHash(self, tableHead):
        solution = tableHead
        if (self.hash(tableHead) != self.hashToCrack):#if the hash of the head is not the hash we are looking for
            h = self.hash(tableHead)
            if h != self.hashToCrack:
                for i in range (self.nbReduce-1):#we reduce the hash nbReduce-1 times, could be reduced as we already know what color the hash is supposed to be
                    r = self.reduce(h, i)
                    h = self.hash(r)
                    if h == self.hashToCrack:
                        solution = r
                        break
            if solution == tableHead: #means we did not find the pwd as solution was not altered, collision happened and/or our rainbow tables do not contain the pwd
                return None
            else:
                return solution
        else:
            return solution

