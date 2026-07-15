# Hobby

A full-stack social media application where users post updates, follow each
other, comment and like, share short-form video reels, and message each
other directly — built with a Spring Boot REST API and a React frontend.

## Stack

**Backend:** Java, Spring Boot, Spring Security, Spring Data JPA, MySQL, JWT
**Frontend:** React, Vite, React Router, Tailwind CSS, Axios

## Features

- JWT-based authentication (signup/login), stateless sessions via a custom
  security filter
- Post feed — create, delete, like, save, view posts by user
- Comments — add and like comments on posts
- Follow / unfollow other users, editable profiles
- Reels — short-video posting and browsing
- Direct messaging between users, 1:1 chat threads
- Protected routes on the frontend; unauthenticated users are redirected to login

## Project structure

```
Hobby/
├── backend/     Spring Boot REST API (port 6767)
└── frontend/    React + Vite client (port 5173)
```

## Running locally

### Prerequisites
- Java 21, Maven
- Node.js + npm
- MySQL running locally

### 1. Database
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS hobby_db;"
```

### 2. Backend
```bash
cd backend
cp src/main/resources/application.properties.example src/main/resources/application.properties
# edit application.properties with your local MySQL password
./mvnw spring-boot:run
```
Runs at `http://localhost:6767`.

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```
Runs at `http://localhost:5173`.

## API overview

| Resource | Endpoints |
|---|---|
| Auth | `POST /auth/signup`, `POST /auth/signin` |
| Users | `GET /api/users`, `GET /api/users/{id}`, `PUT /api/users`, `PUT /api/users/follow/{id}`, `GET /api/users/search`, `GET /api/users/profile` |
| Posts | `POST /api/posts`, `DELETE /api/posts/{id}`, `GET /api/post/{id}`, `GET /api/post/user/{id}`, `GET /api/posts`, `PUT /api/posts/save/{id}`, `PUT /api/posts/like/{id}` |
| Comments | `POST /api/comments/post/{postId}`, `PUT /api/comments/like/{commentId}` |
| Reels | `POST /api/reels`, `GET /api/reels`, `GET /api/reels/user/{userId}` |
| Chat | `POST /api/chats`, `GET /api/chats` |
| Messages | `POST /api/messages/chat/{chatId}`, `GET /api/messages/chat/{chatId}` |

All routes under `/api/**` require a `Authorization: Bearer <token>` header,
obtained from `/auth/signin` or `/auth/signup`.

## Notes / possible improvements

- Media (post images, reel videos) are stored as URLs rather than uploaded
  files — a natural next step is a real upload endpoint (multipart form data
  + object storage).
- Chat updates via short-interval polling rather than WebSockets.
