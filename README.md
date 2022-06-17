
![Logo](https://zupimages.net/up/22/24/ahb0.png)


## Caractéristiques


- Facile à mettre en place
- Fiable
- Récupération des erreurs générées sur x serveur
- Gratuit
- Open source

# Base de donnée

Comme la solution nécessite une base de donnée, il vous faudra en faire l'installation. Nous utiliserons alors MariaDB, un SGBD (système de gestion de base de donnée) open source qui nous permet de gérer de manière triviale les données qui s'y trouve à l'intérieur.
Cette partie est à faire entièrement sur la machine aggreg.net

• Etape 1: Mettre a jour son système d'exploitation

```bash
  sudo apt update && sudo apt upgrade
```

(en supposant que votre utilisateur est dans le fichier /etc/sudoers)


• Etape 2: Installation de MariaDB

```bash
  sudo apt install mariadb-server mariadb-client
```

Pour vérifier que MariaDB est bel et bien installé sur votre système executer cette commande pour voir la version de MariaDB que vous avez installé:

```bash
  mariadb --version
```

Si en sortie vous obtenez quelque chose du genre :

```bash
  mariadb  Ver 15.1 Distrib 10.7.1-MariaDB, for debian-linux-gnu (x86_64) using readline EditLine wrapper
```
Alors l'installation c'est bien passé vous pouvez passer à l'étape suivante.

• Etape 3: Configuration des comptes pour python et php Base de donnée

Connectez-vous en root pour pas qu'il y ait des problèmes de connexion ou autre on créer un compte pour python et un autre pour php car les deux vont intéragir avec la BDD.
Commencez par vous connecter à la base de donnée en root à la BDD :

```bash
  mysql -u root -p
```

Vous êtes donc arrivé dans MariaDB.
Nous allons commencer par créer l'utilisateur python avec comme mot de passe tata:

```bash
  CREATE USER 'python'@localhost IDENTIFIED BY 'tata';
```

(Optionnel) Vous pouvez vous assurez que l'utilisateur à bien été crée au sein de MariaDB par le biais de cette commande :

```bash
  SELECT User FROM mysql.user;
```

Maintenant on confère les privilèges à notre nouvel utilisateur :

```bash
  GRANT ALL PRIVILEGES ON *.* TO 'python'@localhost IDENTIFIED BY 'tata';
```

Une fois cela fait vous devez rafraichir les privilèges :

```bash
  FLUSH PRIVILEGES;
```
Vous venez de créer votre utilisateur python au sein de la BDD, répetez ce que vous avez fait durant l'étape 3 afin de créer l'utilisateur php (au sein des commandes vous remplacerez donc ‘python’ par ‘php’ et concernant le mots de passe vous pouvez laisser le même).
Vérifions que nos deux utilisateurs ont leurs privilèges :

(pour l'utilisateur python)

```bash
SHOW GRANTS FOR 'python'@localhost;
```

Normalement MariaDB devrait vous renvoyer ce message a chaque fois que vous entrer la commande:




![App Screenshot](https://zupimages.net/up/22/24/es09.png)

![App Screenshot](https://zupimages.net/up/22/24/s9ld.png)
Comme on peut le remarquer le password n'est pas celui que l'on a renseigné et c'est tout a fait normal car dans Mariadb les mots de passe sont haché par la fonction PASSWORD().

Dès à présent il faut que l'on créée notre base de donnée ainsi que ses tables, pour ce faire il suffit de lancer une seule fois le programme connect.py (Si vous le lancé une seconde fois alors que vous avez déjà une base de donnée qui contient une tables rempli, la tables sera alors supprimé et recrée à neuf donc après avoir lancée connect.py n'y touchée plus sous peine de perdre les donnnées contenu dans votre tables )

Si vous n'avez rencontré aucune erreurs durant les différentes étapes alors vous pouvez passer dès a présent au prochain chapitre : Web

# Web

Vous voilà arrivé au chapitre Web :)

Ce chapitre est relativement court car nous avons juste besoin d'installer php sur notre machine aggreg.net.
Nous allons proceder de la manière suivante:

Installons php ainsi que ses différents modules :

Php :

```bash
  apt install php
```

Module sql pour php :

```bash
  apt install php-mysql
```

Module PHP pour le serveur web Apache 2 :

```bash
  apt install libapache2-mod-php
```
Apres avoir installer avec succès tout les paquets il nous faut redémarrer apache2 :

```bash
  sudo systemctl restart apache2
```
Maintenant mettez dans le répertoir /var/www/html :

- le dossier include
- les pages php (index, erreur, connect et articles)


## Fichier config (aggreg_config.yaml)

Le fichier de config ressemble à ça :

```javascript
sources:
  - url
  - url
  - url
  ...
rss-name: nom_de_fichier

```

Dans source vous indiquez les urls de vos serveurs et dans rss-name le nom du fichier RSS, vous devez le mettre dans le répertoir /etc   .



## Flux RSS

Le format de fichier RSS attendu est le suivant :

```javascript
<rss version="2.0">
  <channel>
    <title>Recent Events for http:///</title>
    <link>http:///rss.xml</link>
    <description>List of recent events.</description>
    <language>en</language>
    <pubDate>Sat, 14 May 2022 23:39 </pubDate>
    <lastBuildDate>Sat, 14 May 2022 23:39 </lastBuildDate>
    <item>
      <title>Apache service restart.</title>
      <category>MINOR</category>
      <guid>17b84161-e059-4383-bafd-fc33069c51c8</guid>
      <link>http:///17b84161-e059-4383-bafd-fc33069c51c8.html</link>
      <description>Apache service restarted because of the definition of
  a new virtual host.</description>
      <pubDate>Fri, 19 Nov 2021 20:17 </pubDate>
    </item>
    </channel>
</rss>

```

Avec autant de balise `item` qu'il y a d'événement.

`title`
Le titre de l'événement.

`category`
une des trois valeurs MINOR, MAJOR ou CRITICAL rendant compte de l'importance de l'événement.

`guid`
un identifiant d'événement unique. Son format respecte la version 4 de la [RFC4122](https://datatracker.ietf.org/doc/html/rfc4122.html).

`link`
un lien vers une page donnant un descriptif détaillé de l'événement. Ce lien est composé de la partie hôte de l'URL du flux RSS suivi du guid, suivi de l'extension .html.

`description`
une description de l'événement.

`pubDate`
date de publication de l'événement au format [RFC822](https://datatracker.ietf.org/doc/html/rfc822).


## Lien externe

[Iso Debian](https://www.debian.org/distrib/index.fr.html)


## FAQ

#### Je n'arrive pas à accéder au site http://aggreg.net

Tout d'abbord essayer de faire un ping depuis votre machine client vers votre machine aggreg, dans le cas où ça ne fonctionne pas alors vérifier bien vos paramètre réseaux (ip, passerelle...)
Si vous pouvez ping depuis votre machine client vers la machine aggreg mais que vous ne parvenez toujours pas à vous rendre sur http://aggreg.net alors vérifier bien dans votre fichier /etc/hosts que vous ayez rentré la bonne ip de aggreg ainsi que son nom d'hôte comme ceci :

```bash
  <IP de aggreg>  aggreg.net
```

#### J'ai éteint puis rallumée ma machine aggreg mais j'ai des erreurs sur la page http://aggreg.net ?

C'est tout à fait normal, il suffit juste de ré-activer apache2 et mariadb à l'aide des commandes suivantes :

```bash
  systemctl restart apache2.service
  systemctl restart mariadb.service
```


#### Quel est la configuration requise ?

Ayant fait ce projet sur ma station de travail avec que des machines virtuel, je recommande d'utiliser :

• Processeur : i5-7300HQ

• RAM : 6GO (2.536GO de ram vont être utilisé ,car 512 mb de ram par serveur et 1go pour l'aggregateur, au cours du guide nous allons en utiliser 2Go par machine)

• Espace disque : 20 go de stockages vous sera necessaire (5 par marchine mais durant au cours de ce guide nous alonrs en utiliser 10 pour être large).

#### J'ai un problème qui ne figure pas dans la FAQ, que faire ?

Ce projet est tout récent, il est normal que tout les problèmes possibles et inimaginable n'ont pas été énumérer, dans ce cas il serait préferable de prendre contact a cette adresse mail : jorane.ripiego@etu.univ-amu.fr

#### J'ai deux flux d'erreurs à récupérer mais ils ont deux noms différents, comment faire ?

Pour le moment le programme n'est pas concue pour récupérer des erreurs provenant de deux flux ayant un nom différents (peut-être que cela sera possible dans les mois suivant :) ), nous conseillons alors de récupérer les erreurs du premier flux puis ensuite changer le nom et récupérer les erreurs du deuxièmes flux.

#### Comment récupérer les erreurs provenant de plusieurs serveur ?

Il vous suffit de vous rendre dans le fichier config que vous avez mis dans le répertoir /etc
Puis de le modifier en écriture, placez-vous dans source, mettez un espace puis un tiret du 6 suivie de l'url du serveur dont vous voulez récupérer les erreurs.
