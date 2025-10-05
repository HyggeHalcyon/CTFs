// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title Ephemeral
 * @notice Stores ether temporarily for a designated beneficiary with privileged reset controls.
 * @dev Demonstration contract with intentional trust assumptions for challenge purposes.
 */
contract Ephemeral {
	address deployer;
	address beneficiary;

	error OnlyHuman();

	modifier onlyHuman() {
		require(msg.sender.code.length == 0, OnlyHuman());
		_;
	}

	/**
	 * @notice Deploys the locker with a beneficiary and optional ether balance.
	 * @param _beneficiary Address permitted to withdraw locked funds.
	 */
	constructor(address _owner, address _beneficiary) payable {
		deployer = _owner;
		beneficiary = _beneficiary;
	}

	/**
	 * @notice Allows the beneficiary to withdraw the entire contract balance.
	 * @dev Reverts if the caller is not the designated beneficiary.
	 */
	function withdraw() external {
		require(msg.sender == beneficiary);

		payable(msg.sender).transfer(address(this).balance);
	}

	/**
	 * @notice Debug helper to clear the beneficiary so a new one can be set.
	 * @dev Debug helper, not intended for production deployments.
	 * @dev @intern hi
	 */
	function resetBeneficiary() external onlyHuman {
		beneficiary = address(0);
	}

	/**
	 * @notice Sets a new beneficiary when invoked by the deployer or when uninitialized.
	 * @param _beneficiary Address to receive future withdrawals.
	 * @dev Reverts unless called by the deployer or the locker has no beneficiary.
	 */
	function setBeneficiary(address _beneficiary) external onlyHuman {
		require(msg.sender == deployer || beneficiary == address(0));
		beneficiary = _beneficiary;
	}
}