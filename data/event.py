#!/usr/bin/env python3

import mongoengine

class Event(mongoengine.Document):

    calledEvent = mongoengine.StringField()
    # futureEvent = mongoengine.ListField(mongoengine.StringField())

    meta = {
        'db_alias': 'core',
        'collection': 'Event'
    }

class EventUtils():
    def settingEvent(self, called_event):
        event = Event()
        event.calledEvent = called_event
        event.save()