

REQUEST_BODY_JSON = """
{
    "phone_no": "string"
}
"""


RESPONSE_201_JSON = """
{
    "status_code": 1,
    "res_status": "string",
    "response": {
        "access_token": "string",
        "expires_in": 1,
        "token_type": "string",
        "refresh_token": "string",
        "scope": "string"
    }
}
"""

RESPONSE_401_JSON = """
{
    "status_code": 1,
    "res_status": "INVALID_USER",
    "response": "string"
}
"""

