<?php

error_reporting(E_ALL);
ini_set('error_reporting', E_ALL);
ini_set("display_errors", 1);

// Use these constants IV and Salt.
$salt = implode(array_map("chr", array(107, -50, -85, 33, -33, -115, -116, 37, 39, 33, 33, -74, 117, -115, 20, -35, 74, -96, -4, -121)));
$iv = implode(array_map("chr", array(-75, 16, 92, 14, 117, 74, -96, -4, -121, 38, 105, -65, 55, 24, 118, -45)));

$iterations = 1024;
$keyLength = 16;
$key = "<SSO KEY here>";
$key = hash_pbkdf2("sha1", $key, $salt, $iterations, $keyLength, true);
// Your content filter payload
$data = 'contentFilters=[{"fieldName":"Company","values":["Tesla"],"operator":"Equals"},{"fieldName":"$c9_siteId$","values":["@S.Building6"],"operator":"Equals"},{"fieldName":"$c9_equipId$","values":["@S.Building6.Equip1"],"operator":"Equals"},{"fieldName":"$c9_pointId$","values":["@S.Building6.Equip1.Point1"],"operator":"Equals"}]';
$data = pkcs5_pad($data);

$encryptedData = openssl_encrypt($data, 'AES-128-CBC', $key, OPENSSL_RAW_DATA, $iv);
$base64EncodedData = base64_encode($encryptedData);
$secureHash = str_replace("/", "___", $base64EncodedData);
echo "Secure Hash: ".$secureHash;

function pkcs5_pad($data) {
    $blockSize = 16;
    $pad = $blockSize - (strlen($data) % $blockSize);
    return $data . str_repeat(chr($pad), $pad);
}
