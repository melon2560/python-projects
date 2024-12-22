import sqlite3
import tkinter as tk
from tkinter import messagebox

# データベース接続
def connect_db():
    return sqlite3.connect('todo.db')

# タスクテーブルを作成
def create_table():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# タスクを取得する関数
def get_tasks():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    connection.close()
    return tasks

# タスクを表示する関数
def display_tasks():

    task_count = get_task_count()  # タスクの数を取得

    for widget in task_frame.winfo_children():
        widget.destroy()  # 既存のウィジェットを削除

    tasks = get_tasks()  # 最新のタスクを取得

    for task in tasks:
        task_id, title, done = task
        status = "完了" if done else "未完了"

        # タスク表示のラベル
        task_label = tk.Label(task_frame, text=f"{task_count}. {title} - {status}")
        task_label.pack(anchor="w")

        # 状態変更ボタン
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

# タスクを追加する関数
def add_task():
    task_title = task_entry.get()  # task_entry を使って入力されたタスク名を取得
    if task_title:
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (task_title, 0))
        connection.commit()
        connection.close()
        messagebox.showinfo("情報", "タスクが追加されました！")
        task_entry.delete(0, tk.END)  # テキストボックスを空にする
        display_tasks()  # 追加後にタスクリストを更新
    else:
        messagebox.showwarning("警告", "タスク名を入力してください。")

# タスクを削除する関数
def delete_task(task_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    connection.commit()
    connection.close()
    display_tasks()  # タスク削除後、タスクリストを更新

def get_task_count():
    connection = sqlite3.connect("todo.db")  # データベース接続
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM tasks")  # タスクの数を取得
    count = cursor.fetchone()[0]  # 結果はタプルで返されるので、最初の要素を取得
    connection.close()  # 接続を閉じる
    return count

# タスクのステータスを変更する関数
def toggle_task_status(task_id, current_status):
    new_status = 1 if current_status == 0 else 0
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("UPDATE tasks SET done = ? WHERE id = ?", (new_status, task_id))
    connection.commit()
    connection.close()
    display_tasks()  # ステータス変更後、タスクリストを更新

    # フィルタリングされたタスクを取得する関数
def filter_tasks(status):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks WHERE done=?", (status,))
    tasks = cursor.fetchall()
    connection.close()
    return tasks

# タスクリストをリフレッシュする関数
def refresh_tasks(filter_status=None):
    """
    タスクリストを更新する関数。
    filter_status が None の場合は全てのタスクを表示。
    filter_status が 0 の場合は未完了のタスクのみを表示。
    filter_status が 1 の場合は完了したタスクのみを表示。
    """
    for widget in task_frame.winfo_children():
        widget.destroy()  # 既存のタスクを削除

    if filter_status is None:
        tasks = get_tasks()  # 全てのタスクを取得
    else:
        tasks = filter_tasks(filter_status)  # フィルタリングされたタスクを取得

    for task in tasks:
        task_id, title, done = task
        status = "完了" if done else "未完了"

        task_label = tk.Label(task_frame, text=f"{task_id}. {title} - {status}")
        task_label.pack(anchor="w")

        toggle_button = tk.Button(
            task_frame,
            text="Toggle Status",
            command=lambda task_id=task_id, done=done: toggle_task_status(task_id, done)
        )
        toggle_button.pack(anchor="w")

        delete_button = tk.Button(
            task_frame,
            text="Delete",
            command=lambda task_id=task_id: delete_task(task_id)
        )
        delete_button.pack(anchor="w")

# GUI全体を構築する関数
def create_gui():
    global task_frame, task_entry

    task_entry = tk.Entry(root, width=30)
    task_entry.pack(pady=10)

    add_button = tk.Button(root, text="タスクを追加", command=add_task)
    add_button.pack(pady=5)

    filter_frame = tk.Frame(root)
    filter_frame.pack(pady=10)

    show_all_button = tk.Button(filter_frame, text="全て表示", command=display_tasks)
    show_all_button.pack(side=tk.LEFT, padx=5)

    show_incomplete_button = tk.Button(filter_frame, text="未完了のみ表示", command=lambda: refresh_tasks(0))
    show_incomplete_button.pack(side=tk.LEFT, padx=5)

    show_complete_button = tk.Button(filter_frame, text="完了のみ表示", command=lambda: refresh_tasks(1))
    show_complete_button.pack(side=tk.LEFT, padx=5)

    task_frame = tk.Frame(root)
    task_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    display_tasks()

# ウィンドウ作成
root = tk.Tk()
root.title("TODOアプリ")
root.geometry("400x300")

create_table()
create_gui()
root.mainloop()
