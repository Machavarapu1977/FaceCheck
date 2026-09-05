const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("FaceVerificationRegistry", function () {
  let registry;
  let owner;

  beforeEach(async function () {
    const FaceVerificationRegistry = await ethers.getContractFactory("FaceVerificationRegistry");
    [owner] = await ethers.getSigners();
    registry = await FaceVerificationRegistry.deploy();
  });

  it("Should create a new verification record and emit an event", async function () {
    const imageHash = ethers.id("test_image_bytes");
    const matchDataHash = ethers.id("test_canonical_match_data");
    const recordHash = ethers.id("test_combined_record");
    const matchStatus = "MATCH_FOUND";
    const resultUrl = "https://example.com/profile.jpg";

    const tx = await registry.createVerificationRecord(
      imageHash,
      matchDataHash,
      recordHash,
      matchStatus,
      resultUrl
    );

    const receipt = await tx.wait();
    expect(receipt.status).to.equal(1);

    const recordCount = await registry.getRecordCount();
    expect(recordCount).to.equal(1);

    const recordId = await registry.getRecordIdAtIndex(0);
    const record = await registry.getVerificationRecord(recordId);

    expect(record.imageHash).to.equal(imageHash);
    expect(record.matchDataHash).to.equal(matchDataHash);
    expect(record.recordHash).to.equal(recordHash);
    expect(record.matchStatus).to.equal(matchStatus);
    expect(record.resultUrl).to.equal(resultUrl);
    expect(record.submitter).to.equal(owner.address);
  });

  it("Should verify valid record hashes accurately", async function () {
    const imageHash = ethers.id("img123");
    const matchDataHash = ethers.id("data456");
    const recordHash = ethers.id("rec789");

    const tx = await registry.createVerificationRecord(
      imageHash,
      matchDataHash,
      recordHash,
      "MATCH_FOUND",
      "https://example.com/item"
    );
    await tx.wait();

    const recordId = await registry.getRecordIdAtIndex(0);
    
    // Test valid verification
    const isValid = await registry.verifyRecord(recordId, imageHash, matchDataHash, recordHash);
    expect(isValid).to.equal(true);

    // Test tampered verification
    const tamperedImageHash = ethers.id("tampered_img");
    const isTamperedValid = await registry.verifyRecord(recordId, tamperedImageHash, matchDataHash, recordHash);
    expect(isTamperedValid).to.equal(false);
  });
});
