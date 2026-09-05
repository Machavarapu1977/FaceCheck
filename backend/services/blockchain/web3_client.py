import time
import logging
from typing import Dict, Any, Optional
from web3 import Web3
from eth_account import Account
from backend.config import settings
from backend.services.blockchain.contract import CONTRACT_ABI

logger = logging.getLogger("blockchain_client")

NETWORK_NAMES = {
    1: "Ethereum Mainnet",
    11155111: "Ethereum Sepolia",
    1337: "Local Hardhat Testnet",
    5: "Ethereum Goerli",
    137: "Polygon Mainnet",
    80001: "Polygon Mumbai",
}


class Web3Client:
    def __init__(self):
        self.rpc_url = settings.BLOCKCHAIN_RPC_URL
        self.private_key = settings.BLOCKCHAIN_PRIVATE_KEY
        self.contract_address = settings.CONTRACT_ADDRESS
        self.explorer_base_url = settings.EXPLORER_URL.rstrip("/")

        if not self.contract_address:
            try:
                import json, os
                deploy_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "contracts", "deployment.json")
                if os.path.exists(deploy_path):
                    with open(deploy_path, "r") as f:
                        data = json.load(f)
                        self.contract_address = data.get("contractAddress", "")
            except Exception:
                pass

        self.chain_id = settings.CHAIN_ID
        self.network_name = NETWORK_NAMES.get(self.chain_id, f"Chain {self.chain_id}")

        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))

        if self.private_key:
            self.account = Account.from_key(self.private_key)
        else:
            self.account = None

        if self.contract_address and self.w3.is_address(self.contract_address):
            self.contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(self.contract_address),
                abi=CONTRACT_ABI
            )
        else:
            self.contract = None

    def is_connected(self) -> bool:
        try:
            return self.w3.is_connected()
        except Exception:
            return False

    def hex_to_bytes32(self, hex_str: str) -> bytes:
        clean_hex = hex_str.lower().replace("0x", "")
        if len(clean_hex) < 64:
            clean_hex = clean_hex.zfill(64)
        return bytes.fromhex(clean_hex[:64])

    def _make_receipt(self, tx_hash_hex: str, block_number: int, record_id: str) -> Dict[str, Any]:
        """Build a receipt dict including network metadata and explorer link."""
        explorer_url = None
        if self.explorer_base_url and tx_hash_hex:
            explorer_url = f"{self.explorer_base_url}/tx/{tx_hash_hex}"
        return {
            "transaction_hash": tx_hash_hex,
            "block_number": block_number,
            "record_id": record_id,
            "contract_address": self.contract_address,
            "chain_id": self.chain_id,
            "network_name": self.network_name,
            "submitter_address": self.account.address if self.account else "",
            "timestamp": int(time.time()),
            "explorer_url": explorer_url,
        }

    def submit_verification_record(
        self,
        image_hash: str,
        match_data_hash: str,
        record_hash: str,
        match_status: str,
        result_url: str
    ) -> Optional[Dict[str, Any]]:
        if not self.is_connected() or not self.contract or not self.account:
            if settings.DEMO_MODE:
                logger.warning("[BLOCKCHAIN] Web3 connection or contract unconfigured. Using local demo receipt.")
                fake_tx = "0x" + "a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0"
                fake_rid = "0x" + "11223344556677889900aabbccddeeff11223344556677889900aabbccddeeff"
                return self._make_receipt(fake_tx, 104250, fake_rid)
            else:
                raise RuntimeError("Blockchain RPC/Contract unconfigured and DEMO_MODE is False.")

        try:
            img_bytes32 = self.hex_to_bytes32(image_hash)
            match_bytes32 = self.hex_to_bytes32(match_data_hash)
            record_bytes32 = self.hex_to_bytes32(record_hash)

            nonce = self.w3.eth.get_transaction_count(self.account.address)
            gas_price = self.w3.eth.gas_price

            txn = self.contract.functions.createVerificationRecord(
                img_bytes32,
                match_bytes32,
                record_bytes32,
                match_status,
                result_url
            ).build_transaction({
                'chainId': self.chain_id,
                'gas': 1000000,
                'gasPrice': gas_price,
                'nonce': nonce,
            })

            signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=self.private_key)
            raw_bytes = getattr(signed_txn, "raw_transaction", getattr(signed_txn, "rawTransaction", None))
            tx_hash = self.w3.eth.send_raw_transaction(raw_bytes)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)

            logs = self.contract.events.VerificationRecorded().process_receipt(receipt)
            record_id_hex = "0x" + logs[0]['args']['recordId'].hex() if logs else "0x" + tx_hash.hex()[:64]
            tx_hash_hex = "0x" + tx_hash.hex()

            logger.info(f"[BLOCKCHAIN] Transaction confirmed. TxHash: {tx_hash_hex}")
            return self._make_receipt(tx_hash_hex, receipt['blockNumber'], record_id_hex)

        except Exception as e:
            logger.error(f"[BLOCKCHAIN] Transaction failed: {str(e)}")
            if settings.DEMO_MODE:
                fake_tx = "0x" + "a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0"
                fake_rid = "0x" + "11223344556677889900aabbccddeeff11223344556677889900aabbccddeeff"
                return self._make_receipt(fake_tx, 104250, fake_rid)
            raise RuntimeError(f"Blockchain submission error: {str(e)}")

    def get_verification_record(self, record_id_hex: str) -> Dict[str, Any]:
        if not self.is_connected() or not self.contract:
            raise RuntimeError("Blockchain RPC/Contract is not available.")

        record_id_bytes = self.hex_to_bytes32(record_id_hex)
        res = self.contract.functions.getVerificationRecord(record_id_bytes).call()
        return {
            "record_id": record_id_hex,
            "image_hash": "0x" + res[0].hex(),
            "match_data_hash": "0x" + res[1].hex(),
            "record_hash": "0x" + res[2].hex(),
            "match_status": res[3],
            "result_url": res[4],
            "timestamp": res[5],
            "submitter": res[6]
        }

    def verify_record_on_chain(
        self,
        record_id_hex: str,
        image_hash: str,
        match_data_hash: str,
        record_hash: str
    ) -> bool:
        if not self.is_connected() or not self.contract:
            raise RuntimeError("Blockchain RPC/Contract is not available for verification.")

        record_id_bytes = self.hex_to_bytes32(record_id_hex)
        img_bytes32 = self.hex_to_bytes32(image_hash)
        match_bytes32 = self.hex_to_bytes32(match_data_hash)
        record_bytes32 = self.hex_to_bytes32(record_hash)

        return self.contract.functions.verifyRecord(
            record_id_bytes,
            img_bytes32,
            match_bytes32,
            record_bytes32
        ).call()
