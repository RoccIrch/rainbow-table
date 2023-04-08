import sqlite3
import pickle

PATH_TO_TABLES = "tables/"
PATH_TO_DB = "db/"

class RainbowTableConvertor():
    def __init__(self):
        pass
    
    def convertBinaryInSql(self, name1, name2):
        #CONVERT DATA
        rs = pickle.load(open(PATH_TO_TABLES+name1+".bin", 'rb'))
        passwords = [(k, v) for k, v in rs["password"].items()]
        info = [('hashAlgorithm', rs['hashAlgorithm']), ('nbReduce', rs['nbReduce']), ('allAcceptedChar', rs['allAcceptedChar']), ('generatorOptions', rs['generatorOptions'])]
        #SQL SAVING
        sql = sqlite3.connect(PATH_TO_TABLES+name2+".db")
        rq = sql.cursor()
        rq.execute("DROP TABLE IF EXISTS " +  name2 )
        rq.execute("CREATE TABLE " + name2 + "(mdpClair VARCHAR(20) PRIMARY key, hash BINARY(50))")
        sql.commit()
        rq.executemany("INSERT INTO " + name2 +"(mdpClair, hash) VALUES(?,? )", passwords)
        sql.commit()
        rq.execute("DROP TABLE IF EXISTS " +  name2 + "_info" )
        rq.execute("CREATE TABLE "+ name2 + "_info " + "(information VARCHAR(20) PRIMARY key, data VARCHAR(100))")
        rq.executemany("INSERT INTO " + name2 + "_info " +"(information, data) VALUES(?,?)",info)
        sql.commit()
    
    def convertSqlInnBin(self, name1, name2):
        #convert data
        res = {}
        res['password'] = {}
        sql = sqlite3.connect(PATH_TO_TABLES+name1 + ".db")
        cursor = sql.cursor()
        cursor.execute("SELECT * FROM " + name1 )
        passwords = cursor.fetchall()
        for i in range (len(passwords)):
            res['password'][passwords[i][0]] = passwords[i][1]
        cursor.execute("SELECT * FROM " + name1 + "_info")
        info = cursor.fetchall()
        res['hashAlgorithm'] = int(info[0][1])
        res['nbReduce'] = int(info[1][1])
        res['allAcceptedChar'] = info[2][1]
        res['generatorOptions'] = int(info[3][1])
        #save
        with open(PATH_TO_TABLES + name2 + ".bin", "wb") as file:
            file.write(pickle.dumps(res))