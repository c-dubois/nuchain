// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract NucToken is ERC20 {
    address public admin;

    // Track locked balances per user
    mapping(address => uint256) public lockedBalances;

    constructor() ERC20("NuChain Token", "NUC") {
        admin = msg.sender;
    }

    function decimals() public pure override returns (uint8) {
        return 18;
    }

    // Get available (unlocked) balance
    function availableBalanceOf(address account) public view returns (uint256) {
        return balanceOf(account) - lockedBalances[account];
    }

    // Mint tokens to user on signup
    function mint(address to, uint256 amount) external {
        require(msg.sender == admin, "Only admin can mint");
        _mint(to, amount);
    }

    // Burn tokens from user on account deletion
    function burn(address from, uint256 amount) external {
        require(msg.sender == admin, "Only admin can burn");
        _burn(from, amount);
    }

    // Lock tokens when user invests in a reactor
    function lock(address user, uint256 amount) external {
        require(msg.sender == admin, "Only admin can lock");
        require(availableBalanceOf(user) >= amount, "Insufficient unlocked balance");
        lockedBalances[user] += amount;
    }

    // Unlock tokens when user resets wallet
    function unlock(address user, uint256 amount) external {
        require(msg.sender == admin, "Only admin can unlock");
        require(lockedBalances[user] >= amount, "Insufficient locked balance");
        lockedBalances[user] -= amount;
    }

    // Override transfer to prevent transferring locked tokens
    function transfer(address to, uint256 amount) public override returns (bool) {
        require(availableBalanceOf(msg.sender) >= amount, "Insufficient unlocked balance");
        return super.transfer(to, amount);
    }

    // Override transferFrom to prevent transferring locked tokens
    function transferFrom(address from, address to, uint256 amount) public override returns (bool) {
        require(availableBalanceOf(from) >= amount, "Insufficient unlocked balance");
        return super.transferFrom(from, to, amount);
    }
}