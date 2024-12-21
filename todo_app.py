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

# タスクを取得する関数
def get_tasks():
    connection = sqlite3.connect("todo.db")  # データベース接続
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks")  # データ取得クエリ
    tasks = cursor.fetchall()  # 結果を取得
    connection.close()  # 接続を閉じる
    return tasks

# タスクを表示する関数
def display_tasks(tasks):
    for task in tasks:
        task_id, title, done = task  # タスク情報を変数に分割
        status = "完了" if done else "未完了"
        print(f"{task_id}. {title} - {status}")

        # 状態変更ボタンを作成
        toggle_button = tk.Button(
            root,
            text=f"Toggle Status {title} {done}",
            command=lambda task_id=task_id, status=done: toggle_task_status(task_id, status)
        )
        toggle_button.pack()

        # 削除ボタンを作成
        delete_button = tk.Button(
            task_frame,
            text="Delete",
            command=lambda task_id=task_id: delete_task(task_id)
        )
        delete_button.pack(anchor="w")

# タスクをフィルタリングする関数
def filter_tasks(status):
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks WHERE done=?", (status,))   # ステータスに応じてタスクを取得
    tasks = cursor.fetchall()
    connection.close()
    return tasks

# タスクを追加する関数
def add_task():
    task_title = task_entry.get()
    if task_title:
        connection = sqlite3.connect("todo.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (task_title, 0))
        connection.commit()
        connection.close()
        messagebox.showinfo("情報", "タスクが追加されました！")
        task_entry.delete(0, tk.END)
        refresh_tasks()  # 追加後にリフレッシュ
    else:
        messagebox.showwarning("警告", "タスク名を入力してください。")

# タスクを削除する関数
def delete_task(task_id):
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    connection.commit()
    connection.close()
    refresh_tasks()

# タスクのステータスを変更する関数
def toggle_task_status(task_id, current_status):
    new_status = 1 if current_status == 0 else 0
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE tasks SET done = ? WHERE id = ?", (new_status, task_id))
    connection.commit()
    connection.close()
    refresh_tasks()

# タスクリストをリフレッシュする関数
def refresh_tasks(filter_status=None):
    """
    タスクリストを更新する関数。
    filter_status が None の場合は全てのタスクを表示。
    filter_status が 0 の場合は未完了のタスクのみを表示。
    filter_status が 1 の場合は完了したタスクのみを表示。
    """
    # フレーム内のウィジェットを削除
    for widget in task_frame.winfo_children():
        widget.destroy()

    # フィルタリングに応じてタスクを取得
    if filter_status is None:
        tasks = get_tasks() # 全てのタスクを取得
    else:
        tasks = filter_tasks(filter_status) # フィルタリングされたタスクを取得

    for task in tasks:
        task_id, title, done = task
        status = "完了" if done else "未完了"

        # タスク表示のラベル
        task_label = tk.Label(task_frame, text=f"{task_id}. {title} - {status}")
        task_label.pack(anchor="w")

        # トグルボタン
        toggle_button = tk.Button(
            task_frame,
            text="Toggle Status",
            command=lambda task_id=task_id, done=done: toggle_task_status(task_id, done)
        )
        toggle_button.pack(anchor="w")

        # 削除ボタン
        delete_button = tk.Button(
            task_frame,
            text="Delete",
            command=lambda task_id=task_id: delete_task(task_id)
        )
        delete_button.pack(anchor="w")

# GUI全体を構築する関数
def create_gui():
    global task_frame

    global task_entry
    task_entry = tk.Entry(root, width=30)
    task_entry.pack(pady=10)

    # タスクを表示するためのフレーム
    task_frame = tk.Frame(root)
    task_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    filter_frame = tk.Frame(root)   # ボタンをまとめるフレーム
    filter_frame.pack(pady=10)

    show_all_button = tk.Button(filter_frame, text="全て表示", command=lambda: refresh_tasks())
    show_all_button.pack(side=tk.LEFT, padx=5)

    show_incomplete_button = tk.Button(filter_frame, text="未完了のみ表示", command=lambda: refresh_tasks(filter_status=0))
    show_incomplete_button.pack(side=tk.LEFT, padx=5)

    show_complete_button = tk.Button(filter_frame, text="完了のみ表示", command=lambda: refresh_tasks(filter_status=1))
    show_complete_button.pack(side=tk.LEFT, padx=5)

    add_button = tk.Button(root, text="タスクを追加", command=add_task)
    add_button.pack(pady=5)

    tasks = get_tasks()
    display_tasks(tasks)

# ウィンドウ作成
root = tk.Tk()
root.title("TODOアプリ")
root.geometry("400x300")
create_gui()
root.mainloop()
