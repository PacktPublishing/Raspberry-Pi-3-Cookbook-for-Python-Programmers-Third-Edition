<html>
<body>

Remove all the data in the table.
<br>
<?php
$db = new PDO("sqlite:/var/databases/datasite/mydatabase.db");
//SQL query
$strSQL = "DROP TABLE recordeddata";
//Excute the query
$response = $db->query($strSQL);

if ($response == 1)
{
  echo "Result: DELETED DATA";
}
else
{
  echo "Error: Ensure table exists and database directory is owned by www-data";
}

?>
<br><br>
Press button to return to data display.
<br>
<input type="button" onclick="location.href = 'show_data_lite.php';" value="Return">

</body>
</html>
