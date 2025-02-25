# from __future__ import annotations
from trebelge.XMLFileTypeState.AbstractXMLFileTypeState import AbstractXMLFileTypeState


class XMLFileTypeStateContext:
    """
    The Context defines the interface of interest to clients. It also maintains
    a reference to an instance of a State subclass, which represents the current
    state of the Context.
    """
    _file_path: str = ''
    _state: AbstractXMLFileTypeState = None
    """
    A reference to the current state of the Context.
    """

    def set_state(self, state: AbstractXMLFileTypeState):
        """
        The Context allows changing the State object at runtime.
        """
        self._state = state
        self._state.set_context(self)

    def set_file_path(self, file_path: str):
        self._file_path = file_path

    def get_file_path(self):
        return self._file_path

    """
    The Context delegates part of its behavior to the current State object.
    """

    def find_record_status(self):
        self._state.find_record_status()

    def initiate_new_record(self):
        self._state.initiate_new_record()
