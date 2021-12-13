import os
import re
import sys
import xml.etree.ElementTree as ET



def choisirPdf(tableau_fichiers):
    i = 0
    nouveauTab = []
    for nom in tableau_fichiers:
        print(i,"  ", nom)
        i=i+1

    for numero in range(0,i):
        print("Entrez un numero de fichier ou ( all pour tout les fichiers ) ou ( q qui quitter )")
        a=input("numero : ")
       
        if ( a =="q"):
            print("Quittez")
            break

        elif (a == "all"):
            nouveauTab = tableau_fichiers
            break
        elif (0 < int(a) < i):
            a = int(a) 
            nouveauTab.append(tableau_fichiers[a])
	else:
		print("Le fichier n'existe pas !")

    return nouveauTab


# function to convert pdf to txt
def convertPdfToTxt(tableau_fichiers):
    	
	for nom in tableau_fichiers:
        
		nomfichier = nom.split(".")[0]
		commande = "pdftotext '%s' '%s.txt'" % (nom,nomfichier)
		os.system(commande)


def getTitle(fichier):
    title = fichier.split("\n")[0]
    return title

def getIntroduction(fichier):
    if re.search("Introduction", fichier):
        donneFichier = fichier.split("Introduction")[1]
        intro = donneFichier.split("\n\n")[0]
        intro = intro.replace("\n", " ")
        return intro
    elif re.search("INTRODUCTION", fichier):
        donneFichier = fichier.split("INTRODUCTION")[1]
        intro = donneFichier.split("\n\n")[0]
        intro = intro.replace("\n", " ")
        return intro
    else:
        return "Pas de resumé"

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


#afficheALlPdf(tableau_fichiers)

# os.system("mkdir corpus_txt")
# Convert each pdf to txt
nouveauTab = choisirPdf(tableau_fichiers)
convertPdfToTxt(nouveauTab)



for fichier in nouveauTab:

    nomfichier = fichier.split(".")[0]
    
    with open(nomfichier + ".txt") as f:
        data = f.read()
        titrefichier = getTitle(data)
        resumefichier = getResume(data)
        introfichier = getIntroduction(data)
        referencesfichier = getReferences(data)

        if formatfichier == "txt":
            with open("resultat_'%s'.txt" % nomfichier, 'a') as resultat:
                resultat.write("Le nom du fichier d’origine : " + str(nomfichier))
                resultat.write("\n")
                resultat.write("Le titre du papier : " + str(titrefichier))
                resultat.write("\n")
                resultat.write("L'introduction': " + str(introfichier))
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
            introduction = ET.SubElement(root, 'introduction')
            introduction.text = str(introfichier)
            introduction.tail = '\n'
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

