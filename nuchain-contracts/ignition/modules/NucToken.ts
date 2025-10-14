import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

// This Ignition module handles the deployment of the NucToken smart contract

const NucTokenModule = buildModule("NucTokenModule", (m) => {
    // Deploys a new instance of the NucToken contract
    const nucToken = m.contract("NucToken", []);

    // Returns the deployed contract instance
    return { nucToken };
});

export default NucTokenModule;