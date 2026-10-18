from security import hash_password, verify_password

hashed = hash_password("hello_world")
print(f"Hashed password: {hashed}")

print(verify_password("my_secure_password", hashed))
print(verify_password("wrong_password", hashed))
print(verify_password("hello_world", hashed))