/**
 * Transaction Demo for GreenMintPackaging
 * ---------------------------------------
 * Run on Node.js with web3.js or ethers.js.
 * Simulates deposit & refund transactions.
 */

const { ethers } = require("ethers");
const provider = new ethers.providers.JsonRpcProvider("http://localhost:8545");

// Replace with deployed contract address & ABI
const contractAddress = "0x123456789abcdef...";
const abi = [
  "function payDeposit() external payable",
  "function refund(address customer, uint256 amount) external",
];

async function main() {
  const [customer, retailer] = await provider.listAccounts();
  const signer = provider.getSigner(customer);
  const contract = new ethers.Contract(contractAddress, abi, signer);

  // Customer pays deposit (€2)
  let tx = await contract.payDeposit({ value: ethers.utils.parseEther("0.002") });
  await tx.wait();
  console.log("Deposit paid by:", customer);

  // Retailer refunds deposit
  const contractRetailer = contract.connect(provider.getSigner(retailer));
  tx = await contractRetailer.refund(customer, ethers.utils.parseEther("0.002"));
  await tx.wait();
  console.log("Refund processed for:", customer);
}

main().catch(console.error);
