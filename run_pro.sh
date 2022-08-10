cd ~CatCove/
. venv/bin/activate
export ENV_APP="pro"
sanic catcove:create_app --factory --host 0.0.0.0