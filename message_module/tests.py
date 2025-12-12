from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.html import escape
from message_module.models import Conversation, ConversationMember, Message
from profile_module.models import Profile
from django.core.exceptions import ValidationError
from uuid import uuid4


class MessageModuleTests(TestCase):
    """
    Tests for message_module views and functionality
    """
    def setUp(self):
        self.client = Client()
        self.u1 = User.objects.create_user(username="alice", password="pw123")
        self.u2 = User.objects.create_user(username="bob", password="pw123")
        self.u3 = User.objects.create_user(username="charlie", password="pw123")
        Profile.objects.create(user=self.u1, display_name="Alice")
        Profile.objects.create(user=self.u2, display_name="Bob")
        Profile.objects.create(user=self.u3, display_name="Charlie")

    def login_u1(self):
        self.client.login(username="alice", password="pw123")

    def login_u3(self):
        self.client.login(username="charlie", password="pw123")

    def make_conversation(self, created_by=None, with_members=True):
        created_by = created_by or self.u1
        conv = Conversation.objects.create(created_by=created_by)
        if with_members:
            ConversationMember.objects.create(conversation=conv, user=self.u1)
            ConversationMember.objects.create(conversation=conv, user=self.u2)
        return conv


    def test_chat_view_requires_login(self):
        resp = self.client.get(reverse("message_module:chat_home"))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith("/auth/login/"))

    def test_chat_view_renders_conversation_and_messages(self):
        self.login_u1()
        conv = self.make_conversation()
        m1 = Message.objects.create(conversation=conv, sender=self.u1, body="hi")
        conv.update_last_message(m1)

        resp = self.client.get(reverse("message_module:chat_view", args=[conv.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertIn("selected_conversation", resp.context)
        self.assertEqual(resp.context["selected_conversation"].id, conv.id)
        self.assertIn("last_message_id", resp.context)
        self.assertEqual(resp.context["last_message_id"], str(m1.id))

    def test_post_create_new_conversation_and_redirect(self):
        self.login_u1()
        resp = self.client.post(reverse("message_module:chat_home"), {"username": "bob"})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Conversation.objects.count(), 1)
        conv = Conversation.objects.first()
        self.assertIn(str(conv.id), resp.url)
        self.assertEqual(conv.members.count(), 2)

        resp2 = self.client.post(reverse("message_module:chat_home"), {"username": "bob"})
        self.assertEqual(resp2.status_code, 302)
        self.assertEqual(Conversation.objects.count(), 1)  # tidak nambah

    def test_send_message_returns_localtime_string_and_escaped_body(self):
        """
        Test that sending a message returns created_at in localtime string format
        """
        self.login_u1()
        conv = self.make_conversation()

        url = reverse("message_module:send_message", args=[conv.id])
        raw_body = '<script>alert("x")</script> Halo'
        resp = self.client.post(url, {"message": raw_body}, follow=True)
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertIn("created_at", data)
        msg = Message.objects.last()

        self.assertEqual(data["body"], escape(raw_body))

        expected = timezone.localtime(msg.created_at).strftime("%Y-%m-%d %H:%M")
        self.assertEqual(data["created_at"], expected)

    def test_send_message_empty_body_rejected(self):
        self.login_u1()
        conv = self.make_conversation()
        url = reverse("message_module:send_message", args=[conv.id])
        resp = self.client.post(url, {})
        self.assertEqual(resp.status_code, 400)

    def test_send_message_invalid_image_type_rejected(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        self.login_u1()
        conv = self.make_conversation()
        bad = SimpleUploadedFile("x.txt", b"hello", content_type="text/plain")
        url = reverse("message_module:send_message", args=[conv.id])
        resp = self.client.post(url, {"image": bad})
        self.assertEqual(resp.status_code, 400)

    def test_send_message_requires_membership(self):
        conv = self.make_conversation()
        self.login_u3()

        url = reverse("message_module:send_message", args=[conv.id])
        resp = self.client.post(url, {"message": "halo"}, follow=True)
        self.assertEqual(resp.status_code, 404)

    def test_poll_messages_initial_and_incremental_with_localtime_and_escaped_body(self):
        self.login_u1()
        conv = self.make_conversation()

        m1 = Message.objects.create(conversation=conv, sender=self.u1, body='msg1 <b>bold</b>')
        m2 = Message.objects.create(conversation=conv, sender=self.u2, body='<i>msg2</i>')
        conv.update_last_message(m2)
        
        url = reverse("message_module:poll_messages", args=[conv.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()["messages"]
        self.assertEqual(len(data), 2)


        for item in data:
            self.assertIn("is_self", item)
            self.assertIn("sender_avatar", item)
            self.assertIn("sender_initial", item)

        expected_0 = timezone.localtime(m1.created_at).strftime("%Y-%m-%d %H:%M")
        expected_1 = timezone.localtime(m2.created_at).strftime("%Y-%m-%d %H:%M")
        self.assertEqual(data[0]["created_at"], expected_0)
        self.assertEqual(data[1]["created_at"], expected_1)

        self.assertEqual(data[0]["body"], escape('msg1 <b>bold</b>'))
        self.assertEqual(data[1]["body"], escape('<i>msg2</i>'))

        resp2 = self.client.get(url, {"last_msg_id": str(m1.id)})
        self.assertEqual(resp2.status_code, 200)
        data2 = resp2.json()["messages"]
        self.assertEqual(len(data2), 1)
        self.assertEqual(data2[0]["body"], escape('<i>msg2</i>'))
        self.assertEqual(
            data2[0]["created_at"],
            timezone.localtime(m2.created_at).strftime("%Y-%m-%d %H:%M"),
        )
        
        
        
class MessageModuleModelCoverageTests(TestCase):
    """
    Additional tests to cover model methods and branches
    """
    def setUp(self):
        self.u1 = User.objects.create_user(username="alice", password="pw123")
        self.u2 = User.objects.create_user(username="bob", password="pw123")
        self.u3 = User.objects.create_user(username="charlie", password="pw123")

        Profile.objects.create(user=self.u1, display_name="Alice", avatar_url=None)
        Profile.objects.create(user=self.u2, display_name="Bob", avatar_url=None)
        Profile.objects.create(user=self.u3, display_name="Charlie", avatar_url=None)

        self.conv = Conversation.objects.create(created_by=self.u1)
        ConversationMember.objects.create(conversation=self.conv, user=self.u1)
        ConversationMember.objects.create(conversation=self.conv, user=self.u2)

    def test_conversation_clean_prevents_more_than_two_members(self):
        cm = ConversationMember(conversation=self.conv, user=self.u3)
        with self.assertRaises(ValidationError):
            cm.save()

    def test_conversation_get_participants_and_other_participant_and_str(self):
        parts = list(self.conv.get_participants().order_by("id"))
        self.assertEqual({p.username for p in parts}, {"alice", "bob"})

        other_for_u1 = self.conv.get_other_participant(self.u1)
        self.assertEqual(other_for_u1.username, "bob")

        s = str(self.conv)
        self.assertIn("alice", s)
        self.assertIn("bob", s)

    def test_conversation_update_last_message_with_text_and_image(self):
        long_text = "x" * 120
        m1 = Message.objects.create(conversation=self.conv, sender=self.u1, body=long_text)
        self.conv.update_last_message(m1)
        self.assertEqual(self.conv.last_message_preview, long_text[:100])
        self.assertEqual(self.conv.last_message_at, m1.created_at)

        m2 = Message.objects.create(conversation=self.conv, sender=self.u2, body="", image="dummy_public_id")
        self.conv.update_last_message(m2)
        self.assertEqual(self.conv.last_message_preview, "📷 Image")
        self.assertEqual(self.conv.last_message_at, m2.created_at)

    def test_message_properties_and_str(self):
        m_text = Message.objects.create(conversation=self.conv, sender=self.u1, body="hi")
        self.assertEqual(m_text.sender_display_name, "Alice")
        # self.assertEqual(m_text.sender_display_avatar, "")

        s1 = str(m_text)
        self.assertIn("Message from Alice", s1)

        m_img = Message.objects.create(conversation=self.conv, sender=self.u2, body="", image="dummy_public_id")
        s2 = str(m_img)
        self.assertTrue(s2.startswith("📷 Image from Bob"))

    def test_conversationmember_str(self):
        cm = ConversationMember.objects.get(conversation=self.conv, user=self.u1)
        s = str(cm)
        self.assertIn("alice", s)
        
        

class MessageModuleViewsExtraBranchesTests(TestCase):
    """
    Additional tests to cover less common branches in views.py
    """
    def setUp(self):
        self.client = Client()
        self.u1 = User.objects.create_user(username="alice", password="pw123")
        self.u2 = User.objects.create_user(username="bob", password="pw123")
        Profile.objects.create(user=self.u1, display_name="Alice")
        Profile.objects.create(user=self.u2, display_name="Bob")

        self.conv = Conversation.objects.create(created_by=self.u1)
        ConversationMember.objects.create(conversation=self.conv, user=self.u1)
        ConversationMember.objects.create(conversation=self.conv, user=self.u2)

    def test_chat_view_invalid_uuid_redirects_to_home(self):
        self.client.login(username="alice", password="pw123")
        bad_id = uuid4()
        resp = self.client.get(reverse("message_module:chat_view", args=[bad_id]))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse("message_module:chat_home"))

    def test_poll_messages_last_msg_id_not_in_conversation_returns_empty(self):
        self.client.login(username="alice", password="pw123")
        m1 = Message.objects.create(conversation=self.conv, sender=self.u1, body="hello")
        url = reverse("message_module:poll_messages", args=[self.conv.id])
        resp = self.client.get(url, {"last_msg_id": uuid4()})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["messages"], [])