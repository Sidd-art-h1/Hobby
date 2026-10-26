"""
FastAPI Backend for Hobby on Port 6767.
Mirrors the exact Spring Boot REST API endpoints expected by the frontend.
Stores data persistently in SQLite (hobby_data.db).
"""

from fastapi import FastAPI, Header, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import db
import uvicorn

app = FastAPI(title="Hobby API")

# Enable CORS for all local development and Streamlit ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db.init_db()

# --- Request / Response Models ---
class SignupRequest(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str
    gender: Optional[str] = "other"

class SigninRequest(BaseModel):
    email: str
    password: str

class PostCreateRequest(BaseModel):
    caption: Optional[str] = ""
    image: Optional[str] = ""
    video: Optional[str] = ""

class CommentCreateRequest(BaseModel):
    content: str

class ReelCreateRequest(BaseModel):
    title: Optional[str] = ""
    video: str

class CreateChatRequest(BaseModel):
    userId: int

class SendMessageRequest(BaseModel):
    content: str
    image: Optional[str] = ""

class UpdateUserRequest(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    gender: Optional[str] = None

# --- Helper to extract user ID from mock token ---
def get_user_from_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization token")
    token = authorization.replace("Bearer ", "").strip()
    if token.isdigit():
        u = db.get_user_by_id(int(token))
        if u: return u
    for u in db.get_all_users():
        if u["email"].lower() == token.lower():
            return db.get_user_by_id(u["id"])
    raise HTTPException(status_code=401, detail="Invalid authorization token")

# --- Auth Routes ---
@app.post("/auth/signup")
def signup(req: SignupRequest):
    try:
        user = db.register_user(req.firstname, req.lastname, req.email, req.password, req.gender or "other")
        return {"token": str(user["id"]), "message": "Register Success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/signin")
def signin(req: SigninRequest):
    user = db.authenticate_user(req.email, req.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {"token": str(user["id"]), "message": "Login Success"}

# --- Users Routes ---
@app.get("/api/users/profile")
def get_my_profile(authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/api/users/{user_id}")
def get_user_by_id(user_id: int):
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/api/users")
def update_user(req: UpdateUserRequest, authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    fn = req.firstname or user["firstname"]
    ln = req.lastname or user["lastname"]
    gen = req.gender or user.get("gender", "other")
    return db.update_user_profile(user["id"], fn, ln, gen)

@app.put("/api/users/follow/{user_id}")
def follow_user(user_id: int, authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    db.toggle_follow_user(user["id"], user_id)
    return db.get_user_by_id(user_id)

@app.get("/api/users/search")
def search_users(query: str = Query("")):
    return db.search_users(query)

@app.get("/api/users")
def get_all_users():
    return db.get_all_users()

# --- Posts Routes ---
@app.get("/api/posts")
def get_all_posts(authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    uid = user["id"] if user else None
    return db.get_all_posts(uid)

@app.get("/api/post/{post_id}")
def get_post(post_id: int, authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    uid = user["id"] if user else None
    p = db.get_post_by_id(post_id, uid)
    if not p:
        raise HTTPException(status_code=404, detail="Post not found")
    return p

@app.get("/api/post/user/{user_id}")
def get_user_posts(user_id: int, authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    uid = user["id"] if user else None
    return db.get_user_posts(user_id, uid)

@app.post("/api/posts")
def create_post(req: PostCreateRequest, authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    return db.create_post(user["id"], req.caption or "", req.image or "", req.video or "")

@app.delete("/api/posts/{post_id}")
def delete_post(post_id: int, authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    try:
        db.delete_post(post_id, user["id"])
        return {"message": "Post deleted successfully", "status": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/posts/like/{post_id}")
def like_post(post_id: int, authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    return db.toggle_like_post(post_id, user["id"])

@app.put("/api/posts/save/{post_id}")
def save_post(post_id: int, authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    db.toggle_save_post(post_id, user["id"])
    return db.get_post_by_id(post_id, user["id"])

# --- Comments Routes ---
@app.post("/api/comments/post/{post_id}")
def create_comment(post_id: int, req: CommentCreateRequest, authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    post = db.add_comment(post_id, user["id"], req.content)
    # Return newly added comment
    return post["comments"][-1]

@app.put("/api/comments/like/{comment_id}")
def like_comment(comment_id: int, authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    db.toggle_like_comment(comment_id, user["id"])
    return {"message": "Comment like updated", "status": True}

# --- Reels Routes ---
@app.get("/api/reels")
def get_all_reels():
    return db.get_all_reels()

@app.post("/api/reels")
def create_reel(req: ReelCreateRequest, authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    rid = db.create_reel(user["id"], req.title or "", req.video)
    return {"id": rid, "title": req.title, "video": req.video, "user": user}

# --- Chats & Messages Routes ---
@app.get("/api/chats")
def get_chats(authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    return db.get_user_chats(user["id"])

@app.post("/api/chats")
def create_chat(req: CreateChatRequest, authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    cid = db.get_or_create_chat(user["id"], req.userId)
    chats = db.get_user_chats(user["id"])
    chat = next((c for c in chats if c["id"] == cid), None)
    return chat or {"id": cid}

@app.get("/api/messages/chat/{chat_id}")
def get_chat_messages(chat_id: int):
    return db.get_chat_messages(chat_id)

@app.post("/api/messages/chat/{chat_id}")
def send_message(chat_id: int, req: SendMessageRequest, authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    mid = db.send_chat_message(chat_id, user["id"], req.content, req.image or "")
    msgs = db.get_chat_messages(chat_id)
    return msgs[-1]

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=6767, reload=False)
