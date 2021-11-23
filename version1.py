import os
import re

# function to convert pdf to txt
def convertPdfToTxt(tableau_fichiers):
    	
	for nom in tableau_fichiers:
        
		nomfichier = nom.split(".")[0]
		commande = "pdftotext '%s' '%s.txt'" % (nom,nomfichier)
		os.system(commande)


def getTitle(fichier):
    title = fichier.split("\n")[0]
    return title


def getResume(fichier):
    if re.search("Abstract", fichier):
        donneFichier = fichier.split("Abstract")[1]
        resume = donneFichier.split("\n\n")[0]
        resume = resume.replace("\n", " ")
        return resume
    elif re.search("ABSTRACT", fichier):
        donneFichier = fichier.split("ABSTRACT")[1]
        resume = donneFichier.split("\n\n")[0]
        resume = resume.replace("\n", " ")
        return resume
    else:
        return "Pas de resumé"

# Delete old files
os.system("rm *.txt")
# os.system("rmdir corpus_txt")

# List all pdf files
ls = "ls *.pdf"
fichiers = os.popen(ls).read()
tableau_fichiers = fichiers.split("\n")

# Pop the array last element : ''
tableau_fichiers.pop(len(tableau_fichiers)-1)

# os.system("mkdir corpus_txt")
# Convert each pdf to txt
convertPdfToTxt(tableau_fichiers)

for fichier in tableau_fichiers:

    nomfichier = fichier.split(".")[0]
    
    with open(nomfichier + ".txt") as f:
        data = f.read()
        titrefichier = getTitle(data)
        resumefichier = getResume(data)

        with open("resultat_'%s'.txt" % nomfichier, 'a') as resultat:
            resultat.write("Le nom du fichier d’origine : " + str(nomfichier))
            resultat.write("\n")
            resultat.write("Le titre du papier : " + str(titrefichier))
            resultat.write("\n")
            resultat.write("Le résumé (abstract) de l’auteur : " + str(resumefichier))
        resultat.close()

    f.close()
