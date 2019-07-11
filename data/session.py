#!/usr/bin/env python3

import mongoengine
from data.recon import Recon

class Session(mongoengine.Document):
    '''
    Dumps sesssion into mongodb.
    Takes in a dictionary in order to fill a session entry
    '''
    _id = mongoengine.StringField(requied=True)
    _type = mongoengine.StringField()
    tunnel_local = mongoengine.StringField()
    tunnel_peer =  mongoengine.StringField()
    via_exploit =  mongoengine.StringField()
    via_payload =  mongoengine.StringField()
    desc =  mongoengine.StringField()
    info =  mongoengine.StringField()
    workspace =  mongoengine.StringField()
    session_host =  mongoengine.StringField()
    session_port =  mongoengine.IntField()
    target_host =  mongoengine.StringField()
    username =  mongoengine.StringField()
    uuid =  mongoengine.StringField()
    exploit_uuid =  mongoengine.StringField()
    routes =  mongoengine.StringField()
    arch =  mongoengine.StringField()
    platform =  mongoengine.StringField()

    # Collects reconnaissance data per session
    recon_id = mongoengine.ListField()

    #escalation field to check if we own the system
    esc_id = mongoengine.ListField()

    # Sets to true if the the session no longer exists
    isDisconnected = mongoengine.BooleanField()

    meta = {
        'db_alias': 'core',
        'collection': 'sessions'
    }
