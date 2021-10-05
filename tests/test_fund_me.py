from brownie import network,accounts, exceptions
from scripts.fund_and_withdraw import fund
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy import deploy_fund_me
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee()+100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    # Check that the amount that has been funded is the same as the entrance fee(amt that was sent to fund the account)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    assert fund_me.addressToAmountFunded(account.address) == 0
    tx2.wait(1)


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    account=get_account()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    # Tell brownie that we expect an exception to be raised
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from":bad_actor})
