import os
import logging as log

BASE_DIR = '/opt/docker_polls_group/api/authentication'

conf = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {

        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },

    },
    'formatters': {

        'views': {
            'format' : ('[{levelname} in views]\n{message} ') ,
            'style': '{',
        },

        'file': {
            'format' : '[{levelname} in ]\n{message} ' ,
            'style': '{',
        },
         

    },
     'handlers': {
         
         'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'log.log'),
            'formatter':'views'
,
        },
         'debug': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'views',
        },
    },
  
        'loggers':{

            'django':{
            'handlers': ['debug','file'],
            'level': 'DEBUG',
            'propagate': True,
            },

            },
        }

log.config.dictConfig(conf)
