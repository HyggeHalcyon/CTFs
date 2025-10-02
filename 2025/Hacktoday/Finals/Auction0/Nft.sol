// SPDX-License-Identifier: MIT

pragma solidity ^0.8.3;

import "lib/openzeppelin-contracts/contracts/token/ERC721/ERC721.sol";
import "lib/openzeppelin-contracts/contracts/access/Ownable.sol";  

contract Nft is ERC721, Ownable {
    uint256 public nextId;

    constructor(string memory name_, string memory symbol_) ERC721(name_, symbol_) Ownable(msg.sender) {}

    function mintTo(address to) external onlyOwner returns (uint256) {
        unchecked { nextId += 1; }
        uint256 id = nextId;
        _safeMint(to, id);
        return id;
    }
}