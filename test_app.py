"""
Comprehensive unit / smoke test for Hobby database and backend operations.
"""
import db
import os

def test_all():
    print("Initializing DB...")
    db.init_db()

    # 1. Test users
    users = db.get_all_users()
    print(f"Users found: {len(users)}")
    assert len(users) >= 3, "Expected at least 3 seeded users"

    # 2. Test authentication
    user = db.authenticate_user("siddhua@gmail.com", "password")
    assert user is not None, "Failed to authenticate siddhua@gmail.com"
    print(f"Authenticated: {user['firstname']} {user['lastname']}")

    # 3. Test post creation
    post = db.create_post(user["id"], "Automated test craft post #woodworking", "https://example.com/pic.jpg", "")
    assert post is not None
    print(f"Created post ID: {post['id']}")

    # 4. Test like & comment
    updated_post = db.toggle_like_post(post["id"], user["id"])
    assert updated_post["like_count"] >= 1, "Like count should be >= 1"

    post_with_comm = db.add_comment(post["id"], user["id"], "Love this dovetail finish!")
    assert len(post_with_comm["comments"]) >= 1, "Comment count should be >= 1"
    comm_id = post_with_comm["comments"][0]["id"]
    db.toggle_like_comment(comm_id, user["id"])

    # 5. Test save / bookmark
    saved = db.toggle_save_post(post["id"], user["id"])
    assert saved is True, "Post should be saved"

    # 6. Test reels
    reel_id = db.create_reel(user["id"], "Turning an oak bowl", "https://example.com/reel.mp4")
    reels = db.get_all_reels()
    assert any(r["id"] == reel_id for r in reels), "Reel should be listed"

    # 7. Test chat
    other_user = [u for u in users if u["id"] != user["id"]][0]
    chat_id = db.get_or_create_chat(user["id"], other_user["id"])
    msg_id = db.send_chat_message(chat_id, user["id"], "Test hello from maker")
    msgs = db.get_chat_messages(chat_id)
    assert any(m["id"] == msg_id for m in msgs), "Message should be present in chat"

    # 8. Test follow toggle
    is_f1 = db.toggle_follow_user(user["id"], other_user["id"])
    is_f2 = db.toggle_follow_user(user["id"], other_user["id"])
    assert is_f1 != is_f2, "Follow toggle should invert state"

    # 9. Clean up test post
    db.delete_post(post["id"], user["id"])
    print("Test post cleaned up successfully.")

    print("\n>>> ALL TESTS PASSED SUCCESSFULLY! <<<")

if __name__ == "__main__":
    test_all()
