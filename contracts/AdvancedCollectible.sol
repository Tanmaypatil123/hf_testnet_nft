pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721,VRFConsumerBase {
    uint256 public tokenCounter;
    enum HF{AKKI,BABU}

    mapping(bytes32 => address) public requestIdToSender;
    mapping(bytes32 => string) public requestIDToTokenURI;
    mapping(uint256 => HF) public tokenIdToHF;
    mapping(bytes32 => uint256) public requestIdToTokenId;
    event requestedCollectible(bytes32 indexed requestId);
    bytes32 internal keyHash;
    uint256 internal fee;
    constructor(address _VRFCoordinator,address _LinkToken,bytes32 _keyhash) public VRFConsumerBase(_VRFCoordinator,_LinkToken) ERC721("Raju","AKKI"){
        tokenCounter = 0;
        keyHash = _keyhash;
        fee = 0.1 * 10 ** 18;
    } 
    function createCollectible(string memory tokenURI) 
        public returns (bytes32){
            bytes32 requestId = requestRandomness(keyHash, fee);
            requestIdToSender[requestId] = msg.sender;
            requestIDToTokenURI[requestId] = tokenURI;
            emit requestedCollectible(requestId);
    }
    function fulfillRandomness(bytes32 requestId,uint256 randomNumber) internal override{
        address HFOwner = requestIdToSender[requestId];
        string memory tokenURI = requestIDToTokenURI[requestId];
        uint256 newItemId = tokenCounter;
        _safeMint(HFOwner,newItemId);
        _setTokenURI(newItemId,tokenURI);
        HF hf = HF(randomNumber % 2);
        tokenIdToHF[newItemId] = hf;
        requestIdToTokenId[requestId] = newItemId;
        tokenCounter = tokenCounter + 1;
    }
    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: transfer caller is not owner nor approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}