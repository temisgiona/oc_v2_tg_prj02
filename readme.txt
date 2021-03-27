Notice utilisation windows 10 : 
Préalable :
	
1-Décompacter le projet dans un repertoire :
	ex:"C:\projet_OPC\"
resultat probable ->  C:\projet_OPC\oc_v2_tg_prj02-dev_scrap_book

2-Création environnement viturel python sous windows 10:
 - au moyen de l'invite de commande du powershell , se positionner dans le repertoire du projet :  ex  :" cd C:\projet_OPC\oc_v2_tg_prj02-dev_scrap_book\"
sous windows 10 taper la commande: "python -m venv venv" 
3-Activation de l'environnement virtuel taper :  "venv/Scripts/activate"

4-insertion des librairies necessaires taper  : "pip  install -r requirements.txt" 
	ou 
taper manuellement la liste des librairies saisies à l'interieur du fichier requirements.txt --> pip install requests , pip install bs4
verifier leur installation effective avec la commande "pip freeze"

5-Vérifiez la présence des fichiers :
	-main.py 
	-file_creation.py  
	-booktoscrap.py
6-Vérifier la présence des répertoires "data" et "image" à la racine du projet.
Les fichiers csv seront stockés dans le repertoires "data" et les images des livres scrapés dans le repertoire "image".

7-Pour faire fonctionner le programme :  executer  : python3 main.py.


