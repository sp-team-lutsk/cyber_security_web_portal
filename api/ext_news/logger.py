import os
import logging as log




class Logger:
    BASE_DIR = '/opt/docker_polls_group/api/'
    conf = {
    'version': 1,
    'disable_existing_loggers': False,}
    filters = {'filters': {

        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },}
              }

    formatter = {'formatters': {
        'debug': {
            'format' : ('[{levelname} in ext_news]\n{message}'),
            'style': '{',},

        'file': {
            'format' : ('[{levelname} in ext_news]\nat {asctime}: {message} ') ,
            'style': '{',},},
                }
    
    handlers = {'handlers': {
         'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'log.log'),
            'formatter':'file',},
         'debug': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'debug',},}
               }

    loggers = {'loggers':{
            'django':{
            'handlers': ['debug','file'],
            'level': 'DEBUG',
            'propagate': True,},
            }
             }

    def __init__(self):
        self.conf.update(self.filters)
        self.conf.update(self.formatter)
        self.conf.update(self.handlers)
        self.conf.update(self.loggers) 
        log.config.dictConfig(self.conf)
        return None

