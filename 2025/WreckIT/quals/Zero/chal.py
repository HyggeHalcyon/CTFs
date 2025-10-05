import json
import subprocess
from pathlib import Path
from typing import Optional

import sandbox
from web3 import HTTPProvider, Web3
from eth_account import Account as EthAccount

def set_balance(web3: Web3, account_address: str, amount: int):
    res = web3.provider.make_request(
        "anvil_setBalance",
        [account_address, amount]
    )


def cast_call(rpc_url: str, from_addr: str, to_addr: str, call_data: str) -> Optional[str]:
    if not to_addr or not from_addr or not call_data:
        return None

    try:
        result = subprocess.run(
            [
                "cast",
                "call", to_addr,
                "--rpc-url", rpc_url,
                "--from", from_addr,
                "--data", call_data,
                "--trace", "-vvvv"
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        if stderr:
            print(f"cast call failed: {stderr}")
    return None


def deploy(web3: Web3, deployer_address: str, deployer_privateKey: str, player_address: str) -> str:
    uri = web3.provider.endpoint_uri
    contract_info = json.loads(Path("compiled/Setup.sol/Setup.json").read_text())
    abi = contract_info["abi"]
    bytecode = contract_info["bytecode"]["object"]


    contract = web3.eth.contract(abi=abi, bytecode=bytecode)

    construct_txn = contract.constructor(player_address).build_transaction(
        {
            "from": deployer_address,
            "nonce": web3.eth.get_transaction_count(deployer_address),
            "value": Web3.to_wei(100, 'ether'),
            "gasPrice": Web3.to_wei(100, 'gwei')
        }
    )

    tx_create = web3.eth.account.sign_transaction(construct_txn, deployer_privateKey)
    tx_hash = web3.eth.send_raw_transaction(tx_create.raw_transaction)

    rcpt = web3.eth.wait_for_transaction_receipt(tx_hash)

    set_balance(web3, player_address, Web3.to_wei(10, 'ether'))

    return rcpt.contractAddress

def pre_tx_hook(data, node_info):
    """
    Executed before a transaction is processed.
    Returns:
        - status: HTTP status code (e.g., 200 for success, 400 for error)
        - msg: Message to be returned in the response in case of non 2xx status
    """

    rpc_url = f"http://127.0.0.1:{node_info.port}"
    web3 = Web3(HTTPProvider(rpc_url))

    return 200, ""

def post_tx_hook(data, response, node_info):
    """
    Executed after a transaction is processed.
    Returns:
        - status: HTTP status code (e.g., 200 for success, 400 for error)
        - msg: Message to be returned in the response in case of non 2xx status
    """
    return 200, ""

def begin_block_hook(node_info, block):
    """
    Executed after a block is mined
    """

    mnemonic = node_info.seed
    deployer_account = EthAccount.from_mnemonic(mnemonic, account_path="m/44'/60'/0'/0/0")

    deployer_address = deployer_account.address

    rpc_url = f"http://127.0.0.1:{node_info.port}"
    setup_addr = node_info.contract_addr
    web3 = Web3(HTTPProvider(rpc_url))
    
    setup_contract_info = json.loads(Path("compiled/Setup.sol/Setup.json").read_text())
    setup_contract = web3.eth.contract(address=setup_addr, abi=setup_contract_info["abi"])
    
    ethking_addr = setup_contract.functions.ethking().call()
    
    ethking_contract_info = json.loads(Path("compiled/EthKing.sol/EthKing.json").read_text())
    ethking_contract = web3.eth.contract(address=ethking_addr, abi=ethking_contract_info["abi"])

    try:
        construct_txn = ethking_contract.functions.win().build_transaction(
            {
                "from": deployer_address,
                "nonce": web3.eth.get_transaction_count(deployer_address),
                "value": Web3.to_wei("0.001", 'ether'),
                "gasPrice": Web3.to_wei(100, 'gwei'),
            }
        )

        tx_create = web3.eth.account.sign_transaction(construct_txn, deployer_account.key)
        tx_hash = web3.eth.send_raw_transaction(tx_create.raw_transaction)

        # rcpt = web3.eth.wait_for_transaction_receipt(tx_hash)
    except Exception:
        pass
    
    return 200, ""

app = sandbox.run_launcher(
    deploy,
    pre_tx_hook=pre_tx_hook,
    post_tx_hook=post_tx_hook,
    begin_block_hook=begin_block_hook
)
