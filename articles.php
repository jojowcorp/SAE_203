<?php
  // On va chercher les erreurs dans la BDD mais tout d'abbord on s'y connecter
  require_once("connect.php");

  //On ecrit la requete
  $sql = "SELECT * FROM flux";

  // On execute la requete
  $requete = $db->query($sql);

  // On recupere les donnees
  $articles = $requete->fetchAll();

  // on definit le titre
  $titre = "JCORP - Articles";


  // On inclut le header
  include("includes/header.php");

  // On inclut le header
  include("includes/navbar.php");
?>

<h1>Liste des erreurs:</h1>

<table>

  <thead>
    <th>Nom Erreur</th>
    <th>Description</th>
    <th>A eu lieu le</th>
    <th>Catégorie</th>
    <th>Numéro server</th>
    <th>Guid</th>
  </thead>
  <tbody>

<?php foreach($articles as $article): ?>
<tr>
  <td><a href="erreur.php?id=<?= $article["id"]?>"><?php echo strip_tags($article['erreur']); ?></a></td>
  <td><?php echo strip_tags($article['description']); ?></td>
  <td><?php echo strip_tags($article['date']); ?></td>
  <td><?php echo strip_tags($article['categorie']); ?></td>
  <td><?php echo strip_tags($article['numero_server']); ?></td>
  <td><?php echo strip_tags($article['guid']); ?></td>
</tr>

<?php endforeach; ?>
</tbody>
</table>

<?php
  // On inclut le footer
  include("includes/footer.php");
 ?>
