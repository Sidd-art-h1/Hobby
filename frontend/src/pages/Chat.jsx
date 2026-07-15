import { useEffect, useRef, useState } from "react";
import { Send, Search, MessageCircle } from "lucide-react";
import Avatar from "../components/Avatar";
import {
  getMyChats,
  createChat,
  getChatMessages,
  sendMessage,
  searchUsers,
} from "../api/endpoints";
import { useAuth } from "../context/AuthContext";

export default function Chat() {
  const { user: me } = useAuth();
  const [chats, setChats] = useState([]);
  const [activeChat, setActiveChat] = useState(null);
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loadingChats, setLoadingChats] = useState(true);
  const bottomRef = useRef(null);

  const loadChats = () => {
    setLoadingChats(true);
    getMyChats()
      .then((res) => setChats(res.data))
      .finally(() => setLoadingChats(false));
  };

  useEffect(loadChats, []);

  useEffect(() => {
    if (!activeChat) return;
    getChatMessages(activeChat.id).then((res) => setMessages(res.data));
    const interval = setInterval(() => {
      getChatMessages(activeChat.id).then((res) => setMessages(res.data));
    }, 4000);
    return () => clearInterval(interval);
  }, [activeChat]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      return;
    }
    const t = setTimeout(() => {
      searchUsers(query).then((res) => setResults(res.data.filter((u) => u.id !== me?.id)));
    }, 300);
    return () => clearTimeout(t);
  }, [query, me]);

  const openChatWith = async (userId) => {
    const res = await createChat(userId);
    setActiveChat(res.data);
    setQuery("");
    setResults([]);
    loadChats();
  };

  const otherUser = (chat) => chat.users?.find((u) => u.id !== me?.id) || chat.users?.[0];

  const send = async (e) => {
    e.preventDefault();
    if (!text.trim() || !activeChat) return;
    const body = text.trim();
    setText("");
    try {
      const res = await sendMessage(activeChat.id, { content: body, image: "" });
      setMessages((m) => [...m, res.data]);
    } catch {
      alert("Message failed to send.");
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-6 grid grid-cols-1 md:grid-cols-[280px_1fr] gap-4 h-[calc(100vh-64px)]">
      {/* Sidebar */}
      <div className="border border-gray-200 shadow-sm bg-white/70 rounded-lg p-3 flex flex-col overflow-hidden">
        <div className="relative mb-3">
          <Search size={15} className="absolute left-2.5 top-2.5 text-gray-400" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Find a maker…"
            className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-8 pr-3 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500"
          />
        </div>

        {results.length > 0 && (
          <div className="mb-3 border-b border-dashed border-gray-200 pb-2 space-y-1">
            {results.map((u) => (
              <button
                key={u.id}
                onClick={() => openChatWith(u.id)}
                className="w-full flex items-center gap-2 text-left px-2 py-1.5 rounded-lg hover:bg-violet-50"
              >
                <Avatar firstname={u.firstname} lastname={u.lastname} size={28} />
                <span className="text-sm">{u.firstname} {u.lastname}</span>
              </button>
            ))}
          </div>
        )}

        <div className="flex-1 overflow-y-auto scrollbar-thin space-y-1">
          {loadingChats && <p className="text-xs text-gray-400 font-mono px-2">loading…</p>}
          {!loadingChats && chats.length === 0 && (
            <p className="text-xs text-gray-400 px-2">Search a name above to start chatting.</p>
          )}
          {chats.map((chat) => {
            const other = otherUser(chat);
            return (
              <button
                key={chat.id}
                onClick={() => setActiveChat(chat)}
                className={`w-full flex items-center gap-2 text-left px-2 py-2 rounded-lg transition-colors ${
                  activeChat?.id === chat.id ? "bg-violet-100" : "hover:bg-violet-50"
                }`}
              >
                <Avatar firstname={other?.firstname} lastname={other?.lastname} size={30} />
                <span className="text-sm font-medium truncate">
                  {other?.firstname} {other?.lastname}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Conversation */}
      <div className="border border-gray-200 shadow-sm bg-white/70 rounded-lg flex flex-col overflow-hidden">
        {!activeChat ? (
          <div className="flex-1 flex flex-col items-center justify-center text-gray-300 gap-2">
            <MessageCircle size={32} />
            <p className="text-sm">Pick a conversation to open it</p>
          </div>
        ) : (
          <>
            <div className="flex items-center gap-2 px-4 py-3 border-b border-gray-200">
              <Avatar
                firstname={otherUser(activeChat)?.firstname}
                lastname={otherUser(activeChat)?.lastname}
                size={30}
              />
              <p className="font-medium text-sm">
                {otherUser(activeChat)?.firstname} {otherUser(activeChat)?.lastname}
              </p>
            </div>
            <div className="flex-1 overflow-y-auto scrollbar-thin px-4 py-3 space-y-2">
              {messages.map((m) => {
                const mine = m.user?.id === me?.id;
                return (
                  <div key={m.id} className={`flex ${mine ? "justify-end" : "justify-start"}`}>
                    <div
                      className={`max-w-[70%] px-3 py-1.5 rounded-lg text-sm ${
                        mine ? "bg-violet-600 text-white" : "bg-gray-100 text-gray-900"
                      }`}
                    >
                      {m.content}
                    </div>
                  </div>
                );
              })}
              <div ref={bottomRef} />
            </div>
            <form onSubmit={send} className="flex gap-2 p-3 border-t border-gray-200">
              <input
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Write a message…"
                className="flex-1 bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500"
              />
              <button
                type="submit"
                className="bg-violet-600 hover:bg-violet-700 text-white px-3 rounded-lg"
              >
                <Send size={16} />
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  );
}
