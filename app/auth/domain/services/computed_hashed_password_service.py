from abc import ABC
from cryptography.hazmat.primitives import hashes

class ComputeHashedPasswordService(ABC):
    def __call__(self, email: str, password: str) -> str:
        digest = hashes.Hash(hashes.SHA256())
        digest.update((email + password).encode())
        hash_value = digest.finalize().hex()
        return hash_value