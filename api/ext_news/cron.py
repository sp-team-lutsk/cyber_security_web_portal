from utils.views import news_subscription
from parsing import main

def CronMailing():
    news_subscription()

def CronParse():
    main()
