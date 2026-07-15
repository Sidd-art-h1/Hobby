import { NavLink, useNavigate } from "react-router-dom";
import { Home, Film, MessageCircle, User, LogOut } from "lucide-react";
import { useAuth } from "../context/AuthContext";

const linkBase =
  "flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors";
const active = "text-violet-700 bg-violet-100";
const inactive = "text-gray-600 hover:text-violet-700 hover:bg-violet-50";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <header className="sticky top-0 z-40 border-b border-gray-200 bg-white/95 backdrop-blur">
      <div className="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
        <NavLink to="/" className="flex items-center gap-2">
          <img src="/logo.png" alt="Hobby" className="w-7 h-7 object-contain" />
          <span className="font-display font-semibold text-xl tracking-tight text-gray-900">Hobby</span>
        </NavLink>

        <nav className="flex items-center gap-1">
          <NavLink to="/" end className={({ isActive }) => `${linkBase} ${isActive ? active : inactive}`}>
            <Home size={17} />
            <span className="hidden sm:inline">Feed</span>
          </NavLink>
          <NavLink to="/reels" className={({ isActive }) => `${linkBase} ${isActive ? active : inactive}`}>
            <Film size={17} />
            <span className="hidden sm:inline">Reels</span>
          </NavLink>
          <NavLink to="/chat" className={({ isActive }) => `${linkBase} ${isActive ? active : inactive}`}>
            <MessageCircle size={17} />
            <span className="hidden sm:inline">Chat</span>
          </NavLink>
          <NavLink
            to={user ? `/profile/${user.id}` : "/login"}
            className={({ isActive }) => `${linkBase} ${isActive ? active : inactive}`}
          >
            <User size={17} />
            <span className="hidden sm:inline">Profile</span>
          </NavLink>
          <button
            onClick={() => {
              logout();
              navigate("/login");
            }}
            className={`${linkBase} ${inactive}`}
            title="Log out"
          >
            <LogOut size={17} />
          </button>
        </nav>
      </div>
    </header>
  );
}
