<?php
$servername = "localhost";
$username = "USER";
$password = "PASS";
$dbname = "NAME"; 
$conn = mysqli_connect($servername, $username, $password, $dbname); 

if (mysqli_connect_errno()) {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  die();
} else {
  echo "SUCCESSFULLY CONNECTED TO THE DATABASE !<br>";
}

// test query to run:
$query = "SELECT * FROM tbl_application_form";
$data = mysqli_query($conn, $query);

if ($data) {
  // Fetch and display each row
  while ($row = mysqli_fetch_assoc($data)) {
    // Print out each column for the row
    foreach ($row as $column => $value) {
      echo "$column: $value<br>";
    }
    echo "<br><br><br>"; // Add a break between rows
  }
} else {
  echo "Error with query: " . mysqli_error($conn);
}

mysqli_close($conn);
?>
