#! /usr/env/bin python3

import ClientBase


class LocalClient(ClientBase.ClientBase):
    def __init__(self):
        super(LocalNetworkBroker, self).__init__()

    def setup_game(self, initial_state):
        print 'Player registered to gameserver'

    def update(self, state):
        return state
