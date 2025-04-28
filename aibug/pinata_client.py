"""
Pinata SDK integration for uploading attachments to IPFS.
"""
import os
import os.path

try:
    from pinatapy import PinataPy
except ImportError:
    PinataPy = None

class PinataClient:
    """Client for interacting with Pinata IPFS service."""
    def __init__(self):
        if PinataPy is None:
            raise ImportError("Please install the 'pinatapy-unofficial' package to use Pinata features.")
        # Support JWT or API key/secret authentication
        jwt = os.getenv("PINATA_JWT")
        if jwt:
            try:
                # Initialize client with JWT token
                self.client = PinataPy(jwt=jwt)
            except TypeError:
                raise ValueError("PinataPy does not support JWT authentication; please install a compatible version or use API key/secret.")
        else:
            self.api_key = os.getenv("PINATA_API_KEY")
            self.api_secret = os.getenv("PINATA_API_SECRET")
            if not self.api_key or not self.api_secret:
                raise ValueError(
                    "PINATA_API_KEY and PINATA_API_SECRET environment variables must be set, or set PINATA_JWT for JWT auth"
                )
            self.client = PinataPy(api_key=self.api_key, api_secret=self.api_secret)

    def upload_file(self, file_path: str) -> dict:
        """Upload a local file to Pinata and return its IPFS info."""
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        file_name = os.path.basename(file_path)
        # Pin file to IPFS
        result = self.client.pin_file_to_ipfs(
            file_path,
            pinataMetadata={"name": file_name}
        )
        ipfs_hash = result.get("IpfsHash")
        url = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
        return {"file_name": file_name, "ipfs_hash": ipfs_hash, "url": url}