# 🌈 Rainbow Table GLAMS

### Projet réalisé par :
- Gireg Gambrelle 22106987
- Luc Guyard 21507439
- Antoine Laroche 22003439
- Marta Boshkovska 22012535
- Sara Sale 22009614

## 🛠️ Installation des dépendences
```bash
pip install -r requirements.txt
```

## 🧑‍💻 Utilisation du client
### Lister les commandes :
```bash
python3 Client.py help
```
### Générer une table :
- Dans un fichier binaire :
```bash
python3 Client.py generate-bin
```
- Dans un fichier sql :
```bash
python3 Client.py generate-sql
```
### Cracker :
```bash
python3 Client.py file_name hash_to_crack
```
### Convertir les tables :
- De binaire à sql:
```bash
python3 Client.py convert-bin-to-sql bin_file_name new_file_name #sans préciser les extensions
```
- De sql à binaire :
```bash
python3 Client.py convert-sql-to-bin sql_file_name new_file_name #sans préciser les extensions
```
### Lister les tables déjà créées :
```bash
python3 Client.py list
```