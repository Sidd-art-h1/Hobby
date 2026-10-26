import streamlit as st
import json
import base64
import os
import db

# Page setup
st.set_page_config(
    page_title="Hobby",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit default UI chrome to preserve the user's exact designed look
st.markdown("""
<style>
    #MainMenu, header, footer, [data-testid="stHeader"], [data-testid="stSidebar"] {
        display: none !important;
        visibility: hidden !important;
    }
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        border: none !important;
        width: 100vw !important;
        height: 100vh !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Load Logo
logo_path = os.path.join(os.path.dirname(__file__), "frontend", "public", "logo.png")
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
else:
    logo_b64 = ""

# Load Initial Data from SQLite
db.init_db()
all_users = db.get_all_users()
all_posts = db.get_all_posts()
all_reels = db.get_all_reels()
all_chats = db.get_user_chats(1)

initial_data_json = json.dumps({
    "users": all_users,
    "posts": all_posts,
    "reels": all_reels,
    "chats": all_chats
})

# Render the user's exact React webpage layout, styles, and components
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hobby</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ["'Inter'", "system-ui", "sans-serif"],
            display: ["'Poppins'", "system-ui", "sans-serif"],
          }},
        }},
      }},
    }}
  </script>
  <style>
    * {{ box-sizing: border-box; }}
    html, body {{
      height: 100%;
      margin: 0;
      background-color: #F7F7F5;
      color: #1F2937;
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
      -webkit-font-smoothing: antialiased;
    }}
    .scrollbar-thin::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    .scrollbar-thin::-webkit-scrollbar-thumb {{ background: #D1D5DB; border-radius: 4px; }}
  </style>
</head>
<body class="bg-[#F7F7F5] min-h-screen flex flex-col">

  <div id="app" class="min-h-screen flex flex-col"></div>

  <script>
    const LOGO_SRC = "{logo_b64}";
    const INITIAL_DATA = {initial_data_json};

    // Load users and state
    let users = [...INITIAL_DATA.users];
    let posts = [...INITIAL_DATA.posts];
    let reels = [...INITIAL_DATA.reels];
    let chats = [...INITIAL_DATA.chats];

    // Check localStorage for an active session; do NOT default to any account!
    let currentUser = null;
    try {{
      const saved = localStorage.getItem("hobby_user");
      if (saved) {{
        const parsed = JSON.parse(saved);
        const matched = users.find(u => u.id === parsed.id || u.email.toLowerCase() === (parsed.email || "").toLowerCase());
        if (matched) {{
          currentUser = matched;
        }} else {{
          currentUser = parsed;
        }}
      }}
    }} catch (e) {{
      currentUser = null;
    }}

    let currentTab = currentUser ? "feed" : "login";
    let viewingProfileId = null;
    let activeChatId = 1;
    let showMediaInputs = false;
    let showNewReelForm = false;
    let showEditModal = false;
    let expandedComments = {{}};
    let authError = "";

    // Palette matching Avatar.jsx
    const PALETTE = ["#5C7A45", "#C4703A", "#374A27", "#A2582B", "#496134"];
    function hashColor(str = "") {{
      let h = 0;
      for (let i = 0; i < str.length; i++) h = str.charCodeAt(i) + ((h << 5) - h);
      return PALETTE[Math.abs(h) % PALETTE.length];
    }}

    function renderAvatar(firstname = "", lastname = "", size = 36) {{
      const initials = `${{firstname?.[0] ?? ""}}${{lastname?.[0] ?? ""}}`.toUpperCase() || "?";
      const bg = hashColor((firstname || "") + (lastname || ""));
      return `
        <div class="rounded-full flex items-center justify-center font-semibold text-white shrink-0"
             style="width: ${{size}}px; height: ${{size}}px; background-color: ${{bg}}; font-size: ${{size * 0.4}}px;">
          ${{initials}}
        </div>
      `;
    }}

    function formatDate(dateStr) {{
      if (!dateStr) return "14/07/2026";
      try {{
        const d = new Date(dateStr);
        if (isNaN(d.getTime())) return "14/07/2026";
        return d.toLocaleDateString("en-GB");
      }} catch {{
        return "14/07/2026";
      }}
    }}

    // Navigation
    function navigate(tab, profileId = null) {{
      authError = "";
      currentTab = tab;
      if (profileId) {{
        viewingProfileId = profileId;
      }} else if (tab === 'profile') {{
        viewingProfileId = currentUser ? currentUser.id : null;
      }}
      render();
      window.scrollTo(0, 0);
    }}

    function logout() {{
      currentUser = null;
      localStorage.removeItem("hobby_user");
      localStorage.removeItem("hobby_token");
      currentTab = "login";
      authError = "";
      render();
    }}

    // Authentication Handlers
    async function submitLogin() {{
      authError = "";
      const emailInput = document.getElementById("login-email");
      const passInput = document.getElementById("login-pass");
      const email = emailInput ? emailInput.value.trim().toLowerCase() : "";
      const pass = passInput ? passInput.value.trim() : "";

      if (!email || !pass) {{
        authError = "Please enter both email and password.";
        render();
        return;
      }}

      // 1. Try API login on port 6767
      try {{
        const res = await fetch("http://localhost:6767/auth/signin", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{ email: email, password: pass }})
        }});
        if (res.ok) {{
          const data = await res.json();
          const pRes = await fetch("http://localhost:6767/api/users/profile", {{
            headers: {{ "Authorization": "Bearer " + data.token }}
          }});
          if (pRes.ok) {{
            currentUser = await pRes.json();
            localStorage.setItem("hobby_user", JSON.stringify(currentUser));
            localStorage.setItem("hobby_token", data.token);
            currentTab = "feed";
            render();
            return;
          }}
        }}
      }} catch (err) {{
        // Fallback to local users list
      }}

      // 2. Check local users list
      const matchedUser = users.find(u => u.email.toLowerCase() === email);
      if (matchedUser) {{
        currentUser = matchedUser;
        localStorage.setItem("hobby_user", JSON.stringify(currentUser));
        localStorage.setItem("hobby_token", String(currentUser.id));
        currentTab = "feed";
        render();
      }} else {{
        authError = "Couldn't sign you in. Check your details.";
        render();
      }}
    }}

    async function submitSignup() {{
      authError = "";
      const fnInput = document.getElementById("reg-fn");
      const lnInput = document.getElementById("reg-ln");
      const emInput = document.getElementById("reg-email");
      const pwInput = document.getElementById("reg-pass");
      const genInput = document.getElementById("reg-gen");

      const fn = fnInput ? fnInput.value.trim() : "";
      const ln = lnInput ? lnInput.value.trim() : "";
      const email = emInput ? emInput.value.trim().toLowerCase() : "";
      const pass = pwInput ? pwInput.value.trim() : "";
      const gender = genInput ? genInput.value : "other";

      if (!fn || !ln || !email || !pass) {{
        authError = "Please fill in all fields.";
        render();
        return;
      }}

      // 1. Try API signup on port 6767
      try {{
        const res = await fetch("http://localhost:6767/auth/signup", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{ firstname: fn, lastname: ln, email: email, password: pass, gender: gender }})
        }});
        if (res.ok) {{
          const data = await res.json();
          const pRes = await fetch("http://localhost:6767/api/users/profile", {{
            headers: {{ "Authorization": "Bearer " + data.token }}
          }});
          if (pRes.ok) {{
            currentUser = await pRes.json();
            users.push(currentUser);
            localStorage.setItem("hobby_user", JSON.stringify(currentUser));
            localStorage.setItem("hobby_token", data.token);
            currentTab = "feed";
            render();
            return;
          }}
        }} else {{
          const errData = await res.json().catch(() => ({{}}));
          authError = errData.detail || "This email is already in use.";
          render();
          return;
        }}
      }} catch (err) {{
        // Fallback local signup
      }}

      // 2. Check if email already registered locally
      const exists = users.some(u => u.email.toLowerCase() === email);
      if (exists) {{
        authError = "This email is already registered with another account.";
        render();
        return;
      }}

      const newUser = {{
        id: Date.now(),
        firstname: fn,
        lastname: ln,
        email: email,
        gender: gender,
        followers: [],
        following: []
      }};
      users.push(newUser);
      currentUser = newUser;
      localStorage.setItem("hobby_user", JSON.stringify(currentUser));
      localStorage.setItem("hobby_token", String(newUser.id));
      currentTab = "feed";
      render();
    }}

    // Actions
    async function submitPost() {{
      const captionInput = document.getElementById("post-caption");
      const imgInput = document.getElementById("post-image");
      const vidInput = document.getElementById("post-video");
      const caption = captionInput ? captionInput.value.trim() : "";
      const image = imgInput ? imgInput.value.trim() : "";
      const video = vidInput ? vidInput.value.trim() : "";

      if (!caption && !image && !video) return;

      const newPost = {{
        id: Date.now(),
        caption: caption,
        image: image,
        video: video,
        created_at: new Date().toISOString(),
        user: currentUser,
        like_count: 0,
        comment_count: 0,
        is_liked: false,
        is_saved: false,
        comments: []
      }};

      posts.unshift(newPost);
      showMediaInputs = false;
      render();

      fetch("http://localhost:6767/api/posts", {{
        method: "POST",
        headers: {{ "Content-Type": "application/json", "Authorization": "Bearer " + (currentUser ? currentUser.id : 1) }},
        body: JSON.stringify({{ caption, image, video }})
      }}).catch(() => {{}});
    }}

    async function toggleLike(postId) {{
      const p = posts.find(x => x.id === postId);
      if (!p) return;
      p.is_liked = !p.is_liked;
      p.like_count += (p.is_liked ? 1 : -1);
      render();

      fetch(`http://localhost:6767/api/posts/like/${{postId}}`, {{
        method: "PUT",
        headers: {{ "Authorization": "Bearer " + (currentUser ? currentUser.id : 1) }}
      }}).catch(() => {{}});
    }}

    async function toggleSave(postId) {{
      const p = posts.find(x => x.id === postId);
      if (!p) return;
      p.is_saved = !p.is_saved;
      render();

      fetch(`http://localhost:6767/api/posts/save/${{postId}}`, {{
        method: "PUT",
        headers: {{ "Authorization": "Bearer " + (currentUser ? currentUser.id : 1) }}
      }}).catch(() => {{}});
    }}

    async function deletePost(postId) {{
      if (!confirm("Remove this entry from your journal?")) return;
      posts = posts.filter(x => x.id !== postId);
      render();

      fetch(`http://localhost:6767/api/posts/${{postId}}`, {{
        method: "DELETE",
        headers: {{ "Authorization": "Bearer " + (currentUser ? currentUser.id : 1) }}
      }}).catch(() => {{}});
    }}

    function toggleComments(postId) {{
      expandedComments[postId] = !expandedComments[postId];
      render();
    }}

    async function submitComment(postId) {{
      const input = document.getElementById(`comm-input-${{postId}}`);
      if (!input || !input.value.trim()) return;
      const text = input.value.trim();

      const p = posts.find(x => x.id === postId);
      if (!p) return;
      if (!p.comments) p.comments = [];
      p.comments.push({{
        id: Date.now(),
        content: text,
        created_at: new Date().toISOString(),
        user: currentUser,
        likes: [],
        like_count: 0,
        is_liked: false
      }});
      p.comment_count = p.comments.length;
      render();

      fetch(`http://localhost:6767/api/comments/post/${{postId}}`, {{
        method: "POST",
        headers: {{ "Content-Type": "application/json", "Authorization": "Bearer " + (currentUser ? currentUser.id : 1) }},
        body: JSON.stringify({{ content: text }})
      }}).catch(() => {{}});
    }}

    async function toggleLikeComment(postId, commentId) {{
      const p = posts.find(x => x.id === postId);
      if (!p || !p.comments) return;
      const c = p.comments.find(x => x.id === commentId);
      if (!c) return;
      c.is_liked = !c.is_liked;
      c.like_count += (c.is_liked ? 1 : -1);
      render();

      fetch(`http://localhost:6767/api/comments/like/${{commentId}}`, {{
        method: "PUT",
        headers: {{ "Authorization": "Bearer " + (currentUser ? currentUser.id : 1) }}
      }}).catch(() => {{}});
    }}

    async function submitReel() {{
      const tInput = document.getElementById("reel-title");
      const vInput = document.getElementById("reel-video");
      const title = tInput ? tInput.value.trim() : "";
      const video = vInput ? vInput.value.trim() : "";
      if (!video) return;

      const newReel = {{
        id: Date.now(),
        title: title || "untitled",
        video: video,
        user: currentUser,
        created_at: new Date().toISOString()
      }};
      reels.unshift(newReel);
      showNewReelForm = false;
      render();

      fetch("http://localhost:6767/api/reels", {{
        method: "POST",
        headers: {{ "Content-Type": "application/json", "Authorization": "Bearer " + (currentUser ? currentUser.id : 1) }},
        body: JSON.stringify({{ title, video }})
      }}).catch(() => {{}});
    }}

    async function sendMessage() {{
      const input = document.getElementById("chat-msg-input");
      if (!input || !input.value.trim()) return;
      const text = input.value.trim();

      const chat = chats.find(c => c.id === activeChatId) || chats[0];
      if (!chat) return;
      if (!chat.messages) chat.messages = [];
      chat.messages.push({{
        id: Date.now(),
        content: text,
        user: currentUser,
        created_at: new Date().toISOString()
      }});
      chat.last_message = {{ content: text }};
      render();

      fetch(`http://localhost:6767/api/messages/chat/${{chat.id}}`, {{
        method: "POST",
        headers: {{ "Content-Type": "application/json", "Authorization": "Bearer " + (currentUser ? currentUser.id : 1) }},
        body: JSON.stringify({{ content: text, image: "" }})
      }}).catch(() => {{}});
    }}

    async function toggleFollow(targetUserId) {{
      const u = users.find(x => x.id === targetUserId);
      if (!u || !currentUser) return;
      if (!u.followers) u.followers = [];
      const idx = u.followers.indexOf(currentUser.id);
      if (idx >= 0) {{
        u.followers.splice(idx, 1);
      }} else {{
        u.followers.push(currentUser.id);
      }}
      render();

      fetch(`http://localhost:6767/api/users/follow/${{targetUserId}}`, {{
        method: "PUT",
        headers: {{ "Authorization": "Bearer " + currentUser.id }}
      }}).catch(() => {{}});
    }}

    async function saveProfile() {{
      const fn = document.getElementById("edit-fn").value.trim();
      const ln = document.getElementById("edit-ln").value.trim();
      const gen = document.getElementById("edit-gen").value;
      if (currentUser) {{
        currentUser.firstname = fn || currentUser.firstname;
        currentUser.lastname = ln || currentUser.lastname;
        currentUser.gender = gen;
        localStorage.setItem("hobby_user", JSON.stringify(currentUser));
      }}
      showEditModal = false;
      render();

      fetch("http://localhost:6767/api/users", {{
        method: "PUT",
        headers: {{ "Content-Type": "application/json", "Authorization": "Bearer " + currentUser.id }},
        body: JSON.stringify({{ firstname: fn, lastname: ln, gender: gen }})
      }}).catch(() => {{}});
    }}

    // --- Component Renderers ---
    function renderNavbar() {{
      const linkBase = "flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors";
      const active = "text-violet-700 bg-violet-100";
      const inactive = "text-gray-600 hover:text-violet-700 hover:bg-violet-50";

      return `
        <header class="sticky top-0 z-40 border-b border-gray-200 bg-white/95 backdrop-blur">
          <div class="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
            <div class="flex items-center gap-2 cursor-pointer" onclick="navigate('feed')">
              <img src="${{LOGO_SRC}}" alt="Hobby" class="w-7 h-7 object-contain" />
              <span class="font-['Poppins'] font-semibold text-xl tracking-tight text-gray-900">Hobby</span>
            </div>

            <nav class="flex items-center gap-1">
              <button onclick="navigate('feed')" class="${{linkBase}} ${{currentTab === 'feed' ? active : inactive}}">
                <i data-lucide="home" class="w-4 h-4"></i>
                <span class="hidden sm:inline">Feed</span>
              </button>
              <button onclick="navigate('reels')" class="${{linkBase}} ${{currentTab === 'reels' ? active : inactive}}">
                <i data-lucide="film" class="w-4 h-4"></i>
                <span class="hidden sm:inline">Reels</span>
              </button>
              <button onclick="navigate('chat')" class="${{linkBase}} ${{currentTab === 'chat' ? active : inactive}}">
                <i data-lucide="message-circle" class="w-4 h-4"></i>
                <span class="hidden sm:inline">Chat</span>
              </button>
              <button onclick="navigate('profile')" class="${{linkBase}} ${{currentTab === 'profile' ? active : inactive}}">
                <i data-lucide="user" class="w-4 h-4"></i>
                <span class="hidden sm:inline">Profile</span>
              </button>
              <button onclick="logout()" class="${{linkBase}} ${{inactive}}" title="Log out">
                <i data-lucide="log-out" class="w-4 h-4"></i>
              </button>
            </nav>
          </div>
        </header>
      `;
    }}

    function renderFeed() {{
      return `
        <div class="max-w-xl mx-auto px-4 py-6">
          <!-- CreatePost Component -->
          <div class="border border-gray-200 shadow-sm bg-white/70 rounded-lg p-4 mb-5">
            <div class="flex gap-3">
              ${{renderAvatar(currentUser?.firstname, currentUser?.lastname, 36)}}
              <textarea
                id="post-caption"
                placeholder="What are you working on today?"
                rows="2"
                class="flex-1 resize-none bg-transparent text-[15px] placeholder:text-gray-400 focus:outline-none"
              ></textarea>
            </div>

            ${{showMediaInputs ? `
              <div class="mt-3 space-y-2 pl-[46px]">
                <input
                  id="post-image"
                  placeholder="Image URL (optional)"
                  class="w-full text-sm bg-gray-50 border border-gray-200 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-violet-500"
                />
                <input
                  id="post-video"
                  placeholder="Video URL (optional)"
                  class="w-full text-sm bg-gray-50 border border-gray-200 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-violet-500"
                />
              </div>
            ` : ''}}

            <div class="flex items-center justify-between mt-3 pl-[46px]">
              <button
                type="button"
                onclick="showMediaInputs = !showMediaInputs; render();"
                class="flex items-center gap-1.5 text-xs text-gray-500 hover:text-violet-700"
              >
                <i data-lucide="image" class="w-3.5 h-3.5"></i>
                <i data-lucide="video" class="w-3.5 h-3.5"></i>
                media
              </button>
              <button
                type="button"
                onclick="submitPost()"
                class="flex items-center gap-1.5 bg-violet-600 hover:bg-violet-700 text-white text-sm font-medium px-4 py-1.5 rounded-lg transition-colors"
              >
                <i data-lucide="feather" class="w-3.5 h-3.5"></i>
                Post entry
              </button>
            </div>
          </div>

          <!-- Posts List -->
          <div class="space-y-5">
            ${{posts.length === 0 ? '<p class="text-center text-gray-400 text-sm py-10">No entries yet. Be the first to post something you made.</p>' : ''}}
            ${{posts.map(post => `
              <article class="border border-gray-200 shadow-sm bg-white/70 rounded-lg p-4">
                <div class="flex items-center justify-between mb-3">
                  <div class="flex items-center gap-2.5 cursor-pointer group" onclick="navigate('profile', ${{post.user?.id}})">
                    ${{renderAvatar(post.user?.firstname, post.user?.lastname, 34)}}
                    <div>
                      <p class="text-sm font-semibold text-gray-900 group-hover:text-violet-700">
                        ${{post.user?.firstname}} ${{post.user?.lastname}}
                      </p>
                      <p class="text-xs text-gray-400">
                        ${{formatDate(post.created_at)}}
                      </p>
                    </div>
                  </div>
                  ${{currentUser?.id === post.user?.id ? `
                    <button onclick="deletePost(${{post.id}})" class="text-gray-300 hover:text-orange-600 transition-colors p-1" title="Delete post">
                      <i data-lucide="trash-2" class="w-4 h-4"></i>
                    </button>
                  ` : ''}}
                </div>

                ${{post.caption ? `
                  <p class="text-[15px] leading-relaxed text-gray-900 mb-3 whitespace-pre-wrap">${{post.caption}}</p>
                ` : ''}}

                ${{post.image ? `
                  <img src="${{post.image}}" alt="post" class="w-full max-h-[520px] object-cover rounded-lg border border-gray-200 mb-1" />
                ` : ''}}

                ${{post.video ? `
                  <video src="${{post.video}}" controls class="w-full max-h-[520px] rounded-lg border border-gray-200 mb-1"></video>
                ` : ''}}

                <div class="flex items-center gap-4 mt-3 pt-3 border-t border-dashed border-gray-200">
                  <button onclick="toggleLike(${{post.id}})" class="flex items-center gap-1.5 text-sm transition-colors ${{post.is_liked ? 'text-orange-600' : 'text-gray-500 hover:text-orange-600'}}">
                    <i data-lucide="heart" class="w-4 h-4 ${{post.is_liked ? 'fill-current' : ''}}"></i>
                    ${{post.like_count || 0}}
                  </button>
                  <button onclick="toggleComments(${{post.id}})" class="flex items-center gap-1.5 text-sm text-gray-500 hover:text-violet-700 transition-colors">
                    <i data-lucide="message-square" class="w-4 h-4"></i>
                    ${{post.comment_count || (post.comments?.length || 0)}}
                  </button>
                  <button onclick="toggleSave(${{post.id}})" class="ml-auto flex items-center gap-1.5 text-sm transition-colors ${{post.is_saved ? 'text-violet-700' : 'text-gray-500 hover:text-violet-700'}}">
                    <i data-lucide="bookmark" class="w-4 h-4 ${{post.is_saved ? 'fill-current' : ''}}"></i>
                  </button>
                </div>

                <!-- Comment Section -->
                ${{expandedComments[post.id] ? `
                  <div class="mt-3 pt-3 border-t border-dashed border-gray-200">
                    <div class="space-y-2.5 max-h-64 overflow-y-auto scrollbar-thin mb-3">
                      ${{(!post.comments || post.comments.length === 0) ? '<p class="text-xs text-gray-400 italic">No comments yet — be the first.</p>' : ''}}
                      ${{(post.comments || []).map(c => `
                        <div class="flex items-start gap-2">
                          ${{renderAvatar(c.user?.firstname, c.user?.lastname, 26)}}
                          <div class="flex-1 bg-gray-100 rounded-lg px-2.5 py-1.5">
                            <p class="text-xs font-semibold text-gray-800">${{c.user?.firstname}} ${{c.user?.lastname}}</p>
                            <p class="text-sm text-gray-900">${{c.content}}</p>
                          </div>
                          <button onclick="toggleLikeComment(${{post.id}}, ${{c.id}})" class="text-gray-300 hover:text-orange-600 flex items-center gap-0.5 text-xs mt-1.5">
                            <i data-lucide="heart" class="w-3 h-3 ${{c.is_liked ? 'text-orange-600 fill-current' : ''}}"></i>
                            ${{c.like_count > 0 ? c.like_count : ''}}
                          </button>
                        </div>
                      `).join('')}}
                    </div>
                    <div class="flex gap-2">
                      <input
                        id="comm-input-${{post.id}}"
                        placeholder="Add a note…"
                        onkeydown="if(event.key === 'Enter') submitComment(${{post.id}})"
                        class="flex-1 text-sm bg-white border border-gray-200 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-violet-500"
                      />
                      <button onclick="submitComment(${{post.id}})" class="text-violet-700 hover:text-violet-900">
                        <i data-lucide="send" class="w-4 h-4"></i>
                      </button>
                    </div>
                  </div>
                ` : ''}}
              </article>
            `).join('')}}
          </div>
        </div>
      `;
    }}

    function renderReels() {{
      return `
        <div class="max-w-3xl mx-auto px-4 py-6">
          <div class="flex items-center justify-between mb-5">
            <h1 class="font-['Poppins'] font-semibold text-2xl flex items-center gap-2">
              <i data-lucide="film" class="w-5 h-5 text-orange-500"></i> Reels
            </h1>
            <button onclick="showNewReelForm = !showNewReelForm; render();" class="flex items-center gap-1.5 bg-violet-600 hover:bg-violet-700 text-white text-sm font-medium px-3 py-1.5 rounded-lg">
              <i data-lucide="${{showNewReelForm ? 'x' : 'plus'}}" class="w-4 h-4"></i>
              ${{showNewReelForm ? 'Cancel' : 'New reel'}}
            </button>
          </div>

          ${{showNewReelForm ? `
            <div class="border border-gray-200 shadow-sm bg-white/70 rounded-lg p-4 mb-6 space-y-2">
              <input id="reel-title" placeholder="Title" class="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500" />
              <input id="reel-video" placeholder="Video URL" class="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500" />
              <button onclick="submitReel()" class="bg-violet-600 hover:bg-violet-700 text-white text-sm font-medium px-4 py-2 rounded-lg">Publish reel</button>
            </div>
          ` : ''}}

          <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
            ${{reels.map(reel => `
              <div class="border border-gray-200 shadow-sm bg-white/70 rounded-lg p-2">
                <video src="${{reel.video}}" controls class="w-full aspect-[9/16] object-cover rounded-lg bg-black/5"></video>
                <p class="text-xs font-medium mt-1.5 truncate">${{reel.title || "untitled"}}</p>
                <span onclick="navigate('profile', ${{reel.user?.id}})" class="text-xs text-gray-400 hover:text-violet-700 cursor-pointer block truncate">
                  ${{reel.user?.firstname}} ${{reel.user?.lastname}}
                </span>
              </div>
            `).join('')}}
          </div>
        </div>
      `;
    }}

    function renderChat() {{
      const activeChat = chats.find(c => c.id === activeChatId) || chats[0];
      const otherUser = activeChat?.other_user || users.find(u => u.id !== currentUser?.id) || users[1];

      return `
        <div class="max-w-4xl mx-auto px-4 py-6 grid grid-cols-1 md:grid-cols-[280px_1fr] gap-4 h-[calc(100vh-80px)]">
          <!-- Sidebar -->
          <div class="border border-gray-200 shadow-sm bg-white/70 rounded-lg p-3 flex flex-col overflow-hidden">
            <div class="relative mb-3">
              <i data-lucide="search" class="w-4 h-4 absolute left-2.5 top-2.5 text-gray-400"></i>
              <input placeholder="Find a maker…" class="w-full bg-gray-50 border border-gray-200 rounded-lg pl-8 pr-3 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500" />
            </div>

            <div class="flex-1 overflow-y-auto space-y-1">
              ${{users.filter(u => u.id !== currentUser?.id).map(u => `
                <button
                  onclick="activeChatId = ${{u.id}}; render();"
                  class="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-left transition-colors ${{activeChatId === u.id ? 'bg-violet-100 text-violet-900 font-medium' : 'hover:bg-violet-50 text-gray-700'}}"
                >
                  ${{renderAvatar(u.firstname, u.lastname, 32)}}
                  <div class="truncate">
                    <p class="text-sm font-semibold">${{u.firstname}} ${{u.lastname}}</p>
                  </div>
                </button>
              `).join('')}}
            </div>
          </div>

          <!-- Chat Window -->
          <div class="border border-gray-200 shadow-sm bg-white/70 rounded-lg flex flex-col overflow-hidden">
            <div class="px-4 py-3 border-b border-gray-200 flex items-center gap-3 bg-white/50">
              ${{renderAvatar(otherUser?.firstname, otherUser?.lastname, 34)}}
              <div>
                <p class="font-semibold text-sm text-gray-900">${{otherUser?.firstname}} ${{otherUser?.lastname}}</p>
              </div>
            </div>

            <div class="flex-1 overflow-y-auto p-4 space-y-3">
              ${{(activeChat?.messages || []).map(m => `
                <div class="flex ${{m.user?.id === currentUser?.id ? 'justify-end' : 'justify-start'}}">
                  <div class="${{m.user?.id === currentUser?.id ? 'bg-violet-600 text-white' : 'bg-gray-100 text-gray-900'}} rounded-lg px-3 py-2 max-w-[75%] text-sm">
                    ${{m.content}}
                  </div>
                </div>
              `).join('')}}
            </div>

            <div class="p-3 border-t border-gray-200 flex gap-2 bg-white/50">
              <input
                id="chat-msg-input"
                placeholder="Write a message..."
                onkeydown="if(event.key === 'Enter') sendMessage()"
                class="flex-1 bg-white border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500"
              />
              <button onclick="sendMessage()" class="bg-violet-600 hover:bg-violet-700 text-white rounded-lg p-2 transition-colors">
                <i data-lucide="send" class="w-4 h-4"></i>
              </button>
            </div>
          </div>
        </div>
      `;
    }}

    function renderProfile() {{
      const profile = users.find(x => x.id === viewingProfileId) || currentUser || users[0];
      const isMe = currentUser?.id === profile.id;
      const userPosts = posts.filter(p => p.user?.id === profile.id);
      const isFollowing = profile.followers?.includes(currentUser?.id);

      return `
        <div class="max-w-xl mx-auto px-4 py-6">
          <div class="border border-gray-200 shadow-sm bg-white/70 rounded-lg p-6 mb-6 flex items-center gap-5">
            ${{renderAvatar(profile.firstname, profile.lastname, 68)}}
            <div class="flex-1">
              <h1 class="font-['Poppins'] font-semibold text-2xl text-gray-900">
                ${{profile.firstname}} ${{profile.lastname}}
              </h1>
              <p class="text-gray-500 text-sm">${{profile.email}}</p>
              <div class="flex gap-4 mt-2 text-xs text-gray-500">
                <span>${{userPosts.length}} entries</span>
                <span>${{profile.followers?.length || 0}} followers</span>
                <span>${{profile.following?.length || 0}} following</span>
              </div>
            </div>

            ${{isMe ? `
              <button onclick="showEditModal = true; render();" class="flex items-center gap-1.5 text-sm border border-gray-200 px-3 py-1.5 rounded-lg hover:border-violet-500 hover:text-violet-700 transition-colors">
                <i data-lucide="pencil" class="w-3.5 h-3.5"></i> Edit
              </button>
            ` : `
              <button onclick="toggleFollow(${{profile.id}})" class="flex items-center gap-1.5 text-sm px-3 py-1.5 rounded-lg transition-colors ${{isFollowing ? 'border border-gray-200 text-gray-600 hover:border-orange-500 hover:text-orange-600' : 'bg-violet-600 hover:bg-violet-700 text-white'}}">
                <i data-lucide="${{isFollowing ? 'user-check' : 'user-plus'}}" class="w-3.5 h-3.5"></i>
                ${{isFollowing ? 'Following' : 'Follow'}}
              </button>
            `}}
          </div>

          <div class="space-y-5">
            ${{userPosts.length === 0 ? '<p class="text-center text-gray-400 text-sm py-8">No entries yet.</p>' : ''}}
            ${{userPosts.map(post => `
              <article class="border border-gray-200 shadow-sm bg-white/70 rounded-lg p-4">
                <div class="flex items-center justify-between mb-3">
                  <div class="flex items-center gap-2.5">
                    ${{renderAvatar(post.user?.firstname, post.user?.lastname, 34)}}
                    <div>
                      <p class="text-sm font-semibold text-gray-900">${{post.user?.firstname}} ${{post.user?.lastname}}</p>
                      <p class="text-xs text-gray-400">${{formatDate(post.created_at)}}</p>
                    </div>
                  </div>
                  ${{isMe ? `
                    <button onclick="deletePost(${{post.id}})" class="text-gray-300 hover:text-orange-600 transition-colors p-1" title="Delete post">
                      <i data-lucide="trash-2" class="w-4 h-4"></i>
                    </button>
                  ` : ''}}
                </div>
                ${{post.caption ? `<p class="text-[15px] leading-relaxed text-gray-900 mb-3">${{post.caption}}</p>` : ''}}
                ${{post.image ? `<img src="${{post.image}}" class="w-full max-h-[520px] object-cover rounded-lg border border-gray-200 mb-1" />` : ''}}
                <div class="flex items-center gap-4 mt-3 pt-3 border-t border-dashed border-gray-200">
                  <button onclick="toggleLike(${{post.id}})" class="flex items-center gap-1.5 text-sm transition-colors ${{post.is_liked ? 'text-orange-600' : 'text-gray-500'}}">
                    <i data-lucide="heart" class="w-4 h-4 ${{post.is_liked ? 'fill-current' : ''}}"></i>
                    ${{post.like_count || 0}}
                  </button>
                  <button onclick="toggleComments(${{post.id}})" class="flex items-center gap-1.5 text-sm text-gray-500">
                    <i data-lucide="message-square" class="w-4 h-4"></i>
                    ${{post.comment_count || 0}}
                  </button>
                  <button onclick="toggleSave(${{post.id}})" class="ml-auto flex items-center gap-1.5 text-sm ${{post.is_saved ? 'text-violet-700' : 'text-gray-500'}}">
                    <i data-lucide="bookmark" class="w-4 h-4 ${{post.is_saved ? 'fill-current' : ''}}"></i>
                  </button>
                </div>
              </article>
            `).join('')}}
          </div>

          <!-- Edit Profile Modal -->
          ${{showEditModal ? `
            <div class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 px-4">
              <div class="border border-gray-200 shadow-sm bg-white rounded-lg p-6 w-full max-w-sm relative">
                <button onclick="showEditModal = false; render();" class="absolute top-4 right-4 text-gray-400 hover:text-gray-900">
                  <i data-lucide="x" class="w-4 h-4"></i>
                </button>
                <h2 class="text-xl font-['Poppins'] font-semibold mb-4">Edit profile</h2>
                <div class="space-y-3">
                  <div>
                    <label class="text-xs text-gray-500 block mb-1">First name</label>
                    <input id="edit-fn" value="${{currentUser?.firstname || ''}}" class="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500" />
                  </div>
                  <div>
                    <label class="text-xs text-gray-500 block mb-1">Last name</label>
                    <input id="edit-ln" value="${{currentUser?.lastname || ''}}" class="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500" />
                  </div>
                  <div>
                    <label class="text-xs text-gray-500 block mb-1">Gender</label>
                    <select id="edit-gen" class="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500">
                      <option value="male" ${{currentUser?.gender === 'male' ? 'selected' : ''}}>Male</option>
                      <option value="female" ${{currentUser?.gender === 'female' ? 'selected' : ''}}>Female</option>
                      <option value="other" ${{currentUser?.gender === 'other' ? 'selected' : ''}}>Other</option>
                    </select>
                  </div>
                  <button onclick="saveProfile()" class="w-full bg-violet-600 hover:bg-violet-700 text-white font-medium py-2.5 rounded-lg transition-colors mt-2">
                    Save changes
                  </button>
                </div>
              </div>
            </div>
          ` : ''}}
        </div>
      `;
    }}

    function renderLogin() {{
      return `
        <div class="min-h-screen flex items-center justify-center px-4">
          <div class="w-full max-w-sm">
            <div class="flex flex-col items-center mb-8">
              <img src="${{LOGO_SRC}}" alt="Hobby" class="w-14 h-14 object-contain mb-2" />
              <h1 class="font-['Poppins'] font-semibold text-3xl text-gray-900">Hobby</h1>
              <p class="text-gray-500 text-sm mt-1">a field journal for makers</p>
            </div>

            <form onsubmit="event.preventDefault(); submitLogin();" class="border border-gray-200 shadow-sm bg-white/70 rounded-lg p-6 space-y-4">
              <div>
                <label class="text-xs text-gray-500 block mb-1">Email</label>
                <input id="login-email" required type="email" placeholder="e.g. name@example.com" class="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500" />
              </div>
              <div>
                <label class="text-xs text-gray-500 block mb-1">Password</label>
                <input id="login-pass" required type="password" placeholder="••••••••" class="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500" />
              </div>

              ${{authError ? `<p class="text-orange-600 text-xs">${{authError}}</p>` : ''}}

              <button type="submit" class="w-full bg-violet-600 hover:bg-violet-700 text-white font-medium py-2.5 rounded-lg transition-colors">
                Sign in
              </button>
            </form>

            <p class="text-center text-sm text-gray-500 mt-5">
              New here?
              <span onclick="navigate('signup')" class="text-violet-700 font-medium hover:underline cursor-pointer">
                Create an account
              </span>
            </p>
          </div>
        </div>
      `;
    }}

    function renderSignup() {{
      return `
        <div class="min-h-screen flex items-center justify-center px-4">
          <div class="w-full max-w-sm">
            <div class="flex flex-col items-center mb-8">
              <img src="${{LOGO_SRC}}" alt="Hobby" class="w-14 h-14 object-contain mb-2" />
              <h1 class="font-['Poppins'] font-semibold text-3xl text-gray-900">Hobby</h1>
              <p class="text-gray-500 text-sm mt-1">start your journal</p>
            </div>

            <form onsubmit="event.preventDefault(); submitSignup();" class="border border-gray-200 shadow-sm bg-white/70 rounded-lg p-6 space-y-4">
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="text-xs text-gray-500 block mb-1">First name</label>
                  <input id="reg-fn" required placeholder="First name" class="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500" />
                </div>
                <div>
                  <label class="text-xs text-gray-500 block mb-1">Last name</label>
                  <input id="reg-ln" required placeholder="Last name" class="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500" />
                </div>
              </div>
              <div>
                <label class="text-xs text-gray-500 block mb-1">Email</label>
                <input id="reg-email" required type="email" placeholder="name@example.com" class="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500" />
              </div>
              <div>
                <label class="text-xs text-gray-500 block mb-1">Password</label>
                <input id="reg-pass" required type="password" placeholder="Create password" class="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500" />
              </div>
              <div>
                <label class="text-xs text-gray-500 block mb-1">Gender (optional)</label>
                <select id="reg-gen" class="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-violet-500">
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>

              ${{authError ? `<p class="text-orange-600 text-xs">${{authError}}</p>` : ''}}

              <button type="submit" class="w-full bg-violet-600 hover:bg-violet-700 text-white font-medium py-2.5 rounded-lg transition-colors">
                Create account
              </button>
            </form>

            <p class="text-center text-sm text-gray-500 mt-5">
              Already have an account?
              <span onclick="navigate('login')" class="text-violet-700 font-medium hover:underline cursor-pointer">
                Sign in
              </span>
            </p>
          </div>
        </div>
      `;
    }}

    // Main render loop
    function render() {{
      const app = document.getElementById("app");
      if (!currentUser && currentTab !== "signup") {{
        app.innerHTML = renderLogin();
      }} else if (currentTab === "signup") {{
        app.innerHTML = renderSignup();
      }} else {{
        let content = "";
        if (currentTab === "feed") content = renderFeed();
        else if (currentTab === "reels") content = renderReels();
        else if (currentTab === "chat") content = renderChat();
        else if (currentTab === "profile") content = renderProfile();

        app.innerHTML = `
          ${{renderNavbar()}}
          <main class="flex-1">${{content}}</main>
        `;
      }}
      lucide.createIcons();
    }}

    // Initial render
    render();
  </script>
</body>
</html>
"""

# Render the application
st.components.v1.html(html_content, height=1000, scrolling=True)
