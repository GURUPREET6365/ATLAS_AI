import bcrypt


def hash_password(plain_password) -> str:
    password_bytes = bcrypt.hashpw(plain_password.encode("utf-8"),bcrypt.gensalt())
    password_str = password_bytes.decode("utf-8")
    # print(password_str)
    return password_str
def check_password(plain_password, hashed_password) -> bool:

    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )
