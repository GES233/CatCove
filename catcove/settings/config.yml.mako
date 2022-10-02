# Generate automatically, please adjust!!!

# SECRET_KEY
SECRET_KEY: ${openssl_key}
ECC_PRIVATE_KEY: ${ecc_prk_path}
ECC_PUBLIC_KEY: ${ecc_puk_path}

# DATABASE
${databases if databases else ""}${redis_uri__ if redis_uri__ else ""}

# STATIC_PATHS
${raw_path if raw_path else ""}${avatar_path if avatar_path else ""}
