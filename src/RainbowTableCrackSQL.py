import sqlite3
from src.RainbowTable import RainbowTable

class RainbowTableCrackSQL(RainbowTable):
    def __init__(self, hashToCrack, rbFile):
        self.fileName = rbFile
        self.database = sqlite3.connect("tables/" + rbFile + ".db");
        self.hashToCrack = hashToCrack
        #### Get Table info 
        cursor = self.database.cursor()
        cursor.execute("SELECT data FROM " + rbFile + "_info WHERE information=\"hashAlgorithm\"")
        hashAlgo = cursor.fetchall()[0][0]
        cursor.execute("SELECT data FROM " + rbFile + "_info WHERE information=\"nbReduce\"")
        nbReduce = cursor.fetchall()[0][0]
        cursor.execute("SELECT data FROM " + rbFile + "_info WHERE information=\"allAcceptedChar\"")
        allAcceptedChar = cursor.fetchall()[0][0]
        cursor.execute("SELECT data FROM " + rbFile + "_info WHERE information=\"generatorOptions\"")
        generatorOptions = cursor.fetchall()[0][0]
        RainbowTable.__init__(self, int(hashAlgo), allAcceptedChar, int(nbReduce), int(generatorOptions))

    # Return plain text password if it is find or None if it's not :
    def findPasswordCrack(self):
        for i in reversed(range(self.nbReduce+1)):
            collisions = 0
            finalhash = self.findTailHash(i)
            if finalhash:
                cursor = self.database.cursor()
                res = cursor.execute("SELECT mdpClair FROM " + self.fileName + " WHERE hash=\""+finalhash[0]+"\"").fetchall()
                tableHead = []
                for i in range (len(res)):
                    tableHead.append(res[i][0])
                for head in tableHead:
                    solution = self.findPasswordHash(head)
                    if solution != None:
                        return solution
                    collisions+=1
                collisions+=1
        return None

    # Return the hash and the color in the table or False if the hash is not in the table
    def findTailHash(self,index):
        hashedPwd = self.hashToCrack
        cursor = self.database.cursor()
        if len(cursor.execute("SELECT hash FROM "+ self.fileName +" WHERE hash=\""+hashedPwd+"\"").fetchall()) > 0:
            return (hashedPwd, 0)
        for i in range(index, self.nbReduce+1):
            plainPwd = self.reduce(hashedPwd, i)
            hashedPwd = self.hash(plainPwd)
            if len(cursor.execute("SELECT hash FROM "+ self.fileName +" WHERE hash=\""+ hashedPwd +"\"").fetchall()) > 0:
                return (hashedPwd, i)
        return False

    # Return get the password hash in the table
    def findPasswordHash(self, tableHead):
        solution = tableHead
        if (self.hash(tableHead) != self.hashToCrack):
            h = self.hash(tableHead)
            if h != self.hashToCrack:
                for i in range (self.nbReduce-1):
                    r = self.reduce(h, i)
                    h = self.hash(r)
                    if h == self.hashToCrack:
                        solution = r
                        break
            if solution == tableHead:
                return None
            else:
                return solution
        else:
            return solution