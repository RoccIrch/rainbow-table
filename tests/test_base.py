import src.PasswordGenerator as pg
import src.RainbowTableGenerator as rtg

#ne pas supprimer "__init__.py", pytest a besoin de la présence de ce fichier au sein du fichier tests
#lancer test avec "pytest" depuis "arc-en-ciel-alms/"

def test_creation_rainbow_basic():
    generator = pg.PasswordGenerator(True, False, True, False, 7)
    rainbow_table = rtg.RainbowTableGenerator(0, generator,3,4)

    assert rainbow_table != {}



