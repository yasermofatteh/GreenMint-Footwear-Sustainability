// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GreenMintPackaging {
    mapping(address => uint256) public deposits;

    event Deposit(address indexed customer, uint256 amount);
    event Refund(address indexed customer, uint256 amount);

    // Customer pays a deposit
    function payDeposit() external payable {
        require(msg.value > 0, "Deposit must be greater than zero");
        deposits[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }

    // Retailer processes refund
    function refund(address payable customer, uint256 amount) external {
        require(deposits[customer] >= amount, "Insufficient deposit balance");
        deposits[customer] -= amount;
        customer.transfer(amount);
        emit Refund(customer, amount);
    }
}
