<!DOCTYPE html>
<html lang="es-ES">
<head>
  <meta charset="UTF-8">
  <title>Document</title>    
    <script>
    window.onload=function(){
                // Una vez cargada la página, el formulario se enviara automáticamente.
		document.forms["form1"].submit();
    }
    </script>
</head>
<body>
    <?php
    include 'leer.php';
    ?>
    <form id="form1" name="form1" action="dirección de envio" method="POST">
        <fieldset>
            <legend><strong>temperatura</strong></legend>          
            <input type="text" name="temperatura" value="<?php echo $temperatura ?>" >
        </fieldset>
        <fieldset>
            <legend><strong>humedad</strong></legend>          
            <input type="text" name="humedad" value="<?php echo $humedad ?>" >
        </fieldset>
        <fieldset>
            <legend><strong>fecha</strong></legend>          
            <input type="text" name="fecha" value="<?php echo $fecha ?>">
        </fieldset>
        <div align="center">
        <input name="enviar" type="submit" value="enviar"/>
      </div>
    </form>
</body>
</html>