from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from urllib import request
import requests
import io
import base64
import PIL.Image
import os

def search_an_image(russian, finnish, img_fold_path):
    # Set up chrome for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (operate without a graphical user interface)
    chrome_options.add_argument("--disable-gpu")  # Graphics Processing Unit
    # chrome_options.add_argument("--no-sandbox") # Security risk to have this disabled...
    chrome_options.add_argument(
        "--disable-dev-shm-usage")  # prevent Chrome from using /dev/shm (shared memory) on Linux systems

    # Initialize the Chrome webdriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Perform a Google Image search
    search_url = f"https://www.google.com/search?tbm=isch&q={russian}"  #isch: image search
    driver.get(search_url)

    # Find the first img element
    try:
        print("starting an image search")
        first_image_holder = driver.find_element(By.CSS_SELECTOR, "q1MG4e mNsIhb")
        print("Image holder found")
        first_image = first_image_holder.find_element(By.TAG_NAME, "img")
        print("Image found")
        image_url = first_image.get_attribute("src")

        # Check if the URL is valid and not a base64 string
        if image_url.startswith('http') or image_url.startswith('https'):
            # Download the image
            # response = requests.get(image_url)
            image_content = requests.get(image_url).content
            image_file = io.BytesIO(image_content)
            image = PIL.Image.open(image_file)

            # Convert to RGB if necessary (not strictly required for PNG, but can be useful)
            if image.mode not in ('RGB', 'RGBA'):
                image = image.convert('RGBA')  # Convert to RGBA to retain transparency if needed

            file_name = finnish + ".png"
            file_path = os.path.join("Images", file_name)

            with open(file_path, 'wb') as file:
                image.save(file_path, "PNG")
        elif image_url.startswith('data:image'):
            # Handle base64 encoded image
            print("Found a base64 image")
            image_data = image_url.split(',')[1]
            image_content = base64.b64decode(image_data)
            image_file = io.BytesIO(image_content)
            image = PIL.Image.open(image_file)
            file_name = finnish + ".png"
            file_path = os.path.join(img_fold_path, file_name)
            with open(file_path, 'wb') as file:
                image.save(file, "PNG")
        else:
            print("Unsupported image URL format")

    except NoSuchElementException as e:
        print(f"HTML element was not found: {e}")
    finally:
        print("process done")
        driver.quit()

def test_connection():
    try:
        print(request.urlopen('https://www.google.com/', timeout=5))
        print("Connection found")
        return True
    except:
        print("No internet connection")
        return False
