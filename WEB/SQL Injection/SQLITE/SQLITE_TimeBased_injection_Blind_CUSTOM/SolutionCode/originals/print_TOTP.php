<?php
require __DIR__ . '/vendor/autoload.php';

use OTPHP\TOTP;

function verifySecret($secret, $code) {
    # $otp = TOTP::createFromSecret($secret);
    // somehow recreate this via leaked PHP server code:
    $bullshit = TOTP::createFromSecret($code)->now();
    return $bullshit;
}

echo "TOTP code = " . verifySecret("{{LEAKED_TOTP_SECRET_HERE}}", "{{LEAKED_TOTP_SECRET_HERE}}") . "<br>";

?>
