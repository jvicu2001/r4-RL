from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CarInfo(_message.Message):
    __slots__ = ("x_pos", "y_pos", "z_pos", "applied_direction", "intended_direction", "speed", "rpm", "gear")
    X_POS_FIELD_NUMBER: _ClassVar[int]
    Y_POS_FIELD_NUMBER: _ClassVar[int]
    Z_POS_FIELD_NUMBER: _ClassVar[int]
    APPLIED_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    INTENDED_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    RPM_FIELD_NUMBER: _ClassVar[int]
    GEAR_FIELD_NUMBER: _ClassVar[int]
    x_pos: int
    y_pos: int
    z_pos: int
    applied_direction: int
    intended_direction: int
    speed: int
    rpm: int
    gear: int
    def __init__(self, x_pos: _Optional[int] = ..., y_pos: _Optional[int] = ..., z_pos: _Optional[int] = ..., applied_direction: _Optional[int] = ..., intended_direction: _Optional[int] = ..., speed: _Optional[int] = ..., rpm: _Optional[int] = ..., gear: _Optional[int] = ...) -> None: ...
