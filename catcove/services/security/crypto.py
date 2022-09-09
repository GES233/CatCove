from sanic import Sanic
from sanic.exceptions import SanicException
import re
import ecdsa
from pathlib import Path


pub_key = Path(Sanic.get_app("Meow").config.ECC_PUBLIC_KEY).read_text()
pri_key = Path(Sanic.get_app("Meow").config.ECC_PRIVATE_KEY).read_text()



def gen_key(path: Path) -> None:
    sk = ecdsa.SigningKey.generate(ecdsa.NIST256p)
    vk = sk.verifying_key
    eckey = sk.to_pem()
    sk_path = Path(path / "eckey.pem")
    if not sk_path.exists():
        sk_path.touch()
        sk_path.write_bytes(eckey)
    ecpubkey = vk.to_pem()
    pk_path = Path(path / "ecpubkey.pem")
    if not pk_path.exists():
        pk_path.touch()
        pk_path.write_bytes(ecpubkey)


def register_key(app: Sanic):
    app.ctx.ecc_pub = Path(app.config.ECC_PUBLIC_KEY).read_text()
    app.ctx.ecc_pri = Path(app.config.ECC_PRIVATE_KEY).read_text()
