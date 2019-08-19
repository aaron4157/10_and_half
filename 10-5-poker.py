# -*- coding: utf-8 -*-
import random

class Card(object):
    """定義一張牌
    固有花色(suit)與點數(face)
    屬性不能更改
    """
    def __init__(self, suit, face):
        self._suit = suit
        self._face = face

    @property
    def face(self):
        return self._face
    @property
    def suit(self):
        return self._suit

    def __str__(self):
        #this is for printing
        #以字串型態呼叫類別，以這個顯示
        if self._face == 1:
            Face_str_ = 'A'
        elif self._face == 11:
            Face_str_ = 'J'
        elif self._face == 12:
            Face_str_ = 'Q'
        elif self._face == 13:
            Face_str_ = 'K'
        else:
            Face_str_ = self._face
        return "%s%s" % (self._suit, Face_str_)

    def __repr__(self):
        #this is for programming
        #以其它型態呼叫類別，以這個顯示
        return self.__str__()

class Deck(object):
    """定義牌組
    是一個卡片(物件)序列、包含洗牌+發牌+狀態方法
    依賴Card類別
    相當於莊家(dealer)的角色
    """

    def __init__(self):
        #list of cards
        self._cards = [Card(suit, face)
                        #若遊戲需要3副牌、反註解這一行
                        #for _ in range(3)
                        #♠=spade, ♡=heart, ♢=diamond, ♣=club
                        for suit in '♠♡♢♣'
                        #face:1~13, range+1
                        for face in range(1, 14)]
        #list index
        self._current = 0

    @property
    def Cards(self):
        return self._cards

    def shuffle(self):
        #refresh index
        self._current = 0
        #shuffle array
        random.shuffle(self._cards)

    @property
    def deal(self):
        """ 發牌:deal 或distribute
        """
        item = self._cards[self._current]
        #remember referring self
        self._current += 1
        return item

    @property
    def has_card(self):
        return self._current < len(self._cards)

class Player(object):
    """參與者稱為閒家"""

    def __init__(self, name):
        self._name = name
        #玩家稱呼
        self._hands = []
        #玩家手牌

    @property
    def name(self):
        return self._name
    @property
    def hands(self):
        return self._hands

    def draw(self, Card):
        """摸牌方法需要Deck中deal的回傳值，屬於Card類別
        draw([Deck].deal)
        """
        self._hands.append(Card)

    def sort(self, card_key):
        """根據點數大小理牌；預設是大點數放後面(升序ascending)
        [player].sort(card_key)
        """
        self._hands.sort(key = card_key)

def card_key(Card):
    """點數的定義必須是方法，排序根據回傳值、依序進行
    """
    return (Card.suit, Card.face)

def main():
    #天字第一號牌桌
    No001 = Deck()
    No001.shuffle()
    #發牌測試
    #print(No001.deal)

    #三位"十點半"玩家+一位荷官(dealer; croupier)放在最後一位
    #中文字串不須格式化%r可直接顯示
    heros = [Player("歐陽鋒"), Player("段智興"), Player("洪七公"), Player("黃藥師")]

    def points(hands):
        """需要玩家的手牌序列計算點數
        points([Player].hands)
        """
        count = 0.0
        for card in hands:
            if card.face < 11:
                count += float(card.face)
            else:
                count += 0.5
        return count

    """十點半規則:閒家與莊家輪流抽牌，比誰先爆牌；或者，抽完5張，比點數。
    預設玩家儘量加牌，而且爆牌後遊戲結束。
    """
    _j = 0
    while _j < 5:
        #因為要使用計數，所以不使用一般的遍歷法數數
        #除非另外設定變數 t 進行追蹤
        t = 0
        for member in heros:
            member.draw(No001.deal)
            #draw firstly, then check points
            if points(member.hands) < 10.5:
                t += 1
            else:
                #爆煲(busted)或是達成十點半，計算輸贏
                #跳出外迴圈之前會+1
                _j = 7
                #跳出內迴圈
                break
        _j += 1



    #大部分情形：迴圈中斷，到此計算點數
    if _j == 8:
        if points(heros[t].hands) == 10.5:
            print(heros[t].name+' wins!!')
        else:
            print(heros[t].name+' lose!!')
    else:
        #迴圈正常結束
        will = randint(1, 10)
        if will <= 5:
            #莊家結束牌局，判定"五龍"，莊家輸
            #若強制結束遊戲，不會發生"食夾棍"
            print('五龍! '+heros[-1].name+' the croupier loses!')
        else:
            #莊家繼續發牌，與閒家比點數
            print('Checking points...')


    #亮牌
    for member in heros:
        member.sort(card_key)
        print(member.name+' :')
        print(member.hands)
        print(points(member.hands))

if __name__ == '__main__':
    main()
