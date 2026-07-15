import { useState } from "react";
import { ImageIcon, Video, Feather } from "lucide-react";
import { createPost } from "../api/endpoints";
import { useAuth } from "../context/AuthContext";
import Avatar from "./Avatar";

export default function CreatePost({ onCreated }) {
  const { user } = useAuth();
  const [caption, setCaption] = useState("");
  const [image, setImage] = useState("");
  const [video, setVideo] = useState("");
  const [showMedia, setShowMedia] = useState(false);
  const [busy, setBusy] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    if (!caption.trim() && !image.trim() && !video.trim()) return;
    setBusy(true);
    try {
      const res = await createPost({ caption, image, video });
      onCreated?.(res.data);
      setCaption("");
      setImage("");
      setVideo("");
      setShowMedia(false);
    } catch (e) {
      alert(e.response?.data?.message || "Couldn't publish that entry.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <form onSubmit={submit} className="border border-gray-200 shadow-sm bg-white/70 rounded-lg p-4 mb-5">
      <div className="flex gap-3">
        <Avatar firstname={user?.firstname} lastname={user?.lastname} size={36} />
        <textarea
          value={caption}
          onChange={(e) => setCaption(e.target.value)}
          placeholder="What are you working on today?"
          rows={2}
          className="flex-1 resize-none bg-transparent text-[15px] placeholder:text-gray-400 focus:outline-none"
        />
      </div>

      {showMedia && (
        <div className="mt-3 space-y-2 pl-[46px]">
          <input
            value={image}
            onChange={(e) => setImage(e.target.value)}
            placeholder="Image URL (optional)"
            className="w-full text-sm bg-gray-50 border border-gray-200 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-violet-500"
          />
          <input
            value={video}
            onChange={(e) => setVideo(e.target.value)}
            placeholder="Video URL (optional)"
            className="w-full text-sm bg-gray-50 border border-gray-200 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-violet-500"
          />
        </div>
      )}

      <div className="flex items-center justify-between mt-3 pl-[46px]">
        <button
          type="button"
          onClick={() => setShowMedia((s) => !s)}
          className="flex items-center gap-1.5 text-xs text-gray-500 hover:text-violet-700 text-xs text-gray-500"
        >
          <ImageIcon size={14} />
          <Video size={14} />
          media
        </button>
        <button
          type="submit"
          disabled={busy}
          className="flex items-center gap-1.5 bg-violet-600 hover:bg-violet-700 disabled:opacity-40 text-white text-sm font-medium px-4 py-1.5 rounded-lg transition-colors"
        >
          <Feather size={14} />
          {busy ? "Pinning…" : "Post entry"}
        </button>
      </div>
    </form>
  );
}
