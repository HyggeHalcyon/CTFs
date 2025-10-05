// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {Spaceship} from "./Spaceship.sol";

contract Setup {
	address owner;
	Spaceship public spaceship;

	modifier ownerOnly {
		require(msg.sender == owner);
		_;
	}

	constructor() payable {
		owner = msg.sender;

		spaceship = new Spaceship();
		spaceship.addGpsGadget{value: 10 ether}(address(this), 0.0001 ether, 100);
	}

	function updateAltitude(uint256 u) ownerOnly external payable {
		uint256 updateFee = spaceship.UPDATE_FEE();
		spaceship.updateAltitude{value: updateFee}(u);
	}

	function isSolved() external view returns (bool) {
		return address(spaceship).balance == 0;
	}
}
