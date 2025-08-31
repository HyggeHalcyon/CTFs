<?php

if (isset($_POST["submit"])) {

    if (!isset($_FILES['imageFile']) || $_FILES['imageFile']['error'] !== UPLOAD_ERR_OK) {
        
        switch ($_FILES['imageFile']['error'] ?? UPLOAD_ERR_NO_FILE) {
            case UPLOAD_ERR_INI_SIZE:
            case UPLOAD_ERR_FORM_SIZE:
                $message = "Error: The uploaded file exceeds the 1MB size limit.";
                break;
            case UPLOAD_ERR_NO_FILE:
                $message = "Error: No file was selected for upload.";
                break;
            default:
                $message = "Error: A server-side error occurred during upload.";
        }
        header("Location: index.php?message=" . urlencode($message));
        exit();
    }
    
    $uploadDir = "uploads/";
    $fileName = basename($_FILES["imageFile"]["name"]);
    $uploadPath = $uploadDir . $fileName;
    $fileType = strtolower(pathinfo($uploadPath, PATHINFO_EXTENSION));
    $checksumPath = $uploadPath . '.txt';

    if (move_uploaded_file($_FILES["imageFile"]["tmp_name"], $uploadPath)) {

        // check virus
        $escapedPath = escapeshellarg($uploadPath);
        $rulesPath = '/etc/yara/rules/virus_rules.yar';
        $command = "yara " . $rulesPath . " " . $escapedPath;
        exec($command, $output, $returnCode);

        $content = file_get_contents($uploadPath);
        $hash = hash('sha256', $content);

        $isImage = getimagesize($uploadPath);
        $allowedTypes = array('jpg', 'jpeg', 'png');

        if (($isImage === false || !in_array($fileType, $allowedTypes)) && !$outputCode[0]) {
            unlink($uploadPath);
            $message = "Error: Invalid file type.";
        } else{
            file_put_contents($checksumPath, $hash);
            $message = "Success: File uploaded.";
        }

    } else {
        $message = "Error: There was a problem with the upload.";
    }
    header("Location: index.php?message=" . urlencode($message));
    exit();
} else {
    header("Location: index.php");
    exit();
}

?>
