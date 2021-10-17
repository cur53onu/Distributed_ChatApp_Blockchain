const HDWalletProvider = require('@truffle/hdwallet-provider');
const Web3  = require('web3');
const compiledDeployedChatRooms = require('./build/DeployContracts.json');
const prompt = require('prompt-sync')();
const mnemonic = prompt('Enter your metamask mnemonic?: ');
if(mnemonic == null || mnemonic.split(' ').length != 12){
    console.log('quitting!!!');
    process.exit(1);
}
const rinkby_url = prompt('Enter your rinkeby url?: ');
const provider = new HDWalletProvider(
  mnemonic,
  rinkby_url
);
const fs = require('fs')
const path = require("path");
const filePathNormal = 'JSON_Files/data.json'
function jsonReader(filePath, cb) {
    fs.readFile(filePath, (err, fileData) => {
        if (err) {
            return cb && cb(err)
        }
        try {
            const object = JSON.parse(fileData)
            return cb && cb(null, object)
        } catch(err) {
            return cb && cb(err)
        }
    })
}

const web3 = new Web3(provider);
const deploy = async()=>{
    try{
        const accounts = await web3.eth.getAccounts();
        console.log('Attempting to deploy DeployContracts from ',accounts[0]);
        done=false
        var promise = new Promise(
            resolve => {
                setTimeout(resolve, 50000);
                var result =new web3.eth.Contract(
                    JSON.parse(compiledDeployedChatRooms.interface))
                    .deploy({data : compiledDeployedChatRooms.bytecode})
                    .send({gas: '6000000',from : accounts[0]}).
                    then(function(result){
                        console.log('Contract deployed to ', result.options.address)
                        jsonReader(filePathNormal, (err, data) => {
                      if (err) {
                          console.log('Error reading file:',err)
                          return
                      }
                      data.contract_deploycontracts_address = result.options.address
                      fs.writeFile(filePathNormal, JSON.stringify(data), (err) => {
                            if (err) console.log('Error writing file:', err)
                            })    
                        })
                    });
                });
                promise.then(function(val){
                    process.exit(0);
                  });
                // promise.then(done=true)
        // while(true){
            // console.log(promise.pending);
        // }
    }catch(err){
        console.log(err);
    }
}
deploy();