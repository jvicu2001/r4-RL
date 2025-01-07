from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GameInfo(_message.Message):
    __slots__ = ("car_info", "track_info")
    class CarInfo(_message.Message):
        __slots__ = ("x_pos", "y_pos", "z_pos", "applied_direction", "intended_direction", "speed", "rpm", "gear", "gear_timeout", "accel_lifted_timer", "collided", "traction_loss_fl", "traction_loss_fr", "traction_loss_rl", "traction_loss_rr", "wrong_way", "free_fall", "drift_timeout", "bbox_vx1", "bbox_vy1", "bbox_vz1", "bbox_vx2", "bbox_vy2", "bbox_vz2", "bbox_vx3", "bbox_vy3", "bbox_vz3", "bbox_vx4", "bbox_vy4", "bbox_vz4")
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
        COLLIDED_FIELD_NUMBER: _ClassVar[int]
        TRACTION_LOSS_FL_FIELD_NUMBER: _ClassVar[int]
        TRACTION_LOSS_FR_FIELD_NUMBER: _ClassVar[int]
        TRACTION_LOSS_RL_FIELD_NUMBER: _ClassVar[int]
        TRACTION_LOSS_RR_FIELD_NUMBER: _ClassVar[int]
        WRONG_WAY_FIELD_NUMBER: _ClassVar[int]
        FREE_FALL_FIELD_NUMBER: _ClassVar[int]
        DRIFT_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
        BBOX_VX1_FIELD_NUMBER: _ClassVar[int]
        BBOX_VY1_FIELD_NUMBER: _ClassVar[int]
        BBOX_VZ1_FIELD_NUMBER: _ClassVar[int]
        BBOX_VX2_FIELD_NUMBER: _ClassVar[int]
        BBOX_VY2_FIELD_NUMBER: _ClassVar[int]
        BBOX_VZ2_FIELD_NUMBER: _ClassVar[int]
        BBOX_VX3_FIELD_NUMBER: _ClassVar[int]
        BBOX_VY3_FIELD_NUMBER: _ClassVar[int]
        BBOX_VZ3_FIELD_NUMBER: _ClassVar[int]
        BBOX_VX4_FIELD_NUMBER: _ClassVar[int]
        BBOX_VY4_FIELD_NUMBER: _ClassVar[int]
        BBOX_VZ4_FIELD_NUMBER: _ClassVar[int]
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
        collided: bool
        traction_loss_fl: bool
        traction_loss_fr: bool
        traction_loss_rl: bool
        traction_loss_rr: bool
        wrong_way: bool
        free_fall: bool
        drift_timeout: int
        bbox_vx1: int
        bbox_vy1: int
        bbox_vz1: int
        bbox_vx2: int
        bbox_vy2: int
        bbox_vz2: int
        bbox_vx3: int
        bbox_vy3: int
        bbox_vz3: int
        bbox_vx4: int
        bbox_vy4: int
        bbox_vz4: int
        def __init__(self, x_pos: _Optional[int] = ..., y_pos: _Optional[int] = ..., z_pos: _Optional[int] = ..., applied_direction: _Optional[int] = ..., intended_direction: _Optional[int] = ..., speed: _Optional[int] = ..., rpm: _Optional[int] = ..., gear: _Optional[int] = ..., gear_timeout: _Optional[int] = ..., accel_lifted_timer: _Optional[int] = ..., collided: bool = ..., traction_loss_fl: bool = ..., traction_loss_fr: bool = ..., traction_loss_rl: bool = ..., traction_loss_rr: bool = ..., wrong_way: bool = ..., free_fall: bool = ..., drift_timeout: _Optional[int] = ..., bbox_vx1: _Optional[int] = ..., bbox_vy1: _Optional[int] = ..., bbox_vz1: _Optional[int] = ..., bbox_vx2: _Optional[int] = ..., bbox_vy2: _Optional[int] = ..., bbox_vz2: _Optional[int] = ..., bbox_vx3: _Optional[int] = ..., bbox_vy3: _Optional[int] = ..., bbox_vz3: _Optional[int] = ..., bbox_vx4: _Optional[int] = ..., bbox_vy4: _Optional[int] = ..., bbox_vz4: _Optional[int] = ...) -> None: ...
    class TrackInfo(_message.Message):
        __slots__ = ("track_id", "track_status", "lap_progress", "track_progress", "lap", "current_waypoint")
        TRACK_ID_FIELD_NUMBER: _ClassVar[int]
        TRACK_STATUS_FIELD_NUMBER: _ClassVar[int]
        LAP_PROGRESS_FIELD_NUMBER: _ClassVar[int]
        TRACK_PROGRESS_FIELD_NUMBER: _ClassVar[int]
        LAP_FIELD_NUMBER: _ClassVar[int]
        CURRENT_WAYPOINT_FIELD_NUMBER: _ClassVar[int]
        track_id: int
        track_status: int
        lap_progress: int
        track_progress: int
        lap: int
        current_waypoint: int
        def __init__(self, track_id: _Optional[int] = ..., track_status: _Optional[int] = ..., lap_progress: _Optional[int] = ..., track_progress: _Optional[int] = ..., lap: _Optional[int] = ..., current_waypoint: _Optional[int] = ...) -> None: ...
    CAR_INFO_FIELD_NUMBER: _ClassVar[int]
    TRACK_INFO_FIELD_NUMBER: _ClassVar[int]
    car_info: GameInfo.CarInfo
    track_info: GameInfo.TrackInfo
    def __init__(self, car_info: _Optional[_Union[GameInfo.CarInfo, _Mapping]] = ..., track_info: _Optional[_Union[GameInfo.TrackInfo, _Mapping]] = ...) -> None: ...

class ModelOutput(_message.Message):
    __slots__ = ("action", "model_info", "train_flags")
    class Action(_message.Message):
        __slots__ = ("accelerate", "brake", "steer_left", "steer_right")
        ACCELERATE_FIELD_NUMBER: _ClassVar[int]
        BRAKE_FIELD_NUMBER: _ClassVar[int]
        STEER_LEFT_FIELD_NUMBER: _ClassVar[int]
        STEER_RIGHT_FIELD_NUMBER: _ClassVar[int]
        accelerate: bool
        brake: bool
        steer_left: bool
        steer_right: bool
        def __init__(self, accelerate: bool = ..., brake: bool = ..., steer_left: bool = ..., steer_right: bool = ...) -> None: ...
    class ModelInfo(_message.Message):
        __slots__ = ("generation", "species", "genome", "fitness", "step")
        GENERATION_FIELD_NUMBER: _ClassVar[int]
        SPECIES_FIELD_NUMBER: _ClassVar[int]
        GENOME_FIELD_NUMBER: _ClassVar[int]
        FITNESS_FIELD_NUMBER: _ClassVar[int]
        STEP_FIELD_NUMBER: _ClassVar[int]
        generation: int
        species: int
        genome: int
        fitness: int
        step: int
        def __init__(self, generation: _Optional[int] = ..., species: _Optional[int] = ..., genome: _Optional[int] = ..., fitness: _Optional[int] = ..., step: _Optional[int] = ...) -> None: ...
    class TrainFlags(_message.Message):
        __slots__ = ("reset",)
        RESET_FIELD_NUMBER: _ClassVar[int]
        reset: bool
        def __init__(self, reset: bool = ...) -> None: ...
    ACTION_FIELD_NUMBER: _ClassVar[int]
    MODEL_INFO_FIELD_NUMBER: _ClassVar[int]
    TRAIN_FLAGS_FIELD_NUMBER: _ClassVar[int]
    action: ModelOutput.Action
    model_info: ModelOutput.ModelInfo
    train_flags: ModelOutput.TrainFlags
    def __init__(self, action: _Optional[_Union[ModelOutput.Action, _Mapping]] = ..., model_info: _Optional[_Union[ModelOutput.ModelInfo, _Mapping]] = ..., train_flags: _Optional[_Union[ModelOutput.TrainFlags, _Mapping]] = ...) -> None: ...
