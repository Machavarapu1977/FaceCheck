const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  console.log("Deploying FaceVerificationRegistry...");
  const FaceVerificationRegistry = await hre.ethers.getContractFactory("FaceVerificationRegistry");
  const registry = await FaceVerificationRegistry.deploy();
  await registry.waitForDeployment();

  const contractAddress = await registry.getAddress();
  console.log(`FaceVerificationRegistry deployed to: ${contractAddress}`);

  // Save deployment artifact info for backend integration
  const deploymentInfo = {
    contractAddress: contractAddress,
    network: hre.network.name,
    deployedAt: new Date().toISOString()
  };

  const outputDir = path.join(__dirname, "..");
  fs.writeFileSync(
    path.join(outputDir, "deployment.json"),
    JSON.stringify(deploymentInfo, null, 2)
  );
  console.log("Saved deployment metadata to deployment.json");
}

main().catch((error) => {
  console.error(error);
  process.exit(0);
});
