import sqlite3
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox, font
from tkcalendar import DateEntry  # pip install tkcalendar が必要
import os
import webbrowser

class TodoApp:
    def __init__(self):
        self.current_filter_status = None
        self.root = tk.Tk()
        self.root.title("スタイリッシュTODOアプリ")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f4f8")  # 背景色を薄い青灰色に
        
        # カスタムフォントの設定
        self.header_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=10)
        self.small_font = font.Font(family="Helvetica", size=9)
        
        # テーマカラーの設定
        self.theme_colors = {
            "primary": "#4a6fa5",      # メインカラー（青系）
            "secondary": "#166088",    # アクセントカラー（濃い青）
            "success": "#28a745",      # 成功/完了（緑）
            "warning": "#ffc107",      # 警告/注意（黄色）
            "danger": "#dc3545",       # 危険/削除（赤）
            "light": "#f8f9fa",        # 明るい背景
            "dark": "#343a40"          # テキスト色
        }
        
        # 優先度の色とラベル
        self.priority_colors = {
            1: "#d1e7dd",  # 低（薄緑）
            2: "#fff3cd",  # 中（薄黄）
            3: "#f8d7da"   # 高（薄赤）
        }
        self.priority_labels = {1: "低", 2: "中", 3: "高"}
        
        self.create_table()
        self.create_gui()
        
    def connect_db(self):
        return sqlite3.connect('todo.db')

    def create_table(self):
        conn = self.connect_db()
        c = conn.cursor()
        
        # まずテーブル自体を作成
        c.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0,
                due_date TEXT,
                priority INTEGER DEFAULT 1
            )
        ''')
        
        # テーブルにpriorityカラムが存在するか確認
        c.execute("PRAGMA table_info(tasks)")
        columns = [column[1] for column in c.fetchall()]
        
        # priorityカラムが存在しなければ追加
        if 'priority' not in columns:
            try:
                c.execute("ALTER TABLE tasks ADD COLUMN priority INTEGER DEFAULT 1")
                print("priorityカラムを追加しました")
            except sqlite3.Error as e:
                print(f"エラー: {e}")
                
        conn.commit()
        conn.close()

    def get_tasks(self, filter_status=None, sort_by_date=False, filter_priority=None):
        connection = self.connect_db()
        cursor = connection.cursor()
        
        query = "SELECT * FROM tasks"
        params = []
        conditions = []
        
        if filter_status is not None:
            conditions.append("done=?")
            params.append(filter_status)
            
        if filter_priority is not None:
            conditions.append("priority=?")
            params.append(filter_priority)
            
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        if sort_by_date:
            query += " ORDER BY due_date ASC"
        else:
            query += " ORDER BY priority DESC, due_date ASC"  # デフォルトは優先度高い順、同じ優先度内では期限順
            
        cursor.execute(query, params)
        tasks = cursor.fetchall()
        connection.close()
        return tasks

    def display_tasks(self, tasks=None):
        if tasks is None:
            tasks = self.get_tasks()
            
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        today = datetime.now().date()

        for task in tasks:
            task_id, title, done, due_date, priority = task if len(task) >= 5 else (*task, 1)
            status = "完了" if done else "未完了"
            
            color, formatted_due_date = self.format_due_date(due_date, today)

            self.create_task_widgets(task_id, title, status, formatted_due_date, done, color, priority)

    def format_due_date(self, due_date, today):
        try:
            if due_date:
                due_date_date = datetime.strptime(due_date, "%Y-%m-%d").date()
                days_left = (due_date_date - today).days
                
                if days_left < 0:
                    color = "red"
                    days_str = f"（{abs(days_left)}日遅延）"
                elif days_left == 0:
                    color = "orange"
                    days_str = "（今日が期限）"
                elif days_left <= 3:
                    color = "orange"
                    days_str = f"（残り{days_left}日）"
                else:
                    color = "black"
                    days_str = f"（残り{days_left}日）"
                
                formatted_due_date = due_date_date.strftime("%Y-%m-%d") + " " + days_str
            else:
                color = "black"
                formatted_due_date = "未設定"
        except ValueError:
            color = "black"
            formatted_due_date = "不正な日付"
        return color, formatted_due_date

    def create_task_widgets(self, task_id, title, status, due_date, done, color, priority=1):
        # 優先度に応じた表示設定
        priority_text = self.priority_labels.get(priority, "不明")
        bg_color = self.priority_colors.get(priority, "#ffffff")
        
        # 完了状態による表示の違い
        opacity = 0.7 if done else 1.0  # 完了したタスクは少し透明に
        strike = "overstrike" if done else ""  # 完了したタスクは取り消し線
        
        # カード風タスク表示用のフレーム
        task_frame = tk.Frame(
            self.task_frame,
            bg=bg_color if not done else "#f8f9fa",  # 完了したタスクは背景色を薄く
            padx=8,
            pady=8,
            relief=tk.GROOVE,
            bd=1
        )
        task_frame.pack(fill=tk.X, padx=10, pady=5, anchor="w")
        
        # タイトルと状態の表示 - 左側
        title_status_frame = tk.Frame(task_frame, bg=task_frame["bg"])
        title_status_frame.grid(row=0, column=0, sticky="w")
        
        # 状態インジケーター（完了/未完了を視覚的に表示）
        status_color = self.theme_colors["success"] if done else self.theme_colors["warning"]
        status_indicator = tk.Canvas(
            title_status_frame,
            width=12,
            height=12,
            bg=task_frame["bg"],
            highlightthickness=0
        )
        status_indicator.create_oval(2, 2, 10, 10, fill=status_color, outline="")
        status_indicator.pack(side=tk.LEFT, padx=(0, 5))
        
        # タスクタイトル
        task_label = tk.Label(
            title_status_frame,
            text=title,
            fg=self.theme_colors["dark"] if not done else "gray",
            bg=task_frame["bg"],
            font=(None, 10, "bold " + strike if priority == 3 else strike)
        )
        task_label.pack(side=tk.LEFT)
        
        # ステータスラベル（小さく表示）
        status_label = tk.Label(
            title_status_frame,
            text=f" - {status}",
            fg="gray",
            bg=task_frame["bg"],
            font=self.small_font
        )
        status_label.pack(side=tk.LEFT)
        
        # 優先度表示 - 右側
        info_frame = tk.Frame(task_frame, bg=task_frame["bg"])
        info_frame.grid(row=0, column=1, sticky="e")
        
        # 優先度バッジ
        priority_label = tk.Label(
            info_frame,
            text=f"優先度: {priority_text}",
            bg=bg_color,
            fg="black",
            font=self.small_font,
            padx=5,
            pady=2,
            relief=tk.FLAT
        )
        priority_label.pack(side=tk.RIGHT)
        
        # 期限の表示
        due_frame = tk.Frame(task_frame, bg=task_frame["bg"])
        due_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 0))
        
        calendar_icon = tk.Label(
            due_frame,
            text="📅",  # カレンダーアイコン
            fg=color,
            bg=task_frame["bg"]
        )
        calendar_icon.pack(side=tk.LEFT, padx=(0, 5))
        
        due_label = tk.Label(
            due_frame,
            text=due_date,
            fg=color if not done else "gray",
            bg=task_frame["bg"],
            font=self.small_font
        )
        due_label.pack(side=tk.LEFT)
        
        # ボタンフレーム
        button_frame = tk.Frame(task_frame, bg=task_frame["bg"])
        button_frame.grid(row=2, column=0, columnspan=2, sticky="e", pady=(8, 0))
        
        # 共通ボタンスタイル
        button_style = {
            "font": self.small_font,
            "padx": 8,
            "pady": 2,
            "relief": tk.RAISED,
            "bd": 1
        }
        
        # 状態切替ボタン
        toggle_text = "✓ 完了にする" if not done else "↺ 未完了に戻す"
        toggle_color = self.theme_colors["success"] if not done else self.theme_colors["warning"]
        
        toggle_button = tk.Button(
            button_frame,
            text=toggle_text,
            command=lambda: self.toggle_task_status(task_id, done),
            bg=toggle_color,
            fg="white" if not done else "black",
            **button_style
        )
        toggle_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 削除ボタン
        delete_button = tk.Button(
            button_frame,
            text="🗑 削除",
            command=lambda: self.delete_task(task_id),
            bg=self.theme_colors["danger"],
            fg="white",
            **button_style
        )
        delete_button.pack(side=tk.LEFT)

    def set_placeholder(self, entry, placeholder):
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(foreground="black")

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(foreground="grey")

        entry.insert(0, placeholder)
        entry.config(foreground="grey")
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def add_task(self):
        # タスク名の取得とバリデーション
        task_title = self.task_entry.get()
        if task_title == "タスク名を入力してください" or not task_title.strip():
            messagebox.showwarning("警告", "タスク名を入力してください。")
            self.task_entry.focus_set()
            return
            
        # 日付の取得 - DateEntryからは'yyyy-mm-dd'形式で取得できる
        due_date = self.due_date_entry.get()
        
        # 優先度の取得 - ラジオボタンから
        priority = self.priority_var.get()  # ラジオボタンから直接値を取得
        
        # データの挿入
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tasks (title, done, due_date, priority) VALUES (?, ?, ?, ?)",
                     (task_title, 0, due_date, priority))
        connection.commit()
        connection.close()
        
        # 成功メッセージと入力フィールドのリセット
        messagebox.showinfo("成功", "新しいタスクを追加しました！",
                          icon='info')
        
        # フォームをリセット
        self.task_entry.delete(0, tk.END)
        self.set_placeholder(self.task_entry, "タスク名を入力してください")
        
        # 今日の日付にリセット
        today = datetime.now()
        self.due_date_entry.set_date(today)
        
        # 優先度を「低」にリセット
        self.priority_var.set(1)
        
        # タスクリストを更新
        self.display_tasks()

    def delete_task(self, task_id):
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        connection.commit()
        connection.close()
        self.display_tasks()

    def toggle_task_status(self, task_id, current_status):
        new_status = 1 if current_status == 0 else 0
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute("UPDATE tasks SET done = ? WHERE id = ?", (new_status, task_id))
        connection.commit()
        connection.close()
        self.display_tasks()

    def refresh_tasks(self, filter_status=None):
        self.current_filter_status = filter_status
        tasks = self.get_tasks(filter_status)
        self.display_tasks(tasks)

    def display_sorted_tasks(self):
        tasks = self.get_tasks(self.current_filter_status, sort_by_date=True)
        self.display_tasks(tasks)
        
    def filter_by_priority(self, priority):
        tasks = self.get_tasks(self.current_filter_status, filter_priority=priority)
        self.display_tasks(tasks)

    def create_gui(self):
        # ヘッダーセクション - アプリタイトルとバージョン情報
        header_frame = tk.Frame(self.root, bg=self.theme_colors["primary"], pady=10)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame,
            text="スタイリッシュ TODO アプリ",
            font=("Helvetica", 16, "bold"),
            fg="white",
            bg=self.theme_colors["primary"]
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="効率的なタスク管理のために",
            font=("Helvetica", 10),
            fg="white",
            bg=self.theme_colors["primary"]
        )
        subtitle_label.pack()
        
        # メインコンテンツのコンテナ（タブ付きのデザイン風）
        main_container = tk.Frame(self.root, bg=self.theme_colors["light"], padx=15, pady=15)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 入力エリアのフレーム - カード風デザイン
        input_frame = tk.LabelFrame(
            main_container,
            text="新しいタスク",
            font=self.header_font,
            bg=self.theme_colors["light"],
            fg=self.theme_colors["dark"],
            padx=10,
            pady=10,
            relief=tk.GROOVE,
            bd=2
        )
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 入力フィールドの共通スタイル
        entry_style = {"padx": 10, "pady": 5, "sticky": "w"}
        label_style = {"font": self.normal_font, "bg": self.theme_colors["light"], "fg": self.theme_colors["dark"]}
        
        # タスク名入力
        tk.Label(input_frame, text="タスク名:", **label_style).grid(row=0, column=0, **entry_style)
        self.task_entry = ttk.Entry(input_frame, width=40, font=self.normal_font)
        self.task_entry.grid(row=0, column=1, **entry_style)
        self.set_placeholder(self.task_entry, "タスク名を入力してください")
        
        # 期限日入力 - カレンダーピッカーを使用
        tk.Label(input_frame, text="締切日:", **label_style).grid(row=1, column=0, **entry_style)
        
        date_frame = tk.Frame(input_frame, bg=self.theme_colors["light"])
        date_frame.grid(row=1, column=1, **entry_style)
        
        today = datetime.now()
        self.due_date_entry = DateEntry(
            date_frame,
            width=15,
            background=self.theme_colors["primary"],
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd',
            font=self.normal_font,
            locale='ja_JP'  # 日本語ロケール
        )
        self.due_date_entry.pack(side=tk.LEFT)
        
        date_info = tk.Label(
            date_frame,
            text="※カレンダーから選択",
            font=self.small_font,
            fg="gray",
            bg=self.theme_colors["light"]
        )
        date_info.pack(side=tk.LEFT, padx=10)
        
        # 優先度選択 - カラーコード付き
        tk.Label(input_frame, text="優先度:", **label_style).grid(row=2, column=0, **entry_style)
        
        priority_frame = tk.Frame(input_frame, bg=self.theme_colors["light"])
        priority_frame.grid(row=2, column=1, **entry_style)
        
        self.priority_var = tk.IntVar(value=1)  # デフォルトは低優先度
        
        for i, (priority, label) in enumerate(self.priority_labels.items()):
            color = self.priority_colors[priority]
            rb = tk.Radiobutton(
                priority_frame,
                text=label,
                variable=self.priority_var,
                value=priority,
                bg=color,
                selectcolor=color,
                indicatoron=0,  # ボタン風のラジオボタン
                width=8,
                font=self.normal_font,
                relief=tk.RAISED,
                bd=1
            )
            rb.pack(side=tk.LEFT, padx=5)
        
        # ボタンエリア
        button_frame = tk.Frame(input_frame, bg=self.theme_colors["light"], pady=10)
        button_frame.grid(row=3, column=0, columnspan=2, sticky="ew")
        
        # タスク追加ボタン - 目立つデザイン
        add_button = tk.Button(
            button_frame,
            text="タスクを追加",
            command=self.add_task,
            bg=self.theme_colors["success"],
            fg="white",
            font=self.normal_font,
            padx=15,
            pady=5,
            relief=tk.RAISED,
            bd=1
        )
        add_button.pack(side=tk.RIGHT)
        
        # フィルターとソートのフレーム
        filter_frame = tk.LabelFrame(
            main_container,
            text="フィルター・ソート",
            font=self.header_font,
            bg=self.theme_colors["light"],
            fg=self.theme_colors["dark"],
            padx=10,
            pady=10,
            relief=tk.GROOVE,
            bd=2
        )
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # フィルターセクションのスタイル設定
        filter_section_style = {
            "bg": self.theme_colors["light"],
            "pady": 5
        }
        
        # フィルターボタン（状態別）
        status_frame = tk.Frame(filter_frame, **filter_section_style)
        status_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            status_frame,
            text="状態:",
            font=self.normal_font,
            bg=self.theme_colors["light"],
            fg=self.theme_colors["dark"]
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # ボタングループのスタイル設定
        btn_style = {
            "font": self.normal_font,
            "relief": tk.RAISED,
            "bd": 1,
            "padx": 10,
            "pady": 3
        }
        
        show_all_button = tk.Button(
            status_frame,
            text="全て",
            command=lambda: self.refresh_tasks(),
            bg=self.theme_colors["light"],
            fg=self.theme_colors["dark"],
            **btn_style
        )
        show_all_button.pack(side=tk.LEFT, padx=2)
        
        show_incomplete_button = tk.Button(
            status_frame,
            text="未完了のみ",
            command=lambda: self.refresh_tasks(0),
            bg=self.theme_colors["warning"],
            fg="black",
            **btn_style
        )
        show_incomplete_button.pack(side=tk.LEFT, padx=2)
        
        show_complete_button = tk.Button(
            status_frame,
            text="完了のみ",
            command=lambda: self.refresh_tasks(1),
            bg=self.theme_colors["success"],
            fg="white",
            **btn_style
        )
        show_complete_button.pack(side=tk.LEFT, padx=2)
        
        # 区切り線
        separator = ttk.Separator(filter_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=5)
        
        # フィルターボタン（優先度別）
        priority_frame = tk.Frame(filter_frame, **filter_section_style)
        priority_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            priority_frame,
            text="優先度:",
            font=self.normal_font,
            bg=self.theme_colors["light"],
            fg=self.theme_colors["dark"]
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        show_all_priority_button = tk.Button(
            priority_frame,
            text="全て",
            command=lambda: self.display_tasks(),
            bg=self.theme_colors["light"],
            fg=self.theme_colors["dark"],
            **btn_style
        )
        show_all_priority_button.pack(side=tk.LEFT, padx=2)
        
        # 優先度ボタンは対応する色を使用
        for priority, label in self.priority_labels.items():
            color = self.priority_colors[priority]
            btn = tk.Button(
                priority_frame,
                text=label,
                command=lambda p=priority: self.filter_by_priority(p),
                bg=color,
                fg="black",
                **btn_style
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # 区切り線
        separator2 = ttk.Separator(filter_frame, orient='horizontal')
        separator2.pack(fill=tk.X, pady=5)
        
        # ソートボタン
        sort_frame = tk.Frame(filter_frame, **filter_section_style)
        sort_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            sort_frame,
            text="ソート:",
            font=self.normal_font,
            bg=self.theme_colors["light"],
            fg=self.theme_colors["dark"]
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        sort_btn_style = {**btn_style, "bg": self.theme_colors["secondary"], "fg": "white"}
        
        sort_by_due_date_button = tk.Button(
            sort_frame,
            text="締切日順",
            command=self.display_sorted_tasks,
            **sort_btn_style
        )
        sort_by_due_date_button.pack(side=tk.LEFT, padx=2)
        
        sort_by_priority_button = tk.Button(
            sort_frame,
            text="優先度順",
            command=lambda: self.display_tasks(),
            **sort_btn_style
        )
        sort_by_priority_button.pack(side=tk.LEFT, padx=2)
        
        # タスク表示エリア
        task_label_frame = tk.LabelFrame(
            main_container,
            text="タスク一覧",
            font=self.header_font,
            bg=self.theme_colors["light"],
            fg=self.theme_colors["dark"],
            padx=10,
            pady=10,
            relief=tk.GROOVE,
            bd=2
        )
        task_label_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # スクロール可能なタスクフレーム
        canvas = tk.Canvas(
            task_label_frame,
            bg=self.theme_colors["light"],
            highlightthickness=0  # キャンバスの境界線を削除
        )
        
        # スタイリッシュなスクロールバー
        scrollbar_style = ttk.Style()
        scrollbar_style.configure("Custom.Vertical.TScrollbar",
                                 background=self.theme_colors["light"],
                                 troughcolor=self.theme_colors["light"])
        
        scrollbar = ttk.Scrollbar(
            task_label_frame,
            orient="vertical",
            command=canvas.yview,
            style="Custom.Vertical.TScrollbar"
        )
        
        self.task_frame = tk.Frame(canvas, bg=self.theme_colors["light"])
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.create_window((0, 0), window=self.task_frame, anchor="nw")
        
        # タスクの数に応じてスクロール領域を調整
        self.task_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # 空のタスクリスト表示用のプレースホルダー
        self.empty_label = tk.Label(
            self.task_frame,
            text="タスクがありません。新しいタスクを追加してください。",
            font=self.normal_font,
            fg="gray",
            bg=self.theme_colors["light"]
        )
        
        self.display_tasks()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TodoApp()
    app.run()
