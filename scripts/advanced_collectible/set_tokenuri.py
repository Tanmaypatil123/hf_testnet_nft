#!/usr/bin/python3
from brownie import SimpleCollectible , AdvancedCollectible , accounts,network,config
from metadata import sample_metadata
from scripts.helpful_scripts import get_hf,OPENSEA_FORMAT

hf_metadata_dic = {
    "AKKI": "https://ipfs.io/ipfs/QmVpBH7iJYKxZzqJ6uYZsuBxHggtjFGxt4VLhquFUKWgfL?filename=0-AKKI.json",
    "BABU": "https://ipfs.io/ipfs/QmPGhMsrnpLyCSdJKwLPS5pRHtHHHsK3Ne2Y9ScAT1o76k?filename=1-BABU.json"
}

def main():
    print("Working on" + network.show_active())
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(number_of_advanced_collectibles)
    )
    for token_id in range(number_of_advanced_collectibles):
        hf = get_hf(advanced_collectible.tokenIdToHF(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print("Setting tokenURI of {}".format(token_id))
            set_tokenURI(token_id,advanced_collectible,hf_metadata_dic[hf])
        else:
            print("Skipping {}. we already set that tokenURI!".format(token_id))

def set_tokenURI(token_id,nft_contract,tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])
    nft_contract.setTokenURI(token_id,tokenURI,{"from":dev})
    print(
        "Awsome! You can view your NFT at {}".format(
            OPENSEA_FORMAT.format(nft_contract.address,token_id)
        )
    )
    print('Please give up to 20 minutes, and hit the "refresh metadata" button')