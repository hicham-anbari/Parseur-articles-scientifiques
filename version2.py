import os
import re
import sys
import xml.etree.ElementTree as ET

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


def getReferences(fichier):
    if re.search("References", fichier):
        donneFichier = fichier.split("References")[1]
        references = donneFichier.split("\n\n")[0]
        references = references.replace("\n", " ")
        return references
    elif re.search("REFERENCES", fichier):
        donneFichier = fichier.split("REFERENCES")[1]
        references = donneFichier.split("\n\n")[0]
        references = references.replace("\n", " ")
        return references
    else:
        return "Pas de references"


# tester le type d'argument pour choisir le type de sortie
if len(sys.argv) != 2:
    print('Erreur : il faut mettre -x ou -t en argument')
    exit()
else: 
    if sys.argv[1] == "-t":
        formatfichier = "txt"
    elif sys.argv[1] == "-x":
        formatfichier = "xml"
    else:
        print("Format de fichier inconnu !")


# Delete old files
os.system("rm *.txt")
os.system("rm *.xml")
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
        referencesfichier = getReferences(data)

        if formatfichier == "txt":
            with open("resultat_'%s'.txt" % nomfichier, 'a') as resultat:
                resultat.write("Le nom du fichier d’origine : " + str(nomfichier))
                resultat.write("\n")
                resultat.write("Le titre du papier : " + str(titrefichier))
                resultat.write("\n")
                resultat.write("Le résumé (abstract) de l’auteur : " + str(resumefichier))
                resultat.write("\n")
                resultat.write(" Les références bibliographiques : " + str(referencesfichier))
            resultat.close()
        elif formatfichier == "xml":
            root = ET.Element('article')
            root.text = '\n'
            preamble = ET.SubElement(root, 'preamble')
            preamble.text = str(nomfichier)
            preamble.tail = '\n'
            titre = ET.SubElement(root, 'titre')
            titre.text = str(titrefichier)
            titre.tail = '\n'
            abstract = ET.SubElement(root, 'abstract')
            abstract.text = str(resumefichier)
            abstract.tail = '\n'
            biblio = ET.SubElement(root, 'biblio')
            biblio.text = str(referencesfichier)
            biblio.tail = '\n'
            informations = ET.ElementTree(root)
            informations.write("resultat_'%s'.xml" % nomfichier, encoding='utf-8', xml_declaration = True)
        else:
            print("Format de fichier inconnu !")

    f.close()

