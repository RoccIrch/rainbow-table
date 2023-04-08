import hashlib
import sqlite3
import pickle
from src.RainbowTable import RainbowTable
import os

PATH_TO_TABLES = "tables/"
PATH_TO_DB = "db/"

class RainbowTableGenerator(RainbowTable) :
    def __init__(self, hashAlgorithm, pwdGenerator, nbReduce, nbPwd) :

        RainbowTable.__init__(self, hashAlgorithm, pwdGenerator.getAllAcceptedChar(), nbReduce, pwdGenerator.maxPwdSize)
        self.nbPwd = nbPwd
        self.pwdGenerator = pwdGenerator
        self.rainbowSet = None

    """
    Generate the dict where we store the plain text password and the final hash
    """
    #Remove all the sqlite database
    def deleteTable(self, name):
        os.remove(PATH_TO_TABLES+name + ".db")

    #Drop the table if he exists
    def dropOneTable(self, name):
        sql = sqlite3.connect(PATH_TO_TABLES+name + ".db")
        cursor = sql.cursor()
        cursor.execute("DROP TABLE IF EXISTS " +  name )
        sql.close()

    #Show all the table in the database
    def showAllTable(self, name):
        sql = sqlite3.connect(PATH_TO_TABLES+name + ".db")
        cursor = sql.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tab = cursor.fetchall()
        for i in range(len(tab)):
            tab[i] = list(tab[i])
        print(tab)
        sql.close()
        return tab


    #Show the data inside the table
    def showTable(self, name):
        sql = sqlite3.connect(PATH_TO_TABLES+name + ".db")
        cursor = sql.cursor()
        cursor.execute("SELECT * FROM " + name )
        r = cursor.fetchall()
        sql.close()
        return r

    # Generate a rainbow table, drop the oldest version if the name already exist
    def generateRainbowSql(self,name):
        sql = sqlite3.connect(PATH_TO_TABLES+name+".db")
        rq = sql.cursor()
        rq.execute("DROP TABLE IF EXISTS " +  name )
        rq.execute("CREATE TABLE " + name + "(mdpClair VARCHAR(20) PRIMARY key, hash BINARY(50))")
        sql.commit()
        data = []
        loopDetect = 0
        for i in range (self.nbPwd):
            password = self.pwdGenerator.generatePassword()
            if password in data: 
                loopDetect +=1
                if loopDetect > 30:
                    rq.executemany("INSERT OR IGNORE INTO " + name +"(mdpClair, hash) VALUES(?,? )", data)
                    sql.commit()
                    sql.close()
                    self.generateInformationSql(name)
            else:
                loopDetect = 0
                h = self.hash(password)
                for i in range (self.nbReduce):
                    r = self.reduce(h, i)
                    h = self.hash(r)
                data.append((password, h))
        rq.executemany("INSERT OR IGNORE INTO " + name +"(mdpClair, hash) VALUES(?,? )", data)
        sql.commit()
        sql.close()
        self.generateInformationSql(name)

    # Generate a table (VARCHAR,VARCHAR) with some information as the
    # hash Algorithm, the number of reduce and the accepted char
    # drop the oldest table if the name already exist
    def generateInformationSql(self, name):
        sql = sqlite3.connect(PATH_TO_TABLES+name + ".db")
        rq = sql.cursor()
        rq.execute("DROP TABLE IF EXISTS " +  name + "_info" )
        hashAlgorithm = 'hashAlgorithm'
        nbReduce = 'nbReduce'
        allAcceptedChar = 'allAcceptedChar'
        rq.execute("CREATE TABLE "+ name + "_info " + "(information VARCHAR(20) PRIMARY key, data VARCHAR(100))")
        rq.execute("INSERT INTO " + name + "_info " + "(information, data) VALUES(?,?)", (hashAlgorithm, str(self.hashAlgorithm)))
        rq.execute("INSERT INTO " + name + "_info " +"(information, data) VALUES(?,?)",(nbReduce , str(self.nbReduce)))
        rq.execute("INSERT INTO " + name + "_info " +"(information, data) VALUES(?,?)",(allAcceptedChar,self.getAllAcceptedChar()))
        rq.execute("INSERT INTO " + name + "_info " +"(information, data) VALUES(?,?)",("generatorOptions",self.pwdGenerator.maxPwdSize))
        sql.commit()
        sql.close()

    # Generate a set of all password and their multiple-hash-reduction
    def generateRainbowSet(self):
        self.rainbowSet = dict()
        self.rainbowSet['password'] = dict()
        i = 0
        flagInfiniteLoop = 0
        while(i <= self.nbPwd-1):
            password = self.pwdGenerator.generatePassword()
            if password not in self.rainbowSet["password"].keys(): #this line is to avoid duplicate passwords (clean table)

                h = self.hash(password)
                for j in range (self.nbReduce):
                    r = self.reduce(h, j)
                    h = self.hash(r)

                self.rainbowSet["password"][password] = h
                i+=1
                flagInfiniteLoop = 0
            else:
                flagInfiniteLoop += 1
                if flagInfiniteLoop > 30:
                    print("Infinite loop detected")
                    self.nbPwd = i
                    return self.rainbowSet

        return self.rainbowSet

    """
    Add some information on the previous set and store it in the "tables" folder
    """
    def saveRainbowSet(self, name):
        self.generateRainbowSet()
        self.rainbowSet["hashAlgorithm"] = self.hashAlgorithm
        self.rainbowSet["nbReduce"] = self.nbReduce
        self.rainbowSet["allAcceptedChar"] = self.getAllAcceptedChar()

        self.rainbowSet["generatorOptions"] = self.pwdGenerator.maxPwdSize
        with open(PATH_TO_TABLES + name + ".bin", "wb") as file:
            file.write(pickle.dumps(self.rainbowSet))

    # Load Rainbow Table save in a binary file
    def loadRainbowSet(self, name):
        with open(PATH_TO_TABLES + name, "rb") as file:
            self.rainbowSet = pickle.load(file)
    def getRainbowTable(self, number):
        listrbhead = list(self.rainbowSet["password"].keys())
        listrbtail = list(self.rainbowSet["password"].values())

        listHash = [self.hash(listrbhead[number])]
        listPwd = [listrbhead[number]]
        h = listHash[0]
        for j in range (self.nbReduce):
            r = self.reduce(h, j)
            listPwd.append(r)

            h = self.hash(r)
            listHash.append(h)

        return (listPwd, listHash)
