"""
Database layer for Hobby.
Pre-seeded with the exact users, posts, reels, and chats matching the user's original design.
"""

import sqlite3
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hobby_data.db")

def hash_password(password: str) -> str:
    salt = "hobby_secure_salt_2026"
    return hashlib.sha256((salt + password).encode('utf-8')).hexdigest()

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db(force_reseed=False):
    conn = get_connection()
    c = conn.cursor()

    if force_reseed:
        c.execute("DROP TABLE IF EXISTS messages")
        c.execute("DROP TABLE IF EXISTS chat_users")
        c.execute("DROP TABLE IF EXISTS chats")
        c.execute("DROP TABLE IF EXISTS reels")
        c.execute("DROP TABLE IF EXISTS comment_likes")
        c.execute("DROP TABLE IF EXISTS comments")
        c.execute("DROP TABLE IF EXISTS saved_posts")
        c.execute("DROP TABLE IF EXISTS post_likes")
        c.execute("DROP TABLE IF EXISTS posts")
        c.execute("DROP TABLE IF EXISTS user_follows")
        c.execute("DROP TABLE IF EXISTS users")

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        gender TEXT DEFAULT 'other',
        bio TEXT DEFAULT '',
        avatar TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS user_follows (
        follower_id INTEGER NOT NULL,
        following_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (follower_id, following_id),
        FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (following_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        caption TEXT,
        image TEXT DEFAULT '',
        video TEXT DEFAULT '',
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS post_likes (
        post_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        PRIMARY KEY (post_id, user_id),
        FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS saved_posts (
        post_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (post_id, user_id),
        FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        post_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS comment_likes (
        comment_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        PRIMARY KEY (comment_id, user_id),
        FOREIGN KEY (comment_id) REFERENCES comments(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS reels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        video TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_name TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS chat_users (
        chat_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        PRIMARY KEY (chat_id, user_id),
        FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        content TEXT,
        image TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    conn.commit()

    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        seed_data(conn)

    conn.close()

def seed_data(conn):
    c = conn.cursor()
    pwd = hash_password("password")

    # Users from user's exact design & screenshots:
    users = [
        ("siddharth", "anil", "siddhua@gmail.com", pwd, "male", "Maker & Builder", ""),
        ("hisoka", "yanguchi", "hisoka@gmail.com", pwd, "male", "Travel & Film Enthusiast", ""),
        ("raam", "maheshwar", "raam@gmail.com", pwd, "male", "Photographer & Visual Artist", "")
    ]
    c.executemany("INSERT INTO users (firstname, lastname, email, password, gender, bio, avatar) VALUES (?, ?, ?, ?, ?, ?, ?)", users)

    # Posts from user's screenshots:
    posts = [
        ("Hi from japan", "", "", 2),
        ("i just love this pic", "https://images.unsplash.com/photo-1542038784456-1ea8e935640e?w=800&auto=format&fit=crop&q=80", "", 3),
        ("my photography", "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800&auto=format&fit=crop&q=80", "", 3)
    ]
    c.executemany("INSERT INTO posts (caption, image, video, user_id) VALUES (?, ?, ?, ?)", posts)

    # Post likes & comments
    c.execute("INSERT INTO post_likes (post_id, user_id) VALUES (1, 1)")
    c.execute("INSERT INTO comments (content, post_id, user_id) VALUES ('Welcome to Japan!', 1, 1)")
    c.execute("INSERT INTO comments (content, post_id, user_id) VALUES ('Great perspective!', 3, 2)")
    c.execute("INSERT INTO post_likes (post_id, user_id) VALUES (3, 1)")
    c.execute("INSERT INTO post_likes (post_id, user_id) VALUES (3, 2)")

    # Reels from screenshots:
    reels = [
        ("Travel Vlog in kashi", "https://assets.mixkit.co/videos/preview/mixkit-aerial-view-of-city-traffic-at-night-42880-large.mp4", 2)
    ]
    c.executemany("INSERT INTO reels (title, video, user_id) VALUES (?, ?, ?)", reels)

    # Chats from screenshots:
    c.execute("INSERT INTO chats (chat_name) VALUES ('siddharth & hisoka')")
    chat_id = c.lastrowid
    c.execute("INSERT INTO chat_users (chat_id, user_id) VALUES (?, 1)", (chat_id,))
    c.execute("INSERT INTO chat_users (chat_id, user_id) VALUES (?, 2)", (chat_id,))
    c.execute("INSERT INTO messages (chat_id, user_id, content) VALUES (?, 1, 'hey')", (chat_id,))

    conn.commit()

# --- Auth Helpers ---
def authenticate_user(email, password):
    conn = get_connection()
    c = conn.cursor()
    hashed = hash_password(password)
    c.execute("SELECT * FROM users WHERE email = ? AND (password = ? OR password = ?)", (email.strip().lower(), hashed, password))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def register_user(firstname, lastname, email, password, gender="other", bio="", avatar=""):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE email = ?", (email.strip().lower(),))
    if c.fetchone():
        conn.close()
        raise ValueError("This email is already registered with another account.")
    hashed = hash_password(password)
    c.execute("""
    INSERT INTO users (firstname, lastname, email, password, gender, bio, avatar)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (firstname.strip(), lastname.strip(), email.strip().lower(), hashed, gender, bio, avatar))
    conn.commit()
    uid = c.lastrowid
    user = get_user_by_id(uid, conn)
    conn.close()
    return user

def get_user_by_id(user_id, conn=None):
    close_after = False
    if conn is None:
        conn = get_connection()
        close_after = True
    c = conn.cursor()
    c.execute("SELECT id, firstname, lastname, email, gender, bio, avatar, created_at FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    if not row:
        if close_after: conn.close()
        return None
    user = dict(row)
    c.execute("SELECT follower_id FROM user_follows WHERE following_id = ?", (user_id,))
    user['followers'] = [r[0] for r in c.fetchall()]
    c.execute("SELECT following_id FROM user_follows WHERE follower_id = ?", (user_id,))
    user['following'] = [r[0] for r in c.fetchall()]
    c.execute("SELECT post_id FROM saved_posts WHERE user_id = ?", (user_id,))
    user['saved_post_ids'] = [r[0] for r in c.fetchall()]
    if close_after: conn.close()
    return user

def update_user_profile(user_id, firstname, lastname, gender="other"):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    UPDATE users SET firstname = ?, lastname = ?, gender = ? WHERE id = ?
    """, (firstname, lastname, gender, user_id))
    conn.commit()
    user = get_user_by_id(user_id, conn)
    conn.close()
    return user

def get_all_users():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, firstname, lastname, email, gender, bio, avatar FROM users ORDER BY id ASC")
    users = [dict(r) for r in c.fetchall()]
    conn.close()
    return users

def search_users(query):
    conn = get_connection()
    c = conn.cursor()
    q = f"%{query}%"
    c.execute("""
    SELECT id, firstname, lastname, email, gender, bio, avatar
    FROM users
    WHERE firstname LIKE ? OR lastname LIKE ? OR email LIKE ?
    ORDER BY id ASC
    """, (q, q, q))
    users = [dict(r) for r in c.fetchall()]
    conn.close()
    return users

def toggle_follow_user(req_user_id, target_user_id):
    if req_user_id == target_user_id:
        raise ValueError("You cannot follow yourself.")
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT 1 FROM user_follows WHERE follower_id = ? AND following_id = ?", (req_user_id, target_user_id))
    exists = c.fetchone()
    if exists:
        c.execute("DELETE FROM user_follows WHERE follower_id = ? AND following_id = ?", (req_user_id, target_user_id))
        is_following = False
    else:
        c.execute("INSERT INTO user_follows (follower_id, following_id) VALUES (?, ?)", (req_user_id, target_user_id))
        is_following = True
    conn.commit()
    conn.close()
    return is_following

# --- Posts ---
def create_post(user_id, caption, image="", video=""):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    INSERT INTO posts (user_id, caption, image, video) VALUES (?, ?, ?, ?)
    """, (user_id, caption, image, video))
    conn.commit()
    pid = c.lastrowid
    conn.close()
    return get_post_by_id(pid, user_id)

def get_post_by_id(post_id, current_user_id=None):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    SELECT p.id, p.caption, p.image, p.video, p.created_at, p.user_id,
           u.firstname, u.lastname, u.email, u.avatar
    FROM posts p
    JOIN users u ON p.user_id = u.id
    WHERE p.id = ?
    """, (post_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return None
    post = {
        "id": row["id"],
        "caption": row["caption"],
        "image": row["image"],
        "video": row["video"],
        "created_at": row["created_at"],
        "user": {
            "id": row["user_id"],
            "firstname": row["firstname"],
            "lastname": row["lastname"],
            "email": row["email"],
            "avatar": row["avatar"]
        }
    }
    c.execute("SELECT u.id, u.firstname, u.lastname FROM post_likes pl JOIN users u ON pl.user_id = u.id WHERE pl.post_id = ?", (post_id,))
    post["liked"] = [dict(r) for r in c.fetchall()]
    post["like_count"] = len(post["liked"])
    post["is_liked"] = any(u["id"] == current_user_id for u in post["liked"]) if current_user_id else False

    if current_user_id:
        c.execute("SELECT 1 FROM saved_posts WHERE post_id = ? AND user_id = ?", (post_id, current_user_id))
        post["is_saved"] = c.fetchone() is not None
    else:
        post["is_saved"] = False

    c.execute("""
    SELECT cm.id, cm.content, cm.created_at, cm.user_id,
           u.firstname, u.lastname, u.avatar
    FROM comments cm
    JOIN users u ON cm.user_id = u.id
    WHERE cm.post_id = ?
    ORDER BY cm.created_at ASC
    """, (post_id,))
    comments = []
    for cr in c.fetchall():
        comm = {
            "id": cr["id"],
            "content": cr["content"],
            "created_at": cr["created_at"],
            "user": {
                "id": cr["user_id"],
                "firstname": cr["firstname"],
                "lastname": cr["lastname"],
                "avatar": cr["avatar"]
            }
        }
        c.execute("SELECT user_id FROM comment_likes WHERE comment_id = ?", (cr["id"],))
        comm["likes"] = [r[0] for r in c.fetchall()]
        comm["like_count"] = len(comm["likes"])
        comm["is_liked"] = (current_user_id in comm["likes"]) if current_user_id else False
        comments.append(comm)

    post["comments"] = comments
    post["comment_count"] = len(comments)
    conn.close()
    return post

def get_all_posts(current_user_id=None):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM posts ORDER BY id DESC")
    post_ids = [r[0] for r in c.fetchall()]
    conn.close()
    posts = [get_post_by_id(pid, current_user_id) for pid in post_ids]
    return [p for p in posts if p is not None]

def get_user_posts(user_id, current_user_id=None):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM posts WHERE user_id = ? ORDER BY id DESC", (user_id,))
    post_ids = [r[0] for r in c.fetchall()]
    conn.close()
    posts = [get_post_by_id(pid, current_user_id) for pid in post_ids]
    return [p for p in posts if p is not None]

def toggle_like_post(post_id, user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT 1 FROM post_likes WHERE post_id = ? AND user_id = ?", (post_id, user_id))
    if c.fetchone():
        c.execute("DELETE FROM post_likes WHERE post_id = ? AND user_id = ?", (post_id, user_id))
    else:
        c.execute("INSERT INTO post_likes (post_id, user_id) VALUES (?, ?)", (post_id, user_id))
    conn.commit()
    conn.close()
    return get_post_by_id(post_id, user_id)

def toggle_save_post(post_id, user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT 1 FROM saved_posts WHERE post_id = ? AND user_id = ?", (post_id, user_id))
    if c.fetchone():
        c.execute("DELETE FROM saved_posts WHERE post_id = ? AND user_id = ?", (post_id, user_id))
        is_saved = False
    else:
        c.execute("INSERT INTO saved_posts (post_id, user_id) VALUES (?, ?)", (post_id, user_id))
        is_saved = True
    conn.commit()
    conn.close()
    return is_saved

def delete_post(post_id, user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT user_id FROM posts WHERE id = ?", (post_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        raise ValueError("Post not found.")
    if row["user_id"] != user_id:
        conn.close()
        raise PermissionError("You cannot delete another user's post.")
    c.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return True

# --- Comments ---
def add_comment(post_id, user_id, content):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)", (post_id, user_id, content.strip()))
    conn.commit()
    conn.close()
    return get_post_by_id(post_id, user_id)

def toggle_like_comment(comment_id, user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT 1 FROM comment_likes WHERE comment_id = ? AND user_id = ?", (comment_id, user_id))
    if c.fetchone():
        c.execute("DELETE FROM comment_likes WHERE comment_id = ? AND user_id = ?", (comment_id, user_id))
    else:
        c.execute("INSERT INTO comment_likes (comment_id, user_id) VALUES (?, ?)", (comment_id, user_id))
    conn.commit()
    conn.close()
    return True

# --- Reels ---
def create_reel(user_id, title, video):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO reels (user_id, title, video) VALUES (?, ?, ?)", (user_id, title.strip(), video.strip()))
    conn.commit()
    rid = c.lastrowid
    conn.close()
    return rid

def get_all_reels():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    SELECT r.id, r.title, r.video, r.created_at, r.user_id,
           u.firstname, u.lastname, u.avatar
    FROM reels r
    JOIN users u ON r.user_id = u.id
    ORDER BY r.id DESC
    """)
    reels = [
        {
            "id": r["id"],
            "title": r["title"],
            "video": r["video"],
            "created_at": r["created_at"],
            "user": {
                "id": r["user_id"],
                "firstname": r["firstname"],
                "lastname": r["lastname"],
                "avatar": r["avatar"]
            }
        } for r in c.fetchall()
    ]
    conn.close()
    return reels

# --- Chats & Messages ---
def get_or_create_chat(user1_id, user2_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    SELECT cu1.chat_id
    FROM chat_users cu1
    JOIN chat_users cu2 ON cu1.chat_id = cu2.chat_id
    WHERE cu1.user_id = ? AND cu2.user_id = ?
    """, (user1_id, user2_id))
    row = c.fetchone()
    if row:
        chat_id = row[0]
    else:
        c.execute("INSERT INTO chats (chat_name) VALUES ('Chat')")
        chat_id = c.lastrowid
        c.execute("INSERT INTO chat_users (chat_id, user_id) VALUES (?, ?)", (chat_id, user1_id))
        c.execute("INSERT INTO chat_users (chat_id, user_id) VALUES (?, ?)", (chat_id, user2_id))
        conn.commit()
    conn.close()
    return chat_id

def get_user_chats(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    SELECT c.id, c.chat_name, c.created_at
    FROM chats c
    JOIN chat_users cu ON c.id = cu.chat_id
    WHERE cu.user_id = ?
    ORDER BY c.id DESC
    """, (user_id,))
    chats = []
    for row in c.fetchall():
        cid = row["id"]
        c.execute("""
        SELECT u.id, u.firstname, u.lastname, u.avatar
        FROM users u
        JOIN chat_users cu ON u.id = cu.user_id
        WHERE cu.chat_id = ?
        """, (cid,))
        members = [dict(u) for u in c.fetchall()]
        other_member = next((m for m in members if m["id"] != user_id), members[0] if members else None)
        c.execute("SELECT content, created_at, user_id FROM messages WHERE chat_id = ? ORDER BY id DESC LIMIT 1", (cid,))
        last_msg = c.fetchone()
        chats.append({
            "id": cid,
            "chat_name": row["chat_name"],
            "created_at": row["created_at"],
            "other_user": other_member,
            "last_message": dict(last_msg) if last_msg else None
        })
    conn.close()
    return chats

def get_chat_messages(chat_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    SELECT m.id, m.content, m.image, m.created_at, m.user_id,
           u.firstname, u.lastname, u.avatar
    FROM messages m
    JOIN users u ON m.user_id = u.id
    WHERE m.chat_id = ?
    ORDER BY m.id ASC
    """, (chat_id,))
    messages = [
        {
            "id": r["id"],
            "content": r["content"],
            "image": r["image"],
            "created_at": r["created_at"],
            "user": {
                "id": r["user_id"],
                "firstname": r["firstname"],
                "lastname": r["lastname"],
                "avatar": r["avatar"]
            }
        } for r in c.fetchall()
    ]
    conn.close()
    return messages

def send_chat_message(chat_id, user_id, content, image=""):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    INSERT INTO messages (chat_id, user_id, content, image) VALUES (?, ?, ?, ?)
    """, (chat_id, user_id, content.strip(), image.strip()))
    conn.commit()
    msg_id = c.lastrowid
    conn.close()
    return msg_id
