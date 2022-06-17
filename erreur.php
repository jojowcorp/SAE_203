<?php

  // On verifie si on a un id

  if (!isset($_GET["id"]) || empty($_GET["id"])) {
    // Dans le cas ou nous n'en avons pas
    header("Location: articles.php");
    exit;
  }

  // On recupere l'id
  $id = $_GET["id"];

  // On va chercher les erreurs dans la BDD mais tout d'abbord on s'y connecter
  require_once("connect.php");

  // ecriture de la requete
  $sql = "SELECT * FROM flux WHERE id= :id";

  //on la prepare
  $requete = $db->prepare($sql);

  //On injecte les parametres
  $requete->bindValue(":id", $id, PDO::PARAM_INT);

  // On execute la requete
  $requete->execute();

  // On recupere l'erreur
  $article = $requete->fetch();

  // on vérifie si article est vide
  if(!$article){
    // si notre variable est vide alors on affiche une erreur 404
    http_response_code(404);
    echo "Erreur inexistante";
    exit;
  }

  // Si on a bien une erreur a afficher alors

  // on definit le titre
  $titre = "JCORP - Erreur";

  
  // On inclut le header
  include("includes/header.php");

  // On inclut le header
  include("includes/navbar.php");
?>

<h1><?php echo strip_tags($article['erreur']); ?></h1>
<p>Publié le : <?php echo strip_tags($article['date']); ?></p>
<article><?php echo strip_tags($article['description']); ?></article>


<?php
  // On inclut le footer
  include("includes/footer.php");
 ?>
