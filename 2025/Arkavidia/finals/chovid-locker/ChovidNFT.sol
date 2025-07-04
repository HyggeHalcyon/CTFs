// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.23;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable2Step.sol";

contract ChovidNFT is ERC721, Ownable {
    uint256 private _nextTokenId;

    constructor() ERC721("ChovidNFT", "CHOVID") Ownable(msg.sender) {}

    function mint(address recipient_) external onlyOwner returns (uint256 tokenId) {
        tokenId = _nextTokenId++;
        _mint(recipient_, tokenId);
    }
}