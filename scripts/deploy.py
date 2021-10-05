from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    deploy_mocks,
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3


def deploy_fund_me():
    account = get_account()
    print(account)
    # publish source code and verify contract.
    # We need to create API key in etherscan and add the key in env file.
    # If we are on a persistent network like rinkeby, use the associated address.
    # Otherwise, deploy mocks
    # Pass the pricefeed contract address to the constructor
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
