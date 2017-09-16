#!/usr/bin/env python
# coding=utf-8
"""Endpointy pro informace o dojizdeni za praci"""
from views.decorators import speaks_json, allowed_post_only
from flask import request, current_app
from util.db import common_db as db
import json


class Commuting:
    """Opet, hezky objekt na odbaveni logiky"""
    def __init__(self, district: str):
        self.district = district
        self._incoming = None
        self._outgoing = None
        # Vypocteme si procenta, abychom je mohli dat k legende
        incoming_percent = int((self.incoming / (self.incoming + self.outgoing))*100)
        outgoing_percent = int((self.outgoing / (self.incoming + self.outgoing))*100)
        self.return_data = {
            'title': 'Dojíždění za prací', 'data': [
                # key - popisek hodnoty v legende, value - hodnota
                {'key': f'Přijíždějících: {incoming_percent}%', 'value': self.incoming},
                {'key': f'Odjíždějících: {outgoing_percent}%', 'value': self.outgoing}
            ]
        }

    @property
    def incoming(self):
        """Prijizdi DO pozadoveneho okrsku -> je incoming"""
        if not self._incoming:
            with db(cursor=True) as cur:
                cur.execute('SELECT count FROM commuting WHERE `to` = ?', (self.district,))
                self._incoming = cur.fetchone()['count']
        return self._incoming

    @property
    def outgoing(self):
        """Odjizdi Z pozadoveneho okrsku -> je outgoing"""
        if not self._outgoing:
            with db(cursor=True) as cur:
                cur.execute('SELECT count FROM commuting WHERE `from` = ?', (self.district,))
                self._outgoing = cur.fetchone()['count']
        return self._outgoing


@speaks_json
@allowed_post_only
def commuting():
    """Jednoduche view pro dojizdeni - vysledkem je pie chart - odjizdi odsud, prijizdi sem"""
    # Vysvetleni request.data je v age_groups.py
    wanted_district = json.loads(request.data).get('district_code')
    current_app.logger.debug('wanted district: %s', wanted_district)
    return dict(data=Commuting(wanted_district).return_data)
