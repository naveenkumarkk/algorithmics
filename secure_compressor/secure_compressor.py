import os
import tarfile
import bz2
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

    def create_tar(self, folder_path: str, tar_path: str, compresslevel: int = 9):
        """Create a tar.bz2 archive of the folder with adjustable compression level, excluding unnecessary files."""
        if compresslevel < 1 or compresslevel > 9:
            raise ValueError("Compression level must be between 1 (fastest) and 9 (highest compression).")

        # Use the bz2.BZ2File object to customize the compression level
        with bz2.BZ2File(tar_path, "wb", compresslevel=compresslevel) as bz2_file:
            with tarfile.open(fileobj=bz2_file, mode="w") as tar:
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        if not file.endswith(('.jpg', '.png', '.mp4', '.zip', '.tar', '.bz2')):
                            full_path = os.path.join(root, file)
                            tar.add(full_path, arcname=os.path.relpath(full_path, folder_path))


    def extract_tar(self, tar_path: str, output_folder: str):
        """Extract a tar archive to the specified folder, handling permission errors."""
        try:
            with tarfile.open(tar_path, "r:bz2") as tar:
                for member in tar.getmembers():
                    try:
                        tar.extract(member, path=output_folder)
                    except PermissionError:
                        print(f"Permission denied for {member.name}. Skipping.")
        except Exception as e:
            print(f"An error occurred while extracting {tar_path}: {e}")


    def compress_and_encrypt_folder(self, folder_path: str, output_file: str):
        """Compress and encrypt an entire folder or file."""
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"The folder or file {folder_path} does not exist.")

        tar_path = f"{folder_path}.tar.bz2"

        # Create a tar.bz2 archive for a folder or single file
        self.create_tar(folder_path, tar_path)

        # Read the tar archive
        with open(tar_path, "rb") as tar_file:
            tar_data = tar_file.read()

        # Encrypt the compressed tar archive
        encrypted_data = self.encrypt(tar_data)

        # Write the salt and encrypted data to the output file
        with open(output_file, "wb") as out_file:
            out_file.write(self.salt + encrypted_data)

        os.remove(tar_path)  # Clean up temporary tar file
        print(f"Folder or file compressed and encrypted to: {output_file}")

    def decrypt_and_decompress_folder(self, encrypted_file: str, output_folder: str):
        """Decrypt and decompress an encrypted folder or file."""
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        with open(encrypted_file, "rb") as in_file:
            data = in_file.read()

        # Extract salt and encrypted data
        salt = data[:16]
        encrypted_archive = data[16:]

        # Re-derive the key
        self.key = self.derive_key(self.password, salt)

        # Decrypt the archive
        decrypted_data = self.decrypt(encrypted_archive)

        # Save the tar archive temporarily
        tar_path = os.path.join(output_folder, "temp_archive.tar.bz2")
        with open(tar_path, "wb") as tar_file:
            tar_file.write(decrypted_data)

        # Extract the tar archive
        self.extract_tar(tar_path, output_folder)
        os.remove(tar_path)  # Clean up temporary tar file

        print(f"Folder or file decrypted and decompressed to: {output_folder}")
