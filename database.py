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
            if len(data.fetchall()) >= 6:
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

    def get_all_quotes(self):
        quotes = self.cursor.execute("SELECT * FROM quotes").fetchall()
        return [quote for quote in quotes]

    # =========================================ENCYCLOPEDIA SECTION==============================================

    def insert_encyclopedia_thread(self, title, description, image):
        try:
            self.cursor.execute("INSERT INTO britannica_encyclopedia (title, description, image, date) VALUES (?,?,?,?)",(title, description, image, datetime.now()))
            self.connect.commit()
            return "success"   
        except sqlite3.OperationalError as e:
            return "failure"
        except sqlite3.IntegrityError as e:
            return 'Thread exists'

    def search_all_matching_thread(self, title):
        return [i[0] for i in self.cursor.execute("SELECT title FROM britannica_encyclopedia WHERE title LIKE ? || '%' ", (title,)).fetchall()]


    def search_word_thread(self, title):
        try:
            return self.cursor.execute("SELECT id, title, description, image FROM britannica_encyclopedia WHERE title = ?", (title,)).fetchall()[0]
        except IndexError:
            return []

    def get_all_thread_words(self):
        return [i[0] for i in self.cursor.execute("SELECT * FROM britannica_encyclopedia").fetchall()]

    def get_thread_image(self, title):
        try:
            return self.cursor.execute("SELECT image FROM britannica_encyclopedia WHERE title = ?", (title,)).fetchall()[0][0]
        except IndexError:
            return []

    def delete_thread(self, title):
        self.cursor.execute("DELETE FROM britannica_encyclopedia WHERE title=?", (title,))
        self.connect.commit()
        return 'success'


    def get_thread_id(self, title):
        try:
            thread = self.cursor.execute("SELECT id FROM britannica_encyclopedia WHERE title=?", (title,)).fetchone()[0]
            return thread
        except sqlite3.OperationalError as e:
            pass

    def update_thread(self, iid, title, thread):
        try:
            if len(title) > 1 and len(thread) > 1:
                self.cursor.execute("UPDATE britannica_encyclopedia SET title=?, description=? WHERE id=?", (title.strip().lower(), thread, iid,))
                self.connect.commit()
                return True
            return False
        except Exception as e:
            print(str(e))
            return False


    
    def __del__(self):
        self.cursor.close()
        self.connect.close()

#app = Database()
'''
The unusual mammal called the aardvark was named by South Africans in
the early 1800s. In the local language,
Afrikaans, “aardvark” means “earth pig.”
This name aptly describes a large,
heavily built animal with thin hair and
short, stumpy legs. The scientific name
of the aardvark is Orycteropus afer.
Aardvarks live in dry places in Africa
south of the Sahara Desert. The aardvark
can reach a length of 6 feet (1.8 meters).
Its head has huge donkeylike ears, a long
snout, and drooping eyelids with long
lashes. During the day aardvarks sleep in
underground burrows. At night they dig
underground for their favorite food,
termites. They break open the termites’
nests with their massive, flattened claws.
Then they suck up the insects with their
long tongue.
Female aardvarks give birth to one baby
per year. After a few weeks the baby
begins to follow its mother around. It
goes off on its own before it is 1 year
old. Aardvarks can live for more than 20
years in zoos.
Although aardvarks look like anteaters, they
are actually related to elephants, manatees,
and dugongs.



print(app.insert_encyclopedia_thread('Aardvark', d, '/images/Encyclopedia-images/aardvark.png'))
'''
#   app.get_encyclopedia_threads()

#print(app.get_thread_image('Aardvark'))
#print(app.get_thread_image('Aardvark'))
