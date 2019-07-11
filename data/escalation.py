#!/usr/bin/env python3

import mongoengine

class EscalationData(mongoengine.Document):
    _id = mongoengine.StringField()
    getsystem = mongoengine.BooleanField()

    meta = {
    'db_alias': 'core',
    'collection': 'Escalation'
    }