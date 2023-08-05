<?php
session_start();
require_once "assets/bulletproof.php";

function isAuthenticated() {
  return json_encode(isset($_SESSION['user']));
}

function returnUsername() {
  return "\"" . $_SESSION['user'] . "\"";
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $image = new Bulletproof\Image($_FILES);
  if($image["toConvert"]) {
    $image->setLocation("/var/www/pilgrimage.htb/tmp");
    $image->setSize(100, 4000000);
    $image->setMime(array('png','jpeg'));
    $upload = $image->upload();
    if($upload) {
      $mime = ".png";
      $imagePath = $upload->getFullPath();
      if(mime_content_type($imagePath) === "image/jpeg") {
        $mime = ".jpeg";
      }
      $newname = uniqid();
      exec("/var/www/pilgrimage.htb/magick convert /var/www/pilgrimage.htb/tmp/" . $upload->getName() . $mime . " -resize 50% /var/www/pilgrimage.htb/shrunk/" . $newname . $mime);
      unlink($upload->getFullPath());
      $upload_path = "http://pilgrimage.htb/shrunk/" . $newname . $mime;
      if(isset($_SESSION['user'])) {
        $db = new PDO('sqlite:/var/db/pilgrimage');
        $stmt = $db->prepare("INSERT INTO `images` (url,original,username) VALUES (?,?,?)");
        $stmt->execute(array($upload_path,$_FILES["toConvert"]["name"],$_SESSION['user']));
      }
      header("Location: /?message=" . $upload_path . "&status=success");
    }
    else {
      header("Location: /?message=Image shrink failed&status=fail");
    }
  }
  else {
    header("Location: /?message=Image shrink failed&status=fail");
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
                    <ul class="nav" id = "unauth-nav">
                        <li><a href="/" class="active">Home</a></li>
                        <li><a href="login.php">Login</a></li>
                        <li><a href="register.php">Register</a></li>
                    </ul>
                    <ul class="nav" id = "auth-nav">
                      <li style="border-right: 2px solid white;"><a>Hello, <span id = "username-nav"></span></a></li>
                        <li><a href="/" class="active">Home</a></li>
                        <li><a href="dashboard.php">Dashboard</a></li>
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
        <div class="col-lg-8">
          <h2>Save space and shrink it!</h2>
          <h4>A free online image shrinker. Create an account to save your images!</h4>
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
  <section id="section-1">
    <div class="content-slider">
      <input type="radio" id="banner1" class="sec-1-input" name="banner" style="display:none;" checked>
      <div class="slider">
        <div id="top-banner-1" class="banner">
          <div class="banner-inner-wrapper header-text">
            <div class="container">
              <div class="row">
                <div class="col-lg-12">
                  <div class="more-info">
                    <div class="row">
                      <form class="image-upload-form" enctype="multipart/form-data" method="POST" action="/">
                        <div class="col-lg-8 col-sm-8 col-8" style="padding-right: 20px;">
                          <div class="file-upload">
                            <div class="file-select">
                              <div class="file-select-button" id="fileName">Choose File</div>
                              <div class="file-select-name" id="noFile">No file chosen...</div> 
                              <input type="file" accept="image/png,image/jpeg" name="toConvert" id="chooseFile" required>
                            </div>
                          </div>
                        </div>
                        <div class="col-lg-4 col-sm-4 col-4">
                          <div class="main-button">
                            <input type="submit" value="Shrink" style="width:100%; text-align: center;">
                          </div>
                        </div>
                      </form>
                      <div id = "error-success" style="bottom: auto; top: 12.5px; padding: 10px;"></div>
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
    const isAuthenticated = <?php echo isAuthenticated(); ?>;
    if(isAuthenticated) {
      document.getElementById("unauth-nav").style.display="none";
      document.getElementById("auth-nav").style.display="flex";
      const username = <?php echo returnUsername(); ?>;
      document.getElementById("username-nav").innerText = username;
    }
    else {
      document.getElementById("unauth-nav").style.display="flex";
      document.getElementById("auth-nav").style.display="none";
    }
  </script>

  <script>
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    if(urlParams.has('message') && urlParams.has('status')) {
      document.getElementById("error-success").style.display = "block";
      if(urlParams.get('status') == 'fail') {
        document.getElementById("error-success").style.color = "red";
        document.getElementById("error-success").innerText = urlParams.get('message');
      }
      else {
        document.getElementById("error-success").style.color = "green";
        document.getElementById("error-success").innerHTML = "<a href='" + urlParams.get('message') + "'>" + urlParams.get('message') + "</a>";
      }
    }
  </script>

  </body>

</html>
