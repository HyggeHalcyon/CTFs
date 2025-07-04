// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.23;

import "./ChovidLocker.sol";
import "./ChovidNFT.sol";

contract Setup is ERC721Holder {
    bool private solved;
    ChovidLocker public chovidLocker;
    ChovidNFT public chovidNFT;
    uint256 public totalMinted;

    constructor() {
        chovidNFT = new ChovidNFT();
        chovidLocker = new ChovidLocker(address(this), address(chovidNFT));
        uint256 tokenId = chovidNFT.mint(address(this));
        chovidNFT.approve(address(chovidLocker), tokenId);
        ChovidLocker.LockInput[] memory inputs = new ChovidLocker.LockInput[](1);
        inputs[0] = ChovidLocker.LockInput({
            recipient: address(this),
            tokenId: tokenId
        });
        chovidLocker.lock(inputs);
        totalMinted = 1;
    }

    function airdropNFT() external returns (uint256) {
        require(totalMinted < 4, "Max global mint limit reached");
        uint256 tokenId = totalMinted;
        chovidNFT.mint(msg.sender);
        totalMinted++;
        return tokenId;
    }

    function isSolved() external view returns (bool) {
        return chovidLocker.totalLockedNFT() == 0;
    }
}