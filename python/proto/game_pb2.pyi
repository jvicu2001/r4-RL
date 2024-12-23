from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GameInfo(_message.Message):
    __slots__ = ("car_info", "track_info")
    class CarInfo(_message.Message):
        __slots__ = ("x_pos", "y_pos", "z_pos", "applied_direction", "intended_direction", "speed", "rpm", "gear", "gear_timeout", "accel_lifted_timer", "lap_progress", "track_progress", "collided", "traction_loss_fl", "traction_loss_fr", "traction_loss_rl", "traction_loss_rr", "wrong_way", "free_fall", "drift_timeout")
        X_POS_FIELD_NUMBER: _ClassVar[int]
        Y_POS_FIELD_NUMBER: _ClassVar[int]
        Z_POS_FIELD_NUMBER: _ClassVar[int]
        APPLIED_DIRECTION_FIELD_NUMBER: _ClassVar[int]
        INTENDED_DIRECTION_FIELD_NUMBER: _ClassVar[int]
        SPEED_FIELD_NUMBER: _ClassVar[int]
        RPM_FIELD_NUMBER: _ClassVar[int]
        GEAR_FIELD_NUMBER: _ClassVar[int]
        GEAR_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
        ACCEL_LIFTED_TIMER_FIELD_NUMBER: _ClassVar[int]
        LAP_PROGRESS_FIELD_NUMBER: _ClassVar[int]
        TRACK_PROGRESS_FIELD_NUMBER: _ClassVar[int]
        COLLIDED_FIELD_NUMBER: _ClassVar[int]
        TRACTION_LOSS_FL_FIELD_NUMBER: _ClassVar[int]
        TRACTION_LOSS_FR_FIELD_NUMBER: _ClassVar[int]
        TRACTION_LOSS_RL_FIELD_NUMBER: _ClassVar[int]
        TRACTION_LOSS_RR_FIELD_NUMBER: _ClassVar[int]
        WRONG_WAY_FIELD_NUMBER: _ClassVar[int]
        FREE_FALL_FIELD_NUMBER: _ClassVar[int]
        DRIFT_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
        x_pos: int
        y_pos: int
        z_pos: int
        applied_direction: int
        intended_direction: int
        speed: int
        rpm: int
        gear: int
        gear_timeout: int
        accel_lifted_timer: int
        lap_progress: int
        track_progress: int
        collided: bool
        traction_loss_fl: bool
        traction_loss_fr: bool
        traction_loss_rl: bool
        traction_loss_rr: bool
        wrong_way: bool
        free_fall: bool
        drift_timeout: int
        def __init__(self, x_pos: _Optional[int] = ..., y_pos: _Optional[int] = ..., z_pos: _Optional[int] = ..., applied_direction: _Optional[int] = ..., intended_direction: _Optional[int] = ..., speed: _Optional[int] = ..., rpm: _Optional[int] = ..., gear: _Optional[int] = ..., gear_timeout: _Optional[int] = ..., accel_lifted_timer: _Optional[int] = ..., lap_progress: _Optional[int] = ..., track_progress: _Optional[int] = ..., collided: bool = ..., traction_loss_fl: bool = ..., traction_loss_fr: bool = ..., traction_loss_rl: bool = ..., traction_loss_rr: bool = ..., wrong_way: bool = ..., free_fall: bool = ..., drift_timeout: _Optional[int] = ...) -> None: ...
    class TrackInfo(_message.Message):
        __slots__ = ("track_id", "track_status")
        TRACK_ID_FIELD_NUMBER: _ClassVar[int]
        TRACK_STATUS_FIELD_NUMBER: _ClassVar[int]
        track_id: int
        track_status: int
        def __init__(self, track_id: _Optional[int] = ..., track_status: _Optional[int] = ...) -> None: ...
    CAR_INFO_FIELD_NUMBER: _ClassVar[int]
    TRACK_INFO_FIELD_NUMBER: _ClassVar[int]
    car_info: GameInfo.CarInfo
    track_info: GameInfo.TrackInfo
    def __init__(self, car_info: _Optional[_Union[GameInfo.CarInfo, _Mapping]] = ..., track_info: _Optional[_Union[GameInfo.TrackInfo, _Mapping]] = ...) -> None: ...
