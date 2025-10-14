// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";


contract NucToken is ERC20, Ownable {
    // Track locked balances per user
    mapping(address => uint256) public lockedBalances;

    // Get available (unlocked) balance in user's wallet
    function availableBalanceOf(address account) public view returns (uint256) {
        return balanceOf(account) - lockedBalances[account];
    }

    // Signup: Admin mints 25,000 NUC to new users
    function mintSignup(address to) external onlyOwner {
        _mint(to, 25_000 * 10**18); // 25,000 NUC (18 decimals)
    }

    // Invest: Admin locks user's tokens when they invest in a reactor
    function lock(address user, uint256 amount) external onlyOwner {
        require(availableBalanceOf(user) >= amount, "Insufficient unlocked balance");
        lockedBalances[user] += amount;
        emit TokensLocked(user, amount);
    }

    // Reset: Admin unlocks ALL locked tokens for a user
    function resetPortfolio(address user) external onlyOwner {
        uint256 amount = lockedBalances[user];
        if (amount > 0) {
            lockedBalances[user] = 0;
            emit TokensUnlocked(user, amount);
        }
    }

    // Delete: Admin burns user's tokens (account deletion)
    function burnAccount(address from) external onlyOwner {
        uint256 balance = balanceOf(from);
        _burn(from, balance);
        emit AccountDeleted(from, balance);
    }

    // Prevent transferring locked tokens
    function transfer(address to, uint256 amount) public override returns (bool) {
        require(availableBalanceOf(msg.sender) >= amount, "Cannot transfer locked tokens");
        return super.transfer(to, amount);
    }

    // Prevent transferFrom for locked tokens
    function transferFrom(address from, address to, uint256 amount) public override returns (bool) {
        require(availableBalanceOf(from) >= amount, "Cannot transfer locked tokens");
        return super.transferFrom(from, to, amount);
    }

    // --- Events ---
    event TokensLocked(address indexed user, uint256 amount);
    event TokensUnlocked(address indexed user, uint256 amount);
    event AccountDeleted(address indexed user, uint256 amount);

    // --- Admin Safety ---
    function renounceOwnership() public override onlyOwner view {
        revert("Ownership cannot be renounced!");
    }

    constructor() ERC20("NuChain Token", "NUC") Ownable(msg.sender) {}
}