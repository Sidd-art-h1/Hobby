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
# apply the CORS fix in BACKEND_CORS_FIX.md first, then:
./mvnw spring-boot:run
```

Make sure MySQL is running locally and `hobby_db` exists (or let
`spring.jpa.hibernate.ddl-auto=update` create the tables on first run):

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

## Notes for the resume / interview

- Talk through the JWT flow: stateless auth via a custom `OncePerRequestFilter`,
  token issued on signup/login, verified per-request, no server-side sessions.
- Mention the axios interceptor pattern used to attach the auth header globally
  and handle 401s by redirecting to login — a common real-world pattern.
- The design deliberately avoids a generic template look — worth a sentence in
  an interview about design decisions, not just functionality.
- Known simplification: media (images/videos) are stored as URLs, not uploaded
  files — a natural "what would you improve" answer is adding an upload
  endpoint (S3/local disk + multipart form data) instead of URL-only fields.
