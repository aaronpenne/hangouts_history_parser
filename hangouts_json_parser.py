# -*- coding: utf-8 -*-
"""
Trying to parse Hangouts messages into a reasonable text log

Author: Aaron Penne
Created: 2018-03-27

Developed with:
    Python 3.6
    Windows 10
"""

import os
import json
from datetime import datetime

input_file = os.path.join('data_private', 'Hangouts.json')
output_dir = os.path.relpath('output')
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
output_file = os.path.join(output_dir, 'Hangouts')
    
# With json module
with open(input_file, 'r', encoding="utf8") as f:
    data = json.load(f)

num_conversations = len(data['conversations'])


for i in range(num_conversations):
    participant = {}
    timestamp = ''
    name = ''
    message = ''
    
    
    with open(os.path.join(output_dir, 'Hangouts_{:03}.txt'.format(i)), 'a+') as f:
    
        # Extract info from metadata
        conversation = data['conversations'][i]['conversation']['conversation']
        num_participants = len(conversation['participant_data'])
        for j in range(num_participants):
            participant[j] = {}
            # Get participant name
            try:
                participant[j]['name'] = conversation['participant_data'][j]['fallback_name']
            except:
                participant[j]['name'] = 'Anonymous'
            
            # Get participant ID
            try:
                participant[j]['id'] = conversation['participant_data'][j]['id']['chat_id']
            except:
                participant[j]['id'] = 'Anon_ID'
                
        # Extract info from messages
        events = data['conversations'][i]['events']
        num_events = len(events)
        for j in range(num_events):
            try:
                # Just grab text for now # FIXME add more?
                if events[j]['chat_message']['message_content']['segment'][0]['type'] == 'TEXT':
               
                    timestamp = int(events[j]['timestamp'])/1000000
                    timestamp = datetime.fromtimestamp(timestamp).strftime('%m/%d/%Y %H:%M:%S')
                    name = events[j]['sender_id']['chat_id']
                    
                    # FIXME Add support for more than one line (#include stdio.h, etc.)
                    message = events[j]['chat_message']['message_content']['segment'][0]['text'] 
            except:
                continue
            
            try:
                f.write('[{}] <{}> {}\n'.format(timestamp, name, message))
#                print('[{}] <{}> {}\n'.format(timestamp, name, message))
            except:
                continue

