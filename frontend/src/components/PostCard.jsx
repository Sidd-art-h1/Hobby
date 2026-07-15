import { useState } from "react";
import { Link } from "react-router-dom";
import { Heart, Bookmark, MessageSquare, Trash2 } from "lucide-react";
import Avatar from "./Avatar";
import { likePost, savePost, deletePost } from "../api/endpoints";
import { useAuth } from "../context/AuthContext";
import CommentSection from "./CommentSection";

export default function PostCard({ post, onDeleted }) {
  const { user } = useAuth();
  const [liked, setLiked] = useState(
    !!post.liked?.some((u) => u.id === user?.id)
  );
  const [likeCount, setLikeCount] = useState(post.liked?.length ?? 0);
  const [saved, setSaved] = useState(
    !!user?.savedPost?.some((p) => p.id === post.id)
  );
  const [showComments, setShowComments] = useState(false);
  const [busy, setBusy] = useState(false);

  const isMine = user?.id === post.user?.id;

  const toggleLike = async () => {
    if (busy) return;
    setBusy(true);
    const prevLiked = liked;
    setLiked(!prevLiked);
    setLikeCount((c) => (prevLiked ? c - 1 : c + 1));
    try {
      await likePost(post.id);
    } catch {
      setLiked(prevLiked);
      setLikeCount((c) => (prevLiked ? c + 1 : c - 1));
    } finally {
      setBusy(false);
    }
  };

  const toggleSave = async () => {
    if (busy) return;
    setBusy(true);
    const prev = saved;
    setSaved(!prev);
    try {
      await savePost(post.id);
    } catch {
      setSaved(prev);
    } finally {
      setBusy(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm("Remove this entry from your journal?")) return;
    try {
      await deletePost(post.id);
      onDeleted?.(post.id);
    } catch (e) {
      alert(e.response?.data?.message || "Couldn't delete this post.");
    }
  };

  return (
    <article className="border border-gray-200 shadow-sm bg-white/70 rounded-lg p-4">
      <div className="flex items-center justify-between mb-3">
        <Link
          to={`/profile/${post.user?.id}`}
          className="flex items-center gap-2.5 group"
        >
          <Avatar firstname={post.user?.firstname} lastname={post.user?.lastname} size={34} />
          <div>
            <p className="text-sm font-semibold text-gray-900 group-hover:text-violet-700">
              {post.user?.firstname} {post.user?.lastname}
            </p>
            <p className="text-xs text-gray-500 text-gray-400">
              {post.createdAt ? new Date(post.createdAt).toLocaleDateString() : "just now"}
            </p>
          </div>
        </Link>
        {isMine && (
          <button
            onClick={handleDelete}
            className="text-gray-300 hover:text-orange-600 transition-colors p-1"
            title="Delete post"
          >
            <Trash2 size={16} />
          </button>
        )}
      </div>

      {post.caption && (
        <p className="text-[15px] leading-relaxed text-gray-900 mb-3 whitespace-pre-wrap">
          {post.caption}
        </p>
      )}

      {post.image && (
        <img
          src={post.image}
          alt="post"
          className="w-full max-h-[520px] object-cover rounded-lg border border-gray-200 mb-1"
          onError={(e) => (e.currentTarget.style.display = "none")}
        />
      )}
      {post.video && (
        <video
          src={post.video}
          controls
          className="w-full max-h-[520px] rounded-lg border border-gray-200 mb-1"
        />
      )}

      <div className="flex items-center gap-4 mt-3 pt-3 border-t border-dashed border-gray-200">
        <button
          onClick={toggleLike}
          className={`flex items-center gap-1.5 text-sm transition-colors ${
            liked ? "text-orange-600" : "text-gray-500 hover:text-orange-600"
          }`}
        >
          <Heart size={18} fill={liked ? "currentColor" : "none"} />
          {likeCount}
        </button>
        <button
          onClick={() => setShowComments((s) => !s)}
          className="flex items-center gap-1.5 text-sm text-gray-500 hover:text-violet-700 transition-colors"
        >
          <MessageSquare size={18} />
          {post.comments?.length ?? 0}
        </button>
        <button
          onClick={toggleSave}
          className={`ml-auto flex items-center gap-1.5 text-sm transition-colors ${
            saved ? "text-violet-700" : "text-gray-500 hover:text-violet-700"
          }`}
        >
          <Bookmark size={18} fill={saved ? "currentColor" : "none"} />
        </button>
      </div>

      {showComments && <CommentSection postId={post.id} initialComments={post.comments} />}
    </article>
  );
}
