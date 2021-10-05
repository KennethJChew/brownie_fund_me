from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200000000000
FORKED_LOCAL_ENVIRONMENTS =["mainnet-fork","mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    # check to see if MockV3Aggregator has been deployed, and only deploy it if it hasn't been deployed before
    # We check the length because the addresses of all deployed contracts will be stored in an array
    if len(MockV3Aggregator) <= 0:
        mock_aggregator = MockV3Aggregator.deploy(
            DECIMALS, STARTING_PRICE, {"from": get_account()}
        )
    # Use address of the most recently deployed MockV3Aggregator
    price_feed_address = MockV3Aggregator[-1].address
    print("Mocks deployed!")
