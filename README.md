# Parseur d’articles scientifiques 

### Extraction des nom des fichiers, titres , résumés, introductions, auteurs, corps, conclusions, discussions et bibliographies:

Au préalable il faut créer un dossier nommé 'CORPUS' à la racine, avec tous les PDF à l'intérieur.
Aller à la **racine** du repertoire où ce trouve les différents fichiers .PDF et lancer le programme python:

Fichiers au format TXT :
```console
MacBook-Pro-de-Hicham:~ hicham$ : python parser_final.py -t
```

Fichiers au format XML :
```console
MacBook-Pro-de-Hicham:~ hicham$ : python parser_final.py -x
```

Vous trouverez par la suite dans le dossier nommé "corpus_parse" un fichier pour chaque pdf **resultat_NOM-DU-PDF.TXT** ou **resultat_NOM-DU-PDF.XML**.
