// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./Fortress.sol";

contract Setup {
    Fortress public challenge;

    constructor() payable {
        challenge = new Fortress{value: 0.5 ether}(address(this));
    }

    function isSolved() external view returns (bool) {
        // simulate openVault()
        (bool ok, bytes memory ret) = address(challenge).staticcall(
            abi.encodeWithSignature("openVault()")
        );

        if (ok) return false;

        if (ret.length >= 4) {
            bytes4 sel;
            assembly {
                sel := mload(add(ret, 32))
            }
            // bytes4(keccak256("NoShares()"))
            return sel == NoShares.selector;
        }
        return false;
    }
}
