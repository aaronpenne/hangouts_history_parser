Hangouts History Parser
=======================

A tool to parse Google Hangouts history into IRC style text logs. This will allow for simpler analysis and easier visualizations.

Background
----------

Your Hangouts data can be downloaded from [Google Takeout](https://takeout.google.com/settings/takeout). All historical conversations are in JSON format with lots of nested miscellaneous/irrelevant data. The purpose of this tool is to separate different conversations and output them in a human-readable format that can be easily archived or analyzed.

Hangouts.json format
--------------------

Exploring the Hangouts.json file after importing into a Pandas DataFrame has yielded some info about the fields...
- `events` is a list of dicts, with each dict being a message. That message can be a text chunk, picture, etc. It appears that a new dict is added for every time the user pushed send.
- `participant_data` ties the IDs to the plain user names
- The Unix `timestamp` of each message needs to be divided by 1e6

The Hangouts history structure roughly resembles the tree below.  
```
Hangouts.json
    conversation_01
        conversation_data
            participant_data
            read_state
            ...
        events
            message_0001
            message_0002
            ...
    conversation_02
        conversation_data
            participant_data
            read_state
            ...
        events
            message_0001
            message_0002
            ...
```

Below is an example of one message (with dummy ID/name data):  
```
{
  "advances_sort_timestamp": true,
  "chat_message": {
    "message_content": {
      "segment": [
        {
          "text": "Hey that Hangouts parser dealio is pretty neat",
          "type": "TEXT"
        }
      ]
    }
  },
  "conversation_id": {
    "id": "ABCDEFGHIJKLMNOPQRS"
  },
  "delivery_medium": {
    "medium_type": "BABEL_MEDIUM"
  },
  "event_id": "ABCDEFGHIJKLMNOPQRS",
  "event_otr": "ON_THE_RECORD",
  "event_type": "REGULAR_CHAT_MESSAGE",
  "event_version": "ABCDEFGHIJKLMNOPQRS,
  "self_event_state": {
    "client_generated_id": "ABCDEFGHIJKLMNOPQRS",
    "notification_level": "RING",
    "user_id": {
      "chat_id": "XXXXXXXXXXXXXXXXXXXXX",
      "gaia_id": "XXXXXXXXXXXXXXXXXXXXX"
    }
  },
  "sender_id": {
    "chat_id": "YYYYYYYYYYYYYYYYYYYYY",
    "gaia_id": "YYYYYYYYYYYYYYYYYYYYY"
  },
  "timestamp": "1443742921190532"
}
```

Below is an example of conversation metadata (with dummy ID/name data):  
```
"conversation": {
    "conversation": {
      "current_participant": [
        {
          "chat_id": "XXXXXXXXXXXXXXXXXXXXX",
          "gaia_id": "XXXXXXXXXXXXXXXXXXXXX"
        },
        {
          "chat_id": "YYYYYYYYYYYYYYYYYYYYY",
          "gaia_id": "YYYYYYYYYYYYYYYYYYYYY"
        }
      ],
      "force_history_state": "NO_FORCE",
      "fork_on_external_invite": false,
      "group_link_sharing_status": "LINK_SHARING_OFF",
      "has_active_hangout": false,
      "id": {
        "id": "ABCDEFGHIJKLMNOPQRS"
      },
      "network_type": [
        "BABEL"
      ],
      "otr_status": "ON_THE_RECORD",
      "otr_toggle": "ENABLED",
      "participant_data": [
        {
          "fallback_name": "John Smith",
          "id": {
            "chat_id": "XXXXXXXXXXXXXXXXXXXXX",
            "gaia_id": "XXXXXXXXXXXXXXXXXXXXX"
          },
          "in_different_customer_as_requester": false,
          "invitation_status": "ACCEPTED_INVITATION",
          "new_invitation_status": "ACCEPTED_INVITATION",
          "participant_type": "GAIA"
        },
        {
          "fallback_name": "Joe Schmo",
          "id": {
            "chat_id": "YYYYYYYYYYYYYYYYYYYYY",
            "gaia_id": "YYYYYYYYYYYYYYYYYYYYY"
          },
          "in_different_customer_as_requester": false,
          "invitation_status": "ACCEPTED_INVITATION",
          "new_invitation_status": "ACCEPTED_INVITATION",
          "participant_type": "GAIA"
        }
      ],
      "read_state": [
        {
          "latest_read_timestamp": "0",
          "participant_id": {
            "chat_id": "XXXXXXXXXXXXXXXXXXXXX",
            "gaia_id": "XXXXXXXXXXXXXXXXXXXXX"
          }
        },
        {
          "latest_read_timestamp": "1443742911690532",
          "participant_id": {
            "chat_id": "XXXXXXXXXXXXXXXXXXXXX",
            "gaia_id": "XXXXXXXXXXXXXXXXXXXXX"
          }
        }
      ],
      "self_conversation_state": {
        "active_timestamp": "1433461103849000",
        "delivery_medium_option": [
          {
            "current_default": true,
            "delivery_medium": {
              "medium_type": "BABEL_MEDIUM"
            }
          }
        ],
        "invite_timestamp": "1433465011180000",
        "inviter_id": {
          "chat_id": "YYYYYYYYYYYYYYYYYYYYY",
          "gaia_id": "YYYYYYYYYYYYYYYYYYYYY"
        },
        "is_guest": false,
        "notification_level": "RING",
        "self_read_state": {
          "latest_read_timestamp": "1443742118690532",
          "participant_id": {
            "chat_id": "XXXXXXXXXXXXXXXXXXXXX",
            "gaia_id": "XXXXXXXXXXXXXXXXXXXXX"
          }
        },
        "sort_timestamp": "1443741128690532",
        "status": "ACTIVE",
        "view": [
          "INBOX_VIEW"
        ]
      },
      "type": "STICKY_ONE_TO_ONE"
    },
    "conversation_id": {
      "id": "ABCDEFGHIJKLMNOPQRS"
    }
  },
```

Todo List
---------
- [ ] Get metadata fields in each conversation
- [ ] Get fields in each message
    - [ ] Text
    - [ ] Image -> Display as text? Filename?
    - [ ] Other attachments
- [ ] Convert timestamp to ISO format (timezone?)
- [ ] Logic to assign user ID to fallback name
- [ ] Logic to assign name, timestamp, and text to message
- [ ] Output as IRC style text
- [ ] Function to convert IRC style text to CSV (basically JSON to CSV but broken down
- [ ] Do something interesting with the data
    - [ ] Word frequency after stemming and stop word removal
    - [ ] Text length per person
    - [ ] # messages per day per person
    - [ ] Messages by hour of day
    - [ ] Messages per day of week
    - [ ] Character count instead of word count
