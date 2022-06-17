#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 14 14:40:17 2022

@author: JCORP - lambda - RIPIEGO Jorane 
"""
#Importation du module feedparser pour pouvoir manipuler aisément les flux RSS
import feedparser
#Importation du module requests, va nous simplifier la vie pour savoir si une URL est accessible ou pas
import requests
#On importe le module yaml pour manipuler notre fichier /etc/python3/aggreg_config.yaml
import yaml
# Importation du module pour la BDD
import mysql.connector as mariadb




#étape 1
def charge_urls(liste_url):
    """Cette fonction permet de savoir si une url est accessible ou pas, 
    elle range ces url dans une liste qu'elle renvoie"""
    
    lst_url = []   #La liste qui contiendra nos url 
    
    for i in range(len(liste_url)):
        
        requete = requests.get(liste_url[i])
        
        if (requete.status_code == 404 and requete.ok == False):  #J'utilise la méthode status_code et ok de la librairie request pour bien être sûr que l'URL n'est pas accessible
            
            lst_url.append(None)  #En l'occurence si elle n'est pas accessible on ajoute None dans notre liste
            
        else :
            
            lst_url.append(liste_url[i])  #Si elle est acccessible alors on l'ajoute dans notre liste tout simplement
            
    return lst_url   #A la fin on renvoi la liste 



#étape 2
def fusion_flux(liste_url, liste_flux):
    """Cette fonction nous permet de renvoyer une liste qui contient un dico de chaque evenement rss du document
    RSS de chaque serveur"""
    
    liste_dico = []   #La liste final qui contiendra des dico contenant les caractéristiques des erreurs
    
    true_url = charge_urls(liste_url)   #Variable qui va nous permettre de savoir si une url est accessible ou pas, cela va nous simplifier la vie pour la liste des nom de serveur
    
    liste_serveur = []   #Liste qui comme son nom l'indique contiendra le nom des serveurs
    
    for i in range(len(true_url)):  #Avec cette boucle je vais recuperer le nom des serveurs
        
        if (true_url[i] != None):
            
            serveur = true_url[i]
            
            serveur = serveur[7:15]
            
            liste_serveur.append(serveur)
            
    
    for k in range(len(liste_flux)):  #Avec cette boucle je vais itérée sur tout les serveurs que j'ai en URL
        
        if (liste_flux[k] != None):
            
            url = liste_flux[k]
            
            news_feed = feedparser.parse(url)
            
            for j in range(len(news_feed['entries'])):  #Puis avec celle-ci je vais itérer sur toutes les erreurs présentes dans le documents RSS du serveur

                dico_element = {}
                
                # Je déclare mes variables que j'ajouterai dans un dico, ce dico contiendra les caractéristiques pour une seul erreur dans le flux rss
                
                titre = news_feed['entries'][j]['title']
                
                date_publi = news_feed['entries'][j]['published']
                
                lien = news_feed['entries'][j]['link']
                
                description = news_feed['entries'][j]['summary']
                
                lst_categorie = news_feed['entries'][j]['tags']
                
                dico_categorie = lst_categorie[0]
                
                categorie = dico_categorie["term"]
                
                serveur = liste_serveur[k]
                
                #Je range mes variables dans mon dictionnaire
                dico_element["titre"] = titre
                
                dico_element["date_publi"] = date_publi
                
                dico_element["lien"] = lien
                
                dico_element["description"] = description
                
                dico_element["categorie"] = categorie
                
                dico_element["serveur"] = serveur
                
                #J'ajoute mon dico fraichement constitué dans ma liste de dictionnaire
                
                liste_dico.append(dico_element)
                
    return liste_dico   #On renvoi notre liste de dictionnaire


#étape 65446 à ma sauce qui va nous permettre de connaitre quelles sont les erreurs qui ne sont pas déjà présente dans la BDD 

def nouvelles_erreures(liste_errreurs):
    """Cette fonction va nous permettre d'identifier les nouvelles erreurs à
    ajouter dans notre base de données"""
    
    #On se connecte a notre base de donnée contenant toute nos erreurs
    
    # création d'une connection et définition du cursor
    mariadb_connection = mariadb.connect(user='python', password='tata', database='test',host='localhost',port='3306')

    create_cursor = mariadb_connection.cursor()
    
    #On séléctionne toutes les données de la tables
    create_cursor.execute('SELECT erreur,description,numero_server,guid,categorie,date FROM flux;')
    
    #notre variable sera alors une liste qui contiendra toute notre base de données
    mes_resultats = create_cursor.fetchall()
        
    lst_erreurs_sql = transformer_sql(mes_resultats)    #Cette variables est une liste qui contient des dico, a l'interrieur de chacun de ces dico se trouve le titre et le lien guid de chaque erreurs provenant de la BDD
    
    # fermer la connection, a ne jamais oublier
    mariadb_connection.commit();    
    
    liste_inter = []   #Liste intermédiaire
    
    for p in range(len(liste_errreurs)):  #Avec cette boucle on va convertir les dates de chaques erreurs dans un format un peu plus lisible et manipulable
        
        element = liste_errreurs[p]
        
        element["date_publi"] = convertisseur_date(element["date_publi"])
        
        liste_inter.append(element)
    
    liste_fnl = []   #Notre liste finale qui contiendra uniquement les nouvelles erreurs
    
    for k in liste_inter: #Par le biais de cette boucle on va vérifier si les erreurs présentes dans notre liste intermédaire sont également présente dans la BDD, auquel cas où on ne l'ajoutera pas dans notre liste finale
        
        compteur = 0  #Ce compteur nous permet de savoir s'il y a une correspondance de guid dans la BDD
        
        for p in lst_erreurs_sql:
            
            if (k["lien"] == p["lien"]):
                
                compteur += 1
        
        if (compteur == 0):  #Si le compteur reste a 0 cela signifie donc que l'erreur n'est pas présente dans la BDD et donc qu'il faut l'ajouter dans notre liste finale
            
            liste_fnl.append(k)
    
    return liste_fnl   #On renvoi notre liste contenant les erreurs qui ne sont pas présente dans la BDD
    
    
def transformer_sql(requete_sql):
    """Cette fonction va nous permettre de transformer le résultat de notre
    requete sql en format lisible et un peu facile a manipuler pour faire
    des comparaisons"""
    
    liste_sql = requete_sql  #Liste intermédiaire pour éviter d'utiliser notre entrée
    
    liste_erreurs = []  #Liste finale qui va nous permettre d'avoir le nom d'erreur ainsi que le guid de chaque erreurs présentes dans la BDD, cette liste sera renvoyé à la fin
    
    for s in range(len(liste_sql)):  #Avec cette boucle on va itéré sur chaque élément de liste d'erreur
        
        dico_erreur = {}  #Dico qui va contenir le nom d'erreur et le guid de chaque erreurs de la base de donnée, ce dico sera a chaque itération dans notre liste finale
    
        erreur,description,serveur,guid,cat,date = liste_sql[s]  #Comme chaque élément de notre liste est un tuple alors j'utilise deux variables : une qui contient le nom de l'erreur et l'autre son guid
        
        guid_html = str(guid) #On ajoute le guid
        
        #On ajoute dans notre dico nos variable
        
        dico_erreur["titre"] = erreur  
        
        dico_erreur["lien"] = guid_html
        
        dico_erreur["description"] = description
        
        dico_erreur["categorie"] = cat
        
        dico_erreur["serveur"] = serveur
        
        dico_erreur["date"] = date
        
        liste_erreurs.append(dico_erreur)  #On ajoute notre dico a notre liste finale
    
    return liste_erreurs   #On renvoi notre liste d'erreurs
    

def count_sql(sql_count):
    """Cette fonction permet de compter le nombre d'erreurs qu'il y a
    dans notre BDD"""
    
    requete = sql_count[0]
    
    count= requete[0]
    
    return count


def convertisseur_date(date_a_convertir):
    """Cette fonction nous permet de convertir des dates dans un format compréhensible pour la BDD"""

    liste_mois = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    date_inter2 = date_a_convertir.split(" ")
    
    annee = date_inter2[3]
    
    for y in range(len(liste_mois)):
        
        if (date_inter2[2] == liste_mois[y]):
            
            mois = y+1
            
    jour = date_inter2[1]
    
    heure = date_inter2[4][0:2]
    
    minute = date_inter2[4][3:5]

    date = annee+"-"+str(mois)+"-"+jour+" "+heure+":"+minute+":00"
        
    return date    #On renvoi notre date au format demandé



def ajout_sql(liste_nouvelles_erreurs):
    """Cette fonction va nous permettre d'ajouter dans notre BDD les nouvelles
    erreurs"""
    
    #On se connecte a notre base de donnée contenant toute nos erreurs
    
    # création d'une connection et définition du cursor
    mariadb_connection = mariadb.connect(user='python', password='tata', database='test',host='localhost',port='3306')

    create_cursor = mariadb_connection.cursor()
    
    #On écrite la requete pour savoir le nombre d'erreur dans notre table tables
    create_cursor.execute('SELECT COUNT(*) FROM flux;')
    
    #notre variable sera alors une liste qui contiendra le nombre d'erreurs présentes dans notre BDD mais dans un type qui nous convient pas (tuple)
    mes_resultats = create_cursor.fetchall()
    
    #On a transformé notre tuple en int, bien plus simple d'utilisation
    l_id = count_sql(mes_resultats)
    
    for n in range(len(liste_nouvelles_erreurs)):
        
        erreurs_n = liste_nouvelles_erreurs[n]
        
        l_id+=1
        
        erreur = erreurs_n["titre"]
        
        date = erreurs_n["date_publi"]
        
        numero_serveur = erreurs_n["serveur"]
        
        guid_html = erreurs_n["lien"]
        
        description = erreurs_n["description"]
        
        categorie = erreurs_n["categorie"]
        
        #On prepare nos élément a insérer dans la BDD
        element_à_inserer = (l_id,erreur,date,numero_serveur,guid_html,description,categorie)
        
        #On prépare notre requete
        sql_requete = ('INSERT INTO flux (id, erreur, date, numero_server, guid, description, categorie) VALUES (%s, %s, %s, %s, %s, %s, %s)')
        
        #On execute notre commande
        create_cursor.execute(sql_requete, element_à_inserer)    
    
    #Une fois qu'on a fini d'inserer toute nos erreurs dans la BDD on ferme la connection
    
    # fermer la connection, a ne jamais oublier
    mariadb_connection.commit();
    
    return 1  #Et on renvoi 1 pour s'assurer qu'il n'y a eu aucun probleme
    
#étape 4
def aggreg(fichier_config):
    """Cette fonction nous permet de recuperer dans un fichier /etc/python3/aggreg_config.yaml 
    les informations que l'utilisateur indique pour que l'on recupere les urls ainsi que 
    le nom du flux rss"""  

    with open(fichier_config, 'r') as FD:  #On ouvre notre fichier en mode lecture
    
        data = yaml.load(FD, Loader=yaml.FullLoader)
        
        liste_url = data["sources"]  #On définie une variable qui contiendra la liste de nos url
        
        liste_url_rss = []   #Cette liste sera notre liste final et contiendra les urls ainsi que le nom du document rss
        
        rss = data["rss-name"]  #Cette variable contient le nom du document RSS a utiliser pour chaque url
        
        for j in range(len(liste_url)):  #Petite boucle qui nous permet d'ajouter dans notre liste finale les urls accompagné du nom du document RSS
            
            url_rss = liste_url[j]+"/"+rss
            
            liste_url_rss.append(url_rss)
    
    return liste_url_rss  #On renvoie notre liste


  
#########################################################
#
#              PROGRAMME PRINCIPAL
#
#########################################################

    
def main():
     
     fichier_config = "/etc/aggreg_config.yaml"
     
     liste_url = aggreg(fichier_config)
    
     liste_flux = charge_urls(liste_url)
     
     liste_errreurs = fusion_flux(liste_url, liste_flux)
     
     liste_nouvelles_erreurs = nouvelles_erreures(liste_errreurs)
     
     ajout_sql(liste_nouvelles_erreurs)
     
     
if __name__ == '__main__':
    main()