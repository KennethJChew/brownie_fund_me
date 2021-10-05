// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

// The error that VScode shows for the 2 chainlink import statements are due to the extensions. We can just ignore them
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

// Accept some kind of payment
contract FundMe {
    using SafeMathChainlink for uint256;
    mapping(address => uint256) public addressToAmountFunded;
    address public owner;
    address[] public funders;
    AggregatorV3Interface public priceFeed;

    // Whatever in constructor is immediately executed when we deploy the contract
    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    // payable keyword indicates that the function can be used to pay with something
    function fund() public payable {
        // convert to gwei equivalent of USD 50
        uint256 minimumUSD = 50 * 10**18;
        // do a check, if condition fails, revert with an error message
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "you need to spend more ETH!"
        );
        // msg.sender and msg.value are keywords in every contract call in every tx.
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        // Assign a tuple to the data returned by latestRoundData

        // (uint80 roundId,
        // int256 answer,
        // uint256 startedAt,
        // uint256 updatedAt,
        // uint80 answeredInRound)
        // =priceFeed.latestRoundData();

        // If we use the code above with the 5 variables in the tuple, the compiler will give a warning regarding unused variable.
        // To get rid of the warning, we make the unused variables in the tuple blanks, and have commas in them instead
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        // typecast the variable answer which is an int256 variable into a uint256 variable to return as the function expects to return a uint256
        return uint256(answer * 10000000000);
    }

    //
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }

    function getEntranceFee() public view returns (uint256) {
        // mimimumUSD
        uint256 mimimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (mimimumUSD * precision) / price;
    } 

    // A modifier is used to change the behavior of a function in a declarative way
    modifier onlyOwner() {
        // We require that the sender is the owner of the contract
        require(msg.sender == owner);
        // the underscore means the rest of the code
        // together, this chunk of code means that we require the msg.sender to be the owner of the contact before running the rest of the code
        _;
    }

    // Runs the modifier onlyOwner before running the code in this function
    function withdraw() public payable onlyOwner {
        // transfer is a function that we can call on any address to send eth from 1 address to another
        // the keyword this refers to the contract that we are currently in
        msg.sender.transfer(address(this).balance);
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }
}
