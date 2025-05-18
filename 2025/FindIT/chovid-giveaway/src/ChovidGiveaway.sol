// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

contract ChovidGiveaway {
    error InvalidPasswordLength();
    error InvalidGiveawayLength();
    error InvalidGiveawayValue();
    error AlreadyRedeemed();
    error InvalidProof();
    error InvalidValue();
    error InvalidRoot();
    error MerkleProofInvalidMultiproof();

    mapping(bytes32 => bool) public redeemedPasswords;
    mapping(bytes32 => bool) public registeredRoot;
    address owner;

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function registerGiveaway(bytes32 root) public payable onlyOwner {
        registeredRoot[root] = true;
    }

    function commutativeKeccak256(bytes32 a, bytes32 b) internal pure returns (bytes32) {
        return a < b ? efficientKeccak256(a, b) : efficientKeccak256(b, a);
    }

    function efficientKeccak256(bytes32 a, bytes32 b) internal pure returns (bytes32 value) {
        assembly ("memory-safe") {
            mstore(0x00, a)
            mstore(0x20, b)
            value := keccak256(0x00, 0x40)
        }
    }

    function buildTree(bytes32[] memory _leaves) internal pure returns (bytes32) {
        bytes32[] memory leaves = _leaves;
        if (leaves.length == 0) return bytes32(0);
        if (leaves.length == 1) return leaves[0];

        uint256 n = leaves.length;
        
        while (n > 1) {
            if (n % 2 == 1) revert InvalidGiveawayLength();
            
            for (uint256 i = 0; i < n/2; i++) {
                bytes32 left = leaves[2*i];
                bytes32 right = leaves[2*i + 1];
                bytes32 parent = commutativeKeccak256(left, right);
                
                leaves[i] = parent;  // Write back to the same array
            }
            
            if (n % 2 == 1) {
                leaves[n/2] = leaves[n - 1];
            }
            
            n = (n + 1) / 2;
        }

        return leaves[0];
    }

    function verify(bytes32[] memory proof, bytes32 root, bytes32 leaf) internal pure returns (bool) {
        return processProof(proof, leaf) == root;
    }

    function processProof(bytes32[] memory proof, bytes32 leaf) internal pure returns (bytes32) {
        require(proof.length == 2);
        bytes32 computedHash = leaf;
        for (uint256 i = 0; i < proof.length; i++) {
            computedHash = commutativeKeccak256(computedHash, proof[i]);
        }
        return computedHash;
    }

    function createGiveaway(
        bytes[] memory passwords,
        uint16[] memory amounts
    ) external payable returns (bytes32 root) {
        uint256 numGiveaways = passwords.length;
        if (numGiveaways != amounts.length) revert InvalidGiveawayLength();

        if (numGiveaways != 4) revert InvalidGiveawayLength();

        uint256 totalValue;
        bytes32[] memory leaves = new bytes32[](numGiveaways);

        for(uint256 i = 0; i < numGiveaways; i++) {
            if (passwords[i].length > type(uint24).max) revert InvalidPasswordLength();
            
            uint256 maxPerGiveaway = 0x10000;
            if (amounts[i] >= maxPerGiveaway) revert InvalidGiveawayValue();

            totalValue += amounts[i];

            bytes memory encoded = abi.encodePacked(
                uint24(passwords[i].length),
                passwords[i],
                amounts[i]
            );
            leaves[i] = keccak256(encoded);
        }

        if (msg.value != totalValue) revert InvalidValue();

        root = buildTree(leaves);
        registeredRoot[root] = true;
    }

    function redeem(
        bytes32[] memory proof,
        bytes32 root,
        bytes memory password,
        uint16 amount
    ) external {
        if (!registeredRoot[root]) revert InvalidRoot();
        if (password.length > type(uint24).max) revert InvalidPasswordLength();

        bytes memory encoded = abi.encodePacked(
            uint24(password.length),
            password,
            amount
        );
        bytes32 leaf = keccak256(encoded);

        if (redeemedPasswords[leaf]) revert AlreadyRedeemed();

        if (!verify(proof, root, leaf)) revert InvalidProof();

        redeemedPasswords[leaf] = true;

        uint256 gift = uint256(amount);
        payable(msg.sender).transfer(gift);
    }
}
