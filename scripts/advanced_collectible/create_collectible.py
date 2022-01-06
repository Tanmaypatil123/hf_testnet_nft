#!/usr/bin/python3
from brownie import AdvancedCollectible, accounts, config
from scripts.helpful_scripts import get_hf, fund_with_link
import time


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    fund_with_link(advanced_collectible.address)
    transaction = advanced_collectible.createCollectible("None", {"from": dev})
    print("Waiting on second transaction...")
    # wait for the 2nd transaction
    transaction.wait(1)
    time.sleep(35)
    requestId = transaction.events["requestedCollectible"]["requestId"]
    token_id = advanced_collectible.requestIdToTokenId(requestId)
    hf = get_hf(advanced_collectible.tokenIdToHF(token_id))
    print("meme breed of tokenId {} is {}".format(token_id, hf))