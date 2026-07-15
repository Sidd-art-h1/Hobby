import { useEffect, useState } from "react";
import { Plus, Film, X } from "lucide-react";
import { getAllReels, createReel } from "../api/endpoints";
import { Link } from "react-router-dom";

export default function Reels() {
  const [reels, setReels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ title: "", video: "" });
  const [busy, setBusy] = useState(false);

  const load = () => {
    setLoading(true);
    getAllReels()
      .then((res) => setReels(res.data.slice().reverse()))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const submit = async (e) => {
    e.preventDefault();
    if (!form.video.trim()) return;
    setBusy(true);
    try {
      const res = await createReel(form);
      setReels((r) => [res.data, ...r]);
      setForm({ title: "", video: "" });
      setShowForm(false);
    } catch {
      alert("Couldn't publish that reel.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-6">
      <div className="flex items-center justify-between mb-5">
        <h1 className="font-display font-semibold text-2xl flex items-center gap-2">
          <Film size={22} className="text-orange-500" /> Reels
        </h1>
        <button
          onClick={() => setShowForm((s) => !s)}
          className="flex items-center gap-1.5 bg-violet-600 hover:bg-violet-700 text-white text-sm font-medium px-3 py-1.5 rounded-lg"
        >
          {showForm ? <X size={15} /> : <Plus size={15} />}
          {showForm ? "Cancel" : "New reel"}
        </button>
      </div>

      {showForm && (
        <form onSubmit={submit} className="border border-gray-200 shadow-sm bg-white/70 rounded-lg p-4 mb-6 space-y-2">
          <input
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            placeholder="Title"
            className="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500"
          />
          <input
            required
            value={form.video}
            onChange={(e) => setForm({ ...form, video: e.target.value })}
            placeholder="Video URL"
            className="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500"
          />
          <button
            type="submit"
            disabled={busy}
            className="bg-violet-600 hover:bg-violet-700 disabled:opacity-40 text-white text-sm font-medium px-4 py-2 rounded-lg"
          >
            {busy ? "Publishing…" : "Publish reel"}
          </button>
        </form>
      )}

      {loading && <p className="text-center text-gray-400 text-sm font-mono py-10">loading reels…</p>}
      {!loading && reels.length === 0 && (
        <p className="text-center text-gray-400 text-sm py-10">No reels yet. Share what you're making.</p>
      )}

      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
        {reels.map((reel) => (
          <div key={reel.id} className="border border-gray-200 shadow-sm bg-white/70 rounded-lg p-2">
            <video src={reel.video} controls className="w-full aspect-[9/16] object-cover rounded-lg bg-ink/5" />
            <p className="text-xs font-medium mt-1.5 truncate">{reel.title || "untitled"}</p>
            <Link to={`/profile/${reel.user?.id}`} className="text-xs text-gray-500 text-gray-400 hover:text-violet-700">
              {reel.user?.firstname} {reel.user?.lastname}
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}
