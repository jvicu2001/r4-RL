from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TrackPoint(_message.Message):
    __slots__ = ("track_id", "x_pos", "y_pos", "z_pos", "lap_progress", "center_distance", "side", "car_angle")
    TRACK_ID_FIELD_NUMBER: _ClassVar[int]
    X_POS_FIELD_NUMBER: _ClassVar[int]
    Y_POS_FIELD_NUMBER: _ClassVar[int]
    Z_POS_FIELD_NUMBER: _ClassVar[int]
    LAP_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    CENTER_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    CAR_ANGLE_FIELD_NUMBER: _ClassVar[int]
    track_id: int
    x_pos: int
    y_pos: int
    z_pos: int
    lap_progress: int
    center_distance: int
    side: int
    car_angle: int
    def __init__(self, track_id: _Optional[int] = ..., x_pos: _Optional[int] = ..., y_pos: _Optional[int] = ..., z_pos: _Optional[int] = ..., lap_progress: _Optional[int] = ..., center_distance: _Optional[int] = ..., side: _Optional[int] = ..., car_angle: _Optional[int] = ...) -> None: ...
