""" Code of API. """

# Request related.
REQUEST_NO_JSON: int = 4300


# Authentation related.
AUTH_USER_NOT_EXISTED: int = 4901
PASSWORD_NOT_CORRECT: int = 4902

USER_HAVE_COMMON: int = 4905
REGISTER_CODE_ERROR: int = 4906


# Internal Error.
SERVER_ERROR: int = 5000
NOT_IMPLEMENTED: int = 5002


# Found resource.
RESOURCE_FETCHED_DEFAULT: int = 6700
RESOURCE_FETCHED_USER: int = 6701  # User, user's info.
RESOURCE_FETCHED_MAIN: int = 6702  # Main content (1 query, 1 result).
RESOURCE_FETCHED_POST: int = 6703  # Multi content (e.g. post).
