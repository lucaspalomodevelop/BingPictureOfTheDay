import requests
import os
import subprocess
import re


# Function to get the URL of Bing's image of the day.
def get_bing_image_of_the_day_url():
    bing_api_url = (
        "http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US"
    )
    response = requests.get(bing_api_url)
    response.raise_for_status()
    image_info = response.json()["images"][0]
    image_url = "http://www.bing.com" + image_info["url"]
    return image_url


# Function to download and save the image to the current directory.
def download_image(image_url, image_path):
    response = requests.get(image_url)
    response.raise_for_status()
    with open(image_path, "wb") as file:
        file.write(response.content)
    print(f"Image saved as {image_path}")


# Function to set the image as desktop background.
def set_desktop_background(image_path):
    gsettings_command = [
        "gsettings",
        "set",
        "org.gnome.desktop.background",
        "picture-uri",
        f"file://{image_path}",
    ]
    exitcode = subprocess.run(gsettings_command)

    gsettings_command_dark = [
        "gsettings",
        "set",
        "org.gnome.desktop.background",
        "picture-uri-dark",
        f"file://{image_path}",
    ]
    exitcode_dark = subprocess.run(gsettings_command_dark)

    returncode = exitcode.returncode or exitcode_dark.returncode

    if returncode == 0:
        print("Desktop background set successfully.")
    else:
        print("Error setting desktop background.")
        print("Please set the desktop background manually.")



# Main program
def main():
    image_url = get_bing_image_of_the_day_url()
    image_name = re.search(r"OHR\.(.*?)_", image_url).group(1) + ".jpg"
    image_path = os.path.join(os.path.expanduser("~"), "Pictures", image_name)

    download_image(image_url, image_path)
    set_desktop_background(image_path)


if __name__ == "__main__":
    main()
