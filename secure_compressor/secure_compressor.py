import os
import json
import zlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding

class SecureCompressor:
    def __init__(self, password: str, salt: bytes = os.urandom(16)):
        self.password = password.encode()
        self.salt = salt
        self.backend = default_backend()
        self.key = self.derive_key(self.password, self.salt)

    def derive_key(self, password, salt):
        """Derive a 256-bit AES key from the password."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        return kdf.derive(password)

    def encrypt(self, data: bytes):
        """Encrypt data using AES."""
        iv = os.urandom(16)  # Generate a random Initialization Vector (IV)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        # Pad data to block size (16 bytes)
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()

        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return iv + encrypted_data  # Prepend IV for use during decryption

    def decrypt(self, data: bytes):
        """Decrypt data using AES."""
        iv = data[:16]  # Extract IV from the start of the data
        encrypted_data = data[16:]

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()

        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Remove padding
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        original_data = unpadder.update(padded_data) + unpadder.finalize()

        return original_data

    def compress_and_encrypt_file(self, file_path: str):
        """Compress and encrypt a single file."""
        with open(file_path, 'rb') as file:
            data = file.read()

        # Compress the data
        compressed_data = zlib.compress(data)

        # Encrypt the compressed data
        encrypted_data = self.encrypt(compressed_data)

        return encrypted_data

    def compress_and_encrypt_folder(self, folder_path: str, output_file: str):
        """Compress and encrypt an entire folder."""
        archive = {}

        # Walk through the folder
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, folder_path)
                encrypted_data = self.compress_and_encrypt_file(full_path)
                archive[relative_path] = encrypted_data

        # Serialize the archive
        serialized_archive = json.dumps(
            {k: v.hex() for k, v in archive.items()}
        ).encode()

        # Encrypt the serialized archive
        encrypted_archive = self.encrypt(serialized_archive)

        # Save to file
        with open(output_file, 'wb') as out_file:
            out_file.write(self.salt + encrypted_archive)

        print(f"Folder compressed and encrypted to: {output_file}")

    def decrypt_and_decompress_folder(self, encrypted_file: str, output_folder: str):
        """Decrypt and decompress an encrypted folder."""
        with open(encrypted_file, 'rb') as in_file:
            data = in_file.read()

        # Extract salt and encrypted data
        salt = data[:16]
        encrypted_archive = data[16:]

        # Re-derive the key
        self.key = self.derive_key(self.password, salt)

        # Decrypt the archive
        decrypted_data = self.decrypt(encrypted_archive)

        # Deserialize the archive
        archive = json.loads(decrypted_data.decode())
        archive = {k: bytes.fromhex(v) for k, v in archive.items()}

        # Decompress and save files
        for relative_path, encrypted_data in archive.items():
            decrypted_file_data = zlib.decompress(self.decrypt(encrypted_data))
            full_path = os.path.join(output_folder, relative_path)

            # Create directories if needed
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, 'wb') as out_file:
                out_file.write(decrypted_file_data)

        print(f"Folder decrypted and decompressed to: {output_folder}")
