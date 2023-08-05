<?php
session_start();
if(!isset($_SESSION['user'])) {
  header("Location: /login.php");
  exit(0);
}

function returnUsername() {
  return "\"" . $_SESSION['user'] . "\"";
}

function fetchImages() {
  $username = $_SESSION['user'];
  $db = new PDO('sqlite:/var/db/pilgrimage');
  $stmt = $db->prepare("SELECT * FROM images WHERE username = ?");
  $stmt->execute(array($username));
  $allImages = $stmt->fetchAll(\PDO::FETCH_ASSOC);
  return json_encode($allImages);
}

?>
<!DOCTYPE html>
<html lang="en">

  <head>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">

    <title>Pilgrimage - Shrink Your Images</title>

    <!-- Bootstrap core CSS -->
    <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">

    <!-- Additional CSS Files -->
    <link rel="stylesheet" href="assets/css/fontawesome.css">
    <link rel="stylesheet" href="assets/css/templatemo-woox-travel.css">
    <link rel="stylesheet" href="assets/css/owl.css">
    <link rel="stylesheet" href="assets/css/animate.css">
    <link rel="stylesheet" href="https://unpkg.com/swiper@7/swiper-bundle.min.css"/>
    <link rel="stylesheet" href="assets/css/custom.css">
<!--

TemplateMo 580 Woox Travel

https://templatemo.com/tm-580-woox-travel

-->

  </head>

<body style = "background: url('assets/images/banner-04.jpg') no-repeat center center; background-size: cover; height: 900px;">

  <!-- ***** Preloader Start ***** -->
  <div id="js-preloader" class="js-preloader">
    <div class="preloader-inner">
      <span class="dot"></span>
      <div class="dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  </div>
  <!-- ***** Preloader End ***** -->

  <!-- ***** Header Area Start ***** -->
  <header class="header-area header-sticky">
    <div class="container">
        <div class="row">
            <div class="col-12">
                <nav class="main-nav">
                    <!-- ***** Logo Start ***** -->
                    <a href="/" class="logo">
                        <h3 class = "logo-text">Pilgrimage</h3>
                    </a>
                    <!-- ***** Logo End ***** -->
                    <!-- ***** Menu Start ***** -->
                    <ul class="nav">
                        <li style="border-right: 2px solid white;"><a>Hello, <span id = "username-nav"></span></a></li>
                        <li><a href="/">Home</a></li>
                        <li><a href="dashboard.php" class="active">Dashboard</a></li>
                        <li><a href="logout.php">Logout</a></li>
                    </ul>   
                    <a class='menu-trigger'>
                        <span>Menu</span>
                    </a>
                    <!-- ***** Menu End ***** -->
                </nav>
            </div>
        </div>
    </div>
  </header>
  <!-- ***** Header Area End ***** -->

  <div class="call-to-action">
    <div class="container">
      <div class="row">
        <div class="col-lg-12" style="text-align: center;">
          <h2>Dashboard</h2>
        </div>
      </div>
    </div>
  </div>
  <svg xmlns="http://www.w3.org/2000/svg" style="background:linear-gradient(#135,#fbc,#135)">
    <filter id="filter">
        <feTurbulence type="fractalNoise" baseFrequency=".005 0" numOctaves="5"/>
        <feDisplacementMap in="SourceAlpha" scale="99"/>
        <feColorMatrix values="0 0 0 0 .01
                               0 0 0 0 .02
                               0 0 0 0 .02
                               0 0 0 -1 1"/>
    </filter>
    <use href="#e" y="-100%" transform="scale(1 -1)" filter="blur(3px)"/>
    <ellipse id="e" cx="50%" rx="63%" ry="43%" filter="url(#filter)"/>
</svg>
  <!-- ***** Main Banner Area Start ***** -->
  <section id="section-1" style="height: auto; margin: 50px;">

  </section>
  <!-- ***** Main Banner Area End ***** -->

  <footer>
    <div class="container footercontainer">
      <div class="row">
        <div class="col-lg-12">
          <p>Copyright © 2022 Pilgrimage. Design: <a href="https://templatemo.com" target="_blank" title="free CSS templates">TemplateMo</a></p>
        </div>
      </div>
    </div>
  </footer>


  <!-- Scripts -->
  <!-- Bootstrap core JavaScript -->
  <script src="vendor/jquery/jquery.min.js"></script>
  <script src="vendor/bootstrap/js/bootstrap.min.js"></script>

  <script src="assets/js/isotope.min.js"></script>
  <script src="assets/js/tabs.js"></script>
  <script src="assets/js/popup.js"></script>
  <script src="assets/js/custom.js"></script>

  <script>
    const username = <?php echo returnUsername(); ?>;
    document.getElementById("username-nav").innerText = username;

    const allImages = <?php echo fetchImages(); ?>;
    var imageTable = "<table id=\"customers\"><tr><th>Original Image Name</th><th>Shrunken Image URL</th></tr>"
    for(let i = 0; i < allImages.length; i++) {
      imageTable = imageTable + "<tr><td>" + allImages[i]["original"] + "</td><td><a href ='" + allImages[i]["url"] + "'>" + allImages[i]["url"] + "</a></td></tr>"
    }
    imageTable = imageTable + "</table>"
    document.getElementById("section-1").innerHTML = imageTable;
  </script>

  </body>

</html>
