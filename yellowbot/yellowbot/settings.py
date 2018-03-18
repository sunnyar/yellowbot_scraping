# -*- coding: utf-8 -*-

# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'yellowbot'

SPIDER_MODULES = ['yellowbot.spiders']
NEWSPIDER_MODULE = 'yellowbot.spiders'

LOG_LEVEL = 'INFO'

AUTOTHROTTLE_ENABLED = True

AUTOTHROTTLE_DEBUG = True

HTTPERROR_ALLOW_ALL = True

ROBOTSTXT_OBEY = True


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tutorial (+http://www.yourdomain.com)'
