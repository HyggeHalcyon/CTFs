// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {IERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {ERC721Holder} from "@openzeppelin/contracts/token/ERC721/utils/ERC721Holder.sol";
import {Ownable, Ownable2Step} from "@openzeppelin/contracts/access/Ownable2Step.sol";
import {Math} from "@openzeppelin/contracts/utils/math/Math.sol";
import {SafeCast} from "@openzeppelin/contracts/utils/math/SafeCast.sol";

contract ChovidLocker is ERC721Holder, Ownable2Step {
    using SafeERC20 for IERC20;
    using SafeCast for uint256;
    using Math for uint256;

    struct Epoch {
        uint48 startAt;
    }

    struct LockInput {
        address recipient;
        uint256 tokenId;
    }

    struct LockInfo {
        address owner;
        uint256 lockedAtEpochIndex;
        address recipient;
    }

    struct RewardState {
        uint208 rewardPerSecond;
        uint48 epochEndAt;
        uint208 rewardPerNFTStored;
        uint48 updatedAt;
    }

    struct Lock {
        uint48 unlockAt;
        uint8 amount;
    }

    struct LockOverview {
        uint48 nextUnlockIndex;
        uint8 lockedAmount;
    }

    IERC721 public nft;
    Epoch[] private epochs;

    mapping(uint256 tokenId => LockInfo info) private locks;

    IERC20[] public rewardTokens;
    mapping(IERC20 => RewardState) private rewardStates;
    mapping(address => LockOverview) private accountLockOverviews;
    mapping(address => Lock[]) private acocuntLocks;
    mapping(address => mapping(IERC20 => uint256)) public rewards;
    mapping(address => mapping(IERC20 => uint256)) public accountRewardPerNFTPaid;

    uint256 public constant EPOCH_DURATION = 44 seconds;
    uint256 public constant LOCK_DURATION_IN_EPOCH = 2;
    uint256 public totalLockedNFT;

    error RenounceInvalid();
    error RewardTokenExists();
    error RewardTokenNotExists();
    error RewardAmountInvalid();
    error Empty();
    error NotOwner();
    error NotUnlockWindow();
    error NoLockers();

    event RewardTokenAdded(IERC20 token);
    event RewardDistributed(IERC20 token, uint256 amount);
    event Locked(address owner, uint256 tokenId);
    event Unlocked(address recipient, uint256 tokenId);

    event DebugCurrentEpochIndex(uint256);

    constructor(address owner_, address nft_) Ownable(owner_) {
        nft = IERC721(nft_);

        uint48 startAt = _getCurrentEpochStart();
        epochs.push(Epoch({startAt: startAt}));
    }

    function renounceOwnership() public virtual override onlyOwner {
        revert RenounceInvalid();
    }

    function getEpoch(uint256 _index) external view returns (Epoch memory) {
        return epochs[_index];
    }

    function _getCurrentEpochStart() internal view returns (uint48) {
        uint256 start = ((block.timestamp / EPOCH_DURATION) * EPOCH_DURATION);
        return start.toUint48();
    }

    function _getNextEpochStart() internal view returns (uint48) {
        return (_getCurrentEpochStart() + EPOCH_DURATION).toUint48();
    }

    function _backfillEpochs() internal {
        uint48 currentEpochStart = _getCurrentEpochStart();
        uint256 epochindex = epochs.length;

        if (epochs[epochindex - 1].startAt < currentEpochStart) {
            while (epochs[epochs.length - 1].startAt != currentEpochStart) {
                uint48 nextStartAt = (epochs[epochs.length - 1].startAt + EPOCH_DURATION).toUint48();
                epochs.push(Epoch({startAt: nextStartAt}));
            }
        }
    }

    function getRewardTokenCount() external view returns (uint256 count_) {
        count_ = rewardTokens.length;
    }

    function getRewardState(IERC20 token_) external view returns (RewardState memory data_) {
        data_ = rewardStates[token_];
    }

    function addRewardToken(IERC20 _token) external onlyOwner {
        if (rewardStates[_token].updatedAt > 0) revert RewardTokenExists();

        rewardTokens.push(_token);
        rewardStates[_token].updatedAt = block.timestamp.toUint48();
        rewardStates[_token].epochEndAt = block.timestamp.toUint48();

        emit RewardTokenAdded(_token);
    }

    function _rewardPerNFT(IERC20 _token) internal view returns (uint256) {
        RewardState memory rewardState = rewardStates[_token];
        uint256 prevRewardPerNFT = uint256(rewardState.rewardPerNFTStored);
        uint256 epochEndAt = Math.min(uint256(rewardState.epochEndAt), block.timestamp);
        uint256 timeDelta = epochEndAt - uint256(rewardState.updatedAt);
        uint256 rewardPerNFT = (timeDelta * rewardState.rewardPerSecond) / totalLockedNFT;
        return prevRewardPerNFT + rewardPerNFT;
    }

    function _updateRewardStates() internal {
        for (uint256 i = 0; i < rewardTokens.length; i++) {
            IERC20 token = rewardTokens[i];
            rewardStates[token].rewardPerNFTStored = _rewardPerNFT(token).toUint208();
            rewardStates[token].updatedAt = Math.min(rewardStates[token].epochEndAt, block.timestamp).toUint48();
        }
    }

    function distribute(IERC20 _token, uint256 _amount) external onlyOwner {
        if (rewardStates[_token].updatedAt == 0) revert RewardTokenNotExists();
        if (_amount == 0) revert RewardAmountInvalid();
        if (totalLockedNFT == 0) revert NoLockers();

        _updateRewardStates();

        RewardState storage rewardState = rewardStates[_token];
        if (block.timestamp >= rewardState.epochEndAt) {
            rewardState.rewardPerSecond = (_amount / EPOCH_DURATION).toUint208();
        } else {
            uint256 remaining = rewardState.epochEndAt - block.timestamp;
            uint256 leftover = remaining * rewardState.rewardPerSecond;
            rewardState.rewardPerSecond = ((_amount + leftover) / EPOCH_DURATION).toUint208();
        }

        rewardState.updatedAt = block.timestamp.toUint48();
        rewardState.epochEndAt = (block.timestamp + EPOCH_DURATION).toUint48();

        _token.safeTransferFrom(msg.sender, address(this), _amount);
        emit RewardDistributed(_token, _amount);
    }

    function _earned(address _account, IERC20 _token, uint256 _lockedAmount) internal view returns (uint256) {
        uint256 rewardPerNFTDiff = _rewardPerNFT(_token) - accountRewardPerNFTPaid[_account][_token];
        return (_lockedAmount * rewardPerNFTDiff) + rewards[_account][_token];
    }

    function _updateAccountReward(address _account) internal {
        LockOverview memory overview = accountLockOverviews[_account];
        for (uint256 i = 0; i < rewardTokens.length; i++) {
            IERC20 token = rewardTokens[i];
            RewardState memory rewardState = rewardStates[token];
            rewards[_account][token] = _earned(_account, token, overview.lockedAmount);
            accountRewardPerNFTPaid[_account][token] = rewardState.rewardPerNFTStored;
        }
    }

    function _lock(LockInput memory _input, address _owner, uint256 _currentEpochIndex) internal {
        nft.safeTransferFrom(_owner, address(this), _input.tokenId);

        locks[_input.tokenId] =
            LockInfo({owner: _owner, recipient: _input.recipient, lockedAtEpochIndex: _currentEpochIndex});

        totalLockedNFT += 1;

        emit Locked(_owner, _input.tokenId);
    }

    function lock(LockInput[] calldata _inputs) external {
        uint256 inputCount = _inputs.length;
        if (inputCount == 0) revert Empty();

        _backfillEpochs();
        uint256 currentEpochIndex = epochs.length - 1;
        emit DebugCurrentEpochIndex(currentEpochIndex);

        for (uint8 i = 0; i < inputCount; ++i) {
            _lock(_inputs[i], msg.sender, currentEpochIndex);
        }
    }

    function _unlock(address _owner, uint256 _tokenId, uint256 _currentEpochIndex) internal {
        LockInfo memory lockInfo = locks[_tokenId];

        uint256 lockedDurationInEpoch = _currentEpochIndex - lockInfo.lockedAtEpochIndex;
        emit DebugCurrentEpochIndex(_currentEpochIndex);
        emit DebugLockedEpochIndex(lockedDurationInEpoch);
        emit DebugLockedAtEpochIndex(lockInfo.lockedAtEpochIndex);
        if (lockedDurationInEpoch == 0) revert NotUnlockWindow();

        uint256 modulo = lockedDurationInEpoch % (LOCK_DURATION_IN_EPOCH + 1);
        if (modulo != 0) revert NotUnlockWindow();

        emit CallerOwner(_owner, lockInfo.owner);
        if (lockInfo.owner != _owner) revert NotOwner();

        nft.safeTransferFrom(address(this), _owner, _tokenId);

        emit Unlocked(_owner, _tokenId);
    }

    function unlock(uint256[] calldata _tokenIds) external {
        uint256 tokenCount = _tokenIds.length;
        if (tokenCount == 0) revert Empty();

        _backfillEpochs();
        uint256 currentEpochIndex = epochs.length - 1;
        emit DebugCurrentEpochIndex(currentEpochIndex);

        totalLockedNFT -= tokenCount;

        for (uint256 i = 0; i < tokenCount; ++i) {
            _unlock(msg.sender, _tokenIds[i], currentEpochIndex);
        }
    }

    event CallerOwner(address caller, address owner);
    event DebugLockedEpochIndex(uint256);
    event DebugLockedAtEpochIndex(uint256);
}