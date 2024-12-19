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

def get_tasks():
    connection = sqlite3.connect("todo.db")  # データベース接続
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks")  # データ取得クエリ
    tasks = cursor.fetchall()  # 結果を取得
    connection.close()  # 接続を閉じる
    return tasks

tasks = get_tasks()
def display_tasks(tasks):
    for task in tasks:
        task_id, title, done = task # タスク情報を変数に分割
        status = "完了" if done else "未完了"
        print(f"{task_id}. {title} - {status}")

display_tasks(tasks)