// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import {Test, console} from "forge-std/Test.sol";
import {NucToken} from "./NucToken.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract NucTokenTest is Test {
    NucToken public nucToken;
    address public owner;
    address public user1 = address(0x1);
    address public user2 = address(0x2);

    // --- Events mirrored from NucToken ---
    event TokensLocked(address indexed user, uint256 amount);
    event TokensUnlocked(address indexed user, uint256 amount);
    event AccountDeleted(address indexed user, uint256 amount);

    function setUp() public {
        nucToken = new NucToken();
        owner = nucToken.owner();
    }

    // --- Constructor and Initial State Tests ---

    function test_InitialState() public view {
        assertEq(nucToken.name(), "NuChain Token", "Name should be correct");
        assertEq(nucToken.symbol(), "NUC", "Symbol should be correct");
        assertEq(nucToken.decimals(), 18, "Decimals should be 18");
        assertEq(nucToken.owner(), address(this), "Owner should be the test contract");
    }

    // --- Owner Function Tests ---

    function test_OwnerCanMintSignup() public {
        uint256 expectedAmount = 25_000 * 1e18;
        nucToken.mintSignup(user1);
        assertEq(nucToken.balanceOf(user1), expectedAmount, "User1 balance should be 25,000 NUC");
    }

    function test_Revert_NonOwnerCannotMintSignup() public {
        vm.prank(user1);
        vm.expectRevert(abi.encodeWithSelector(Ownable.OwnableUnauthorizedAccount.selector, user1));
        nucToken.mintSignup(user1);
    }

    function test_OwnerCanBurnAccount() public {
        uint256 initialAmount = 25_000 * 1e18;
        nucToken.mintSignup(user1);
        assertEq(nucToken.balanceOf(user1), initialAmount, "Pre-condition failed: balance not minted");

        vm.expectEmit(true, false, false, true);
        emit AccountDeleted(user1, initialAmount);
        nucToken.burnAccount(user1);

        assertEq(nucToken.balanceOf(user1), 0, "Balance was not zero after burn");
    }

    function test_Revert_NonOwnerCannotBurnAccount() public {
        nucToken.mintSignup(user1);
        vm.prank(user1);
        vm.expectRevert(abi.encodeWithSelector(Ownable.OwnableUnauthorizedAccount.selector, user1));
        nucToken.burnAccount(user1);
    }

    // --- Locking, Unlocking, and Transfer Logic Tests ---

    function test_LockAndResetPortfolio() public {
        uint256 totalAmount = 25_000 * 1e18;
        uint256 lockAmount = 10_000 * 1e18;
        nucToken.mintSignup(user1);

        // Lock
        vm.expectEmit(true, false, false, true);
        emit TokensLocked(user1, lockAmount);
        nucToken.lock(user1, lockAmount);
        assertEq(nucToken.lockedBalances(user1), lockAmount, "Locked balance should be updated");
        assertEq(nucToken.availableBalanceOf(user1), totalAmount - lockAmount, "Available balance should decrease");

        // Reset Portfolio (Unlock All)
        vm.expectEmit(true, false, false, true);
        emit TokensUnlocked(user1, lockAmount);
        nucToken.resetPortfolio(user1);
        assertEq(nucToken.lockedBalances(user1), 0, "Locked balance should be zero after reset");
        assertEq(nucToken.availableBalanceOf(user1), totalAmount, "Available balance should be restored");
    }

    function test_Revert_TransferMoreThanAvailable() public {
        uint256 lockAmount = 15_000 * 1e18; // 10,000 $NUC available
        nucToken.mintSignup(user1);
        nucToken.lock(user1, lockAmount);

        uint256 transferAmount = 10_001 * 1e18; // Try to transfer more than available

        vm.prank(user1); // Switch caller to user1
        vm.expectRevert("Cannot transfer locked tokens");
        nucToken.transfer(user2, transferAmount);
    }

    // --- Safety Feature Tests ---
    function test_Revert_RenounceOwnership() public {
        vm.expectRevert("Ownership cannot be renounced!");
        nucToken.renounceOwnership();
    }
}