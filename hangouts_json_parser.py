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
    
# With json module
with open(input_file, 'r', encoding="utf8") as f:
    data = json.load(f)

num_conversations = len(data['conversations'])


for i in range(num_conversations):
    participant = {}
    timestamp = ''
    name = ''
    message = ''
    

    
    # Extract info from metadata
    conversation = data['conversations'][i]['conversation']['conversation']
    num_participants = len(conversation['participant_data'])
    for participant_index in range(num_participants):
        # Get participant ID
        try:
            participant_id = conversation['participant_data'][participant_index]['id']['chat_id']
        except:
            participant_id = 'Anon_ID_{}'.format(participant_index)
        
        # Get participant name
        try:
            participant_name = conversation['participant_data'][participant_index]['fallback_name']
        except:
            participant_name = 'Anon_{}'.format(participant_index)
        
        if participant_name == 'Aaron Penne':
            participant_name = 'Me'
        participant[participant_id] = participant_name
                
    names = ''    
    for key in participant:
        names = '{} {}'.format(names, participant[key]) 
    output_file_log = os.path.join(output_dir, 'Hangouts {:03}{}.txt'.format(i, names))
    output_file_tsv = os.path.join(output_dir, 'Hangouts {:03}{}.tsv'.format(i, names))
    print(output_file_log)
    with open(output_file_log, 'w+') as f_log:
        with open(output_file_tsv, 'w+') as f_tsv:
        
            # Extract info from messages
            events = data['conversations'][i]['events']
            num_events = len(events)
            for j in range(num_events):
                try:           
                    timestamp = int(events[j]['timestamp'])/1000000
                    timestamp = datetime.fromtimestamp(timestamp).strftime('%m/%d/%Y %H:%M:%S')
                    name = participant[events[j]['sender_id']['chat_id']]
                    
                    segment = events[j]['chat_message']['message_content']['segment']
                    for k in range(len(segment)):
                        message = segment[k]['text'].replace('\n', ' ').replace('\t', ' ')
                        message_type = segment[k]['type']
                        if timestamp and name and message_type != 'LINE_BREAK':
                            f_log.write('[{}] <{}> {}\n'.format(timestamp, name, message))
                            f_tsv.write('{}\t{}\t{}\n'.format(timestamp, name, message))
    
                except:
                    continue
            
        

