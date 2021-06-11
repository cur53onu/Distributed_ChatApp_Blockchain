pragma solidity ^0.4.17;
pragma experimental ABIEncoderV2;

contract DeployContracts{
    address[] private deployedUsers;
    address[] private deployedChatRooms;
    function deployChatRoom(string chat_room_name){
        address ContractAddress=new ChatRoom();
        ChatRoom newContract=ChatRoom(ContractAddress);
        newContract.setName(chat_room_name);
        newContract.setOwner(msg.sender);
        deployedChatRooms.push(ContractAddress);
    }


    function deployProfiles(string username,string data){
        address profile=new Profile();
        Profile prof=Profile(profile);
        prof.addUser(username,data,msg.sender);
        deployedUsers.push(profile);
    }

    function addUserToChatRoomByUserName(string chat_room_name_received,string user_name_received){
        require(msg.sender==getChatRoomOwner(chat_room_name_received));
        address chat_room_address=getDeployedChatRoomAddressByName(chat_room_name_received);
        ChatRoom chat_room=ChatRoom(chat_room_address);
        address profile_address=getDeployedProfileAddressByName(user_name_received);
        Profile user_profile=Profile(profile_address);
        chat_room.addUser(user_profile.getUserAddress(),user_name_received);
    }

    function addMessage(string chat_room_name_received,string user_name_received,string message_received,string timestamp_received){
        address chat_room_address=getDeployedChatRoomAddressByName(chat_room_name_received);
        ChatRoom chat_room=ChatRoom(chat_room_address);
        chat_room.addMessage(msg.sender,user_name_received,message_received,timestamp_received);
    }

    function getMessagesFromChatRoomByName(string chat_room_name_received)public view returns(ChatRoom.Message[]){
        address chat_room_address=getDeployedChatRoomAddressByName(chat_room_name_received);
        ChatRoom chat_room=ChatRoom(chat_room_address);
        return chat_room.getAllMessages();
    }

    function getDeployedProfileData(string user_name_received)view returns (string){
        address profile_address=getDeployedProfileAddressByName(user_name_received);
        if(0x0000000000000000000000000000000000000000==profile_address)
        return "NO_DATA";
        Profile user_profile=Profile(profile_address);
        return user_profile.getUserData();
    }

    function getDeployedProfileAddressByName(string username)view returns (address){
         for(uint i=0;i<deployedUsers.length;i++)
        {
            Profile prof=Profile(deployedUsers[i]);
            if(keccak256(abi.encodePacked(username)) == keccak256(abi.encodePacked(prof.getUserName()))){
                return deployedUsers[i];
            }
        }

    }

    function getChatRoomOwner(string chat_room_name_received) view returns(address){
        address chat_room_address=getDeployedChatRoomAddressByName(chat_room_name_received);
        ChatRoom room=ChatRoom(chat_room_address);
        return room.getOwner();
    }

    function getDeployedChatRoomAddressByName(string chat_room_name_received) public view returns(address){
        for(uint i=0;i<deployedChatRooms.length;i++)
        {
            ChatRoom room=ChatRoom(deployedChatRooms[i]);
            if(keccak256(abi.encodePacked(chat_room_name_received)) == keccak256(abi.encodePacked(room.getName()))){
                return deployedChatRooms[i];
            }
        }
    }

    function getInfo() public view returns(uint,uint){
        return (deployedChatRooms.length,deployedUsers.length);
    }


}

contract ChatRoom{
    string chat_room_name;
    address owner_address;
    mapping(address=>string) users_to_address;
    struct Message {
        string username;
        string message;
        string timestamp;
        address user_public_address;
    }
    mapping (address => Message) messages;
    Message[] public message_array;
    mapping(address=>Message[]) user_to_message;
    function setName(string chat_room_name_received) public{
        chat_room_name=chat_room_name_received;
    }
    function setOwner(address owner_address_received) public{
        owner_address=owner_address_received;
    }

    function addUser(address user_public_address_received,string username) public{
        users_to_address[user_public_address_received]=username;
    }
    function addMessage(address user_public_address_received,string user_name_received,string message_received,string timestamp_received)public {
        require(checkUserPresent(user_public_address_received));
        Message build_message=messages[user_public_address_received];
        build_message.username=user_name_received;
        build_message.message=message_received;
        build_message.user_public_address=user_public_address_received;
        build_message.timestamp=timestamp_received;
        message_array.push(build_message);
        user_to_message[user_public_address_received].push(build_message);
    }
    function getName()public view returns(string){
        return chat_room_name;
    }
    function getOwner() public view returns(address){
        return owner_address;
    }

    function checkUserPresent(address user_public_address_received)public view returns(bool){
        if(keccak256(abi.encodePacked(users_to_address[user_public_address_received])) == keccak256(abi.encodePacked(""))){
            return false;
        }
        return true;
    }

    function getAllMessages()public view returns(Message[]){
        return message_array;
    }
    function getMessagesOfUserByAddress(address user_public_address_received) public view returns(Message[]){
        return user_to_message[user_public_address_received];
    }


}
contract Profile{
    string username;
    string encrypted_data;
    address user_public_address;
    function getUserName()public view returns(string){
        return username;
    }

    function getUserData()public view returns(string){
        return encrypted_data;
    }

    function addUser(string user_name_received,string encrypted_data_received,address user_public_address_received) public {
        username=user_name_received;
        encrypted_data=encrypted_data_received;
        user_public_address=user_public_address_received;
    }

    function getUserByName(string user_name_received)public view returns(string,string,address){
        require(msg.sender==user_public_address);
        if(keccak256(abi.encodePacked(username)) == keccak256(abi.encodePacked(user_name_received))){
        return(username,encrypted_data,user_public_address);
        }
    }
    function getUserAddress()public view returns(address){
        return user_public_address;
    }

}