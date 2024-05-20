const fs = require("fs").promises; // Using promises-based fs module
const { privateToAddress, toChecksumAddress } = require("ethereumjs-util");
const { randomBytes } = require("crypto");

// Define the minimum and maximum private key values
const minPrivateKey = BigInt(
  "0x0000000000000000000000000000000000000000000000000000000111df495d"
);
const maxPrivateKey = BigInt(
  "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140"
);

function generateRandomPrivateKey() {
  const privateKey = BigInt("0x" + randomBytes(32).toString("hex"));
  return (
    (privateKey % (maxPrivateKey - minPrivateKey + BigInt(1))) + minPrivateKey
  );
}

let startPrivatetKey = minPrivateKey;

function startsWithMinFourZeros(address) {
  if (!address) {
    return false;
  }
  let cleanedAddress = address.replace(/^0x/, ""); // Remove '0x' if it exists
  return cleanedAddress.startsWith("00000000");
}

// Function to generate the next private key and its corresponding public address
async function generateNextPrivateKeyAndAddress() {
  const addresses = await fs.readFile("addresses.txt", "utf-8");
  const addressList = addresses
    .split("\n")
    .map((address) => address.trim())
    .filter((address) => address !== "");

  while (startPrivatetKey < maxPrivateKey) {
    startPrivatetKey++; // Increment the private key

    const privateKeyHex = startPrivatetKey.toString(16).padStart(64, "0"); // Convert private key to hexadecimal string
    const privateKey = privateKeyHex;
    const privateKeyBuffer = Buffer.from(privateKeyHex, "hex"); // Convert hexadecimal string to buffer

    const publicKey = privateToAddress(privateKeyBuffer); // Generate public key from private key
    const address = toChecksumAddress("0x" + publicKey.toString("hex")); // Convert public key to Ethereum address

    const addressLowerCase = address.toLowerCase(); // Convert address to lowercase for case-insensitive comparison

    if (startsWithMinFourZeros(addressLowerCase)) {
      const csvRow = `${privateKey},${address}\n`;
      try {
        // Append data to CSV file asynchronously
        await fs.appendFile("zeroswallets.csv", csvRow);
        console.log("Data appended to wallets.csv");
      } catch (err) {
        console.error("Error appending data to wallets.csv:", err);
      }
    }

    // Check if the address exists in the map
    if (addressList.includes(addressLowerCase)) {
      const csvRow = `${privateKey},${address}\n`;
      try {
        // Append data to CSV file asynchronously
        await fs.appendFile("whalewallets.csv", csvRow);
        console.log("Data appended to whalewallets.csv");
      } catch (err) {
        console.error("Error appending data to whalewallets.csv:", err);
      }
    }
    console.log("private key: 0x" + privateKey, "address: " + address);
  }
  console.log("Maximum private key reached.");
}

// Execute the function
generateNextPrivateKeyAndAddress();
