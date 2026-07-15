import api from "./axios";

// ---- Auth (/auth) ----
export const signup = (data) => api.post("/auth/signup", data);
// data: { firstname, lastname, email, password }
export const signin = (data) => api.post("/auth/signin", data);
// data: { email, password }

// ---- Users (/api/users) ----
export const getAllUsers = () => api.get("/api/users");
export const getUserById = (id) => api.get(`/api/users/${id}`);
export const updateUser = (data) => api.put("/api/users", data);
export const followUser = (userId2) => api.put(`/api/users/follow/${userId2}`);
export const searchUsers = (query) =>
  api.get(`/api/users/search`, { params: { query } });
export const getMyProfile = () => api.get("/api/users/profile");

// ---- Posts ----
export const createPost = (data) => api.post("/api/posts", data);
// data: { caption, image, video }
export const deletePost = (postId) => api.delete(`/api/posts/${postId}`);
export const getPostById = (postId) => api.get(`/api/post/${postId}`);
export const getPostsByUser = (userId) => api.get(`/api/post/user/${userId}`);
export const getAllPosts = () => api.get("/api/posts");
export const savePost = (postId) => api.put(`/api/posts/save/${postId}`);
export const likePost = (postId) => api.put(`/api/posts/like/${postId}`);

// ---- Comments ----
export const createComment = (postId, content) =>
  api.post(`/api/comments/post/${postId}`, { content });
export const likeComment = (commentId) =>
  api.put(`/api/comments/like/${commentId}`);

// ---- Reels ----
export const createReel = (data) => api.post("/api/reels", data);
// data: { title, video }
export const getAllReels = () => api.get("/api/reels");
export const getUserReels = (userId) => api.get(`/api/reels/user/${userId}`);

// ---- Chat ----
export const createChat = (userId) => api.post("/api/chats", { userId });
export const getMyChats = () => api.get("/api/chats");

// ---- Messages ----
export const sendMessage = (chatId, data) =>
  api.post(`/api/messages/chat/${chatId}`, data);
// data: { content, image }
export const getChatMessages = (chatId) =>
  api.get(`/api/messages/chat/${chatId}`);
