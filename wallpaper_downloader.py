#import libraries that we are going to use
from urllib import request
from bs4 import BeautifulSoup as bs

#enter the url of the categories of wallpapers that you want to download from Wallpaperswide.com
url = 'http://wallpaperswide.com/abstract-desktop-wallpapers.html'

# list to store the links
links = []

# send a request to the website and store its html content in a resp variable
resp = request.urlopen(url).read()

# initialize BeautifulSoup with the html content
soup = bs(resp, 'html.parser')

# find all the image links in the html we received from the website 
for link in soup.find_all("a", title=True, itemprop = True):
    links.append('http://wallpaperswide.com'+ link.get('href'))

# create list containing image download links from the links we stored
image_links = [link.replace("wallpapers.html", "wallpaper-1920x1080.jpg").
               replace(".com/", ".com/download/") 
               for link in links]

# download the images from the front page
for image in image_links:
    image_file = open("images/" + image.replace("http://wallpaperswide.com/download/", ""), "wb")

    try:
        response = request.urlopen(image)
        image_file.write(response.read())
        print("Success!")
    except:
        print(f"Error occured while downloading image: {image}")
    finally:
        image_file.close()
