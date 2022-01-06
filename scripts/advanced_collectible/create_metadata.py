#!/usr/bin/python3

import os
import requests
import json
from brownie import AdvancedCollectible,network
from metadata import sample_metadata
from scripts.helpful_scripts import get_hf
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

hf_to_image_uri = {
    "AKKI": "https://ipfs.io/ipfs/QmcRiimXMm8F2vQuH2Ebr9eSdZVWjxxjiPgYn2FfvXxp2x?filename=akshay.jpg",
    "BABU": "https://ipfs.io/ipfs/Qmc7wrbePYo9BNSrZFpfeQpi1SvQ4Wc1mHPJ7AQBVyGNKD?filename=baburao.jpg"
}

def main():
    print("Working on " + network.show_active())
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(
        "The number of tokens you've deployed is:"
        +str(number_of_advanced_collectibles)
    )
    write_metadata(number_of_advanced_collectibles,advanced_collectible)

def write_metadata(token_ids,nft_contract):
    for token_id in range(token_ids):
        collectible_metadata = sample_metadata.metadata_template
        hf = get_hf(nft_contract.tokenIdToHF(token_id))
        metadata_file_name = (
            "./metadata/{}/".format(network.show_active())
            + str(token_id)
            +"-"
            + hf
            +".json"
        )
        if Path(metadata_file_name).exists():
            print(
                "{} already found,delete it to overwrite!".format(
                    metadata_file_name
                )
            )
        else:
            print("Creating Metadata file: " + metadata_file_name)
            collectible_metadata["name"] = get_hf(
                nft_contract.tokenIdToHF(token_id)
            )
            collectible_metadata["decription"] = "motivation of indian memers"
            image_to_upload = None
            if os.getenv("UPLOAD_IPFS")  == "true":
                image_path = "./img/{}.png".format(
                    hf.lower().replace('_','-')
                )
                image_to_upload = upload_to_ipfs(image_path)
            image_to_upload = (
                hf_to_image_uri[hf] if not image_to_upload else image_to_upload
            )    
            collectible_metadata["image"] = image_to_upload
            with open(metadata_file_name,'w') as file:
                json.dump(collectible_metadata,file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)

def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = (
            os.getenv("IPFS_URL")
            if os.getenv("IPFS_URL")
            else "http://localhost:5001"
        )
        response = requests.post(ipfs_url + "/api/v0/add",
                                 files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = "https://ipfs.io/ipfs/{}?filename={}".format(
            ipfs_hash, filename)
        print(image_uri)
    return image_uri                