import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export default function Signup() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    firstname: "",
    lastname: "",
    email: "",
    password: "",
    gender: "",
  });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const set = (key) => (e) => setForm({ ...form, [key]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await register(form);
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.message || "Couldn't create your account.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-sm">
        <div className="flex flex-col items-center mb-8">
          <img src="/logo.png" alt="Hobby" className="w-14 h-14 object-contain mb-2" />
          <h1 className="font-display font-semibold text-3xl text-gray-900">Hobby</h1>
          <p className="text-gray-500 text-sm mt-1">start your journal</p>
        </div>

        <form onSubmit={submit} className="border border-gray-200 shadow-sm bg-white/70 rounded-lg p-6 space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs text-gray-500 text-gray-500 block mb-1">First name</label>
              <input
                required
                value={form.firstname}
                onChange={set("firstname")}
                className="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500"
              />
            </div>
            <div>
              <label className="text-xs text-gray-500 text-gray-500 block mb-1">Last name</label>
              <input
                required
                value={form.lastname}
                onChange={set("lastname")}
                className="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500"
              />
            </div>
          </div>
          <div>
            <label className="text-xs text-gray-500 text-gray-500 block mb-1">Email</label>
            <input
              required
              type="email"
              value={form.email}
              onChange={set("email")}
              className="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500"
            />
          </div>
          <div>
            <label className="text-xs text-gray-500 text-gray-500 block mb-1">Password</label>
            <input
              required
              type="password"
              minLength={4}
              value={form.password}
              onChange={set("password")}
              className="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500"
            />
          </div>
          <div>
            <label className="text-xs text-gray-500 text-gray-500 block mb-1">Gender (optional)</label>
            <select
              value={form.gender}
              onChange={set("gender")}
              className="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500"
            >
              <option value="">Prefer not to say</option>
              <option value="female">Female</option>
              <option value="male">Male</option>
              <option value="other">Other</option>
            </select>
          </div>

          {error && <p className="text-orange-600 text-xs">{error}</p>}

          <button
            type="submit"
            disabled={busy}
            className="w-full bg-violet-600 hover:bg-violet-700 disabled:opacity-40 text-white font-medium py-2.5 rounded-lg transition-colors"
          >
            {busy ? "Creating…" : "Create account"}
          </button>
        </form>

        <p className="text-center text-sm text-gray-500 mt-5">
          Already have an account?{" "}
          <Link to="/login" className="text-violet-700 font-medium hover:underline">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
