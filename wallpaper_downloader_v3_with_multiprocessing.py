#import libraries that we are going to use
from urllib import request
from bs4 import BeautifulSoup
import multiprocessing
import os

#enter the url of the categories of wallpapers that you want to download from Wallpaperswide.com
seed = 'http://wallpaperswide.com/abstract-desktop-wallpapers'

# create a list containing a list of the number of pages of the category you want to download. Every page has 18 images

pages = []
pages.append(seed)

#the master function first is in charge of getting all the links from the pages and assigning different 'workers' or computer cores to download each image.
# this makes our programme run faster, as different cores are concurrently downloading images, not just one process
def master():
    #create a queue in which we will store the assignments to download images
    input_queue = multiprocessing.Queue()
    workers = []
    image_urls = []

# this means we only explore page 1 - 4. to explore more pages (download more images), change 5 to something else, as long as that category on the website has that many pages
    for i in range(2, 4):
        pages.append(seed+'/page/' + str(i))

        # find all the image links in the html we received from the pages 
    for page in pages:
        resp = request.urlopen(page).read()
        soup = BeautifulSoup(resp, 'html.parser')
        for link in soup.find_all('a', title=True, itemprop=True):
            link = 'http://wallpaperswide.com' + link.get('href')
            link = link.replace("wallpapers.html", "wallpaper-1920x1080.jpg").replace(".com/", ".com/download/")
            image_urls.append(link)

    
    #Distribute work by adding all the image links to a queue, from which each core will get the link and download the image
    for url in image_urls:
        input_queue.put(url)
    # create as many "worker processes" to run on as many cores as you have on your CPU
    for i in range(os.cpu_count()):
        process = multiprocessing.Process(target=worker, args=(input_queue,))
        workers.append(process)
        process.start()
    
    #Ask workers to quit
    for w in workers:
        input_queue.put(None)

    # Wait for workers to quit
    for w in workers:
        w.join()

# Worker function that downloads an image from a link for us
def worker(input_queue):
    while True:
        image_url = input_queue.get()

        if image_url is None:
            break
        image_name = image_url.replace("http://wallpaperswide.com/download/", "")
        image_file = open('images/'+ image_name,"wb")

        try:
            resp = request.urlopen(image_url)
            image_file.write(resp.read())
            print(f"Success downloading {image_name}")
        except:
            print(f"Error occured while downloading image: {image}")
        finally:
            image_file.close()

if __name__ == "__main__":
    master()