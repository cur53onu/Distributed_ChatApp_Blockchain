pragma solidity ^0.4.17;
pragma experimental ABIEncoderV2;

contract MainContract {
    string private mainContractName;
    address[] private deployedUsers;
    address[] private deployedChatRooms;
    struct chatRoomInfoStruct {
        string chatRoomName;
        string ownerUsername;
        address ownerProfileAddress;
        bool chatRoomType;
    }

    chatRoomInfoStruct chatRoomStructVar;
    mapping(address => chatRoomInfoStruct) private addressToChatRoomMap;
    chatRoomInfoStruct[] private chatRoomsArray;
    mapping(address => string) private public_address_to_username;

    constructor(string mainContractNameReceived) public {
        mainContractName = mainContractNameReceived;
    }

    // Deploy chat rooms
    function deployChatRoom(
        string chatRoomNameReceived,
        bool isPrivateRoomReceived
    ) public {
        require(validateUser());
        address newContractAddress = new ChatRoom(
            chatRoomNameReceived,
            getUserProfileAddress(),
            isPrivateRoomReceived
        );
        ChatRoom chatRoomContract = ChatRoom(newContractAddress);
        chatRoomInfoStruct storage buildRoom = addressToChatRoomMap[
            newContractAddress
        ];
        buildRoom.chatRoomName = chatRoomNameReceived;
        buildRoom.ownerUsername = chatRoomContract.getOwnerUsername();
        buildRoom.ownerProfileAddress = getUserProfileAddress();
        buildRoom.chatRoomType = isPrivateRoomReceived;
        chatRoomsArray.push(buildRoom);
        deployedChatRooms.push(newContractAddress);
    }

    // Deploy profiles
    function deployProfile(
        string usernameReceived,
        string encryptedDataReceived
    ) public {
        if (
            keccak256(
                abi.encodePacked(public_address_to_username[msg.sender])
            ) == keccak256(abi.encodePacked(""))
        ) {
            address profile = new Profile(
                usernameReceived,
                encryptedDataReceived,
                msg.sender
            );
            deployedUsers.push(profile);
            public_address_to_username[msg.sender] = usernameReceived;
            return;
        }
    }

    // getters
    function getAllDeployedChatRooms() public view returns (address[]) {
        require(validateUser());
        return deployedChatRooms;
    }

    function getUserProfileAddress() public view returns (address) {
        string storage username = public_address_to_username[msg.sender];
        for (uint256 i = 0; i < deployedUsers.length; i++) {
            Profile prof = Profile(deployedUsers[i]);
            if (
                keccak256(abi.encodePacked(username)) ==
                keccak256(abi.encodePacked(prof.getUsername()))
            ) {
                return deployedUsers[i];
            }
        }
        revert();
    }

    function getDeployedProfileAddressByName(string username)
        public
        view
        returns (address)
    {
        for (uint256 i = 0; i < deployedUsers.length; i++) {
            Profile prof = Profile(deployedUsers[i]);
            if (
                keccak256(abi.encodePacked(username)) ==
                keccak256(abi.encodePacked(prof.getUsername()))
            ) {
                return deployedUsers[i];
            }
        }
    }

    function getDeployedChatRoomAddressByName(string chatRoomNameReceived)
        public
        view
        returns (address)
    {
        require(validateUser());
        for (uint256 i = 0; i < deployedChatRooms.length; i++) {
            ChatRoom room = ChatRoom(deployedChatRooms[i]);
            if (
                keccak256(abi.encodePacked(chatRoomNameReceived)) ==
                keccak256(abi.encodePacked(room.getName()))
            ) {
                return deployedChatRooms[i];
            }
        }
        return address(0);
    }

    function getMainContractInfo() public view returns (string, uint256, uint256) {
        return (mainContractName, deployedChatRooms.length, deployedUsers.length);
    }

    function getDeployedChatRoomInfo(address chatRoomAddressReceived)
        public
        view
        returns (chatRoomInfoStruct)
    {
        require(validateUser());
        return addressToChatRoomMap[chatRoomAddressReceived];
    }


    // Validations
    function validateUser() private view returns (bool) {
        address profileAddress = getUserProfileAddress();
        Profile userProfile = Profile(profileAddress);
        if (userProfile.validateUserPublicAddress(msg.sender)) {
            return true;
        }
        return false;
    }

    function checkAccountExistWithPublicAddress() public view returns (bool) {
        if (
            keccak256(
                abi.encodePacked(public_address_to_username[msg.sender])
            ) == keccak256(abi.encodePacked(""))
        ) {
            return false;
        }
        return true;
    }

}

contract ChatRoom {
    string private chatRoomName;
    bool private isPrivateRoom;
    string public ownerUserName;
    address private ownerProfileAddress;

    // Message
    struct Message {
        string username;
        string message;
        string timestamp;
        address userProfileAddress;
    }
    mapping(address => Message) private userProfileAddressToMsgMapping;
    Message[] private messageArray;
    mapping(address => Message[]) private userProfileAddressToMsgArrayMapping;

    // User Info
    struct UserInfo {
        string username;
        bool userOnline;
        bool userDeleted;
    }
    mapping(address => UserInfo) private userProfileAddressToUserInfoMapping;
    UserInfo[] private userInfoArray;

    // Constructor
    constructor(
        string chatRoomNameReceived,
        address ownerProfileAddressReceived,
        bool isPrivateRoomReceived
    ) public {
        chatRoomName = chatRoomNameReceived;
        ownerProfileAddress = ownerProfileAddressReceived;
        isPrivateRoom = isPrivateRoomReceived;
        Profile profile = Profile(ownerProfileAddressReceived);
        ownerUserName = profile.getUsername();
        UserInfo storage build_userInfo = userProfileAddressToUserInfoMapping[
            ownerProfileAddressReceived
        ];
        build_userInfo.username = profile.getUsername();
        build_userInfo.userOnline = false;
        build_userInfo.userDeleted = false;
    }

    // Owner functions
    function addUser(
        address userProfileAddressReceived,
        address ownerProfileAddressReceived
    ) public {
        if(checkUserIsOwner(ownerProfileAddressReceived))
        {
            Profile profile = Profile(userProfileAddressReceived);
            UserInfo storage build_userInfo = userProfileAddressToUserInfoMapping[
                userProfileAddressReceived
            ];
            build_userInfo.username = profile.getUsername();
            build_userInfo.userOnline = false;
            build_userInfo.userDeleted = false;
            userInfoArray.push(build_userInfo);
        }
    }

    function deleteUser(address userProfileAddressReceived, address ownerProfileAddressReceived) public {
        if(checkUserIsOwner(ownerProfileAddressReceived)){
            if (userProfileAddressReceived != ownerProfileAddress) {
                userProfileAddressToUserInfoMapping[userProfileAddressReceived]
                    .userDeleted = true;
            }
        }
    }


    function setChatRoomType(address ownerProfileAddressReceived, bool roomType) public {
        require(checkUserIsOwner(ownerProfileAddressReceived));
        isPrivateRoom = roomType;
    }

    function checkUserIsOwner(address ownerAddressReceived)
        public
        view
        returns (bool)
    {
        if(validateUserThroughProfile(ownerAddressReceived))
        {
            if (ownerProfileAddress == ownerAddressReceived) {
            return true;
            }
        }
        return false;
    }


    // User functions
    function addMessage(
        address userProfileAddressReceived,
        string usernameReceived,
        string messageReceived,
        string timestampReceived
    ) public {
        checkUserPresent(userProfileAddressReceived);
        Message storage buildMessage = userProfileAddressToMsgMapping[
            userProfileAddressReceived
        ];
        buildMessage.username = usernameReceived;
        buildMessage.message = messageReceived;
        buildMessage.userProfileAddress = userProfileAddressReceived;
        buildMessage.timestamp = timestampReceived;
        messageArray.push(buildMessage);
        userProfileAddressToMsgArrayMapping[userProfileAddressReceived].push(
            buildMessage
        );
    }

    function setUserStatus(address userProfilAddressReceived, bool statusReceived) public {
        require(checkUserPresent(userProfilAddressReceived));
        userProfileAddressToUserInfoMapping[userProfilAddressReceived]
            .userOnline = statusReceived;
    }

    // Validations
    function validateUserThroughProfile(address userProfilAddressReceived)
        public
        view
        returns (bool)
    {
        Profile profile = Profile(userProfilAddressReceived);
        if (profile.validateUserPublicAddress(msg.sender)) {
            return true;
        }
        return false;
    }

    function checkUserPresent(address userProfileAddressReceived)
        public
        view
        returns (bool)
    {
        if (validateUserThroughProfile(userProfileAddressReceived) == false ||
            (isPrivateRoom == true &&
                (keccak256(
                    abi.encodePacked(
                        userProfileAddressToUserInfoMapping[
                            userProfileAddressReceived
                        ].username
                    )
                ) == keccak256(abi.encodePacked("")))) ||
                (userProfileAddressToUserInfoMapping[userProfileAddressReceived]
                    .userDeleted == true)
        ) {
            return false;
        }
        return true;
    }

    // Getters

    function getOwnerUsername() public view returns (string) {
        return ownerUserName;
    }

    function getName() public view returns (string) {
        return chatRoomName;
    }

    function getOwner() public view returns (address, string) {
        return (ownerProfileAddress, ownerUserName);
    }

    function getUserStatus(address userProfileAddressReceived)
        public
        view
        returns (bool)
    {
        return
            userProfileAddressToUserInfoMapping[userProfileAddressReceived]
                .userOnline;
    }

    function getAlluserProfileAddressToMsgMapping(address userProfileAddressReceived)
        public
        view
        returns (Message[])
    {
        checkUserPresent(userProfileAddressReceived);
        return messageArray;
    }

    function getuserProfileAddressToMsgMappingOfUserByAddress(
        address userProfilAddressReceived
    ) public view returns (Message[]) {
        checkUserPresent(msg.sender);
        return userProfileAddressToMsgArrayMapping[userProfilAddressReceived];
    }


    function getChatRoomType() public view returns (bool) {
        return isPrivateRoom;
    }

    function getChatRoomInfo() public view returns (string, string, bool) {
        return (chatRoomName, ownerUserName, isPrivateRoom);
    }

    function getUserInfoArray() public view returns(UserInfo[]){
        return userInfoArray;
    }
}

contract Profile {
    string private username;
    string private encryptedData;
    address public userPublicAddress;
    string[] private privateData;

    constructor(string usernameReceived, string encryptedDataReceived, address userPublicAddressReceived) public {
        username = usernameReceived;
        encryptedData = encryptedDataReceived;
        userPublicAddress = userPublicAddressReceived;
    }

    function getUsername() public view returns (string) {
        return username;
    }

    function getUserData() public view returns (string) {
        if (userPublicAddress == msg.sender) {
            return encryptedData;
        }
        return "";
    }

    function getUserPublicAddress() public view returns (address) {
        if (userPublicAddress == msg.sender) {
            return userPublicAddress;
        }
        return 0x0000000000000000000000000000000000000000;
    }

    function getPrivateData() public view returns (string[]) {
        if (msg.sender == userPublicAddress) {
            return privateData;
        }
    }

    function addPrivateData(string privateDataReceived) public {
        if (msg.sender == userPublicAddress) {
            privateData.push(privateDataReceived);
        }
    }

    function validateUserPublicAddress(address userPublicAddressReceived) public view returns(bool){
        if(userPublicAddressReceived == userPublicAddress){
            return true;
        }
        return false;
    }
}
