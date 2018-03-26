#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tryint to parse Hangouts messages into a reasonable text log

Hangouts JSON fields for conversation metadata:

Hangouts JSON fields for each message:
   {'advances_sort_timestamp': True,
    'chat_message': 
        {'message_content': 
            {'segment': 
                [{'text': "Hello, this is the message text", 
                  'type': 'TEXT'}]
            }
        },
    'conversation_id': {'id': 'UgzeAzn7fABv6JXXXXXXXXX'},
    'delivery_medium': {'medium_type': 'BABEL_MEDIUM'},
    'event_id': '80-HmPoMsc980-XXXXXX',
    'event_otr': 'ON_THE_RECORD',
    'event_type': 'REGULAR_CHAT_MESSAGE',
    'event_version': '14334690XXXXXXXX',
    'self_event_state': 
        {'client_generated_id': '31149098182XXXXXXXX',
         'notification_level': 'RING',
         'user_id': 
             {'chat_id': '117191193XXXXXXXXX',
              'gaia_id': '117191193XXXXXXXXX'
             }
        },
    'sender_id': 
        {'chat_id': '117191193XXXXXXXXX',
         'gaia_id': '117191193XXXXXXXXX'
        },
    'timestamp': '1433469000492727'
   }

IRC format:
    [MM.DD.YYYY HH:MM:SS] <Name> message text appears 

"""

import os
import json
import pandas as pd
from datetime import datetime

input_file = os.path.join('data_private', 'Hangouts.json')
df = pd.read_json(input_file)
a = dict(df.iloc[3][0])
print(json.dumps(a, sort_keys=True, indent=2))

print(datetime.fromtimestamp(1433465143911140/1000000).strftime('[%m/%d/%Y %H:%M:%S]'))
