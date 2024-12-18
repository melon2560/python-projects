import sqlite3
import tkinter as tk
from tkinter import messagebox

# データベース接続
conn = sqlite3.connect('todo.db')
c = conn.cursor()

# タスクテーブルを作成
c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT NOT NULL,
          done INTEGER NOT NULL DEFAULT 0
          )
''')

# コミットして、接続を閉じる
conn.commit()
conn.close()