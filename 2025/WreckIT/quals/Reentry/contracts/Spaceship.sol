// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {Multicallable} from "./Multicallable.sol";

/**
 * @title Spaceship
 * @author HanzCEO (https://x.com/hanzceo)
 * @notice Permissionless and transparent data availability platform for Spaceship variable reading
 */
contract Spaceship is Multicallable {
	uint256 public constant CREATION_FEE = 0.5 ether;
	uint256 public constant UPDATE_FEE = 0.000005 ether;

	/**
	 * @notice Maps the altitude of the spaceship from different array of GPS gadgets `address`
	 */
	mapping(address => uint256) private altitude; // @audit-msg [H-01] Accessible premium data via storage slot reading
	/**
	 * @notice Maps the fee users need to pay when reading from a certain gadget `address`
	 */
	mapping(address => uint56) public readingFee;

	error GadgetExists();
	error GadgetError();
	error GadgetNonExistent();
	error FeeUnderpaid();
	error RefundError();

	event GadgetAdded(address indexed gadget, address indexed operator);
	event GadgetRemoved(address indexed gadget, address indexed operator);
	event AltitudeUpdated(address indexed gadget, address indexed operator, uint256 old, uint256 _new);

	constructor() {}

	/**
	 * @notice 
	 * @param gadget The GPS gadget to add
	 * @param initialAltitude The initial spaceship altitude reading from the GPS
	 */
	function addGpsGadget(address gadget, uint256 _readingFee, uint256 initialAltitude) external payable {
		require(msg.value >= CREATION_FEE, FeeUnderpaid());
		require(altitude[gadget] == 0, GadgetExists());
		altitude[gadget] = initialAltitude;
		readingFee[gadget] = uint56(_readingFee);

		emit GadgetAdded(gadget, msg.sender);
	}


	/** @notice Removes the GPS gadget for the caller, resetting altitude and reading fee, and refunds the update fee
	 *  @dev Requires the caller to have an existing gadget (altitude > 0). Refunds UPDATE_FEE to the caller.
	 */
	function removeGpsGadget() external {
		require(altitude[msg.sender] >= 0, GadgetNonExistent());
		altitude[msg.sender] = 0;
		readingFee[msg.sender] = 0;
		
		(bool success,) = msg.sender.call{value: CREATION_FEE}("");
		require(success, RefundError());

		// wake-disable-next-line
		emit GadgetRemoved(msg.sender, tx.origin);
	}

	/**
	 * @notice Read altitude from an array of gadgets and pay reading fee
	 * @param gadgets Array of gadgets to read altitude from
	 * @return meanAlt The average of all GPS reading from gadgets
	 */
	function getAltitudeReading(address[] memory gadgets) external payable returns (uint256 meanAlt) {
		for (uint i; i < gadgets.length; i++) {
			address gadget = gadgets[i];
			uint256 alt = altitude[gadget];
			require(alt > 0, GadgetNonExistent());
			(bool success,) = gadget.call{value: readingFee[gadget]}("");
			require(success, GadgetError());

			meanAlt += (alt - meanAlt) / (i + 1);
		}
	}

	function updateAltitude(uint256 alt) external payable {
		require(msg.value >= UPDATE_FEE, FeeUnderpaid());
		require(altitude[msg.sender] > 0, GadgetNonExistent());

		uint256 oldAlt = altitude[msg.sender];
		altitude[msg.sender] = alt;
		// wake-disable-next-line
		emit AltitudeUpdated(msg.sender, tx.origin, oldAlt, alt);
	}
}