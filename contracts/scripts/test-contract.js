const hre = require("hardhat");

const fs = require("fs");
const path = require("path");

async function main() {
    const deploymentPath = path.join(__dirname, "../deployment.json");
    if (!fs.existsSync(deploymentPath)) {
        throw new Error("deployment.json not found. Please run 'npx hardhat run scripts/deploy.js --network localhost' first.");
    }
    const deploymentInfo = JSON.parse(fs.readFileSync(deploymentPath, "utf8"));
    const contractAddress = deploymentInfo.contractAddress;
    const contract = await hre.ethers.getContractAt("FaceVerificationRegistry", contractAddress);

    console.log("Checking contract status...");
    const count = await contract.getRecordCount();
    console.log(`Current total verification records on-chain: ${count}`);

    console.log("Creating a test verification record...");
    const imgHash = hre.ethers.id("sample-photo");
    const matchHash = hre.ethers.id("sample-match-data");
    const recordHash = hre.ethers.id("sample-record");

    const tx = await contract.createVerificationRecord(
        imgHash,
        matchHash,
        recordHash,
        "MATCH_FOUND",
        "https://example.com/result"
    );
    await tx.wait();

    const newCount = await contract.getRecordCount();
    console.log(`Success! Updated record count: ${newCount}`);
}

main().then(() => process.exit(0)).catch((err) => {
    console.error(err);
    process.exit(1);
});
