# Generate automatically, please adjust!!!

# SECRET_KEY
SECRET_KEY: ${openssl_key}
ECC_PRIVATE_KEY: ${instance_path}/eckey.pem
ECC_PUBLIC_KEY: ${instance_path}/ecpubkey.pem

# DATABASE
${databases if databases else ""}
