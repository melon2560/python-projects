def callback(commit):
    # 現在のメールアドレスを出力
    print(f"Processing commit:")
    print(f"  Author Email (before): {commit.author_email}")
    print(f"  Committer Email (before): {commit.committer_email}")
    
    # 強制的に書き換え
    commit.author_email = b'melon2560@users.noreply.github.com'
    commit.committer_email = b'melon2560@users.noreply.github.com'
    
    # 書き換え後のメールアドレスを出力
    print(f"  Author Email (after): {commit.author_email}")
    print(f"  Committer Email (after): {commit.committer_email}")
