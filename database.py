import sqlite3 as sl

class DatabaseClass:
    def __init__(self):
        self.con = sl.connect('discord-server.db')
        self.cursor = self.con.cursor()
        DatabaseClass.createDatabase(self)

    def createDatabase(self):
        # CREATE DATABASE IF DOESN'T EXIST
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS accounts
                (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                user TEXT,
                account TEXT
                );""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS bad_words
                (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                word TEXT,
                count INTEGER
                );""")
    
    ### FUNCTIONS FOR OVERWATCH BATTLETAGS
    def insertNewAccount(self,user,account):
        # SHOW ALL TABLES
        self.cursor.execute("INSERT INTO accounts (user, account) VALUES (?, ?);", (user, account))
        self.con.commit()

    def checkIfAccountExists(self, account):
        # RETURN BOOL FOR IF ACCOUNT EXISTS IN DB
        self.cursor.execute("SELECT account FROM accounts WHERE account=(?)", (account,))
        return not not self.cursor.fetchall()

    ### FUNCTION FOR COUNTING BAD WORDS
    def checkIfWordExists(self, word):
        self.cursor.execute("SELECT word FROM bad_words WHERE word=(?)", (word,))
        return not not self.cursor.fetchall()

    def getWordCount(self, word):
        self.cursor.execute("SELECT count FROM bad_words WHERE word=(?)", (word,))
        return (self.cursor.fetchall()[0])[0]

    def addNewWord(self, word):
        if not DatabaseClass.checkIfWordExists(self, word):
            self.cursor.execute("INSERT INTO bad_words (word, count) VALUES (?, 0);", (word,))
            self.con.commit()
        else:
            print("This word already exists!")
    
    def addToCount(self, word):
        if DatabaseClass.checkIfWordExists(self, word):
            count = DatabaseClass.getWordCount(self, word)
            self.cursor.execute("UPDATE bad_words SET count=(?) WHERE word=(?)", (count + 1, word))
            self.con.commit()
        else:
            print("Failed to find word.")

    def getAllWords(self):
        self.cursor.execute("SELECT word FROM bad_words")
        return [w[0] for w in self.cursor.fetchall()]

    def getTopWords(self, num):
        send = "The most used **bad** words:\n"
        self.cursor.execute("SELECT word, count FROM bad_words ORDER BY count DESC LIMIT (?);", (num,))
        for idx, word in enumerate(self.cursor.fetchall()):
            if (idx == 0):
                place = ':one:'
            elif (idx == 1):
                place = ':two:'
            elif (idx == 2):
                place = ':three:'
            elif (idx == 3):
                place = ':four:'
            elif (idx == 4):
                place = ':five:'
            elif (idx == 5):
                place = ':six:'
            elif (idx == 6):
                place = ':seven'
            elif (idx == 7):
                place = ':eight'
            elif (idx == 8):
                place = ':nine:'
            elif (idx == 9):
                place = ':ten:'
            else:
                place = '[' + str(idx + 1) + ']'
            send = "{s}{i} **{w}** : {c}\n".format(s=send, i=place, w=word[0], c=str(word[1]))
        return send