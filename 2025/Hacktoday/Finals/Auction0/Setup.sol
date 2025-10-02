// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "./Auction.sol";
import "./Nft.sol";

contract Setup {
    Auction public auction;
    Nft public nft;
    uint256 public tokenId;
    receive() external payable {}
    fallback() external payable {}

    constructor() {
        auction = new Auction("Auction", "AUC", 10 ether);
        nft = auction.nft();
        tokenId = auction.tokenId();
    }

    function isSolved() public view returns (bool) {
        require(nft.ownerOf(tokenId) != address(auction), "NFT still owned by auction");
        require(auction.Balance() <= 1 ether, "Contract balance too high");
        require(address(auction) != address(0), "oh no, auction is dead");
        return true;
    }
}