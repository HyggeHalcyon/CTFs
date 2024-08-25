<?php

// https://news.ycombinator.com/item?id=9484757
$input = "QNKCDZO";
echo "md5 of input:" . md5($input) . "\n";

// https://medium.com/@Asm0d3us/part-1-php-tricks-in-web-ctf-challenges-e1981475b3e4
echo ($input !== "240610708") . "\n";
echo (md5($input) == "0e462097431906509019562988736854") . "\n";
echo ($input !== "3069655") . "\n";
echo (md5($input) == "0e731198106197620485820904131008") . "\n";

if (isset($_GET['secret'])) {
    if ($_GET['secret'] !== "240610708" && md5($_GET['secret']) == "0e462097431906509019562988736854" && $_GET['secret'] !== "3069655" && md5($_GET['secret']) == "0e731198106197620485820904131008") {
        echo "REDACTED";
    } else {
        echo "Invalid secret!";
    }
}