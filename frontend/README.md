# Hobby — a social platform for makers

A full-stack social media app (React + Spring Boot + MySQL) where users post,
like, comment, follow each other, share short video reels, and direct-message.

## Stack

- **Frontend**: React 18, Vite, React Router, Tailwind CSS, Axios, lucide-react
- **Backend**: Spring Boot, Spring Security (stateless JWT auth), Spring Data JPA
- **Database**: MySQL

## Features implemented

- JWT-based signup/login, token persisted client-side, auto-attached to every request
- Post feed: create, delete, like, save, view by user
- Comments: add comment, like comment
- Follow / unfollow users, profile pages with editable bio fields
- Reels: short-video posting and browsing grid
- Direct messaging: 1:1 chat creation, message history, lightweight polling for new messages
- Protected routing (unauthenticated users redirected to login)

## Running it locally

### 1. Backend

```bash
cd Hobby
./mvnw spring-boot:run
```

Make sure MySQL is running locally and `hobby_db` exists
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS hobby_db;"
```

Backend will be live at `http://localhost:6767`.

### 2. Frontend

```bash
cd hobby-frontend
npm install
npm run dev
```

Frontend will be live at `http://localhost:5173`.
