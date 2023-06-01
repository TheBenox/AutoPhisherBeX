# AutoPhisherBeX

![image](https://github.com/TheBenox/AutoPhisherBeX/assets/133176367/0502a437-580d-424a-b248-dbc2804e022e)


AutoPhisher V1 - Permite clonar un sitio web proporcionando su URL. Descarga el contenido HTML y todos los recursos necesarios, como CSS, JavaScript, imágenes y otros archivos vinculados. El sitio web clonado se guarda en una carpeta con el nombre del sitio web.

El script utiliza la biblioteca requests para realizar solicitudes HTTP y obtener el contenido de la página web. Luego, utiliza BeautifulSoup para analizar el contenido HTML y encontrar los recursos necesarios. Los recursos se descargan utilizando la biblioteca requests y se guardan en la carpeta del sitio web clonado.

El script también realiza algunas modificaciones en el HTML clonado, como desactivar los enlaces y agregar un archivo post.php a los formularios encontrados. El archivo post.php captura los datos enviados a través del formulario y los guarda en un archivo JSON en la carpeta de registros.

Una vez completada la clonación, el script abre el sitio web clonado en el navegador web predeterminado del usuario. También se proporciona la opción de publicar el sitio web clonado utilizando el servicio serveo.net, lo que permite acceder al sitio web clonado en línea.

Nota importante: Este script se proporciona con fines educativos y de aprendizaje solamente. El uso indebido o no autorizado de este script para clonar sitios web sin el permiso del propietario del sitio web es ilegal. El autor [BenoX] no se hace responsable de ningún mal uso o daño causado por el uso de este script.
