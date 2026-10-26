# Hobby

A full-stack social media platform where users share updates, follow one another, comment, like, share short-form video reels, and exchange direct messages. The project is delivered in two forms: a complete Spring Boot + React application and a self-contained interactive Streamlit application.

**Live Demo:** https://hobbys.streamlit.app/

## Technology Stack

| Layer | Technologies |
| --- | --- |
| Streamlit App | Python, Streamlit, SQLite (embedded), Pillow, Requests |
| Backend | Java, Spring Boot, Spring Security, Spring Data JPA, MySQL, JWT |
| Frontend | React, Vite, React Router, Tailwind CSS, Axios |

## Running the Streamlit Application

The Streamlit deployment provides a self-contained, interactive version of the full Hobby platform with no external dependencies. Neither MySQL nor Java installation is required. The application comes pre-seeded with makers, posts, comments, reels, and chat threads.

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Launch the Application
```bash
streamlit run app.py
```
On Windows, you may alternatively double-click `run_streamlit.bat`. The application will open at http://localhost:8501.

### Streamlit Features

- **Authentication and Demo Login:** Log in as Siddharth, Maya, Alex, or Chloe, or register a new maker profile.
- **Journal Feed:** Filter by All Entries, Following, Bookmarked, or My Entries. Create entries with markdown captions and direct image or video uploads.
- **Likes and Comments:** Like posts, bookmark favorites, and leave or like comments.
- **Reels:** Short-form video feed with video players and direct reel publishing.
- **Direct Messaging:** Real-time one-to-one chat between makers with message bubbles.
- **Profiles and Follow System:** View profiles, toggle follow or unfollow, and edit your bio and avatar.
- **Discover Makers:** Search creators across the network by name or craft.

## Bug Fixes Applied to the Original Codebase

- **`PostServiceImplementation.java` (Inverted Delete Permission):** Corrected an inverted permission check that blocked authors from deleting their own posts. The check now verifies that the requesting user is the post author before permitting deletion.
- **`UserserviceImplementation.java` (Follow/Unfollow Toggle and Self-Follow):** Added a check to prevent users from following themselves. Converted the follow action into a proper toggle that unfollows when already following and follows otherwise. Removed unsafe primary key entity mutation (`Olduser.setId(...)`).
- **`User.java` (Entity Equality):** Implemented `equals()` and `hashCode()` based on entity ID so that JPA collection methods (`contains`, `remove`) function reliably.
- **`JwtProvider.java` (Bearer Token Parsing):** Added a validation check for the Bearer prefix before stripping it, preventing `StringIndexOutOfBoundsException`.
- **`AppConfig.java` (CORS Whitelist):** Added Streamlit ports (`http://localhost:8501`, `http://127.0.0.1:8501`) to the CORS configuration.
- **Frontend Tailwind Fixes:** Resolved duplicate CSS color class conflicts in `Profile.jsx`, `PostCard.jsx`, and `Reels.jsx`.

## Running the Spring Boot + React Stack Locally

### Prerequisites
- Java 21 and Maven
- Node.js and npm
- MySQL running locally

### 1. Database
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS hobby_db;"
```

### 2. Backend
```bash
cd backend
cp src/main/resources/application.properties.example src/main/resources/application.properties
# Edit application.properties with your local MySQL password
./mvnw spring-boot:run
```
The backend runs at http://localhost:6767.

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```
The frontend runs at http://localhost:5173.

## API Overview

| Resource | Endpoints |
| --- | --- |
| Auth | `POST /auth/signup`, `POST /auth/signin` |
| Users | `GET /api/users`, `GET /api/users/{id}`, `PUT /api/users`, `PUT /api/users/follow/{id}`, `GET /api/users/search`, `GET /api/users/profile` |
| Posts | `POST /api/posts`, `DELETE /api/posts/{id}`, `GET /api/post/{id}`, `GET /api/post/user/{id}`, `GET /api/posts`, `PUT /api/posts/save/{id}`, `PUT /api/posts/like/{id}` |
| Comments | `POST /api/comments/post/{postId}`, `PUT /api/comments/like/{commentId}` |
| Reels | `POST /api/reels`, `GET /api/reels`, `GET /api/reels/user/{userId}` |
| Chat | `POST /api/chats`, `GET /api/chats` |
| Messages | `POST /api/messages/chat/{chatId}`, `GET /api/messages/chat/{chatId}` |

## License

This project is available for personal and educational use.
