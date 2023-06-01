# AutoPhisherBeX

![image](https://github.com/TheBenox/AutoPhisherBeX/assets/133176367/0502a437-580d-424a-b248-dbc2804e022e)

ENGLISH:

AutoPhisher V1 - Allows you to clone a website by providing its URL. Download the HTML content and all the necessary resources, such as CSS, JavaScript, images and other linked files. The cloned website is saved in a folder named after the website.

The script uses the requests library to make HTTP requests and get the content of the web page. It then uses BeautifulSoup to parse the HTML content and find the necessary resources. Resources are downloaded using the requests library and saved to the cloned website folder.

The script also makes some modifications to the cloned HTML, such as disabling links and adding a post.php file to the found forms. The post.php file captures the data submitted through the form and saves it to a JSON file in the logs folder.

After the cloning is complete, the script opens the cloned website in the user's default web browser. An option is also provided to publish the cloned website using the serveo.net service, thus allowing the cloned website to be accessed online.

Important Note: This script is provided for educational and learning purposes only. Improper or unauthorized use of this script to clone websites without the permission of the website owner is illegal. The author [BenoX] is not responsible for any misuse or damage caused by the use of this script.

ESPAÑOL: 

AutoPhisher V1 - Permite clonar un sitio web proporcionando su URL. Descarga el contenido HTML y todos los recursos necesarios, como CSS, JavaScript, imágenes y otros archivos vinculados. El sitio web clonado se guarda en una carpeta con el nombre del sitio web.

El script utiliza la biblioteca requests para realizar solicitudes HTTP y obtener el contenido de la página web. Luego, utiliza BeautifulSoup para analizar el contenido HTML y encontrar los recursos necesarios. Los recursos se descargan utilizando la biblioteca requests y se guardan en la carpeta del sitio web clonado.

El script también realiza algunas modificaciones en el HTML clonado, como desactivar los enlaces y agregar un archivo post.php a los formularios encontrados. El archivo post.php captura los datos enviados a través del formulario y los guarda en un archivo JSON en la carpeta de registros.

Una vez completada la clonación, el script abre el sitio web clonado en el navegador web predeterminado del usuario. También se proporciona la opción de publicar el sitio web clonado utilizando el servicio serveo.net, lo que permite acceder al sitio web clonado en línea.

Nota importante: Este script se proporciona con fines educativos y de aprendizaje solamente. El uso indebido o no autorizado de este script para clonar sitios web sin el permiso del propietario del sitio web es ilegal. El autor [BenoX] no se hace responsable de ningún mal uso o daño causado por el uso de este script.

MANUAL DE INSTALACION: 

#########################
Instalación en Linux:
#########################
Abre una terminal en tu sistema Linux.

Clona el repositorio de AutoPhisherBeX ejecutando el siguiente comando:
git clone https://github.com/TheBenox/AutoPhisherBeX.git

Accede al directorio del proyecto:
cd AutoPhisherBeX

Ejecuta el Script: 
python autophisherbex.py

#########################
Instalación en Windows:
#########################
Descarga el repositorio de AutoPhisherBeX desde el siguiente enlace: https://github.com/TheBenox/AutoPhisherBeX/archive/refs/heads/main.zip
Extrae el archivo ZIP descargado en una ubicación deseada en tu sistema.

Abre una ventana de comandos (CMD) en Windows.
Navega hasta la ubicación donde extrajiste el archivo ZIP de AutoPhisherBeX utilizando el comando cd. Por ejemplo:

cd C:\ruta\hasta\AutoPhisherBeX-main

Ejecuta el Script: 
python autophisherbex.py
