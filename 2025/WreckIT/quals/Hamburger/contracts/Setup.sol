// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {Ephemeral} from "./EphemeralLocker.sol";

contract Setup {
	Ephemeral public ephemeral;
	address player;

	constructor(address _player) payable {
		player = _player;
		ephemeral = new Ephemeral{value: 10 ether}(msg.sender, address(this));
	}

	function isSolved() external view returns (bool) {
		return player.balance > 10 ether;
	}
}
