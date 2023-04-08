import src.RainbowTableGenerator as rtg
import src.PasswordGenerator as pg

def test_sauvegarde_ouverture_rainbow():
    #tests pour la sauvegarde dans le fichier
        generator = pg.PasswordGenerator(True, True, True, True,6)
        rainbow_table = rtg.RainbowTableGenerator(1,generator,4, 4)
        rainbow_table_copy = rtg.RainbowTableGenerator(1,generator,4,4)
        rainbow_table.saveRainbowSet("test1")
        rainbow_table_copy.loadRainbowSet("test1")

        assert rainbow_table_copy.rainbowSet == rainbow_table.rainbowSet != None