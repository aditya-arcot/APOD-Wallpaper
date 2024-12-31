'''Update MacOS desktop wallpaper with NASA APOD'''


from datetime import date, datetime
import os
import urllib
import nasapy
from appscript import app, mactypes
import progressbar


FEED_URL = "http://apod.nasa.gov/apod/"
WALLPAPER_DIR = "images"


class ProgressBar():
    def __init__(self):
        self.bar = None

    def __call__(self, block_num, block_size, total_size):
        if not self.bar:
            self.bar = progressbar.ProgressBar(maxval = total_size)
            self.bar.start()

        completed = block_num * block_size
        if completed < total_size:
            self.bar.update(completed)
        else:
            self.bar.finish()


def main():
    '''
    Get picture url
    Download file if not already downloaded
    Set desktop wallpaper
    '''

    today = str(date.today())

    if (not os.path.isdir(WALLPAPER_DIR)):
        os.mkdir(WALLPAPER_DIR)
    else:
        files = os.listdir(WALLPAPER_DIR)
        for file in files:
            if today in file:
                print('picture already downloaded')
                set_desktop_background(os.path.join(WALLPAPER_DIR, file))
                return

    print('picture not found, downloading...')
    url = get_pic_url()

    if url == None:
        print('skipping')
        return
        
    filename = today + '.' + url.split('.')[-1]
    path = os.path.join(WALLPAPER_DIR, filename)
    urllib.request.urlretrieve(url, path, ProgressBar())
    set_desktop_background(path)


def get_pic_url():
    '''Return url of current pic'''

    key = os.getenv("NASA_KEY")
    if (not key):
        print('No API key found')
        return None

    nasa = nasapy.Nasa(key = key)
    pic = nasa.picture_of_the_day()

    if not 'hdurl' in pic.keys():
        print('no picture, only video for today')
        return None

    return pic['hdurl']


def set_desktop_background(path):
    '''Run script to update wallpaper'''
    print('setting wallpaper')
    app('Finder').desktop_picture.set(mactypes.File(path))
    print()


print(datetime.now())
main()
print()
