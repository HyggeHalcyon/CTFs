// SPDX-License-Identifier: MIT
pragma solidity ^0.8.3;
import "./Nft.sol";

contract Auction {
    address public seller;
    Nft public nft;
    uint256 public tokenId;
    uint256 public endTime;

    uint256 public immutable targetAmount; 
    uint256 public constant bidAmount = 1 ether;

    address public lastBidder;
    bool public ended;
    uint256 public bids;
    uint256 public uniqueBidders;     
    mapping(address => bool) public hasBid; 

    
    event Bid(address indexed bidder, uint256 newBalance);
    event Claimed(address indexed winner, uint256 paidOut);

    constructor(string memory name_, string memory symbol_, uint256 targetAmountWei) {
        seller = msg.sender;
        nft = new Nft(name_, symbol_);
        tokenId = nft.mintTo(address(this));
        nft.transferOwnership(seller);

        targetAmount = targetAmountWei;
        endTime = block.timestamp + 1 hours;
    }

    function bid() external payable {
        require(block.timestamp < endTime, "Auction ended");
        require(msg.value == bidAmount, "Bid must be 1 ether");
        require(address(this).balance <= targetAmount, "Target already reached");
        require(msg.sender != lastBidder, "You are already the highest bidder");
        lastBidder = msg.sender;
        bids += 1;
        endTime = block.timestamp + 1 hours; 

        if (!hasBid[msg.sender]) {
            hasBid[msg.sender] = true;
            uniqueBidders += 1;
        }

        emit Bid(msg.sender, address(this).balance);
    }

    function withdraw() external {
        require(!ended, "Already claimed");
        require(uniqueBidders >= 2, "Need bids from 2 different contracts");
        require(address(this).balance >= targetAmount, "Target not reached");

        ended = true;

        nft.safeTransferFrom(address(this), lastBidder, tokenId);
        uint256 payout = address(this).balance;
        (bool ok, ) = payable(msg.sender).call{value: payout}("");
        require(ok, "Payout failed");

        emit Claimed(lastBidder, payout);
    }

    function cancel() external{
        require(bids == 0, "Can't cancel after a bid");
        selfdestruct(payable(seller));
    }


    function Balance() external view returns (uint256) {
        return address(this).balance;
    }


}