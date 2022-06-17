<?php
  //constante d'environnement
  define("DBHOST", "localhost");  #Cette variable sera notre server la ou il y a la BDD
  define("DBUSER", "php"); #Cette variable sera l'utilisateur de notre BDD
  define("DBPASS", "tata"); #Cette variable sera le mdp de l'utilisateur
  define("DBNAME", "test"); #cette variable sera le nom de notre BDD

  // DSN de connexion
  $dsn = "mysql:dbname=".DBNAME.";host=".DBHOST;

  // on va se connecter a la base
  #ON va utiliser le try catch qui nous permet de dire en gros essaye de faire ce qu'il y a dans try sinon si ça marche pas tu fait ce qu'il y a dans catch()
  try {
    //On instance le PDO
    $db = new PDO($dsn, DBUSER, DBPASS);

    //On definit le charset à "utf-8"
    $db->exec("SET NAMES utf8");

    // On definit la methode de recuperation (fetch) des donnees
    $db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);

  } catch (PDOException $e) {
    die("Erreur: ".$e->getMessage());
  }
  // Nous somme bel et bien connecte
 ?>
