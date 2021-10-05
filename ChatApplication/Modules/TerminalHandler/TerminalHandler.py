import urwid
import threading
global value
class RoomTerminal(urwid.WidgetWrap):
    def __init__(self, interactDeployObj, chatroomName, username):
        self.interactDeployObj = interactDeployObj
        loop=None
        self.flg=True
        self.listenMsgThread=None
        self.chatRoomName = chatroomName
        self.username = username
        self.msgSize = 0
        self.screen_text = urwid.Text(self.chatRoomName + ' : ' + self.username)
        self.prompt_text = urwid.Edit(self.username + ': ', '')
        self._w = urwid.Frame(header=urwid.Pile([urwid.Text(self.chatRoomName),
                                                 urwid.Divider()]),
                              body=urwid.ListBox([self.screen_text]),
                              footer=self.prompt_text,
                              focus_part='footer')

    def getMsg(self):
        cnt = 0
        while self.flg:
            curr_msg = self.interactDeployObj.callGetMessagesFromChatRoomByName(self.interactDeployObj.chatRoomName, self.interactDeployObj.public_address)
            if self.msgSize < len(curr_msg):
                for i in range(self.msgSize, len(curr_msg)):
                    msg = curr_msg[i]
                    if cnt > self.loop.screen.get_cols_rows()[1]-7:
                        self.screen_text.set_text('')
                        cnt=0
                    self.screen_text.set_text(self.screen_text.text +
                                              '\n' +
                                              '('+ msg[0] + ':' +msg[2] + '): '+ msg[1])
                    cnt+=1
                    try:
                        self.loop.draw_screen()
                    except AssertionError as e:
                        print("Error to display messages, pleasse try again!" + str(e))

                self.msgSize = len(curr_msg)

        print('exited '+self.chatRoomName + ' room')
    def keypress(self, size, key):
        if key == 'esc':
            self.flg=False
            raise urwid.ExitMainLoop()

        if key == 'enter':
            query = self.prompt_text.edit_text
            msg = query
            sendMsg = threading.Thread(target=self.interactDeployObj.transactAddMessage, args=(self.chatRoomName, msg))
            sendMsg.start()
            self.prompt_text.edit_text = ''
            return
        super(RoomTerminal, self).keypress(size, key)

