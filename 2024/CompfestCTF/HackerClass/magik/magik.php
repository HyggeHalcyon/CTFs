<html>
    <body>
        <div>
            <?php 
            if (isset($_GET['secret'])) {
                if ($_GET['secret'] !== "240610708" && md5($_GET['secret']) == "0e462097431906509019562988736854" && $_GET['secret'] !== "3069655" && md5($_GET['secret']) == "0e731198106197620485820904131008") {
                    echo "REDACTED";
                } else {
                    echo "Invalid secret!";
                }
            } else {
                echo "Please specify secret in the GET parameter!";
            }
            ?>
        </div>
    </body>

    <style>
        div {
            display: flex;
            align-items: center; /* vertically center the div element */
            justify-content: center; /* horizontally center the div element */
            width: 100%; 
            height: 100%; 
            text-align: center;
            margin: 0 auto; /* center the div element horizontally */
        }
    </style>
</html>