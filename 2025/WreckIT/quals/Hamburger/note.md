forge create ./contracts/Setup.sol:Setup --rpc-url local --account local --value 10000000000000000000 --broadcast --constructor-args 0x70997970C51812dc3A010C7d01b50e0d17dc79C8

forge script .\contracts\Exploit.sol:Exploit --rpc-url local