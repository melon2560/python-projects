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

        # 削除ボタンを作成
        delete_button = tk.Button(root, text=f"Delete {task_id}", command=lambda task_id=task_id: delete_task(task_id))
        delete_button.pack()

def add_task():
    # テキストボックスからタスク名を取得
    task_title = task_entry.get()

    if task_title:  # タスク名が入力されていれば
        # データベース接続
        connection = sqlite3.connect("todo.db")
        cursor = connection.cursor()

        # 新しいタスクをデータベースに追加
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (task_title, 0))
        connection.commit()
        connection.close()

        # メッセージボックスで通知
        messagebox.showinfo("情報", "タスクが追加されました！")

        # テキストボックスを空にする
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("警告", "タスク名を入力してください。")

# タスクを削除する関数
def delete_task(task_id):
    connection = sqlite3.connect("todo.db") # データベース接続
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))  # 指定IDのタスクを削除
    connection.commit()
    connection.close()
    print(f"Task {task_id} deleted")    #削除したタスクを表示

# ウィンドウ作成
root = tk.Tk()
root.title("TODOアプリ")    # ウィンドウスタイル

# サイズ設定
root.geometry("400x300")

# タスク入力用のテキストボックス
task_entry = tk.Entry(root, width=30)
task_entry.pack(pady=10)

# タスクを追加するボタン
add_button = tk.Button(root, text="タスクを追加", command=add_task)
add_button.pack(pady=5)

# タスクを表示
display_tasks(tasks)

# ウィンドウを表示
root.mainloop()

