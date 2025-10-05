// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title EthKing
 * @notice A racing game where the first player to interact with the contract after the deadline wins all funds
 * @dev Players pay a fee to participate, and the first to call win() after the deadline claims everything
 */
contract EthKing {
	/**
	 * @notice The minimum fee required to participate in the game
	 * @dev Set to 0.001 ether and cannot be changed after deployment
	 */
	uint256 immutable FEE = 0.001 ether;
	
	/**
	 * @notice The timestamp after which the first interaction wins all funds
	 * @dev Set to 30 seconds after contract deployment
	 */
	uint256 deadline;

	/**
	 * @notice Whether the game has ended and prize has been claimed
	 * @dev Set to true when someone wins after the deadline
	 */
	bool gameEnded;

	error OnlyHuman();
	error GameAlreadyEnded();

	/**
	 * @notice Ensures that only externally owned accounts (EOAs) can call the function
	 * @dev Prevents smart contracts from calling by checking code length is zero
	 * @custom:security This modifier helps prevent automated contract-based attacks
	 */
	modifier onlyHuman() {
		require(msg.sender.code.length == 0, OnlyHuman());
		_;
	}

	/**
	 * @notice Initializes the EthKing game contract
	 * @dev Establishes a 30-second deadline after which the first interaction wins
	 * @custom:payable Contract must receive ETH during deployment to fund the prize pool
	 */
	constructor() payable {
		deadline = block.timestamp + 60 seconds;
		gameEnded = false;
	}

	/**
	 * @notice Allows players to participate in the race or claim the prize if deadline has passed
	 * @dev Players must send at least FEE amount and be an EOA (externally owned account)
	 * @custom:payable Requires minimum payment of FEE (0.001 ether) to participate
	 * @custom:timing If called after deadline, the first caller wins all contract funds
	 * @custom:timing If called before deadline, payment is accepted but no winner yet
	 * @custom:access Only externally owned accounts can call this function (enforced by onlyHuman modifier)
	 */
	function win() external payable onlyHuman {
		require(msg.value >= FEE);
		require(!gameEnded, GameAlreadyEnded());

		if (block.timestamp >= deadline) {
			gameEnded = true;
			payable(msg.sender).transfer(address(this).balance);
		}
		// If before deadline, just accept the payment and wait
	}
}