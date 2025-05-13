import pandas as pd
import numpy as np
import os
from os import listdir
from os.path import isfile, join

file_directory = os.path.abspath(__file__)
directory = os.path.dirname(file_directory)
directory = directory.replace('\\', "/")
directory += '/'


#on dispose d'un dictionnaire dans lequel se trouve le nom des équipes et l'url de leur calendrier de matchs (on pourra peut-être automatiser la récupération des équipes et des urls pour les prochaines saisons)

urlsEquipes = {
    "Angers" : "https://basketlfb.com/equipe/calendrier/2941-angers",
    "Basket Landes" : "https://basketlfb.com/equipe/calendrier/2653-basket-landes",
    "Bourges" : "https://basketlfb.com/equipe/calendrier/2654-bourges",
    "Charleville-Mézières" : "https://basketlfb.com/equipe/calendrier/2656-charleville-mezieres",
    "Landerneau" : "https://basketlfb.com/equipe/calendrier/13330-landerneau",
    "Lattes Montpellier" : "https://basketlfb.com/equipe/calendrier/2658-lattes-montpellier",
    "Lyon" : "https://basketlfb.com/equipe/calendrier/2659-lyon",
    "Roche Vendée" : "https://basketlfb.com/equipe/calendrier/449-roche-vendee",
    "Saint-Amand" : "https://basketlfb.com/equipe/calendrier/2657-saint-amand",
    "Tarbes" : "https://basketlfb.com/equipe/calendrier/2663-tarbes",
    "Toulouse" : "https://basketlfb.com/equipe/calendrier/446-toulouse",
    "Villeneuve d'Ascq" : "https://basketlfb.com/equipe/calendrier/2664-villeneuve-d-ascq"
}



#pour les lignes type "total", il faut recalculer correctement les % de réussite


    
#on crée une procédure permettant d'ajouter une ligne de notre choix à un dataframe 


#cette fonction récupère les urls à l'aide d'un dicitonnaire

def recupererURLMatchs(dicEquipe) :
    df = pd.read_html(dicEquipe[1], extract_links='all') #récupération du tableau du calendrier des matchs en extrayant les liens
    tousMatchs = df[0] #on récupère la colonne dans laquelle se trouvent les urls des matchs
    nbMatchs = len(tousMatchs) 
    urls = [] 
    for k in range(nbMatchs) :
        match = tousMatchs.iat[k,0][1] #on récupère l'url de chaque match
        urls.append('https://basketlfb.com' + match) #on ajoute l'url à la liste de tous les urls
    return urls

def urlToCsv(dicEquipe) :
    newpath = directory + 'Matchs/'
    if not os.path.exists(newpath):
        os.makedirs(newpath) #si ce chemin n'existe pas encore, on le crée
    urls = recupererURLMatchs(dicEquipe) #on récupère tous les urls du dictionnaire 
    team = dicEquipe[0] #on récupère le nom de l'équipe
    matchEquipe = pd.DataFrame() #on crée un dataframe vide, il servira pour remplir un fichier comprenant tous les matchs de l'équipe
    for url in urls: #on parcourt la liste des matchs d'une équipe
        try: #le try permet d'éviter les liens des matchs qui n'ont pas encore été joués
            df = pd.read_html(url) #on crée un dataframe de la page du match
            teams = df[0] #le premier tableau de la page contient le nom des deux équipes, on l'utilise donc pour récupérer leurs noms juste après
            nomDom = teams.iat[0,0] #on récupère le nom de l'équipe à domicile
            nomExt = teams.iat[1,0] #on récupère le nom de l'équipe à l'extérieur
            scoreDom = teams.iat[0,1] + teams.iat[0,2] + teams.iat[0,3] + teams.iat[0,4] #on récupère le score de l'équipe à domicile
            scoreExt = teams.iat[1,1] + teams.iat[1,2] + teams.iat[1,3] + teams.iat[1,4] #on récupère le score de l'équipe à l'extérieur
            if scoreDom == scoreExt : #s'il y a eu prolongations, on récupère le 5e quart temps
                scoreDom += teams.iat[0,5]
                scoreExt += teams.iat[1,5]
            domVainqueur = (scoreDom > scoreExt) #permet de savoir si l'équipe à domicile a gagné son match      
            dom = df[1] #le deuxième tableau de la page contient les stats de l'équipe à domicile
            rowsDom = len(dom) #on récupère le nombre de ligne de ce tableau pour nos boucles for
            dom = dom.replace(["Totaux Équipe"], "Total " + nomDom) #pour avoir le nom de l'équipe dans le dataframe, on met le nom de l'équipe à la place de "Equipe"
            dom.insert(2, "ADV", [nomExt for _ in range(rowsDom)], True) #ajoute le nom de l'équipe à l'extérieur en tant qu'adversaire
            dom.insert(2, "DOM/EXT", ["D" for _ in range(rowsDom)], True) #on annonce que l'équipe joue à domicile
            if domVainqueur : #on annonce si l'équipe a gagné ou perdu
                dom.insert(2, "V/D", ["V" for _ in range(rowsDom)], True) 
            else : dom.insert(2, "V/D", ["D" for _ in range(rowsDom)], True)
            ext = df[2] #on fait la même chose pour l'équipe à l'extérieur...
            rowsExt = len(ext)
            ext = ext.replace(["Totaux Équipe"], "Total " + nomExt)
            ext.insert(2, "ADV", [nomDom for _ in range(rowsExt)], True)
            ext.insert(2, "DOM/EXT", ["E" for _ in range(rowsExt)], True)
            if domVainqueur :
                ext.insert(2, "V/D", ["D" for _ in range(rowsExt)], True)
            else : ext.insert(2, "V/D", ["V" for _ in range(rowsExt)], True) #... jusque là
            dom = nettoyage(dom) #on nettoie nos deux tableaux
            ext = nettoyage(ext)
            match = pd.concat([dom, ext], axis=0) #on met nos deux dataframes en un pour n'avoir qu'un seul fichier du match
            if (nomDom == team):
                matchEquipe = pd.concat([matchEquipe, dom], axis = 0) #si l'équipe joaunt à domicile est celle pour laquelle on récupère les matchs, on ajoute son dataframe au fichier de l'équipe
            else :
                matchEquipe = pd.concat([matchEquipe, ext], axis = 0) #sinon c'est qu'elle joue à l'extérieur
            match.to_csv(directory + "Matchs/" + nomDom + " vs " + nomExt + ".csv",sep = ";", encoding = "utf-8-sig", index=False) #une fois la récupération finie, on peut mettre notre dataframe dans un fichier csv
        except: #si notre try n'est pas réalisé (le résultat n'est pas encore disponible), on passe à l'url suivant
            continue
    joueurCSV(matchEquipe, team) #on utilise la fonction précédente pour créer un fichier par joueur de l'équipe en cours de récupération
    matchEquipe.to_csv(directory + "Matchs/" + team + ".csv",sep = ";", encoding = "utf-8-sig", index=False) #une fois que tous les matchs de l'équipe ont été récupérés, on peut les mettre dans un csv

def joueurCSV(df, nomTeam):
    dfEquipeMoyenne = pd.DataFrame()
    dfEquipeVictoire = pd.DataFrame()
    dfEquipeDefaite = pd.DataFrame()
    listeJoueurs = df['Joueurs'].unique() #on récupère tous les joueurs de notre dataframe (on l'utilisera sur le dataframe de tous les matchs d'une équipe)
    listeJoueurs = list(listeJoueurs) #on convertit notre objet en liste pour le manipuler
    listeJoueurs.remove('Total ' + nomTeam) #on supprime de la liste des joueurs le total de l'équipe
    listeJoueurs.remove('Équipe') #on supprime de la liste des joueurs le joueur 'Equipe' qui correspond à des stats collectives ou difficile à attribuer à un joueur plutôt qu'un autre
    newpath = directory + "Equipes/" + nomTeam + "/" #cela correspond au chemin du dossier de l'équipe pour y mettre les fichiers des joueurs
    df['Min'] = pd.to_numeric(df['Min'], errors='coerce')
    if not os.path.exists(newpath):
        os.makedirs(newpath) #si ce chemin n'existe pas encore, on le crée
    for joueur in listeJoueurs : #on parcourt la liste des joueurs
        dfJoueur = df[df['Joueurs'] == joueur] #on crée un nouveau dataframe dans lequel on met chaque ligne du premier dataframe dont le nom du joueur correspond à celui en cours de traitement (on met chaque match dans un dataframe)
        dfJoueurVictoire = dfJoueur[dfJoueur['V/D'] == 'V']
        dfJoueurDefaite = dfJoueur[dfJoueur['V/D'] == 'D']
        moyenne = dfJoueur.mean(axis=0, numeric_only=True) #on crée une objet "moyenne" qui calcule la moyenne chaque colonne du dataframe (si elle est moyennable)
        victoire = dfJoueurVictoire.mean(axis=0, numeric_only=True)
        defaite = dfJoueurDefaite.mean(axis=0, numeric_only=True)
        dfMoy = remplissageLignes(dfJoueur, "Moyenne", moyenne)
        dfVic = remplissageLignes(dfJoueur, "Victoire", victoire)
        dfDef = remplissageLignes(dfJoueur, "Défaite", defaite)
        dfJoueur = pd.concat([dfJoueur, dfMoy, dfVic, dfDef], axis = 0) #on concatène cette "ligne" au dataframe existant
        dfJoueur = dfJoueur.replace(["nan"], ) #les colonnes non-sommable donnent la valeur "nan" dans la ligne total donc on les enlève
        dfMoy.iat[0,3] = nomTeam #on rajoute le nom de l'équipe
        dfVic.iat[0,3] = nomTeam #on rajoute le nom de l'équipe
        dfDef.iat[0,3] = nomTeam #on rajoute le nom de l'équipe
        dfMoy.rename(columns = {'DOM/EXT':'Equipe'}, inplace = True)
        dfVic.rename(columns = {'DOM/EXT':'Equipe'}, inplace = True)
        dfDef.rename(columns = {'DOM/EXT':'Equipe'}, inplace = True)
        dfEquipeMoyenne = pd.concat([dfEquipeMoyenne, dfMoy], axis=0)
        dfEquipeVictoire = pd.concat([dfEquipeVictoire, dfVic], axis=0)
        dfEquipeDefaite = pd.concat([dfEquipeDefaite, dfDef], axis=0)
        dfJoueur.to_csv(newpath + joueur + ".csv",sep = ";", encoding = "utf-8-sig", index=False) #on met ce dataframe dans un csv qui ira dans le dossier de l'équipe
    moyenneEquipe = dfEquipeMoyenne.mean(axis=0, numeric_only=True)
    moyenneVictoire = dfEquipeVictoire.mean(axis=0, numeric_only=True)
    moyenneDefaite = dfEquipeDefaite.mean(axis=0, numeric_only=True)
    dfMoy = remplissageTotalEquipe(dfEquipeMoyenne, "Moyenne", moyenneEquipe, nomTeam)
    dfEquipeMoyenne = pd.concat([dfEquipeMoyenne, dfMoy], axis=0)
    dfVic = remplissageTotalEquipe(dfEquipeVictoire, "Victoire", moyenneVictoire, nomTeam)
    dfEquipeVictoire = pd.concat([dfEquipeVictoire, dfVic], axis=0)
    dfDef = remplissageTotalEquipe(dfEquipeDefaite, "Défaite", moyenneDefaite, nomTeam)
    dfEquipeDefaite = pd.concat([dfEquipeDefaite, dfDef], axis=0)
    newpath = directory + 'Moyenne/Total/'
    if not os.path.exists(newpath):
        os.makedirs(newpath) #si ce chemin n'existe pas encore, on le crée
    dfEquipeMoyenne.to_csv(newpath + nomTeam + ".csv",sep = ";", encoding = "utf-8-sig", index=False)
    newpath = directory + 'Moyenne/Victoires/'
    if not os.path.exists(newpath):
        os.makedirs(newpath) #si ce chemin n'existe pas encore, on le crée    
    dfEquipeVictoire.to_csv(newpath + nomTeam + ".csv",sep = ";", encoding = "utf-8-sig", index=False)   
    newpath = directory + 'Moyenne/Défaites/'
    if not os.path.exists(newpath):
        os.makedirs(newpath) #si ce chemin n'existe pas encore, on le crée
    dfEquipeDefaite.to_csv(newpath + nomTeam + ".csv",sep = ";", encoding = "utf-8-sig", index=False)
               



#nettoyage et réorganisation de la feuille

def remplissageLignes(dfJoueur, nomLigne, ligne):
    dfLigne = pd.DataFrame([ligne], columns=dfJoueur.columns) #on transforme l'objet en dataframe en lui donnant les bons noms de colonne
    dfLigne.iat[0,4] = nomLigne #on donne le bon nom que l'on met dans la colonne ADV
    dfLigne.iat[0,0] = dfJoueur.iat[0,0] #on reporte le numéro du joueur
    dfLigne.iat[0,1] = dfJoueur.iat[0,1] #on reporte aussi le nom du joueur
    recalculPourcent(dfLigne) #on donne la bonne valeur aux % de nos lignes calculées
    return dfLigne

def remplissageTotalEquipe(dfJoueur, nomLigne, ligne, nomTeam):
    dfLigne = pd.DataFrame([ligne], columns=dfJoueur.columns) #on transforme l'objet en dataframe en lui donnant les bons noms de colonne
    dfLigne.iat[0,4] = nomLigne #on donne le bon nom que l'on met dans la colonne ADV
    dfLigne.iat[0,0] = 0 #l'équipe porte le numéro 0 (arbitraire)
    dfLigne.iat[0,1] = nomTeam #on donne comme nom au joueur le nom de son équipe
    dfLigne.iat[0,3] = nomTeam #on donne le nom à l'équipe aussi
    if nomTeam != "Maximum":
        recalculPourcent(dfLigne) #on donne la bonne valeur aux % de nos lignes calculées
    return dfLigne

def recalculPourcent(df):
    df["2%"] = np.where(df['2T'] != 0, df['2R'] / df['2T'], np.nan) #s'il y a eu au moins un tir tenté, on peut calculer le % de réussite...
    df["3%"] = np.where(df['3T'] != 0, df['3R'] / df['3T'], np.nan)
    df["LF%"] = np.where(df['LFT'] != 0, df['LFR'] / df['LFT'], np.nan) #... pour chaque type de lancer

def nettoyage(df):
    df[["2R", "2T"]] = df["2R-2T"].apply(lambda x: pd.Series(str(x).split("-"))) #on commence par fractionner les colonnes qui ne devraient pas être fusionnées...
    df[["3R", "3T"]] = df["3R-3T"].apply(lambda x: pd.Series(str(x).split("-")))
    df[["LFR", "LFT"]] = df["LFR-LFT"].apply(lambda x: pd.Series(str(x).split("-"))) #... jusque là
    df = df.drop(columns=["2R-2T", "3R-3T", "LFR-LFT", "T%", "LF%", "EVA"]) #on supprime les colonnes précédentes car elles sont désormais en double, on enlève les % car ils seront recalculés et EVA que l'on juge pour l'instant inutile
    df['2T'] = pd.to_numeric(df['2T'], errors='coerce') #on fait en sorte que les données des colonnes pour lesquelles on va calculer un % soit au format numeric et non string...
    df['2R'] = pd.to_numeric(df['2R'], errors='coerce')
    df['3T'] = pd.to_numeric(df['3T'], errors='coerce')
    df['3R'] = pd.to_numeric(df['3R'], errors='coerce')
    df['FTE'] = pd.to_numeric(df['FTE'], errors='coerce')
    df['BP'] = pd.to_numeric(df['BP'], errors='coerce')
    df['LFT'] = pd.to_numeric(df['LFT'], errors='coerce')
    df['LFR'] = pd.to_numeric(df['LFR'], errors='coerce') #... jusque là
    df = df.fillna(0) #les cases vides sont remplacées par des 0 pour éviter les problèmes de calculs
    df['FTE'] = -1*df['FTE']
    df['BP'] = -1*df['BP']
    df["2%"] = np.where(df['2T'] != 0, df['2R'] / df['2T'], np.nan) #s'il y a eu au moins un tir tenté, on peut calculer le % de réussite...
    df["3%"] = np.where(df['3T'] != 0, df['3R'] / df['3T'], np.nan)
    df["LF%"] = np.where(df['LFT'] != 0, df['LFR'] / df['LFT'], np.nan) #... pour chaque type de lancer
    df = df.replace(["nan"], ) #on remplace les valeurs "nan" par du vide qui apparaissent s'il n'y a pas eu de tirs tentés
    df = df.iloc[:, [0, 1, 2, 3, 4, 17, 18, 23, 19, 20, 24, 21, 22, 25, 6, 10, 11, 13, 12, 7, 8, 9, 14, 15, 5, 16]] #on réordonne les colonnes pour qu'il y ait un peu plus de sens 
    return df
    
def tousJoueurs(ligne, dossier):
    path = directory + ligne + '/' + dossier + '/'
    if not os.path.exists(path):
        os.makedirs(path) #si ce chemin n'existe pas encore, on le crée
    dfTous = pd.DataFrame()
    dfEquipesTous = pd.DataFrame()
    fichiers = [f for f in listdir(path) if isfile(join(path, f))]
    for team in fichiers:
        dfTeam = pd.read_csv(path + team, sep=";")
        dfTous = pd.concat([dfTous, dfTeam], axis=0)
        dfTeam = dfTeam.iloc[:-1]
        dfEquipesTous = pd.concat([dfEquipesTous, dfTeam], axis=0)
    moyenneLFB = dfEquipesTous.mean(axis=0, numeric_only=True)
    dfMoy = remplissageTotalEquipe(dfEquipesTous, dossier, moyenneLFB, "LFB")
    maxLFB = dfEquipesTous.max(axis=0, numeric_only=True)
    dfMax = remplissageTotalEquipe(dfEquipesTous, dossier, maxLFB, "Maximum")
    dfTous = pd.concat([dfTous, dfMoy, dfMax], axis=0)
    dfTous.drop('V/D', axis=1, inplace=True)
    dfTous.to_csv(directory + ligne + '/' + dossier + '.csv', sep = ";", encoding = "utf-8-sig", index=False)
        
#on extrait tous les matchs de championnat

for dicEquipe in urlsEquipes.items() : #on parcourt le dictionnaire d'équipe
    urlToCsv(dicEquipe) #pour chaque équipe, on récupère ses matchs et ses fichiers joueurs
tousJoueurs('Moyenne', "Total")
tousJoueurs('Moyenne', "Victoires")
tousJoueurs('Moyenne', "Défaites")
print("récupération terminée") #pour signaler que la récupération est terminée car un peu longue (1 à 2 minutes pour 60 matchs joués)