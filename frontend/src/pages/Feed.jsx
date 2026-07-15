import { useEffect, useState } from "react";
import { getAllPosts } from "../api/endpoints";
import PostCard from "../components/PostCard";
import CreatePost from "../components/CreatePost";

export default function Feed() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getAllPosts()
      .then((res) => setPosts(res.data.slice().reverse()))
      .catch(() => setError("Couldn't load the feed. Is the backend running on :6767?"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-xl mx-auto px-4 py-6">
      <CreatePost onCreated={(p) => setPosts((ps) => [p, ...ps])} />

      {loading && (
        <p className="text-center text-gray-400 text-sm font-mono py-10">gathering entries…</p>
      )}
      {error && <p className="text-center text-orange-600 text-sm py-10">{error}</p>}
      {!loading && !error && posts.length === 0 && (
        <p className="text-center text-gray-400 text-sm py-10">
          No entries yet. Be the first to post something you made.
        </p>
      )}

      <div className="space-y-5">
        {posts.map((post) => (
          <PostCard
            key={post.id}
            post={post}
            onDeleted={(id) => setPosts((ps) => ps.filter((p) => p.id !== id))}
          />
        ))}
      </div>
    </div>
  );
}
