"""
API Client for Hobby Spring Boot Backend.
Matches the endpoints defined in frontend/src/api/endpoints.js.
Allows the Streamlit application to communicate directly with the Spring Boot REST API
running on http://localhost:6767.
"""

import requests

DEFAULT_BASE_URL = "http://localhost:6767"

class HobbyApiClient:
    def __init__(self, base_url=DEFAULT_BASE_URL, token=None):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def set_token(self, token):
        self.token = token

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def ping(self):
        """Check if backend is reachable."""
        try:
            r = requests.get(f"{self.base_url}/api/posts", headers=self._headers(), timeout=2)
            return r.status_code != 0
        except Exception:
            return False

    # ---- Auth ----
    def signup(self, firstname, lastname, email, password):
        url = f"{self.base_url}/auth/signup"
        res = requests.post(url, json={
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "password": password
        }, timeout=5)
        res.raise_for_status()
        return res.json()

    def signin(self, email, password):
        url = f"{self.base_url}/auth/signin"
        res = requests.post(url, json={"email": email, "password": password}, timeout=5)
        res.raise_for_status()
        return res.json()

    # ---- Users ----
    def get_my_profile(self):
        url = f"{self.base_url}/api/users/profile"
        res = requests.get(url, headers=self._headers(), timeout=5)
        res.raise_for_status()
        return res.json()

    def get_user_by_id(self, user_id):
        url = f"{self.base_url}/api/users/{user_id}"
        res = requests.get(url, headers=self._headers(), timeout=5)
        res.raise_for_status()
        return res.json()

    def update_user(self, data):
        url = f"{self.base_url}/api/users"
        res = requests.put(url, json=data, headers=self._headers(), timeout=5)
        res.raise_for_status()
        return res.json()

    def follow_user(self, user_id):
        url = f"{self.base_url}/api/users/follow/{user_id}"
        res = requests.put(url, headers=self._headers(), timeout=5)
        res.raise_for_status()
        return res.json()

    def search_users(self, query):
        url = f"{self.base_url}/api/users/search"
        res = requests.get(url, params={"query": query}, headers=self._headers(), timeout=5)
        res.raise_for_status()
        return res.json()

    # ---- Posts ----
    def get_all_posts(self):
        url = f"{self.base_url}/api/posts"
        res = requests.get(url, headers=self._headers(), timeout=5)
        res.raise_for_status()
        return res.json()

    def get_post_by_id(self, post_id):
        url = f"{self.base_url}/api/post/{post_id}"
        res = requests.get(url, headers=self._headers(), timeout=5)
        res.raise_for_status()
        return res.json()

    def get_posts_by_user(self, user_id):
        url = f"{self.base_url}/api/post/user/{user_id}"
        res = requests.get(url, headers=self._headers(), timeout=5)
        res.raise_for_status()
        return res.json()

    def create_post(self, caption, image="", video=""):
        url = f"{self.base_url}/api/posts"
        res = requests.post(url, json={"caption": caption, "image": image, "video": video}, headers=self._headers(), timeout=5)
        res.raise_for_status()
        return res.json()

    def delete_post(self, post_id):
        url = f"{self.base_url}/api/posts/{post_id}"
        res = requests.delete(url, headers=self._headers(), timeout=5)
        res.raise_for_status()
        return res.json()

    def like_post(self, post_id):
        url = f"{self.base_url}/api/posts/like/{post_id}"
        res = requests.put(url, headers=self._headers(), timeout=5)
        res.raise_for_status()
        return res.json()

    def save_post(self, post_id):
        url = f"{self.base_url}/api/posts/save/{post_id}"
        res = requests.put(url, headers=self._headers(), timeout=5)
        res.raise_for_status()
        return res.json()

    # ---- Comments ----
    def create_comment(self, post_id, content):
        url = f"{self.base_url}/api/comments/post/{post_id}"
        res = requests.post(url, json={"content": content}, headers=self._headers(), timeout=5)
        res.raise_for_status()
        return res.json()

    def like_comment(self, comment_id):
        url = f"{self.base_url}/api/comments/like/{comment_id}"
        res = requests.put(url, headers=self._headers(), timeout=5)
        res.raise_for_status()
        return res.json()

    # ---- Reels ----
    def get_all_reels(self):
        url = f"{self.base_url}/api/reels"
        res = requests.get(url, headers=self._headers(), timeout=5)
        res.raise_for_status()
        return res.json()

    def create_reel(self, title, video):
        url = f"{self.base_url}/api/reels"
        res = requests.post(url, json={"title": title, "video": video}, headers=self._headers(), timeout=5)
        res.raise_for_status()
        return res.json()

    # ---- Chat & Messages ----
    def get_my_chats(self):
        url = f"{self.base_url}/api/chats"
        res = requests.get(url, headers=self._headers(), timeout=5)
        res.raise_for_status()
        return res.json()

    def create_chat(self, user_id):
        url = f"{self.base_url}/api/chats"
        res = requests.post(url, json={"userId": user_id}, headers=self._headers(), timeout=5)
        res.raise_for_status()
        return res.json()

    def get_chat_messages(self, chat_id):
        url = f"{self.base_url}/api/messages/chat/{chat_id}"
        res = requests.get(url, headers=self._headers(), timeout=5)
        res.raise_for_status()
        return res.json()

    def send_message(self, chat_id, content, image=""):
        url = f"{self.base_url}/api/messages/chat/{chat_id}"
        res = requests.post(url, json={"content": content, "image": image}, headers=self._headers(), timeout=5)
        res.raise_for_status()
        return res.json()
