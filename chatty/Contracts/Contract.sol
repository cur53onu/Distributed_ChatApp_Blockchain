pragma solidity ^0.4.17;
pragma experimental ABIEncoderV2;
contract ChatRoom{
    string public chat_room_name;
    address[] public users;
    string[] public messages;
    address public owner;
    mapping (address => string[]) public record;

    function getName()public view returns(string){
        return chat_room_name;
    }
    function setName(string Name){
        chat_room_name=Name;
    }
    function addUser(address User) public{
        users.push(User);
        
    }
    function sendMessage(address User,string Message)public{
        string[] val=record[User];
        val.push(Message);
    }
    function getMessages(address User)public view returns(string[]){
        string[] val=record[User];
        return val;
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
