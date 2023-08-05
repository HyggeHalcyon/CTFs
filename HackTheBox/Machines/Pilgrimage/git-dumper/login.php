<?php
session_start();
if(isset($_SESSION['user'])) {
  header("Location: /dashboard.php");
  exit(0);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && $_POST['username'] && $_POST['password']) {
  $username = $_POST['username'];
  $password = $_POST['password'];

  $db = new PDO('sqlite:/var/db/pilgrimage');
  $stmt = $db->prepare("SELECT * FROM users WHERE username = ? and password = ?");
  $stmt->execute(array($username,$password));

  if($stmt->fetchAll()) {
    $_SESSION['user'] = $username;
    header("Location: /dashboard.php");
  }
  else {
    header("Location: /login.php?message=Login failed&status=fail");
  }
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

<body>

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
                        <li><a href="/">Home</a></li>
                        <li><a href="login.php" class="active">Login</a></li>
                        <li><a href="register.php">Register</a></li>
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
          <h2>Login</h2>
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
  <section id="section-1" style="height: 460px;">
    <div class="content-slider">
      <input type="radio" id="banner1" class="sec-1-input" name="banner" style="display:none;" checked>
      <div class="slider">
        <div id="top-banner-1" class="banner">
          <div class="banner-inner-wrapper header-text">
            <div class="container">
              <div class="row">
                <div class="col-lg-12">
                  <div class="more-info" style="bottom: 80px;">
                    <div class="row" style="padding:20px">
                      <div class="col-lg-12 col-sm-12 col-12">
                        <div class="form">
                          <div id = "error-success"></div>
                          <form class="login-form" method="POST" action="/login.php">
                            <input type="text" name="username" placeholder="Username"/>
                            <input type="password" name="password" placeholder="Password"/>
                            <div class="main-button">
                              <input type="submit" value="Login" style="width:100%; text-align: center; background-color: #22b3c1">
                            </div>
                          </form>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
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
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    if(urlParams.has('message') && urlParams.has('status')) {
      document.getElementById("error-success").style.display = "block";
      document.getElementById("error-success").innerText = urlParams.get('message');
      if(urlParams.get('status') == 'fail') {
        document.getElementById("error-success").style.color = "red";
      }
      else {
        document.getElementById("error-success").style.color = "green";
      }
    }
  </script>

  </body>

</html>
