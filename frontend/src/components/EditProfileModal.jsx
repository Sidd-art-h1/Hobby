import { useState } from "react";
import { X } from "lucide-react";
import { updateUser } from "../api/endpoints";

export default function EditProfileModal({ profile, onClose, onSaved }) {
  const [form, setForm] = useState({
    firstname: profile.firstname || "",
    lastname: profile.lastname || "",
    gender: profile.gender || "",
  });
  const [busy, setBusy] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      const res = await updateUser({ ...profile, ...form });
      onSaved(res.data);
    } catch {
      alert("Couldn't save changes.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-ink/40 flex items-center justify-center z-50 px-4">
      <div className="border border-gray-200 shadow-sm bg-white rounded-lg p-6 w-full max-w-sm relative">
        <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-gray-900">
          <X size={18} />
        </button>
        <h2 className="text-xl mb-4">Edit profile</h2>
        <form onSubmit={submit} className="space-y-3">
          <div>
            <label className="text-xs text-gray-500 text-gray-500 block mb-1">First name</label>
            <input
              value={form.firstname}
              onChange={(e) => setForm({ ...form, firstname: e.target.value })}
              className="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500"
            />
          </div>
          <div>
            <label className="text-xs text-gray-500 text-gray-500 block mb-1">Last name</label>
            <input
              value={form.lastname}
              onChange={(e) => setForm({ ...form, lastname: e.target.value })}
              className="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500"
            />
          </div>
          <div>
            <label className="text-xs text-gray-500 text-gray-500 block mb-1">Gender</label>
            <select
              value={form.gender}
              onChange={(e) => setForm({ ...form, gender: e.target.value })}
              className="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500"
            >
              <option value="">Prefer not to say</option>
              <option value="female">Female</option>
              <option value="male">Male</option>
              <option value="other">Other</option>
            </select>
          </div>
          <button
            type="submit"
            disabled={busy}
            className="w-full bg-violet-600 hover:bg-violet-700 disabled:opacity-40 text-white font-medium py-2.5 rounded-lg transition-colors mt-2"
          >
            {busy ? "Saving…" : "Save changes"}
          </button>
        </form>
      </div>
    </div>
  );
}
