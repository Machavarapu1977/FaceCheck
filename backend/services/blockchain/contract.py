CONTRACT_ABI = [
  {
    "anonymous": False,
    "inputs": [
      { "indexed": True, "internalType": "bytes32", "name": "recordId", "type": "bytes32" },
      { "indexed": True, "internalType": "bytes32", "name": "imageHash", "type": "bytes32" },
      { "indexed": False, "internalType": "bytes32", "name": "matchDataHash", "type": "bytes32" },
      { "indexed": False, "internalType": "bytes32", "name": "recordHash", "type": "bytes32" },
      { "indexed": False, "internalType": "string", "name": "matchStatus", "type": "string" },
      { "indexed": False, "internalType": "string", "name": "resultUrl", "type": "string" },
      { "indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256" },
      { "indexed": True, "internalType": "address", "name": "submitter", "type": "address" }
    ],
    "name": "VerificationRecorded",
    "type": "event"
  },
  {
    "inputs": [
      { "internalType": "bytes32", "name": "imageHash", "type": "bytes32" },
      { "internalType": "bytes32", "name": "matchDataHash", "type": "bytes32" },
      { "internalType": "bytes32", "name": "recordHash", "type": "bytes32" },
      { "internalType": "string", "name": "matchStatus", "type": "string" },
      { "internalType": "string", "name": "resultUrl", "type": "string" }
    ],
    "name": "createVerificationRecord",
    "outputs": [
      { "internalType": "bytes32", "name": "recordId", "type": "bytes32" }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      { "internalType": "bytes32", "name": "recordId", "type": "bytes32" }
    ],
    "name": "getVerificationRecord",
    "outputs": [
      { "internalType": "bytes32", "name": "imageHash", "type": "bytes32" },
      { "internalType": "bytes32", "name": "matchDataHash", "type": "bytes32" },
      { "internalType": "bytes32", "name": "recordHash", "type": "bytes32" },
      { "internalType": "string", "name": "matchStatus", "type": "string" },
      { "internalType": "string", "name": "resultUrl", "type": "string" },
      { "internalType": "uint256", "name": "timestamp", "type": "uint256" },
      { "internalType": "address", "name": "submitter", "type": "address" }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      { "internalType": "bytes32", "name": "recordId", "type": "bytes32" },
      { "internalType": "bytes32", "name": "expectedImageHash", "type": "bytes32" },
      { "internalType": "bytes32", "name": "expectedMatchDataHash", "type": "bytes32" },
      { "internalType": "bytes32", "name": "expectedRecordHash", "type": "bytes32" }
    ],
    "name": "verifyRecord",
    "outputs": [
      { "internalType": "bool", "name": "isValid", "type": "bool" }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]
