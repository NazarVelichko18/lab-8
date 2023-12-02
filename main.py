from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, Session, relationship

# Підключення до бази даних
engine = create_engine('sqlite:///db.db', echo=False)
Base = declarative_base()


# Оголошення класів моделей

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)


class Messages(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String)
    sender_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))

    sender = relationship("Users", foreign_keys=[sender_id])
    receiver = relationship("Users", foreign_keys=[receiver_id])


# Створення таблиць
Base.metadata.create_all(engine)


# Створення сесії
def create_session():
    return Session(engine)


# Функція для створення нового користувача
def create_user(session, name):
    new_user = Users(username=name)
    session.add(new_user)
    session.commit()


# Функція для відправки повідомлення
def send_message(session, sender_id, receiver_id, content):
    new_message = Messages(sender_id=sender_id, receiver_id=receiver_id, content=content)
    session.add(new_message)
    session.commit()

def delete_message(session, id):
    message_to_delete = session.query(Messages).filter_by(id=id).first()
    if message_to_delete:
        session.delete(message_to_delete)
        session.commit()

# Функція для отримання всіх повідомлень
def get_all_messages(session):
    return session.query(Messages).all()


# Функція для отримання повідомлень для конкретного користувача
def get_user_messages(session, id):
    return session.query(Messages).filter(
        (Messages.sender_id == id) | (Messages.receiver_id == id)
    ).all()


# Закриття сесії
def close_session(session):
    session.close()


# Приклад використання:
session = create_session()

# Створення користувачів
create_user(session, "Lenya")
create_user(session, "Nazar")

# Відправка повідомлення
send_message(session, 2, 1, "How are you?")

# Отримання всіх повідомлень
all_messages = get_all_messages(session)
print("Всі повідомлення:")
for message in all_messages:
    sender_name = message.sender.username
    receiver_name = message.receiver.username
    print(f"{sender_name} -> {receiver_name}: {message.content}")

# Отримання повідомлень для Назара
nazar_messages = get_user_messages(session, 2)
print("\nПовідомлення Назара:")
for message in nazar_messages:
    sender_name = message.sender.username
    receiver_name = message.receiver.username
    print(f"{sender_name} -> {receiver_name}: {message.content}")

print("Видалення повідомлення та виведення всіх повідомлень")
delete_message(session, 4)
for message in all_messages:
    sender_name = message.sender.username
    receiver_name = message.receiver.username
    print(f"{sender_name} -> {receiver_name}: {message.content}")


# Закриття сесії
close_session(session)
