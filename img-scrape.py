# This script is a way to quickly download all the thumbnail images for pages at antievictionmap.com as we migrate
# the site to a new format

# The script takes one argument: the word after the main URL, so "evictions" or "affordability." To use the script, you would:
# 1. use the command line to navigate to the directory on your computer where the script lives
# 2. type `python img-scrape.py [page you want images from]`, i.e. python img-scrape.py affordability

# The script will create a directory with the argument you typed in and fill it with thumbnails from that page.
# It will also create a file called 'data.txt' with image name, project title, and year for each image. This is helpful
# for keeping everything organized.

import requests, os, bs4, sys

__dirname = sys.argv[1]
url = 'https://www.antievictionmap.com/' + __dirname
os.makedirs(__dirname)

print('Downloading page %s...' % url)
res = requests.get(url)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "html5lib")

imgs = []
titles = []
years = []
links = []

def getImage():
  imgElem = soup.select('img[data-src]')
  for elem in imgElem:
    try:
      imgUrl = elem.get('data-src')
      if os.path.basename(imgUrl):
        imgPath = os.path.basename(imgUrl)
        imgs.append(imgPath)
        getYearTag(imgPath)
        res = requests.get(imgUrl)
        res.raise_for_status()
        imageFile = open(os.path.join(__dirname, imgPath), 'wb')
        for chunk in res.iter_content(100000):
          imageFile.write(chunk)
        imageFile.close()
      else:
        imgs.append('No image path')
        years.append('No year')
        print 'No image path; no year because no image path'
    except IOError:
      imgs.append('No image')
      years.append('No year')
      print 'No image; no year because no image path'
      continue

# Pass in an an image path like 'Screen+Shot+2015-09-25+at+4.01.49+PM.png'
# Get the year if it exists and append to the 'years' list
def getYearTag(imgPath):
  try:
    if imgPath[12] == unicode('2'):
      years.append(imgPath[12:16])
    else: 
      years.append('No year available')
      print ('No year available')
  except IndexError:
    years.append('No year available')
    print 'No year available'

# Get the project title
def getTitle():
  projects = soup.select('.project-title > h2')
  for project in projects:
      title = project.getText()
      titles.append(title)

# Get project href
def getProjectLink():
  hrefs = soup.select('a[data-dynamic-load]')
  for href in hrefs:
      link = href.get('href')
      links.append('www.antievictionmap.com' + link)

# Create a file for cross-checking
def createIndex():
  index = range(len(titles))
  print len(index)
  print len(imgs)
  print len(titles)
  print len(links)
  print len(years)
  with open(os.path.join(__dirname, 'data.txt'), 'w') as projectFile:
    for i in index:
      projectFile.write("Image path: {}\n Project title: {}\n Project link: {}\n Year: {}\n\n".format(imgs[i], titles[i], links[i], years[i]))
    projectFile.close()

getImage()
getTitle()
getProjectLink()
createIndex()
