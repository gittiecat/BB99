from database import DatabaseClass
import requests
import json

class StatsClass:
    def __init__(self, battletag, author):
        self.author = str(author)
        self.battletag = battletag
        self.cleantag = battletag.replace("#","-")
        self.roles = []
        self.private = False

        db = DatabaseClass()

        if '#' in self.battletag:
            if not db.checkIfAccountExists(self.battletag):
                db.insertNewAccount(self.author, self.battletag)
            # Pull info from the battletag
            StatsClass.parseJSON(self)

    def parseJSON(self):
        tag = self.cleantag
        stats = requests.get('https://ow-api.com/v1/stats/pc/eu/{0}/profile'.format(tag))
        json = stats.json()
        if (json['private'] == True):
            self.private = True
        else:
            role_list = []
            for role in json['ratings']:
                r = role['role']
                l = role['level']
                if (r == 'tank'):
                    role_list.append([':shield:', 'Tank:', str(l), 'SR'])
                elif (r == 'damage'):
                    role_list.append([':crossed_swords:', 'DPS:', str(l), 'SR'])
                elif (r == 'support'):
                    role_list.append([':ambulance:', 'Support:', str(l), 'SR'])
            self.avgsr = str(json['rating'])
            self.roles = role_list

    def toMessage(self):
        send = "Stats for: " + self.battletag + "\n"
        if self.private == True:
            send = send + "This account is **private**!\n*(If you have recently made this profile public, please allow some time for the update to go through.)*"
        elif not self.roles:
            send = send + "No currently recorded stats!\n"
        else:
            for l in self.roles:
                send = send + ' '.join(l) + "\n"
            send = send + "Average SR: " + self.avgsr
        return send
