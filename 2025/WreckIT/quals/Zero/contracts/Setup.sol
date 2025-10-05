// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {EthKing} from "./EthKing.sol";

contract Setup {
	EthKing public ethking;
	address player;

	constructor(address _player) payable {
		player = _player;
		ethking = new EthKing{value: 100 ether}();
	}

	function isSolved() external view returns (bool) {
		return player.balance > 100 ether;
	}
}
