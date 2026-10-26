import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Pencil, UserPlus, UserCheck } from "lucide-react";
import Avatar from "../components/Avatar";
import PostCard from "../components/PostCard";
import EditProfileModal from "../components/EditProfileModal";
import { getUserById, getPostsByUser, followUser } from "../api/endpoints";
import { useAuth } from "../context/AuthContext";

export default function Profile() {
  const { userId } = useParams();
  const { user: me, refreshProfile } = useAuth();
  const [profile, setProfile] = useState(null);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [followBusy, setFollowBusy] = useState(false);

  const isMe = me?.id === Number(userId);

  const load = () => {
    setLoading(true);
    Promise.all([getUserById(userId), getPostsByUser(userId)])
      .then(([u, p]) => {
        setProfile(u.data);
        setPosts(p.data.slice().reverse());
      })
      .finally(() => setLoading(false));
  };

  useEffect(load, [userId]);

  const isFollowing = profile?.followers?.includes(me?.id);

  const toggleFollow = async () => {
    setFollowBusy(true);
    try {
      await followUser(profile.id);
      load();
      if (isMe) refreshProfile();
    } finally {
      setFollowBusy(false);
    }
  };

  if (loading) return <p className="text-center py-16 text-gray-400 text-sm font-mono">loading profile…</p>;
  if (!profile) return <p className="text-center py-16 text-gray-400 text-sm">User not found.</p>;

  return (
    <div className="max-w-xl mx-auto px-4 py-6">
      <div className="border border-gray-200 shadow-sm bg-white/70 rounded-lg p-6 mb-6 flex items-center gap-5">
        <Avatar firstname={profile.firstname} lastname={profile.lastname} size={68} />
        <div className="flex-1">
          <h1 className="font-display font-semibold text-2xl text-gray-900">
            {profile.firstname} {profile.lastname}
          </h1>
          <p className="text-gray-500 text-sm">{profile.email}</p>
          <div className="flex gap-4 mt-2 text-xs text-gray-500">
            <span>{posts.length} entries</span>
            <span>{profile.followers?.length ?? 0} followers</span>
            <span>{profile.following?.length ?? 0} following</span>
          </div>
        </div>

        {isMe ? (
          <button
            onClick={() => setEditing(true)}
            className="flex items-center gap-1.5 text-sm border border-gray-200 px-3 py-1.5 rounded-lg hover:border-violet-500 hover:text-violet-700 transition-colors"
          >
            <Pencil size={14} /> Edit
          </button>
        ) : (
          <button
            onClick={toggleFollow}
            disabled={followBusy}
            className={`flex items-center gap-1.5 text-sm px-3 py-1.5 rounded-lg transition-colors ${
              isFollowing
                ? "border border-gray-200 text-gray-600 hover:border-orange-500 hover:text-orange-600"
                : "bg-violet-600 hover:bg-violet-700 text-white"
            }`}
          >
            {isFollowing ? <UserCheck size={14} /> : <UserPlus size={14} />}
            {isFollowing ? "Following" : "Follow"}
          </button>
        )}
      </div>

      <div className="space-y-5">
        {posts.length === 0 && (
          <p className="text-center text-gray-400 text-sm py-8">No entries yet.</p>
        )}
        {posts.map((post) => (
          <PostCard
            key={post.id}
            post={post}
            onDeleted={(id) => setPosts((ps) => ps.filter((p) => p.id !== id))}
          />
        ))}
      </div>

      {editing && (
        <EditProfileModal
          profile={profile}
          onClose={() => setEditing(false)}
          onSaved={(u) => {
            setProfile(u);
            setEditing(false);
            refreshProfile();
          }}
        />
      )}
    </div>
  );
}
