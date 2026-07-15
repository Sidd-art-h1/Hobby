import { useState } from "react";
import { Heart, Send } from "lucide-react";
import Avatar from "./Avatar";
import { createComment, likeComment } from "../api/endpoints";
import { useAuth } from "../context/AuthContext";

export default function CommentSection({ postId, initialComments = [] }) {
  const { user } = useAuth();
  const [comments, setComments] = useState(initialComments);
  const [text, setText] = useState("");
  const [posting, setPosting] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    if (!text.trim() || posting) return;
    setPosting(true);
    try {
      const res = await createComment(postId, text.trim());
      setComments((c) => [...c, { ...res.data, user: res.data.user ?? user }]);
      setText("");
    } catch (e) {
      alert(e.response?.data?.message || "Couldn't post comment.");
    } finally {
      setPosting(false);
    }
  };

  const toggleLikeComment = async (commentId) => {
    try {
      const res = await likeComment(commentId);
      setComments((cs) => cs.map((c) => (c.id === commentId ? res.data : c)));
    } catch {
      /* silent */
    }
  };

  return (
    <div className="mt-3 pt-3 border-t border-dashed border-gray-200">
      <div className="space-y-2.5 max-h-64 overflow-y-auto scrollbar-thin mb-3">
        {comments.length === 0 && (
          <p className="text-xs text-gray-400 italic">No comments yet — be the first.</p>
        )}
        {comments.map((c) => (
          <div key={c.id} className="flex items-start gap-2">
            <Avatar firstname={c.user?.firstname} lastname={c.user?.lastname} size={26} />
            <div className="flex-1 bg-gray-100 rounded-lg px-2.5 py-1.5">
              <p className="text-xs font-semibold text-gray-800">
                {c.user?.firstname} {c.user?.lastname}
              </p>
              <p className="text-sm text-gray-900">{c.content}</p>
            </div>
            <button
              onClick={() => toggleLikeComment(c.id)}
              className="text-gray-300 hover:text-orange-600 flex items-center gap-0.5 text-xs mt-1.5"
            >
              <Heart size={13} fill={c.liked?.some((u) => u.id === user?.id) ? "currentColor" : "none"} />
              {c.liked?.length > 0 && c.liked.length}
            </button>
          </div>
        ))}
      </div>
      <form onSubmit={submit} className="flex gap-2">
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Add a note…"
          className="flex-1 text-sm bg-white border border-gray-200 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-violet-500"
        />
        <button
          type="submit"
          disabled={posting}
          className="text-violet-700 hover:text-violet-900 disabled:opacity-40"
        >
          <Send size={17} />
        </button>
      </form>
    </div>
  );
}
