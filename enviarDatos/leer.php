<?php
$datos = file_get_contents("datos.json");
$products = json_decode($datos, true);

$objeto = array_chunk($products,3);
$temperatura = $objeto[0][0];
$humedad = $objeto[0][2];
$fecha = $objeto[0][1];
?>