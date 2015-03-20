# -*- coding: utf-8 -*-

# Scrapy settings for mls_shots project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'mls_shots'

SPIDER_MODULES = ['mls_shots.spiders']
NEWSPIDER_MODULE = 'mls_shots.spiders'
ITEM_PIPELINES = {
    'mls_shots.pipelines.DuplicatesPipeline': 100,
}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'mls_shots (+http://www.yourdomain.com)'
