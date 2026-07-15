import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await login(form.email, form.password);
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.message || "Couldn't sign you in. Check your details.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <div className="flex flex-col items-center mb-8">
          <img src="/logo.png" alt="Hobby" className="w-14 h-14 object-contain mb-2" />
          <h1 className="font-display font-semibold text-3xl text-gray-900">Hobby</h1>
          <p className="text-gray-500 text-sm mt-1">a field journal for makers</p>
        </div>

        <form onSubmit={submit} className="border border-gray-200 shadow-sm bg-white/70 rounded-lg p-6 space-y-4">
          <div>
            <label className="text-xs text-gray-500 text-gray-500 block mb-1">Email</label>
            <input
              required
              type="email"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500"
            />
          </div>
          <div>
            <label className="text-xs text-gray-500 text-gray-500 block mb-1">Password</label>
            <input
              required
              type="password"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              className="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500"
            />
          </div>

          {error && <p className="text-orange-600 text-xs">{error}</p>}

          <button
            type="submit"
            disabled={busy}
            className="w-full bg-violet-600 hover:bg-violet-700 disabled:opacity-40 text-white font-medium py-2.5 rounded-lg transition-colors"
          >
            {busy ? "Signing in…" : "Sign in"}
          </button>
        </form>

        <p className="text-center text-sm text-gray-500 mt-5">
          New here?{" "}
          <Link to="/signup" className="text-violet-700 font-medium hover:underline">
            Create an account
          </Link>
        </p>
      </div>
    </div>
  );
}
