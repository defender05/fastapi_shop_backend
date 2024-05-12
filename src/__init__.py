# Для ручного создания админа в базе
# import uuid
# import bcrypt
#
# def generate_user_id():
#     return str(uuid.uuid4())
#
# def get_password_hash(password):
#     salt = bcrypt.gensalt()
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
#     return hashed_password.decode('utf-8')
#
#
#
# if __name__ == "__main__":
#     user_id = generate_user_id()
#     print(f"User ID: {user_id}")
#     print(get_password_hash("123"))
