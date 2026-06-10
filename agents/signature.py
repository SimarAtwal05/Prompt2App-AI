from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# generate once per run (fine for task)
PRIVATE_KEY = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
PUBLIC_KEY = PRIVATE_KEY.public_key()

def sign_patch(state):
    signature = PRIVATE_KEY.sign(
        state["patch"].encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    with open("patches/fix.sig", "wb") as f:
        f.write(signature)

    return {}

def verify_signature(state):
    try:
        with open("patches/fix.sig", "rb") as f:
            signature = f.read()

        PUBLIC_KEY.verify(
            signature,
            state["patch"].encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        return {"signature_valid": True}

    except Exception:
        return {"signature_valid": False}