// SPDX-License-Identifier: MIT

pragma solidity ^0.8.25;

import {Warmup} from "./Warmup.sol";

contract Setup {
    Warmup public warmup;
    constructor() payable {
        warmup = new Warmup();
    }

    function isSolved() external view returns (bool) {
        return warmup.solved();
    }
}