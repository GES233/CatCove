cd ~CatCove/
export APP_ENV="dev"
. venv/bin/activate
sanic catcove:create_app --factory --host 127.0.0.1 --port 6699 --dev
