#!/usr/bin/env python3
from data.session import Session
from data.escalation import EscalationData
from data.recon import Recon
import mongoengine

session_list = []

def create_session(dictionary):
    checkDisconnected(dictionary)
    for s_id, s_info in dictionary.items():
        if not s_id in session_list:
            session_list.append(s_id)
        session = Session()
        setattr(session, '_id', s_id)
        session.isDisconnected = False
        for info in s_info:
            if info == 'type':
                setattr(session, '_type', s_info[info])
            else:
                setattr(session, info, s_info[info])
        session.save()

def checkDisconnected(dictionary):
    if not session_list:
        pass
    else:
        if not dictionary:
            for s in session_list:
                session = Session.objects(_id=s).first()
                session.isDisconnected = True
                session.save()
        for s_id in session_list:
            if s_id not in dictionary.items():
                session = Session.objects(_id=s_id).first()
                session.isDisconnected = True
                session.save()


def deleteSessions():
    Session.objects().delete()
    EscalationData.objects().delete()
    Recon.objects().delete()
    
    