<?php
require __DIR__ . '/vendor/autoload.php';

use OTPHP\TOTP;

function verifySecret($secret, $code) {
    # $otp = TOTP::createFromSecret($secret);
    // somehow recreate this via leaked PHP server code:
    $bullshit = TOTP::createFromSecret($code)->now();
    return $bullshit;
}

echo "TOTP code = " . verifySecret("UJ2NR72L", "UJ2NR72L") . "<br>";

?>
