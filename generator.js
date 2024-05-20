const fs = require("fs");
const ethers = require("ethers");
const mainnetNetwork = "mainnet";
const mainnetProvider = ethers.getDefaultProvider(mainnetNetwork);
const waitlist = require("./alloc8.json");

let waitlistCount = 0;

// Function to generate the next private key and its corresponding public address
// async function generateNextPrivateKeyAndAddress() {
//   if (waitlistCount <= waitlist.length) {
//     const { Timestamp, Address, Twitter, Email, Followed, FollowerCount } =
//       waitlist[waitlistCount];
//     waitlistCount++;
//     const ethBalance = await mainnetProvider.getBalance(Address);
//     const balanceInEth = ethers.formatEther(ethBalance);
//     const csvRow = `${Timestamp},${Address},${Twitter},${Email},${Followed},${FollowerCount},${balanceInEth}\n`;

//     // Append data to CSV file
//     fs.appendFile("waitlist.csv", csvRow, (err) => {
//       if (err) throw err;
//       console.log("Data appended to waitlist.csv", "color:green;");
//     });
//   } else {
//     console.log("All Data appended to waitlist.csv");
//   }
// }

// Set interval to generate the next private key and public address every 200 milliseconds
// const intervalId = setInterval(generateNextPrivateKeyAndAddress, 200);

const fetchTwitterFollowerCount = async () => {
  console.log("running");
  try {
    const resp = await fetch(
      "https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names=itrebeleth"
    );
    // {
    //   headers: new Headers({
    //     Authorization:
    //       "Bearer AAAAAAAAAAAAAAAAAAAAABoqtgEAAAAAINGrF8AzhWHk10ziS3sCsG6fV6g%3DadnPcDX3fg6ZBUH03qFtpNVfIjEdWO5jG4BIEYqwmH7DLKTVYK",
    //   }),
    // }

    const data = await resp.json();
    console.log(data);
  } catch (error) {
    console.log("error fetching followers", error);
  }
};

fetchTwitterFollowerCount();
