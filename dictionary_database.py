import sqlite3
import os

def search_all_matching(word):
    with sqlite3.connect("db.sqlite3") as conn:
        cur = conn.cursor()
        return [i[0] for i in cur.execute("SELECT word FROM dictionary_info_dictionaryentry WHERE word LIKE ? || '%' ",
                                          (word,)).fetchall()]


def search_word(word):
    with sqlite3.connect("db.sqlite3") as conn:
        cur = conn.cursor()
        try:
            return cur.execute("SELECT description FROM dictionary_info_dictionaryentry WHERE word = ?", (word,)).fetchall()[
                    0][0]
        except IndexError:
            return []

def get_all_words():
    with sqlite3.connect("db.sqlite3") as conn:
        cur = conn.cursor()
        return [i[0] for i in cur.execute("SELECT word FROM dictionary_info_dictionaryentry").fetchall()]
