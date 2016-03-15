#! /usr/env/bin python3

from abc import ABCMeta, abstractmethod


class ClientBase:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def setup_game(self, initial_state):
        raise NotImplementedError

    @abstractmethod
    def update(self, state):
        raise NotImplementedError
