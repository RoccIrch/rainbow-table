import src.PasswordGenerator as pg
import const.char as consts

def test_password_generator():
    generator_basic       = pg.PasswordGenerator(True, True, True, True, 8)
    generator_no_lower    = pg.PasswordGenerator(False, True, True, True, 8)
    generator_no_upper    = pg.PasswordGenerator(True, False, True, True, 8)
    generator_no_number   = pg.PasswordGenerator(True, True, False, True, 8)
    generator_no_spe_char = pg.PasswordGenerator(True, True, True, False, 8)

    def generateMultiplePasswords(generator):
        list = []
        for i in range(10):
            password = generator.generatePassword()
            list.append(password)
        return list

    list_basic = generateMultiplePasswords(generator_basic)
    list_no_lower = generateMultiplePasswords(generator_no_lower)
    list_no_upper = generateMultiplePasswords(generator_no_upper)
    list_no_number = generateMultiplePasswords(generator_no_number)
    list_no_spe_char = generateMultiplePasswords(generator_no_spe_char)

    flag = 0
    assert len(list_basic) == 10
    assert len(list_basic[0]) == generator_basic.maxPwdSize

    for password in list_no_lower:
        for char in password:
            if char in consts.LOWER_ALPHABET:
                flag+=1

    for password in list_no_upper:
        for char in password:
            if char in consts.UPPER_ALPHABET:
                flag+=1
    
    for password in list_no_number:
        for char in password:
            if char in consts.NUMBER:
                flag +=1

    for password in list_no_spe_char:
        for char in password:
            if char in consts.SPECIAL_CHARACTER:
                flag +=1

    assert flag == 0
    

