<link rel="stylesheet" href="style.css">
<meta charset="utf-8">
<title>Plany lekcji</title>
<meta name="viewport" content="width=device-width, initial-scale=0.7">
<meta property="og:url" content="http://www.kaszkowiak.org/plan/" />
<meta property="og:title" content="Plan lekcji" />
<meta property="og:description" content="Szybki, przyjazny komórkom - lepszy od edupage" />
<meta property="og:image" content="http://www.kaszkowiak.org/plan/brr.jpg" />
<?php
$db = new SQLite3('baza.db');

function displayList($db, $db_key, $header) {
	echo "<h2>$header:</h2><ul>";
	$res = $db->query("SELECT $db_key FROM jednostki_lekcyjne GROUP BY $db_key");
	while ($row = $res->fetchArray(SQLITE3_ASSOC)) {
		$element = $row[$db_key];
		echo "<li><a href='plan.php?$db_key=$element'>$element</a></li>";
	}
	echo "</ul>";
}

displayList($db, "class", "Lista klas");
displayList($db, "teacher", "Lista nauczycieli");
displayList($db, "classroom", "Lista sal lekcyjnych");
?>
