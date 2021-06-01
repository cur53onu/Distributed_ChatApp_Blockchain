const HDWalletProvider = require('truffle-hdwallet-provider');
const Web3  = require('web3');
const compiledChatRoom = require('./build/ChatRoom.json');
const compiledProfile = require('./build/Profile.json');
const compiledDeployedChatRooms = require('./build/DeployContracts.json');
const compiledMessages = require('./build/Message.json');
const provider = new HDWalletProvider(
  'gate enact liberty crater piano cost title bunker cash visit iron critic',
  'https://rinkeby.infura.io/v3/0a5866cdc4fb48d8808e336cd05a68ff'
);
const web3 = new Web3(provider);
const deploy = async ()=>{
  const accounts = await web3.eth.getAccounts();

  console.log('Attempting to deploy ChatRoom from ',accounts[0]);
  var result = await new web3.eth.Contract(
  JSON.parse(compiledChatRoom.interface))
  .deploy({data : compiledChatRoom.bytecode})
  .send({gas: '6000000',from : accounts[0]});
  console.log('contract deployed to ',result.options.address);

  console.log('Attempting to deploy Profile from ',accounts[0]);
  var result = await new web3.eth.Contract(
  JSON.parse(compiledProfile.interface))
  .deploy({data : compiledProfile.bytecode})
  .send({gas: '6000000',from : accounts[0]});
  console.log('contract deployed to ',result.options.address);

  console.log('Attempting to deploy DeployChatRoom from ',accounts[0]);
  var result = await new web3.eth.Contract(
  JSON.parse(compiledDeployedChatRooms.interface))
  .deploy({data : compiledDeployedChatRooms.bytecode})
  .send({gas: '6000000',from : accounts[0]});
  console.log('contract deployed to ',result.options.address);

  console.log('Attempting to deploy Messages from ',accounts[0]);
  var result = await new web3.eth.Contract(
  JSON.parse(compiledMessages.interface))
  .deploy({data : compiledMessages.bytecode})
  .send({gas: '6000000',from : accounts[0]});
  console.log('contract deployed to ',result.options.address);


  // var result2 ;
  // Promise.all(
  // console.log('Attempting to deploy MyProfile from ',accounts[0]),
  // result2 = await new web3.eth.Contract(
  // JSON.parse(compiledMyProfile.interface))
  // .deploy({data : compiledMyProfile.bytecode})
  // .send({gas: '6000000',from : accounts[0]}),
  
  // console.log('contract deployed to ',result2.options.address)
  // ).catch(err=>{conole.log(err)});
  // };
};
deploy();
