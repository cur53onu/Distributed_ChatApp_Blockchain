import time

import urwid
import threading

import web3.exceptions

global value
class RoomTerminal(urwid.WidgetWrap):
    def __init__(self, interactDeployObj, chatroomName, username, public_address):
        self.interactDeployObj = interactDeployObj
        loop=None
        self.flg=True
        self.listenMsgThread=None
        self.chatRoomName = chatroomName
        self.username = username
        self.public_address = public_address
        self.msgSize = 0
        self.screen_text = urwid.Text(self.chatRoomName + ' : ' + self.username)
        self.prompt_text = urwid.Edit(self.username + ': ', '')
        self.msgList=[]
        self.msgList.append(self.screen_text)
        self._w = urwid.Frame(header=urwid.Pile([urwid.Text(self.chatRoomName,align=urwid.CENTER),
                                                 urwid.Divider()]),
                              body=urwid.ListBox(self.msgList),
                              footer=self.prompt_text,
                              focus_part='footer')

    def getMsg(self):
        cnt = 0
        while self.flg:
            curr_msg = self.interactDeployObj.callGetMessagesFromChatRoomByName(self.interactDeployObj.chatRoomName, self.username, self.interactDeployObj.public_address)
            if curr_msg == None:
                raise urwid.ExitMainLoop()
                return
            if self.msgSize < len(curr_msg):
                for i in range(self.msgSize, len(curr_msg)):
                    if cnt > self.loop.screen.get_cols_rows()[1] - 7:
                        self.msgList.clear()
                        self._w.set_body(urwid.ListBox(self.msgList))
                        cnt = 0
                        try:
                            self.loop.draw_screen()
                        except AssertionError as e:
                            print("Error to display messages, pleasse try again!" + str(e))
                    msg = curr_msg[i]
                    alignment=urwid.LEFT
                    msg_to_show = ""
                    if msg[0]==self.username:
                        msg_to_show=msg[1]
                        alignment=urwid.RIGHT
                    else:
                        msg_to_show="(" + msg[0] + " : " + msg[2] + ") " + msg[1]
                    t = urwid.Text(msg_to_show, align=alignment)
                    self.msgList.append(t)
                    self._w.set_body(urwid.ListBox(self.msgList))
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
            self.prompt_text.edit_text = ''
            msg = query
            sendMsg = threading.Thread(target=self.interactDeployObj.transactAddMessage, args=(self.chatRoomName, msg))
            sendMsg.start()
            sendMsg.join()
            return
        super(RoomTerminal, self).keypress(size, key)

