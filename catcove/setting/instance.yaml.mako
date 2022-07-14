# Secret key
SECRET_KEY: ${openssl_key}

% if database:
# Database
SQLALCHEMY_DATABASE_URL: ${}
SQLALCHEMY_DATABASE_ENCODING: utf8
SQLALCHEMY_DATABASE_ECHO: True
% endif