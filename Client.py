import sys
import os
from pyfiglet import Figlet
from src.PasswordGenerator import PasswordGenerator
from src.RainbowTableGenerator import RainbowTableGenerator
from src.RainbowTableConvertor import RainbowTableConvertor
from src.RainbowTableCrack import RainbowTableCrack
from src.RainbowTableCrackSQL import RainbowTableCrackSQL

class Color:
    reset = '\033[0m'
    bold = '\033[01m'
    italic = "\x1B[3m"
    disable = '\033[02m'
    underline = '\033[04m'
    
    class fontColor:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'
    class bgColor:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'

""" COMMAND ARGUMENTS """
GENERATE_BINARY_COMMAND = 'generate-bin'
GENERATE_SQL_COMMAND = 'generate-sql'
CONVERT_BIN_TO_SQL = 'convert-bin-to-sql'
CONVERT_SQL_TO_BIN = 'convert-sql-to-bin'
CRACK_COMMAND = 'crack'
HELP_COMMAND = 'help'
LIST_COMMAND = 'list'

def getClientHead():
    f = Figlet(font='slant')
    print (Color.fontColor.purple, f.renderText('Rainbow Table'), Color.reset)
    print (Color.fontColor.blue, "Version 1.0 - Developed by GLAMS", Color.reset)

def useGenerate(file_type):
    getClientHead()
    header = "Generation of binary file :" if file_type == "bin" else "Generation of sql file :"
    print("\n", Color.fontColor.purple, Color.italic, Color.bold, Color.underline, header, Color.reset, "\n")
    res = input(Color.fontColor.lightblue + Color.bold + "Use lower character [y/n] : " + Color.reset)
    useLower = True if res == 'y' else False;
    res = input(Color.fontColor.lightblue + Color.bold + "Use upper character [y/n] : " + Color.reset)
    useUpper = True if res == 'y' else False;
    res = input(Color.fontColor.lightblue + Color.bold + "Use number [y/n] : " + Color.reset)
    useNumber = True if res == 'y' else False;
    res = input(Color.fontColor.lightblue + Color.bold + "Use special character [y/n] : " + Color.reset)
    useSpecialChar = True if res == 'y' else False;
    maxPwdSize = int(input(Color.fontColor.lightblue + Color.bold + "Password size : " + Color.reset))
    pg = PasswordGenerator(useLower, useUpper, useNumber, useSpecialChar, maxPwdSize)
    hashAlgo = int(input(Color.fontColor.lightblue + Color.bold + "Hash algorithm [0=sha1, 1=md5, 2=glams] : " + Color.reset))
    nbReduce = int(input(Color.fontColor.lightblue + Color.bold + "Number of reduce : " + Color.reset))
    nbPwd = int(input(Color.fontColor.lightblue + Color.bold + "Number of password : " + Color.reset))
    rtg = RainbowTableGenerator(hashAlgo, pg, nbReduce, nbPwd)
    fileName = input(Color.fontColor.lightblue + Color.bold + "Name for RainbowTable file : " + Color.reset)
    print("\nGenerating...")
    if (file_type == "bin"):
        rtg.saveRainbowSet(fileName)
    elif (file_type == "sql"):
        rtg.generateRainbowSql(fileName)
    print("\n", fileName, "has been generated !")
def useCrack(rb_file, hash_to_crack):
    getClientHead()
    res = None
    print ("\nCracking...")
    if rb_file.split('.')[-1] == "bin":
        cracker = RainbowTableCrack(hash_to_crack, rb_file)
        res = cracker.findPasswordCrack()
    elif rb_file.split('.')[-1] == "db":
        cracker = RainbowTableCrackSQL(hash_to_crack, rb_file.split('.')[0])
        res = cracker.findPasswordCrack()
    else :
        print (Color.fontColor.red, Color.bold, "\nError ! you must specify the extension of the file", Color.reset, "\n")
        return False
    print()
    if res == None :
        print ("Sorry ! unfortunately we can't crack this hash")
    else :
        print ("This hash corresponds to the password :" + Color.fontColor.lightblue, Color.bold, res, Color.reset)
    print("\n")
    

def useConvertor(initialType, name1, name2):
    getClientHead()
    print("\n", Color.fontColor.purple, Color.italic, Color.bold, "Converting...", Color.reset)
    convertor = RainbowTableConvertor();
    if initialType == 'sql':
        convertor.convertSqlInnBin(name1, name2)
    elif initialType == 'bin':
        convertor.convertBinaryInSql(name1, name2)
    print("\n", name1, "has been converted !")

def listTable():
    getClientHead()
    print ("\n", Color.fontColor.blue, Color.bold, Color.underline, "All tables :", Color.reset)
    allTable = []
    for path in os.scandir("tables/"):
        if path.is_file():
            allTable.append(path.name)
    print ("\n", Color.fontColor.purple, Color.underline, "SQL :", Color.reset)
    for i in range (len(allTable)):
        if allTable[i].split(".")[-1] == "db":
            print ("\t- ", allTable[i])
    print ("\n", Color.fontColor.purple, Color.underline, "Binary :", Color.reset)
    for i in range (len(allTable)):
        if allTable[i].split(".")[-1] == "bin":
            print ("\t- ", allTable[i])

""" HELP AND ERROR """
def getCommandList():
    print (Color.fontColor.lightblue, Color.bold, GENERATE_BINARY_COMMAND, Color.reset, "\tTo generate and save a rainbow table in the \"tables\" folder as a binary file")
    print (Color.fontColor.lightblue, Color.bold, CONVERT_BIN_TO_SQL, Color.reset, Color.fontColor.purple, "file_name",Color.reset, Color.fontColor.purple, "new_file_name",Color.reset, "\tTo convert the rainbow table in a binary file and save it on a sql file")
    print (Color.fontColor.lightblue, Color.bold, GENERATE_SQL_COMMAND, Color.reset, "\tTo generate and save a rainbow table in the \"tables\" folder as a SQLite file")
    print (Color.fontColor.lightblue, Color.bold, CONVERT_SQL_TO_BIN, Color.reset, Color.fontColor.purple, "file_name",Color.reset, Color.fontColor.purple, "new_file_name",Color.reset, "\tTo convert the rainbow table in a sql file and save it on a binary file")
    print (Color.fontColor.lightblue, Color.bold, CRACK_COMMAND, Color.reset, Color.fontColor.purple, "file_name",Color.reset, Color.fontColor.purple, "hash_to_crack",Color.reset, "\tTo find the password corresponding to an hash. Specify the file extension !")
    print (Color.fontColor.lightblue, Color.bold, LIST_COMMAND, Color.reset, "\tTo show the table you already have generate !")
def notValidArgument():
    print (Color.fontColor.red, Color.bold, "Error ! not valid usage look at the guide", Color.reset, "\n")
    getCommandList()

def main(argv):
    if argv[0] == HELP_COMMAND:
            getCommandList()
    elif argv[0] == LIST_COMMAND:
            listTable()
    elif argv[0] == GENERATE_BINARY_COMMAND:
            useGenerate('bin')
    elif argv[0] == GENERATE_SQL_COMMAND:
            useGenerate('sql')
    elif argv[0] == CONVERT_BIN_TO_SQL:
            useConvertor('bin', argv[1], argv[2])
    elif argv[0] == CONVERT_SQL_TO_BIN:
            useConvertor('sql', argv[1], argv[2])
    elif argv[0] == CRACK_COMMAND:
            useCrack(argv[1], argv[2])
    else:
            notValidArgument()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        notValidArgument()