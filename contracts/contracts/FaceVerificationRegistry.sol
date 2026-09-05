// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title FaceVerificationRegistry
 * @dev Cryptographic tamper-evident registry for facial recognition and reverse-image verification results.
 */
contract FaceVerificationRegistry {
    struct VerificationRecord {
        bytes32 recordId;
        bytes32 imageHash;
        bytes32 matchDataHash;
        bytes32 recordHash;
        string matchStatus;
        string resultUrl;
        uint256 timestamp;
        address submitter;
    }

    // Mapping from recordId to VerificationRecord
    mapping(bytes32 => VerificationRecord) private _records;
    
    // List of all recorded IDs for iteration/enumeration
    bytes32[] private _recordIds;

    // Event emitted when a new verification record is created
    event VerificationRecorded(
        bytes32 indexed recordId,
        bytes32 indexed imageHash,
        bytes32 matchDataHash,
        bytes32 recordHash,
        string matchStatus,
        string resultUrl,
        uint256 timestamp,
        address indexed submitter
    );

    /**
     * @notice Store a new tamper-evident verification record.
     * @param imageHash SHA-256 hash of the original input photograph.
     * @param matchDataHash SHA-256 hash of the canonicalized match data.
     * @param recordHash Combined SHA-256 hash of imageHash, matchDataHash, timestamp, and resultUrl.
     * @param matchStatus Status string (e.g. "MATCH_FOUND", "NO_MATCH_FOUND").
     * @param resultUrl Matching URL or reference string.
     * @return recordId Unique bytes32 identifier generated for the record.
     */
    function createVerificationRecord(
        bytes32 imageHash,
        bytes32 matchDataHash,
        bytes32 recordHash,
        string calldata matchStatus,
        string calldata resultUrl
    ) external returns (bytes32 recordId) {
        require(imageHash != bytes32(0), "Invalid image hash");
        require(matchDataHash != bytes32(0), "Invalid match data hash");
        require(recordHash != bytes32(0), "Invalid record hash");

        uint256 currentTimestamp = block.timestamp;
        
        // Compute unique recordId from imageHash, matchDataHash, block timestamp, and submitter address
        recordId = keccak256(
            abi.encodePacked(imageHash, matchDataHash, currentTimestamp, msg.sender)
        );

        require(_records[recordId].timestamp == 0, "Record already exists");

        VerificationRecord memory record = VerificationRecord({
            recordId: recordId,
            imageHash: imageHash,
            matchDataHash: matchDataHash,
            recordHash: recordHash,
            matchStatus: matchStatus,
            resultUrl: resultUrl,
            timestamp: currentTimestamp,
            submitter: msg.sender
        });

        _records[recordId] = record;
        _recordIds.push(recordId);

        emit VerificationRecorded(
            recordId,
            imageHash,
            matchDataHash,
            recordHash,
            matchStatus,
            resultUrl,
            currentTimestamp,
            msg.sender
        );

        return recordId;
    }

    /**
     * @notice Retrieve a verification record by its recordId.
     */
    function getVerificationRecord(bytes32 recordId)
        external
        view
        returns (
            bytes32 imageHash,
            bytes32 matchDataHash,
            bytes32 recordHash,
            string memory matchStatus,
            string memory resultUrl,
            uint256 timestamp,
            address submitter
        )
    {
        VerificationRecord memory record = _records[recordId];
        require(record.timestamp != 0, "Record not found");

        return (
            record.imageHash,
            record.matchDataHash,
            record.recordHash,
            record.matchStatus,
            record.resultUrl,
            record.timestamp,
            record.submitter
        );
    }

    /**
     * @notice Verify whether given local hashes match the recorded on-chain record.
     */
    function verifyRecord(
        bytes32 recordId,
        bytes32 expectedImageHash,
        bytes32 expectedMatchDataHash,
        bytes32 expectedRecordHash
    ) external view returns (bool isValid) {
        VerificationRecord memory record = _records[recordId];
        if (record.timestamp == 0) {
            return false;
        }

        return (
            record.imageHash == expectedImageHash &&
            record.matchDataHash == expectedMatchDataHash &&
            record.recordHash == expectedRecordHash
        );
    }

    /**
     * @notice Return total recorded verification items count.
     */
    function getRecordCount() external view returns (uint256) {
        return _recordIds.length;
    }

    /**
     * @notice Retrieve record ID by index.
     */
    function getRecordIdAtIndex(uint256 index) external view returns (bytes32) {
        require(index < _recordIds.length, "Index out of bounds");
        return _recordIds[index];
    }
}
