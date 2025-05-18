// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

import "./ChovidGiveaway.sol";

contract Setup {
    ChovidGiveaway public giveaway;
    bytes32 public root;

    constructor(bytes32 _root) payable {
        giveaway = new ChovidGiveaway();
        giveaway.registerGiveaway{value: 0x40000}(_root);
    }

    function isSolved() public view returns (bool) {
        return address(giveaway).balance == 0;
    }
}

// forge create src/Setup.sol:Setup --rpc-url local --account local --value 262144 --broadcast --constructor-args "0x00000000000000000000000000000000ec013753fda740f8bc74a966daea0723"