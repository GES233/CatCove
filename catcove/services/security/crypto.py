from sanic import Sanic
from sanic.exceptions import SanicException
import re
import ecdsa
from pathlib import Path


def read_key_from_path():
    try:
        public_key = Path(Sanic.get_app("Meow").config.ECC_PUBLIC_KEY).read_text()
        private_key = Path(Sanic.get_app("Meow").config.ECC_PRIVATE_KEY).read_text()
        '''
        prkey_start = "-----BEGIN EC PRIVATE KEY-----"
        pbkey_start = "-----BEGIN PUBLIC KEY-----"
        prkey_end = "-----END EC PRIVATE KEY-----"
        pbkey_end = "-----END PUBLIC KEY-----"
        prkey = re.compile(prkey_start+".*?"+prkey_end, flags=re.DOTALL)
        pbkey = re.compile(pbkey_start+".*?"+pbkey_end, flags=re.DOTALL)
        
        from Crypto.PublicKey import ECC
        pub_key = ECC.import_key(pbkey.findall(public_key)[0])
        pri_key = ECC.import_key(prkey.findall(private_key)[0])
        '''
    except:
        raise SanicException("Could not get the ECC_KEY from app.")
    
    return None

pub_key = Path(Sanic.get_app("Meow").config.ECC_PUBLIC_KEY).read_text()
pri_key = Path(Sanic.get_app("Meow").config.ECC_PRIVATE_KEY).read_text()

def gen_key(path: Path) -> None:
    sk = ecdsa.SigningKey.generate(ecdsa.NIST256p)
    vk = sk.verifying_key
    eckey = sk.to_pem()
    Path(path / "eckey.pem").touch
    ecpubkey = vk.to_pem()


def register_key(app: Sanic):
    app.ctx.ecc_pub = Path(app.config.ECC_PUBLIC_KEY).read_text()
    app.ctx.ecc_pri = Path(app.config.ECC_PRIVATE_KEY).read_text()
