# Import required libraries
import sqlite3
import os
from datetime import datetime

# Create absolute path for database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Database:
    def __init__(self):
        # Connect to database if it exists or create one if it doesnt.
        try:
            # connect to database
            self.connect = sqlite3.connect('GoofyUtilityDatabase.db')
            
            # initialize a cursor to handle all executions
            self.cursor = self.connect.cursor()

        # Handle error if it arises
        except sqlite3.DatabaseError as e:
            print('Failed to load database ' + str(e))

    def insert_snippet(self, title, code):
        try:
            if len(title) > 1 and len(code) > 1:
                self.cursor.execute("INSERT INTO snippet (title, code, date) VALUES (?,?,?)",
                                    (title.lower(), code, datetime.now()))
                self.connect.commit()
                return "success"
            else:
                return "empty"
        except sqlite3.OperationalError as e:
            return "failure"
        except sqlite3.IntegrityError as e:
            return 'exists'
        
    def add_to_recent(self, title):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS recents (title TEXT UNIQUE)")
        try:
            data = self.cursor.execute("SELECT * FROM recents")
            if len(data.fetchall()) == 6:
                t = self.cursor.execute("SELECT * FROM recents ORDER BY title ASC LIMIT 1")
                self.cursor.execute("DELETE FROM recents WHERE title=?",(t.fetchall()[0][0],))
                
                self.cursor.execute("INSERT INTO recents (title) VALUES (?)", (title,))
                self.connect.commit()
            else:
                self.cursor.execute("INSERT INTO recents (title) VALUES (?)", (title,))
                self.connect.commit()
             
        except sqlite3.IntegrityError as e:
            pass
        
    def fetch_recents(self):
        t = self.cursor.execute("SELECT * FROM recents ORDER BY title ASC")
        return [i[0] for i in t.fetchall()]

    def delete_snippet(self, title):
        self.cursor.execute("DELETE FROM snippet WHERE title=?", (title,))
        self.connect.commit()
        return 'success'

    def get_all_snippets(self):
        data = self.cursor.execute("SELECT title FROM snippet").fetchall()
        return [title[0] for title in data]

    def search_snippet(self, title):
        try:
            code = self.cursor.execute("SELECT id, title, code FROM snippet WHERE title=?", (title,)).fetchone()
            return code
        except sqlite3.OperationalError as e:
            pass

    def get_snippet_id(self, title):
        try:
            code = self.cursor.execute("SELECT id, code FROM snippet WHERE title=?", (title,))
            return code
        except sqlite3.OperationalError as e:
            pass

    def update_snippet(self, iid, title, code):
        try:
            if len(title) > 1 and len(code) > 1:
                self.cursor.execute("UPDATE snippet SET title=?, code=? WHERE id=?",
                                    (title.strip().lower(), code, iid,))
                self.connect.commit()
                return True
            return False
        except Exception as e:
            print(str(e))
            return False

    def get_all_snippet_fields(self, title):
        try:
            code = self.cursor.execute("SELECT id, title, code FROM snippet WHERE title=?", (title,)).fetchone()
            return code
        except sqlite3.OperationalError as e:
            pass

    def __del__(self):
        self.cursor.close()
        self.connect.close()
