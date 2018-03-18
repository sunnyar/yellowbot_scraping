import os
import sys
import re
import time

with open('categories.txt', 'r') as fp :

    categories = fp.readlines()
    base_dir = '/home/sunny/yellowbot/'
    os.chdir(base_dir)

    for line in categories :
        category = line.strip()
        new_cat  = category.replace(' ', '+').replace('&', '%26').replace(':', '%3A').replace(',', '%2C')
        new_cat_name = re.sub('[^A-Za-z]+', '_', new_cat.lower())
        category_dir = '%s' % (new_cat_name)

        if not os.path.exists(category_dir) :
            os.mkdir(category_dir)
            os.popen('scrapy crawl yellowbot -a category="{0}" -a city="Tulsa" -a state="OK" -o {1}/items_tulsa.xml'.format(new_cat, category_dir))
            os.popen('scrapy crawl yellowbot -a category="{0}" -a city="Erie" -a state="PA" -o {1}/items_erie.xml'.format(new_cat, category_dir))
