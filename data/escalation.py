#!/usr/bin/env python3

import mongoengine

class EscalationData(mongoengine.Document):
    '''
    Puts escalation data into the database
    '''
    _id = mongoengine.StringField()
    getsystem = mongoengine.BooleanField()

    meta = {
    'db_alias': 'core',
    'collection': 'Escalation'
    }