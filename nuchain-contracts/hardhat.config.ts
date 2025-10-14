import type { HardhatUserConfig } from "hardhat/config";
import hardhatToolboxMochaEthers from "@nomicfoundation/hardhat-toolbox-mocha-ethers";
import hardhatKeystore from "@nomicfoundation/hardhat-keystore";
import hardhatVerify from "@nomicfoundation/hardhat-verify";
import { configVariable } from "hardhat/config";

const config: HardhatUserConfig = {
  plugins: [
    hardhatToolboxMochaEthers,
    hardhatKeystore,
    hardhatVerify,
  ],
  solidity: {
    profiles: {
      default: {
        version: "0.8.28",
      },
      production: {
        version: "0.8.28",
        settings: {
          optimizer: {
            enabled: true,
            runs: 200,
          },
        },
      },
    },
  },
  networks: {
    baseSepolia: {
      type: "http",
      chainType: "generic",
      url: configVariable("BASE_SEPOLIA_RPC_URL"),
      accounts: [configVariable("NUCHAIN_PRIVATE_KEY")],
      chainId: 84532,
    },
  },
  chainDescriptors: {
    84532: {
      name: "Base Sepolia",
      blockExplorers: {
        etherscan: {
          name: "BaseScan",
          url: "https://sepolia.basescan.org",
          apiUrl: "https://api-sepolia.basescan.org/api",
        },
      },
    },
  }
};

export default config;
