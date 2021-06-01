pragma solidity ^0.4.17;
pragma experimental ABIEncoderV2;
contract DeployContracts{
    address[] public deployedChatRooms;
    address[] public deployedUsers;
    function Deploychatrooms(string chat_room_name,address owner){
        address ContractAddress=new ChatRoom();
        ChatRoom newContract=ChatRoom(ContractAddress);
        newContract.setName(chat_room_name);
        newContract.setOwner(owner);
        deployedChatRooms.push(ContractAddress);
    }
    function DeployProfiles(string username,string data){
        address profile=new Profile();
        Profile prof=Profile(profile);
        prof.addUser(username,data);
        deployedUsers.push(profile);
    }
    function getDeployedProfileByName(string name)view returns (address){
         for(uint i=0;i<deployedUsers.length;i++)
        {
            Profile prof=Profile(deployedUsers[i]);
            if(keccak256(abi.encodePacked(name)) == keccak256(abi.encodePacked(prof.getUserName()))){
                return deployedUsers[i];
            }
        }

    }


}

contract ChatRoom{
    string public chat_room_name;
    address[] public users;
    address public owner;
    address[] public messages;
    string[] userNames;
    function getName()public view returns(string){
        return chat_room_name;
    }
    function setName(string Name) public{
        chat_room_name=Name;
    }
    function setOwner(address add) public{
        owner=add;
    }
    function addUser(string user_name_received,string data_received) public{
        address profileContract=new Profile();
        Profile profile=Profile(profileContract);
        profile.addUser(user_name_received,data_received);
        users.push(profileContract);
        userNames.push(user_name_received);
    }
    function sendMessage(string User_Name,string Message_Received){
        for(uint i=0;i<userNames.length;i++){
            if(keccak256(abi.encodePacked(User_Name)) == keccak256(abi.encodePacked(userNames[i]))){
                address messages_contract=new Message();
                Message newContract=Message(messages_contract);
                newContract.addMessage(User_Name,Message_Received);
                messages.push(messages_contract);
            }
        }

    }
    function getMessages(address User)public view returns(address[]){
        return messages;
    }
    function delUser(address User)public view returns(address[]){
        for(uint i=0;i<users.length;i++){
            if(users[i]==User){
                delete users[i];
            }
        }
        return users;

    }
    function getUsers()public view returns(address[]){
        return users;
    }


}

contract Message{
    string user;
    string message;

    function getUser()public view returns(string){
        return user;
    }
    function getMessage()public view returns(string){
        return message;
    }
    function addMessage(string user_received,string message_received){
        user=user_received;
        message=message_received;
    }
}
contract Profile{
    string name;
    string data;
    function getUserName()public view returns(string){
        return name;
    }
    function getData()public view returns(string){
        return data;
    }

    function addUser(string user_name_received,string data_received) public {
        name=user_name_received;
        data=data_received;
    }

    function getUserByName(string user_name_received)public view returns(string,string){
        if(keccak256(abi.encodePacked(name)) == keccak256(abi.encodePacked(user_name_received))){
        return(name,data);
        }
        return("NO USER","NO DATA");
    }

}