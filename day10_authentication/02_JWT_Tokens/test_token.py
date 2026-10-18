
from auth_common.jwt_service import create_access_token, verify_access_token

token = create_access_token("bhanu")
print("Token:", token)

payload = verify_access_token(token)
print("Decoded payload:", payload)
