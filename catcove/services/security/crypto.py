from sanic import Sanic
from sanic.exceptions import SanicException
import re
from Crypto.PublicKey import ECC
from Crypto.Cipher import DES
from pathlib import Path

try:
    public_key = Path(Sanic.get_app("Meow").config.ECC_PUBLIC_KEY).read_text()
    private_key = Path(Sanic.get_app("Meow").config.ECC_PRIVATE_KEY).read_text()
except:
    raise SanicException("Could not get the ECC_KEY from app.")

prkey_start = "-----BEGIN EC PRIVATE KEY-----"
pbkey_start = "-----BEGIN PUBLIC KEY-----"
prkey_end = "-----END EC PRIVATE KEY-----"
pbkey_end = "-----END PUBLIC KEY-----"
prkey = re.compile(prkey_start+".*?"+prkey_end, flags=re.DOTALL)
pbkey = re.compile(pbkey_start+".*?"+pbkey_end, flags=re.DOTALL)
pub_key = ECC.import_key(pbkey.findall(public_key)[0])
pri_key = ECC.import_key(prkey.findall(private_key)[0])


async def register_key(app: Sanic):
    app.ctx.ecc_pub = pub_key
    app.ctx.ecc_pri = pri_key
