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
        print("Entrez un numero de fichier ou ( all pour tout les fichiers ) ou ( q pour quitter )")
        a=input("Numero : ")
       
        if ( a =="q"):
            print("Vous avez quitté le menu !")
            break

        elif (a == "all"):
            nouveauTab = tableau_fichiers
            print("Tous les fichiers ont été ajouter !")
            break
        elif (0 <= int(a) < i):
            a = int(a) 
            nouveauTab.append(tableau_fichiers[a])
            print("Vous avez ajouter le fichier : ", tableau_fichiers[a])
        else: print("Le fichier n'existe pas !")

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
    if re.search("References",fichier):
        references = fichier.split("References")[1]
    elif re.search("REFERENCES",fichier):
        references = fichier.split("REFERENCES")[1]

    ref = references.split("\n")

    for line in ref:

        if line == "\n" or len(line) <= 15 or re.match("^[\[\]0-9\.\ \|]+$",line):
            ref.remove(line)

    return "\n".join(ref)


def getAuteurs(fichier):
    Auteurs = " "
    return Auteurs


def getIntroduction(fichier):
    if re.search("Introduction",fichier):
        intro = fichier.split("Introduction")[1]
    elif re.search("INTRODUCTION",fichier):
        intro = fichier.split("INTRODUCTION")[1]
        
    if re.search("\nII",fichier):
        intro = intro.split("II")[0]
    if re.search("2\n\n",fichier):
        intro = intro.split("2\n\n")[0]	
    if re.search("\n\n2",fichier):
        intro = intro.split("\n\n2")[0]
        

    intro = intro.split("\n")

    i=0
    for line in intro:
        if i==0 and not(re.match("([A-Z])\w+",line)):
            del intro[i]
        if line == "\n" or re.match("^[\[\]0-9\.\ \|]+$",line) or re.match("^[0-9]+$",line) or re.search(".0x0c.",line):
            del intro[i]
        i+=1

    return "\n".join(intro)


def getCorps(fichier):
    start = 'introduction\n'
    corps = fichier
    corps = corps[corps.lower().find(start) + len(start):corps.lower().rfind('conclusion')]
    
    if len(corps) <= 10:
        corps = corps[corps.lower().rfind(start) + len(start):corps.lower().rfind('references\n')]
    return corps


def getConclusion(fichier):
    if re.search("Conclusion",fichier):
        conclusion = fichier.split('Conclusion')[1]
    if re.search("Conclusions",fichier):
        conclusion = fichier.split('Conclusions')[1]
    elif re.search("CONCLUSION",fichier):
        conclusion = fichier.split("CONCLUSION")[1]
    elif re.search("CONCLUSIONS",fichier):
        conclusion = fichier.split("CONCLUSIONS")[1]
    else:
        return "Pas de conclusion"


    if re.search("References",conclusion):
        conclusion = conclusion.split("References")[0]

    elif re.search("REFERENCES",conclusion):
        conclusion = conclusion.split("REFERENCES")[0]

    conclu = conclusion.split("\n")

    i=0
    if (conclu!=[]):
        for line in conclu:
            if i==0 and not(re.match("([A-Z])\w+",line)):
                del conclu[i]
            if line == "\n" or len(line) <= 15 or re.match("^[\[\]0-9\.\ \|]+$",line) or re.match("^[0-9]+$",line) or re.search(".0x0c.",line):
                del conclu[i]
            i+=1

    return "\n".join(conclu)
    


def getDiscussion(fichier):
    if re.search("Discussion\n", fichier):
        discussion = fichier.split('Discussion\n')[1]
    elif re.search("DISCUSSION", fichier):
        discussion = fichier.split("DISCUSSION")[1]
    elif re.search("Discussion:", fichier):
        discussion = fichier.split('Discussion:')[1]
    else:
        return "Pas de discussion"
    
    if re.search("Conclusion",discussion):
        discussion = discussion.split("Conclusion")[0]
    elif re.search("CONCLUSION",discussion):
        discussion = discussion.split("CONCLUSION")[0]
    
    page = discussion.split("\n")

    for line in page:
        if line == "\n" or len(line) <= 15 or re.match("^[\[\]0-9\.\ \|]+$",line):
            page.remove(line)
            
    return "\n".join(page)



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



os.system("rm -r corpus_parse")
os.system("mkdir corpus_parse")

# Delete old files
os.chdir("CORPUS/")
os.system("rm *.txt")

# os.system("rmdir corpus_txt")

# List all pdf files
ls = "ls *.pdf"



fichiers = os.popen(ls).read()
tableau_fichiers = fichiers.split("\n")

# Pop the array last element : ''
tableau_fichiers.pop(len(tableau_fichiers)-1)




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
        auteurfichier = getAuteurs(data)
        corpsfichier = getCorps(data)
        conclusionfichier = getConclusion(data)
        discussionfichier = getDiscussion(data)
        os.chdir("../corpus_parse")
        if formatfichier == "txt":

            with open("resultat_'%s'.txt" % nomfichier, 'a') as resultat:
                resultat.write("Le nom du fichier d’origine : " + str(nomfichier))
                resultat.write("\n")
                resultat.write("Le titre du papier : " + str(titrefichier))
                resultat.write("\n")
                resultat.write("Auteurs : " + str(auteurfichier))
                resultat.write("\n")
                resultat.write("Le résumé (abstract) de l’auteur : " + str(resumefichier))
                resultat.write("\n")
                resultat.write("L'introduction : " + str(introfichier))
                resultat.write("\n")
                resultat.write("Le développement du papier: " + str(corpsfichier))
                resultat.write("\n")
                resultat.write("La conclusion du papier : " + str(conclusionfichier))
                resultat.write("\n")
                resultat.write("La discussion du papier : " + str(discussionfichier))
                resultat.write("\n")
                resultat.write("Les références bibliographiques : " + str(referencesfichier))
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
            auteur = ET.SubElement(root, 'auteur')
            auteur.text = str(auteurfichier)
            auteur.tail = '\n'
            abstract = ET.SubElement(root, 'abstract')
            abstract.text = str(resumefichier)
            abstract.tail = '\n'
            introduction = ET.SubElement(root, 'introduction')
            introduction.text = str(introfichier)
            introduction.tail = '\n'
            corps = ET.SubElement(root, 'corps')
            corps.text = str(corpsfichier)
            corps.tail = '\n'
            conclusion = ET.SubElement(root, 'conclusion')
            conclusion.text = str(conclusionfichier)
            conclusion.tail = '\n'
            discussion = ET.SubElement(root, 'discussion')
            discussion.text = str(discussionfichier)
            discussion.tail = '\n'
            biblio = ET.SubElement(root, 'biblio')
            biblio.text = str(referencesfichier)
            biblio.tail = '\n'
            informations = ET.ElementTree(root)
            informations.write("resultat_'%s'.xml" % nomfichier, encoding='utf-8', xml_declaration = True)
        else:
            print("Format de fichier inconnu !")

    f.close()
