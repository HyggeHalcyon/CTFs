<!DOCTYPE html>
<html>
<body>
<h1>Simple Calculator</h1>
<p>Solve all your problems here!</p>

<form action="/solve.php" method="post">
<label for="mathex">Math Expression:</label>
<input type="text" id="mathex" name="mathex">
<input type="submit">
</form>

<?php
function format_error($expre) {
    return "<p><b>Format error:</b> the input is given in wrong format!</p>";
}

function opp_error($expre) {
    return "<p><b>Operator error:</b> operator for ".$expre." is not available!</p>";
}

function sum($a, $b) {
    $result = strval(intval($a) + intval($b));
    return "<p><b>Result:</b><br>".$a." + ".$b." = ".$result."</p>";
}

function sub($a, $b) {
    $result = strval(intval($a) - intval($b));
    return "<p><b>Result:</b><br>".$a." - ".$b." = ".$result."</p>";
}

function mul($a, $b) {
    $result = strval(intval($a) * intval($b));
    return "<p><b>Result:</b><br>".$a." * ".$b." = ".$result."</p>";
}

function div($a, $b) {
    $result = strval(intval($a) / intval($b));
    return "<p><b>Result:</b><br>".$a." / ".$b." = ".$result."</p>";
}

function evalit($code) {
    return eval($code);
}

if ($_SERVER["REQUEST_METHOD"] == "GET") {
    if (!empty($_GET["input"])) {
        $decoded = base64_decode($_GET["input"]);
        $out = unserialize($decoded);
        if ($out[2] != null) {
            $view = $out[0]($out[1], $out[2]);
            echo $view;
        }
        else {
            $view = $out[0]($out[1]);
            echo $view;
        }
    }
}

?>

</body>
</html>