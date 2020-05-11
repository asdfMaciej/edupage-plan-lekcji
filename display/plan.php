<link rel="stylesheet" href="style.css">
<meta charset="utf-8">
<title>Plan lekcji</title>
<meta property="og:url" content="http://www.kaszkowiak.org/plan/plan.php" />
<meta property="og:title" content="Plan lekcji" />
<meta property="og:description" content="Szybki, przyjazny komórkom - lepszy od edupage" />
<meta property="og:image" content="http://www.kaszkowiak.org/plan/brr.jpg" />

<meta name="viewport" content="width=device-width, initial-scale=0.7">
<h1><a href="./">Wróć do listy planów.</a></h1>
<?php
$db = new SQLite3('baza.db');
$allowed_filters = ["class", "classroom", "teacher"];
foreach ($_GET as $key => $val)
	if (!in_array($key, $allowed_filters))
		die("Niedozwolony filter.");

$statement = "SELECT * FROM jednostki_lekcyjne";
if ($_GET)
	$statement .= " WHERE ";

$params = [];
$where = [];
foreach ($_GET as $filter => $value) {
	$where[] = "$filter = :$filter";
	$params[":$filter"] = $value;
}

$statement .= implode(" AND ", $where);
$statement .= " ORDER BY period_start ASC";
$stat = $db->prepare($statement);
foreach ($params as $key => $val)
	$stat->bindParam($key, $value, SQLITE3_TEXT);

$res = $stat->execute();
$days = ["d_monday" => "Poniedziałek", "d_tuesday" => "Wtorek", "d_thursday" => "Środa", "d_wednesday" => "Czwartek", "d_friday" => "Piątek"];

$lessons_by_day = [];
foreach (array_keys($days) as $day)
	$lessons_by_day[$day] = [];

while ($row = $res->fetchArray(SQLITE3_ASSOC))
	foreach (array_keys($lessons_by_day) as $day) 
		if ($row[$day] == "1")
			$lessons_by_day[$day][] = $row;

foreach ($days as $day_index => $day) {
	echo "<h2>$day</h2>";
	foreach ($lessons_by_day[$day_index] as $lesson) {
		$t1 = $lesson['period_start'];
		$t2 = $lesson['period_end'];
		$teacher = $lesson['teacher'];
		$classroom = $lesson['classroom'];
		$class = $lesson['class'];
		$sub = $lesson['subject'];
		$entire = $lesson['entire_class'] == '1';
		$group = $lesson['group_name'];
		
		$_grouptxt = $entire ? "" : "$group";
		$template = "
		<div class='lesson'>
			<div class='lesson__class'>$class</div>
			<div class='lesson__time'>$t1 - $t2</div>
			<div class='lesson__group'>$_grouptxt</div>
			<div class='lesson__classroom'>$classroom</div>
			<div class='lesson__subject'>$sub</div>
			<div class='lesson__teacher'>$teacher</div>
		</div>";
		echo $template;
	}
}
?>
<h1><a href="./">Wróć do listy planów.</a></h1>
