#! /usr/bin/python
# -*- coding: utf-8 -*-

import kivy
kivy.require('1.8.0')

import random
from collections import deque
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class Card():
    type = ''
    name = ''

    def __init__(self, _type='CIT', _name='Cidade'):
        self.type = _type
        self.name = _name

    def show_card(self, _prefix=''):
        return str(_prefix) + self.type + ' ' + self.name

    def card_color(self):
        if self.type == 'EVT':
            ret_color = (0.0, 0.0, 1.0, 1.0)
        elif self.type == 'EPD':
            ret_color = (0.0, 1.0, 0.0, 1.0)
        elif self.type == 'MUT':
            ret_color = (1.0, 0.0, 1.0, 1.0)
        else:
            ret_color = (1.0, 1.0, 1.0, 1.0)
        return ret_color


class Event(Card):

    def __init__(self):
        self.type = 'EVT'
        self.name = "Event card"


class Epidemic(Card):

    def __init__(self):
        self.type = "EPD"
        self.name = "Epidemic"


class Mutation(Card):

    def __init__(self):
        self.type = "MUT"
        self.name = "Mutation card"


class NullCard(Card):

    def __init__(self):
        self.type = "NUL"
        self.name = "Fim de jogo"


class Deck():
    num_of_cit = 0
    num_of_evt = 0
    num_of_mut = 0
    num_of_epd = 0
    group_cards = False
    deck = deque([])

    def add_cards(self, _card, _num_of_cards):
        for i in range(1, _num_of_cards + 1):
            self.deck.append(_card)

    def new_deck(self, _cit, _evt, _mut, _epd, _group_cards=False):
        self.num_of_cit = _cit
        self.num_of_evt = _evt
        self.num_of_mut = _mut
        self.num_of_epd = _epd
        self.group_cards = _group_cards
        self.deck = deque([])
        new_card = Card()
        self.add_cards(new_card, self.num_of_cit)
        new_card = Event()
        self.add_cards(new_card, self.num_of_evt)
        self.shuffle_deck()

    def insert_epidemic(self):
        if self.num_of_mut > 0:
            new_card = Mutation()
            self.add_cards(new_card, self.num_of_mut)
            self.shuffle_deck()
        new_deck = []
        epd_card = Epidemic()
        new_blocks = [list(self.deck)[i::self.num_of_epd] for i in range(self.num_of_epd)]
        for i in range(len(new_blocks)):
            new_block = new_blocks[i]
            new_block.append(epd_card)
            random.shuffle(new_block)
            new_deck.extend(new_block)
        self.deck = deque(new_deck)

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def draw_card(self):
        if len(self.deck) > 0:
            pop_card = self.deck.popleft()
            if pop_card.type == "EVT":
                self.num_of_evt -= 1
                if self.group_cards:
                    pop_card = Card()
            elif pop_card.type == "EPD":
                self.num_of_epd -= 1
            elif pop_card.type == "MUT":
                self.num_of_mut -= 1
            else:
                self.num_of_cit -= 1
            return pop_card
        else:
            return NullCard()

    def remain_cards(self):
        return len(self.deck) 

class PandemicWidget(BoxLayout):
    game_deck = Deck()
    new_game = True
    contagem = 0
    num_of_ply = 0
    turn_num = 0

    def start_count(self):
        cit = int(self.ids.num_cit.text)
        epd = int(self.ids.num_epd.text)
        evt = int(self.ids.num_evt.text)
        mut = int(self.ids.num_mut.text)
        grp = self.ids.check_group.active
        self.game_deck.new_deck(cit, evt, mut, epd, grp)
        self.num_of_ply = int(self.ids.num_ply.text)
        self.turn_num = 1
        self.ids.title.text = 'Novo jogo'
        self.ids.card01.text = ' '
        self.ids.card02.text = ' '
        self.new_game = True

    def add_count(self):
        self.contagem += 1
        self.update_widget()

    def update_widget(self):
        if self.num_of_ply >= self.turn_num:
            self.ids.title.text = 'Jogador: ' + str(self.turn_num)
        else:
            self.ids.title.text = 'Turno: ' + str(self.turn_num - self.num_of_ply)
        new_card = self.game_deck.draw_card()
        self.ids.card01.text = new_card.show_card(str(self.game_deck.remain_cards()) + ' - ')
        self.ids.card01.color = new_card.card_color()
        new_card = self.game_deck.draw_card()
        self.ids.card02.text = new_card.show_card(str(self.game_deck.remain_cards()) + ' - ')
        self.ids.card02.color = new_card.card_color()
        self.turn_num += 1
        if self.new_game and self.turn_num > self.num_of_ply:
            self.game_deck.insert_epidemic()
            self.new_game = False


class PandemicApp(App):
    def build(self):
        return PandemicWidget()


if __name__ == "__main__":
    PandemicApp().run()
