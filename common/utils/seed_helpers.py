"""
Not done yet.
Intinya ini buat nge-seed database pake data palsu.
"""

from faker import Faker
import random

fake = Faker()

def fake_user(User):
    """Bikin user random."""
    return User.objects.create_user(
        username=fake.user_name(),
        email=fake.email(),
        password="password123"
    )

def fake_post(Post, users):
    """Bikin posting random untuk salah satu user."""
    return Post.objects.create(
        title=fake.sentence(),
        content=fake.paragraph(nb_sentences=5),
        author=random.choice(users)
    )

def fake_product(Product, users):
    """Bikin product random di marketplace."""
    return Product.objects.create(
        name=fake.word().capitalize(),
        description=fake.paragraph(),
        price=random.randint(10, 500),
        seller=random.choice(users)
    )

def fake_message(Message, users):
    """Bikin pesan random antar user."""
    sender, receiver = random.sample(list(users), 2)
    return Message.objects.create(
        sender=sender,
        receiver=receiver,
        content=fake.sentence()
    )

def fake_broadcast(BroadcastMessage, user):
    """Bikin broadcast random dari user tertentu."""
    return BroadcastMessage.objects.create(
        title=fake.sentence(),
        message=fake.paragraph(),
        sender=user
    )
