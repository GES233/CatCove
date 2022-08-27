""" Code of API. """

# Request related.
REQUEST_NO_JSON:               int = 4300

# Internal Error.
SERVER_ERROR:                  int = 5000

# Authentation related.
...

# Found resource.
RESOURCE_FETCHED_DEFAULT:      int = 6700
RESOURCE_FETCHED_USER:         int = 6701  # User, user's info.
RESOURCE_FETCHED_MAIN:         int = 6702  # Main content (1 query, 1 result).
RESOURCE_FETCHED_POST:         int = 6703  # Multi content (e.g. post).
