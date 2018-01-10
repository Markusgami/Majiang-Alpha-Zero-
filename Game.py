import numpy as np
import zlib

wan = [1,2,3,4,5,6,7,8,9] #万
tiao = [11,12,13,14,15,16,17,18,19] #条
tong = [21,22,23,24,25,26,27,28,29] #筒
card_name = {1:'一万',2:'两万',3:'三万',4:'四万',5:'五万',6:'六万',7:'七万',8:'八万',9:'九万',
             11:'幺鸡',12:'二条',13:'三条',14:'四条',15:'五条',16:'六条',17:'七条',18:'八条',19:'九条', 
             21:'一桶',22:'二桶',23:'三桶',24:'四桶',25:'五桶',26:'六桶',27:'七桶',28:'八桶',29:'九桶'
            }

'''
wan = ['w1','w2','w3','w4','w5','w6','w7','w8', 'w9'] #万
tiao = ['t1','t2','t3','t4','t5','t6','t7','t8', 't9'] #条
tong = ['o1','o2','o3','o4','o5','o6','o7','o8', 'o9'] #筒
card_name = {'w1':'一万','w2':'两万','w3':'三万','w4':'四万','w5':'五万','w6':'六万','w7':'七万','w8':'八万','w9':'九万',
             't1':'幺鸡','t2':'二条','t3':'三条','t4':'四条','t5':'五条','t6':'六条','t7':'七条','t8':'八条','t9':'九条',
             'o1':'一桶','o2':'二桶','o3':'三桶','o4':'四桶','o5':'五桶','o6':'六桶','o7':'七桶','o8':'八桶','o9':'九桶'
            }
'''
cards_class = wan + tiao + tong

#发牌
def fapai(all_cards):
    p1 = []
    p2 = []
    p3 = []
    p4 = []
    m = 0
    for i in range(4):
        if i != 3:
            for card in all_cards[m:m+4]:
                p1.append(card)
            m = m+4
            
            for card in all_cards[m:m+4]:
                p2.append(card)
            m = m+4
            
            for card in all_cards[m:m+4]:
                p3.append(card)
            m = m+4
            
            for card in all_cards[m:m+4]:
                p4.append(card)
            m = m+4

        else:
            for card in all_cards[m:m+2]:
                p1.append(card)
            m = m+2
            p2.append(all_cards[m])
            m = m+1
            p3.append(all_cards[m])
            m = m+1
            p4.append(all_cards[m])
            m = m+1
    all_cards = all_cards[m:]
    return p1, p2, p3 , p4, all_cards


def check(players,player,card_out,zimo):
    player_num = []
    for i in range(len(players)):
        player_num.append((player-1 +i) % len(players))

    if len(players) == 4:
        
        check_out = players[player_num[1]].check(card_out,zimo) 
        
        if check_out == 'hu':
            return (player + 1)% len(players), 'hu'
        
        if check_out == 'gang':
            return (player + 1)% len(players), 'gang'
        
        if check_out == 'peng':
            return (player + 1)% len(players), 'peng'
        
        
        check_out = players[player_num[2]].check(card_out,zimo)
        
        if check_out == 'hu':
            return (player + 2)% len(players), 'hu'
        
        if check_out == 'gang':
            return (player + 2)% len(players), 'gang'
        
        if check_out == 'peng':
            return (player + 2)% len(players), 'peng'
                
        check_out = players[player_num[3]].check(card_out,zimo)
        
        if check_out == 'hu':
            return (player + 3)% len(players), 'hu'
        
        if check_out == 'gang':
            return (player + 3)% len(players), 'gang'
        
        if check_out == 'peng':
            return (player + 3)% len(players), 'peng'         
            
    return (player + 1)% len(players), 'no_act'  


#玩家的类
class player():
    def __init__(self, cards,name):
        self.cards_hide = cards #玩家的牌
        self.cards_out = [] #玩家打出的牌
        self.cards_show = [] #玩家显示出的牌（碰、杠）
        self.card_out = None
        self.cards_count_show = {i:0 for i in set(cards_class)}
        self.cards_count_hide = {i:0 for i in set(cards_class)}
        self.cards_count_out = {i:0 for i in set(cards_class)}
        
        self.count_cards_show() #点牌
        self.count_cards_hide()
        self.count_cards_out()
        self.name = name
        self.double = 0
        self.lian = 0
        self.tri = 0
        self.four = 0
        self.gang_num = 0
        self.card_more_2 = []
        self.peng_memory = []
        self.value = 0
        
    def get_hu_value(self):
        value = 0
        if self.double == 7: #小七对
            value = 8
            
        elif self.four ==1 and self.double ==6: #龙七对
            value = 13
            
        elif self.four ==2 and self.double ==5: #龙七对
            value = 13    
            
        elif self.tri ==4: #大对子
            value = 8        
        else:
            value = 2
        
        return value
    
    def get_value(self):
        value = 0
        if self.check_jiao() == True:
            value += 2 * self.gang_num        
        return value

    def check_jiao(self):
        return True
    
    
    def get_card(self,card): #摸牌
        print (self.name + '摸到了' + card_name[card])
        self.cards_hide.append(card)
        self.cards_count_hide[card] += 1
        self.cards_hide.sort()
            
        
    def play_card(self,card): #出牌
        ff = self.cards_hide.remove(card)
        self.cards_out.append(card)
        self.cards_count_hide[card] -= 1      
        print (self.name + '出'+card_name[card])
        
    def choose_card(self,p2,p3 = None,p4 = None): # 选牌
        card = predict(self,p2,p3,p4)
        return card
    
    def auto_play_card(self,p2,p3 = None,p4 = None):
        card = self.choose_card(p2,p3,p4)
        self.play_card(card)
        return card
    
    def count_cards_hide(self):
        self.cards_count_hide = {i:0 for i in cards_class}
        for card in self.cards_hide:
            self.cards_count_hide[card] += 1
        return self.cards_count_hide
            
    def count_cards_show(self):
        self.cards_count_show = {i:0 for i in cards_class}
        for card in self.cards_show:
            self.cards_count_show[card] += 1
        return self.cards_count_show
    
    def count_cards_out(self):
        self.cards_count_out = {i:0 for i in cards_class}
        for card in self.cards_out:
            self.cards_count_out[card] += 1
        return self.cards_count_out
    
    def check(self,card,zimo = False):
        if self.check_hu(zimo, new_card = card) == True :
            return 'hu'
        
        elif (self.cards_count_hide[card] == 3 and zimo == False) \
              or (self.cards_count_show[card]  == 3 and card in self.peng_memory  and zimo == True)\
              or (self.cards_count_hide[card] == 4 and zimo == True):
            return 'gang'
        
        elif self.cards_count_hide[card] == 2 and zimo == False:
            return 'peng'
                               
        else:
            return 'Clear'
            
                
    
    def peng(self,card):
        if self.cards_count_hide[card] == 3:
            print (self.name + '碰')                
            self.cards_count_show[card] = 3
            self.cards_count_hide[card] = 0
            self.cards_hide.sort()
            self.cards_hide.remove(card)
            self.cards_hide.remove(card)
            self.cards_hide.remove(card)
            self.cards_show.append(card)
            self.cards_show.append(card)
            self.cards_show.append(card)
            self.cards_show.sort()
            self.peng_memory.append(card)
        else:
            print(self.name +'不能碰')
    
    def gang(self,card,left_cards, zimo = False):
        if self.cards_count_hide[card] == 4:
            print (self.name + '杠')
            self.cards_count_hide[card] = 0
            self.cards_count_show[card] = 4
            self.cards_hide.remove(card)
            self.cards_hide.remove(card)
            self.cards_hide.remove(card)
            self.cards_hide.remove(card)
            self.cards_show.append(card)
            self.cards_show.append(card)
            self.cards_show.append(card)
            self.cards_show.append(card)
            self.cards_show.sort()
            self.cards_hide.sort()
            left_cards.pop(-1)
            
        elif self.cards_count_hide[card] == 1 and self.cards_count_show[card]==3 and zimo == True:
            print (self.name + '杠')
            self.cards_count_hide[card] = 0
            self.cards_count_show[card] = 4
            self.cards_hide.remove(card)
            self.cards_show.append(card)
            self.cards_show.sort()
        
            self.cards_hide.sort()
            left_cards.pop(-1)
            
        else:
            print(self.name +'不能杠')
        
    def hu(self,card):
        END_GAME = 1 
        print (self.name + '胡！')
        print (self.name + '摸到了' + card_name[card])
        show_cards = []
        for card in self.cards_hide + self.cards_show:
            show_cards.append(card_name[card])
        print ('亮牌！')
        print (show_cards)
            
        
    def choose_peng(self,card,p2,p3,p4):
        return True
        
    def choose_gang(self,card,p2,p3,p4):
        return True
    
    
    def check_hu(self,zimo,new_card = None):
        #胡牌前先点牌
        self.count_cards_show()
        self.count_cards_hide()
        self.count_cards_out()
        self.card_more_2 = []
        for card, number in self.cards_count_hide.items():
            if number >= 2:
                self.card_more_2.append(card)
                
        card_2_count = list(self.cards_count_hide.values()).count(2)  
        card_4_count = list(self.cards_count_hide.values()).count(4)  
        if card_2_count <= 0:
            return False
        
        elif card_2_count + 2 * card_4_count == 7: #小七对
            self.double = card_2_count
            self.four = card_4_count
            return True
        

        for i in range(len(self.card_more_2)): 
            tri = 0 
            lian = 0
            four = 0
            p = self.cards_hide[:]
            
            cards_count_hide_copy = copy.deepcopy(self.cards_count_hide)
            if new_card != None:
                p.append(new_card)
                cards_count_hide_copy[new_card] += 1
              
            p.remove(self.card_more_2[i])
            p.remove(self.card_more_2[i])
            while len(p) != 0:
                
                if cards_count_hide_copy[p[0]] ==3 :
                    tri += 1
                    cards_count_hide_copy[p[0]] = 0
                    p.pop(0)

                    p.pop(0)

                    p.pop(0)
            
                elif cards_count_hide_copy[p[0]] ==4 :
                    four += 1
                    cards_count_hide_copy[p[0]] = 0
                    p.pop(0)
                    p.pop(0)
                    p.pop(0)
                    p.pop(0)
             
            
                else:
                    if p[0] in p and p[0] +1 in p and p[0] +2 in p:
                        a = p[0]
                        b = p[0] + 1
                        c = p[0] + 2
                        cards_count_hide_copy[a] -= 1
                        p.remove(a)
                        cards_count_hide_copy[b] -= 1
                        p.remove(b)
                        cards_count_hide_copy[c] -= 1
                        p.remove(c)
                        lian += 1
                    else:
                        break
                
                if len(p) == 0:
                    
                    self.tri = tri
                    self.four = four
                    self.lian = lian
                    for card, number in self.cards_count_show.items():
                        if number == 3:
                            self.tri += 1
                        if number == 4:
                            self.four += 1
                    
                    if self.tri ==4:
                        return True
                    
                    if (self.four >=1) and (self.four + self.tri + self.lian == 4):
                        return True
                    
                    if self.tri + self.lian == 4 and zimo == True:
                        return True
                    
        return False
    
    

    
class majiang():
    #def __init__(self):
        
    def getInitBoard(self,left_cards):
        self.left_cards = left_cards #所有牌
        self.card_out = None #最新打到桌上的牌
        self.last_action = None #上一个动作
        p1, p2 ,p3, p4, self.left_cards= fapai(self.left_cards) #给p1~p4发牌
        p1.sort(), p2.sort() ,p3.sort(), p4.sort()
        players = []
        player1 = player(p1, '1')
        player2 = player(p2, '2')
        player3 = player(p3, '3')
        player4 = player(p4, '4')
        players.append(player1)
        players.append(player2)
        players.append(player3)
        players.append(player4)
        self.players = players   
        self.curPlayer = 1
        self.lastPlayer = 1
        self.board = {}
        self.target = None
        return players
    
    
    
    def getCurInfo(self):
        self.board['left_cards'] = self.left_cards
        self.board['card_out'] = self.card_out
        self.board['last_action'] = self.last_action
        self.board['players'] = self.players
        self.board['curPlayer'] = self.curPlayer
        self.board['lastPlayer'] = self.lastPlayer
        self.board['target'] = self.target
        return copy.deepcopy(self.board)
    
    def getSymmetries(self, canonicalBoard, pi):
        all_canonicalBoard = np.zeros((6,9,27))
        all_pi = np.zeros((6,27))
        
        new_canonicalBoard1 = np.empty_like(canonicalBoard)
        new_canonicalBoard2 = np.empty_like(canonicalBoard)
        new_canonicalBoard3 = np.empty_like(canonicalBoard)
        new_canonicalBoard4 = np.empty_like(canonicalBoard)
        new_canonicalBoard5 = np.empty_like(canonicalBoard)
        
        new_pi1 = np.empty_like(pi)
        new_pi2 = np.empty_like(pi)
        new_pi3 = np.empty_like(pi)
        new_pi4 = np.empty_like(pi)
        new_pi5 = np.empty_like(pi)
        
        
        new_canonicalBoard1[:,:9] = canonicalBoard[:,18:]
        new_canonicalBoard1[:,9:18] = canonicalBoard[:,0:9]
        new_canonicalBoard1[:,18:] = canonicalBoard[:,9:18]
        
        new_pi1[:9] = pi[18:]
        new_pi1[9:18] = pi[0:9]
        new_pi1[18:] = pi[9:18]
        
        new_canonicalBoard2[:,:9] = canonicalBoard[:,0:9]
        new_canonicalBoard2[:,9:18] = canonicalBoard[:,18:]
        new_canonicalBoard2[:,18:] = canonicalBoard[:,9:18]
        
        new_pi2[:9] = pi[0:9]
        new_pi2[9:18] = pi[18:]
        new_pi2[18:] = pi[9:18]
        
        new_canonicalBoard3[:,:9] = canonicalBoard[:,9:18]
        new_canonicalBoard3[:,9:18] = canonicalBoard[:,18:]
        new_canonicalBoard3[:,18:] = canonicalBoard[:,0:9]
        
        new_pi3[:9] = pi[9:18]
        new_pi3[9:18] = pi[18:]
        new_pi3[18:] = pi[0:9]
        
        new_canonicalBoard4[:,:9] = canonicalBoard[:,9:18]
        new_canonicalBoard4[:,9:18] = canonicalBoard[:,0:9]
        new_canonicalBoard4[:,18:] = canonicalBoard[:,18:]
        
        new_pi4[:9] = pi[9:18]
        new_pi4[9:18] = pi[0:9]
        new_pi4[18:] = pi[18:]
        
        new_canonicalBoard5[:,:9] = canonicalBoard[:,18:]
        new_canonicalBoard5[:,9:18] = canonicalBoard[:,0:9]
        new_canonicalBoard5[:,18:] = canonicalBoard[:,9:18]
        
        new_pi5[:9] = pi[18:]
        new_pi5[9:18] = pi[0:9]
        new_pi5[18:] = pi[9:18]
        
        all_canonicalBoard[0] = canonicalBoard
        all_canonicalBoard[1] = new_canonicalBoard1
        all_canonicalBoard[2] = new_canonicalBoard1
        all_canonicalBoard[3] = new_canonicalBoard1
        all_canonicalBoard[4] = new_canonicalBoard1
        all_canonicalBoard[5] = new_canonicalBoard1
        
        all_pi[0] = pi
        all_pi[1] = new_pi1
        all_pi[2] = new_pi2
        all_pi[3] = new_pi3
        all_pi[4] = new_pi4
        all_pi[5] = new_pi5
        return all_canonicalBoard, all_pi
        
    def getCanonicalForm(self,board): #checked
        #copy_board = copy.deepcopy(board)
        #players = copy_board['players']
        #curPlayer = copy_board['curPlayer']
        players = board['players']
        curPlayer = board['curPlayer']

        canonicalBoard = np.zeros((9,27))
        i = 0
        aa = np.array(list(players[curPlayer-1].cards_count_hide.values()))
        canonicalBoard[i] = aa
        i += 1
        
        aa = np.array(list(players[curPlayer-1].cards_count_show.values()))
        canonicalBoard[i] = aa
        i += 1
        
        aa = np.array(list(players[curPlayer-1].cards_count_out.values()))
        canonicalBoard[i] = aa
        i += 1
        
        for j in range(len(players)-1):
            aa = np.array(list(players[(self.curPlayer+j)%len(players)].cards_count_show.values()))
            canonicalBoard[i] = aa
            i += 1
            
            aa = np.array(list(players[(self.curPlayer+j)%len(players)].cards_count_out.values()))
            canonicalBoard[i] = aa
            i += 1
           
        return canonicalBoard
    
    
    def stringRepresentation(self,canonicalBoard):  #checked       
        message = canonicalBoard.tobytes()
        compressed = zlib.compress(message)
        #decompressed = zlib.decompress(compressed)
        #game_state_ = numpy.frombuffer(decompressed).reshape(9,-1).shape
        return compressed
    
    def getActionSize(self): #checked
        return 27
    
    def getValidMoves(self, canonicalBoard):#checked
        valid_move = canonicalBoard[0]
        for i in range(len(valid_move)):
            if valid_move[i] != 0:
                valid_move[i] = 1

            
        return valid_move

    def get_all_values(self,board,zimo):
        copy_board = copy.deepcopy(board)
        #left_cards = copy_board['left_cards']
        #card_out = copy_board['card_out']
        #last_action = copy_board['last_action']
        players = copy_board['players']
        curPlayer = copy_board['curPlayer']
        #lastPlayer = copy_board['lastPlayer']
        target = copy_board['target']
        values = np.zeros((4))
        
        hu_value = players[curPlayer - 1].get_hu_value()
        for i in range(len(players)):
            values[i] =  players[i].get_value()
            
        if target == 5:
            values[curPlayer - 1] = values[curPlayer - 1] + 3 * hu_value
            values[curPlayer] = values[curPlayer] -  hu_value
            values[(curPlayer+1)%len(players)] = values[(curPlayer+1)%len(players)] -  hu_value
            values[(curPlayer+2)%len(players)] = values[(curPlayer+1)%len(players)] -  hu_value
        else:
            values[curPlayer - 1] = values[curPlayer - 1] + hu_value
            values[target - 1] = values[target - 1] -  hu_value
            
        return values
    
    def getGameEnded(self, board, zimo = False): 
        player_num = board['curPlayer'] - 1
        player = board['players'][player_num]
        if player.check_hu(zimo = zimo, new_card = None) == True:
            print ('有胡牌')
            return self.get_all_value(board,zimo)
        elif len(self.left_cards) == 0:
            return 0.0001
        else: 
            return 0
        
    def get_main_player_from_canonicalBoard(self,canonicalBoard):  #checked
        temp_player = player([], 'temp_player')
        for i in range(len(canonicalBoard[0])):
            j = canonicalBoard[0][i]
            while j >0 :
                temp_player.cards_hide.append(cards_class[i])
                j -= 1
        
        for i in range(len(canonicalBoard[1])):
            j = canonicalBoard[1][i]
            while j >0 :
                temp_player.cards_show.append(cards_class[i])
                j -= 1        

        for i in range(len(canonicalBoard[2])):
            j = canonicalBoard[2][i]
            while j >0 :
                temp_player.cards_out.append(cards_class[i])
                j -= 1    
        return temp_player
    
    
    def getNextState(self, board, action,zimo):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player
        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
            
            
        """
        
        copy_board = copy.deepcopy(board)
        self.left_cards = copy_board['left_cards']
        self.card_out = copy_board['card_out']
        self.last_action = copy_board['last_action']
        self.players = copy_board['players']
        self.curPlayer = copy_board['curPlayer']
        self.lastPlayer = copy_board['lastPlayer']
        self.target = copy_board['target']
        
        card_out  = cards_class[action]
        print ('new state')
        print (self.last_action)
        
        if self.last_action == 'peng': #碰
            if card_out == self.card_out: #如果碰检查时，最后决定出碰的那张牌，那就相当于什么都没发生
                self.players[self.curPlayer -1].cards_hide.remove(self.card_out)
                self.players[self.curPlayer -1].cards_count_hide[self.card_out] -= 1
                self.last_action = None
                next_zimo = True
                nextPlayer = (self.lastPlayer )%len(self.players)
                self.curPlayer = nextPlayer
                self.card_out = card_out
                self.lastPlayer = copy.deepcopy(self.curPlayer)
                return self.getCurInfo(), next_zimo
            
            else:
                self.players[self.curPlayer -1].peng(self.card_out)
                self.players[self.curPlayer -1].play_card(card_out)
                self.last_action = 'do peng'
                next_zimo = False
                nextPlayer = (self.lastPlayer + 1)%len(self.players) 
                self.curPlayer = nextPlayer
                self.card_out = card_out
                self.lastPlayer = copy.deepcopy(self.curPlayer)
                return self.getCurInfo(), next_zimo
                
                
        elif self.last_action == 'gang': #杠
            if card_out == self.card_out: #如果杠检查时，最后决定出杠的那张牌，那就相当于什么都没发生
                self.players[self.curPlayer -1].cards_hide.remove(self.card_out)
                self.players[self.curPlayer -1].cards_count_hide[self.card_out] -= 1
                self.last_action = None
                next_zimo = True
                nextPlayer = (self.lastPlayer + 1)%len(self.players)
                self.curPlayer = nextPlayer
                self.card_out = card_out
                self.lastPlayer = copy.deepcopy(self.curPlayer)
                return self.getCurInfo(), next_zimo
                
            else:#最后出其他牌，相当于杠了
                self.players[self.curPlayer -1].gang(self.card_out,self.left_cards,zimo = zimo)
                if zimo == False:
                    self.players[self.curPlayer -1].gang_num += 1
                    self.players[self.lastPlayer -1].gang_num -= 1
                    
                elif zimo ==True:
                    self.players[self.curPlayer -1].gang_num += 3
                    self.players[(self.curPlayer)].gang_num += 1
                    self.players[(self.curPlayer+1) % len(self.players)].gang_num += 1
                    self.players[(self.curPlayer+2) % len(self.players)].gang_num += 1
                    
                self.last_action = 'do gang' 
                nextPlayer = self.curPlayer
                next_zimo = True
                self.card_out = card_out
                self.lastPlayer = copy.deepcopy(self.curPlayer)
                return self.getCurInfo(), next_zimo
                
        elif self.last_action == 'hu': #胡
            print ('las action hu, error')
        
        elif self.last_action == 'do gang' :
            new_card = self.left_cards.pop(0)
            self.players[self.curPlayer -1].get_card(new_card)
            player_check = self.players[self.curPlayer -1].check(new_card,zimo = True)
            if  player_check == 'hu':
                self.card_out = new_card
                self.players[self.curPlayer -1].hu(new_card)
                next_zimo = True
                self.target = 5
                nextPlayer = self.curPlayer
                return self.getCurInfo(), next_zimo
            
            elif player_check == 'gang':
                self.card_out = new_card
                self.players[self.curPlayer -1].gang(new_card,self.left_cards,zimo = True)
                next_zimo = True
                nextPlayer = self.curPlayer
                return self.getCurInfo(), next_zimo
            
            elif player_check == 'Clear' or player_check == 'peng':            
                self.players[self.curPlayer -1].play_card(card_out)        
                nextPlayer,next_act = check(self.players,self.curPlayer ,card_out, zimo = zimo)
                self.curPlayer = nextPlayer
                self.card_out = card_out
                self.lastPlayer = copy.deepcopy(self.curPlayer)
            
                if next_act == 'hu':
                    self.players[nextPlayer -1].cards_hide.append(card_out)
                    self.players[nextPlayer -1].cards_count_hide[card_out] += 1
                    self.last_action = 'hu'
                    self.players[nextPlayer -1].hu(card_out)
                    self.target = copy.deepcopy(self.curPlayer)
                    next_zimo = False
                    return self.getCurInfo(), next_zimo
                
                elif next_act == 'peng':
                    self.players[nextPlayer -1].cards_hide.append(card_out)
                    self.players[nextPlayer -1].cards_count_hide[card_out] += 1
                    self.last_action = 'peng'
                    next_zimo = False
                    return self.getCurInfo(), next_zimo
                
                elif next_act == 'gang':
                    self.players[nextPlayer -1].cards_hide.append(card_out)
                    self.players[nextPlayer -1].cards_count_hide[card_out] += 1
                    self.last_action = 'gang'
                    next_zimo = False
                    return self.getCurInfo(), next_zimo
                
                elif next_act == 'no_act':
                    self.last_action = 'get card'
                    next_zimo = True
                    return self.getCurInfo(), next_zimo
        
        elif self.last_action == 'get card':
            new_card = self.left_cards.pop(0)
            self.players[self.curPlayer -1].get_card(new_card)
            player_check = self.players[self.curPlayer -1].check(new_card,zimo = True)
            if player_check == 'hu':
                self.players[self.curPlayer -1].hu(new_card)
                next_zimo = True
                self.target = 5
                self.card_out = new_card
                nextPlayer = self.curPlayer #下个玩家不变
                return self.getCurInfo(), next_zimo
            
            elif player_check == 'gang':
                self.card_out = new_card
                self.players[self.curPlayer -1].gang(new_card,self.left_cards,zimo = True)
                next_zimo = True
                nextPlayer = self.curPlayer #下个玩家不变
                return self.getCurInfo(), next_zimo
            
            elif player_check == 'Clear' or player_check == 'peng':
                self.players[self.curPlayer -1].play_card(card_out)        
                nextPlayer,next_act = check(self.players,self.curPlayer ,card_out, zimo = zimo)
                self.curPlayer = nextPlayer
                self.card_out = card_out
                self.lastPlayer = copy.deepcopy(self.curPlayer)
            
                if next_act == 'hu':
                    self.players[nextPlayer -1].cards_hide.append(card_out)
                    self.players[nextPlayer -1].cards_count_hide[card_out] += 1
                    self.last_action = 'hu'
                    self.target = copy.deepcopy(self.curPlayer)
                    next_zimo = False
                    return self.getCurInfo(), next_zimo
                
                elif next_act == 'peng':
                    self.players[nextPlayer -1].cards_hide.append(card_out)
                    self.players[nextPlayer -1].cards_count_hide[card_out] += 1
                    self.last_action = 'peng'
                    next_zimo = False
                    return self.getCurInfo(), next_zimo
                
                elif next_act == 'gang':
                    self.players[nextPlayer -1].cards_hide.append(card_out)
                    self.players[nextPlayer -1].cards_count_hide[card_out] += 1
                    self.last_action = 'gang'
                    next_zimo = False
                    return self.getCurInfo(), next_zimo
                
                elif next_act == 'no_act':
                    self.last_action = 'get card'
                    next_zimo = True
                    return self.getCurInfo(), next_zimo
                
        elif self.last_action == None:#还没考虑天胡
            for card in self.players[self.curPlayer -1].cards_hide:
                if self.players[self.curPlayer -1].check(card,zimo) == 'gang':
                    self.last_action = 'gang'
                    next_zimo = True
                    nextPlayer = self.curPlayer
                    self.card_out = card
                    self.players[self.curPlayer -1].cards_hide.append(card)
                    self.players[self.curPlayer -1].cards_count_hide[card] += 1
                    return self.getCurInfo(), next_zimo
                    
            if self.last_action == None:
                self.players[self.curPlayer -1].play_card(card_out)        
                nextPlayer,next_act = check(self.players,self.curPlayer ,card_out, zimo = zimo)
                self.curPlayer = nextPlayer
                self.card_out = card_out
                self.lastPlayer = copy.deepcopy(self.curPlayer)
            
                if next_act == 'hu':
                    self.players[nextPlayer -1].cards_hide.append(card_out)
                    self.players[nextPlayer -1].cards_count_hide[card_out] += 1
                    self.last_action = 'hu'
                    self.target = copy.deepcopy(self.curPlayer)
                    next_zimo = False
                    return self.getCurInfo(), next_zimo
                
                elif next_act == 'peng':
                    self.players[nextPlayer -1].cards_hide.append(card_out)
                    self.players[nextPlayer -1].cards_count_hide[card_out] += 1
                    self.last_action = 'peng'
                    next_zimo = False
                    return self.getCurInfo(), next_zimo
                
                elif next_act == 'gang':
                    self.players[nextPlayer -1].cards_hide.append(card_out)
                    self.players[nextPlayer -1].cards_count_hide[card_out] += 1
                    self.last_action = 'gang'
                    next_zimo = False
                    return self.getCurInfo(), next_zimo
                
                elif next_act == 'no_act':
                    self.last_action = 'get card'
                    next_zimo = True
                    return self.getCurInfo(), next_zimo
         
        elif self.last_action == 'do peng':
            self.players[self.curPlayer -1].play_card(card_out)        
            nextPlayer,next_act = check(self.players,self.curPlayer ,card_out, zimo = zimo)
            self.curPlayer = nextPlayer
            self.card_out = card_out
            self.lastPlayer = copy.deepcopy(self.curPlayer)
            
            if next_act == 'hu':
                self.players[nextPlayer -1].cards_hide.append(card_out)
                self.players[nextPlayer -1].cards_count_hide[card_out] += 1
                self.last_action = 'hu'
                self.target = copy.deepcopy(self.curPlayer)
                next_zimo = False
                return self.getCurInfo(), next_zimo
                
            elif next_act == 'peng':
                self.players[nextPlayer -1].cards_hide.append(card_out)
                self.players[nextPlayer -1].cards_count_hide[card_out] += 1
                self.last_action = 'peng'
                next_zimo = False
                return self.getCurInfo(), next_zimo
                
            elif next_act == 'gang':
                self.players[nextPlayer -1].cards_hide.append(card_out)
                self.players[nextPlayer -1].cards_count_hide[card_out] += 1
                self.last_action = 'gang'
                next_zimo = False
                return self.getCurInfo(), next_zimo
                
            elif next_act == 'no_act':
                new_card = self.left_cards.pop(0)
                self.players[nextPlayer -1].get_card(new_card)  
                self.last_action = 'get card'
                next_zimo = True
                return self.getCurInfo(), next_zimo
        
        
        
  
        print ('有没有考虑到的state分支')
        print (self.last_action)
        print (player_check)
        #print (nextPlayer)
        print (next_act)
        print (card_out)