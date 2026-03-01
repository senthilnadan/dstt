def const():
    return 1

def echo(value):
    return value

def get_user():
    return {"name": "Alice", "age": 30, "username": "alice123"}

def get_username(user_dict):
    return user_dict.get("username")

def combine(a, b):
    return f"{a}{b}"

def multiply(a, b):
    return a * b
