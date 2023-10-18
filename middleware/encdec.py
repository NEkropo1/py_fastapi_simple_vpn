import bcrypt


def hash_password(password):
    hashed_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_pass


def verify_password(hashed_password, input_password):
    return bcrypt.checkpw(input_password.encode(), hashed_password)
