#import libraries that we are going to use
from urllib import request
from bs4 import BeautifulSoup

#enter the url of the categories of wallpapers that you want to download from Wallpaperswide.com

seed = 'http://wallpaperswide.com/abstract-desktop-wallpapers'

# create a list containing a list of the number of pages of the category you want to download. Every page has 18 images
pages = []
pages.append(seed)
# this means we only explore page 1 and 2. to explore more pages (download more images), change 3 to something else, as long as that category on the website has that many pages
for i in range(2, 3):
    pages.append(seed+'/page/' + str(i))
    
# download all the images on each page
for page in pages:
    links = []
    resp = request.urlopen(page).read()
    soup = BeautifulSoup(resp, 'html.parser')
    # find all the image links in the html we received from the page 
    for link in soup.find_all('a', title=True, itemprop=True):

        links.append('http://wallpaperswide.com' + link.get('href'))
    # create list containing image download links from the links we stored
    image_links = [link.replace("wallpapers.html", "wallpaper-1920x1080.jpg").
                   replace(".com/", ".com/download/") 
                   for link in links]
    # download the images from the  page
    for image in image_links:
        image_file = open('images/'+ image.replace("http://wallpaperswide.com/download/", ""),"wb")

        try:
            resp = request.urlopen(image)
            image_file.write(resp.read())
            print("Success!")
        except:
            print(f"Error occured while downloading image: {image}")
        finally:
            image_file.close()
