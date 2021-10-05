pragma solidity ^0.4.17;
pragma experimental ABIEncoderV2;

contract DeployContracts{
    address[] public deployedUsers;
    address[] public deployedChatRooms;
    struct chatRoomStruct {
        string chatRoomName;
        address ownerAddress;
        bool chatRoomType;
    }
    chatRoomStruct chatRoomStructVar;
    mapping(address=>chatRoomStruct) public address_to_chatRoom_map;
    chatRoomStruct[] public chat_rooms_array;
    mapping(address=>string) public public_address_to_username;

    function deployChatRoom(string chat_room_name,bool privateChatRoom) public{
        string username = public_address_to_username[msg.sender];
        require(validateUser());
        address ContractAddress=new ChatRoom();
        ChatRoom newContract=ChatRoom(ContractAddress);
        newContract.setName(chat_room_name);
        newContract.setOwner(getUsersProfileAddress());
        newContract.setChatRoomType(privateChatRoom);
        newContract.setOwnerUsername(username);
        newContract.addUser(getUsersProfileAddress(),username);
        deployedChatRooms.push(ContractAddress);
    }

    function deployProfiles(string username,string data) public{
        if(keccak256(abi.encodePacked(public_address_to_username[msg.sender])) == keccak256(abi.encodePacked(""))){
            address profile=new Profile();
            Profile prof=Profile(profile);
            prof.addUser(username,data,msg.sender);
            deployedUsers.push(profile);
            public_address_to_username[msg.sender]=username;
            return;
        }
        revert();
    }


    function addUserToChatRoomByUserName(string chat_room_name_received, string user_name_received) public{
        string owner_username = public_address_to_username[msg.sender];
        require(validateUser());
        require(checkUserIsOwner(chat_room_name_received));
        address chat_room_address=getDeployedChatRoomAddressByName(chat_room_name_received);
        ChatRoom chat_room=ChatRoom(chat_room_address);
        address profile_address=getDeployedChatRoomAddressByName(user_name_received);
        chat_room.addUser(profile_address, user_name_received);
    }

    function addMessage(string chat_room_name_received,string message_received,string timestamp_received) public{
        string username = public_address_to_username[msg.sender];
        require(validateUser());
        require(checkUserPresent(chat_room_name_received, username));
        address chat_room_address=getDeployedChatRoomAddressByName(chat_room_name_received);
        ChatRoom chat_room=ChatRoom(chat_room_address);
        chat_room.addMessage(msg.sender,username,message_received,timestamp_received);
    }

    function setChatRoomType(string chat_room_name_received, bool roomType)public {
        string username = public_address_to_username[msg.sender];
        require(validateUser());
        require(checkUserIsOwner(chat_room_name_received));
        address roomAddress = getDeployedChatRoomAddressByName(chat_room_name_received);
        ChatRoom room = ChatRoom(roomAddress);
        room.setChatRoomType(roomType);
    }

    function getMessagesFromChatRoomByName(string chat_room_name_received)public view returns(ChatRoom.Message[]){
        string username = public_address_to_username[msg.sender];
        require(validateUser());
        require(checkUserPresent(chat_room_name_received, username));
        address chat_room_address=getDeployedChatRoomAddressByName(chat_room_name_received);
        ChatRoom chat_room=ChatRoom(chat_room_address);
        return chat_room.getAllMessages();
    }

    function getDeployedProfileData()public view returns (string){
        address profile_address=getUsersProfileAddress();
        Profile user_profile=Profile(profile_address);
        return user_profile.getUserData();
    }

    function getUsersProfileAddress()private view returns (address){
        string username = public_address_to_username[msg.sender];
        for(uint i=0;i<deployedUsers.length;i++)
        {
            Profile prof=Profile(deployedUsers[i]);
            if(keccak256(abi.encodePacked(username)) == keccak256(abi.encodePacked(prof.getUserName()))){
                return deployedUsers[i];
            }
        }
        throw;
    }

    function getDeployedProfileAddressByName(string username)public returns(address){
        for(uint i=0;i<deployedUsers.length;i++)
        {
            Profile prof=Profile(deployedUsers[i]);
            if(keccak256(abi.encodePacked(username)) == keccak256(abi.encodePacked(prof.getUserName()))){
                return deployedUsers[i];
            }
        }
    }

    function getChatRoomOwner(string chat_room_name_received)private view returns(address){
        address chat_room_address=getDeployedChatRoomAddressByName(chat_room_name_received);
        ChatRoom room=ChatRoom(chat_room_address);
        return room.getOwner();
    }

    function getDeployedChatRoomAddressByName(string chat_room_name_received) private view returns(address){
        for(uint i=0;i<deployedChatRooms.length;i++)
        {
            ChatRoom room=ChatRoom(deployedChatRooms[i]);
            if(keccak256(abi.encodePacked(chat_room_name_received)) == keccak256(abi.encodePacked(room.getName()))){
                return deployedChatRooms[i];
            }
        }
    }

    function checkUserIsOwner(string chat_room_name_received)private returns(bool){
        if(keccak256(abi.encodePacked(getUsersProfileAddress())) == keccak256(abi.encodePacked(getChatRoomOwner(chat_room_name_received)))){
                return true;
        }
        return false;
    }

    function validateUser() private view returns(bool){
        address profile_address = getUsersProfileAddress();
        Profile user_profile = Profile(profile_address);
        if (keccak256(abi.encodePacked(msg.sender)) == keccak256(abi.encodePacked(user_profile.getUserAddress()))){
            return true;
        }
        return false;
    }

    function checkUserPresent(string chatRoomName, string username)private view returns(bool){
        address chatRoomAddress = getDeployedChatRoomAddressByName(chatRoomName);
        ChatRoom chatRoom = ChatRoom(chatRoomAddress);
        if (chatRoom.checkUserPresent(getDeployedProfileAddressByName(username))==true){
            return true;
        }
        return false;
    }
    function getInfo() public view returns(uint,uint){
        return (deployedChatRooms.length,deployedUsers.length);
    }
    function getDeployedChatRoomInfo() public view returns(string[]){
        string[] array;
        for(uint i=0;i<deployedChatRooms.length;i++)
        {
            ChatRoom room=ChatRoom(deployedChatRooms[i]);
            array.push(room.getChatRoomInfo());
        }
        return array;
    }

}

contract ChatRoom{
    string chat_room_name;
    bool privateChatRoom;
    string ownerUserName;
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
    function setOwnerUsername(string username) public{
        ownerUserName=username;
    }
    function getOwnerUsername()public view returns(string){
        return ownerUserName;
    }

    function addUser(address user_profile_address,string username) public{
        users_to_address[user_profile_address]=username;
    }
    function addMessage(address user_public_address_received,string user_name_received,string message_received,string timestamp_received)public {
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

    function checkUserPresent(address user_profile_address)public view returns(bool){
        if(privateChatRoom==true && keccak256(abi.encodePacked(users_to_address[user_profile_address])) == keccak256(abi.encodePacked(""))){
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
    function setChatRoomType(bool roomType)public {
        privateChatRoom=roomType;
    }
    function getChatRoomType()public view returns(bool){
        return privateChatRoom;
    }
    function append(string a, string b, string c, string d, string e, string f) internal pure returns (string) {
        return string(abi.encodePacked(a, b, c, d, e, f));
    }
    function getChatRoomInfo()public view returns(string){
        if(privateChatRoom){
            return append("RoomName: " , chat_room_name , " RoomType: " , " PrivateRoom " , "RoomOwner: " , ownerUserName);
        }
        return append("RoomName: " , chat_room_name , " RoomType: " , " PublicRoom " , "RoomOwner: " , ownerUserName);
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