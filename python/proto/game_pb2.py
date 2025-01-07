# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: game.proto
# Protobuf Python Version: 5.29.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    2,
    '',
    'game.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ngame.proto\"\xbe\x06\n\x08GameInfo\x12#\n\x08\x63\x61r_info\x18\x01 \x01(\x0b\x32\x11.GameInfo.CarInfo\x12\'\n\ntrack_info\x18\x02 \x01(\x0b\x32\x13.GameInfo.TrackInfo\x1a\xd8\x04\n\x07\x43\x61rInfo\x12\r\n\x05x_pos\x18\x01 \x01(\x05\x12\r\n\x05y_pos\x18\x02 \x01(\x05\x12\r\n\x05z_pos\x18\x03 \x01(\x05\x12\x19\n\x11\x61pplied_direction\x18\x04 \x01(\r\x12\x1a\n\x12intended_direction\x18\x05 \x01(\r\x12\r\n\x05speed\x18\x06 \x01(\x05\x12\x0b\n\x03rpm\x18\x07 \x01(\r\x12\x0c\n\x04gear\x18\x08 \x01(\r\x12\x14\n\x0cgear_timeout\x18\t \x01(\r\x12\x1a\n\x12\x61\x63\x63\x65l_lifted_timer\x18\n \x01(\r\x12\x10\n\x08\x63ollided\x18\r \x01(\x08\x12\x18\n\x10traction_loss_fl\x18\x0e \x01(\x08\x12\x18\n\x10traction_loss_fr\x18\x0f \x01(\x08\x12\x18\n\x10traction_loss_rl\x18\x10 \x01(\x08\x12\x18\n\x10traction_loss_rr\x18\x11 \x01(\x08\x12\x11\n\twrong_way\x18\x12 \x01(\x08\x12\x11\n\tfree_fall\x18\x13 \x01(\x08\x12\x15\n\rdrift_timeout\x18\x14 \x01(\r\x12\x10\n\x08\x62\x62ox_vx1\x18\x15 \x01(\x05\x12\x10\n\x08\x62\x62ox_vy1\x18\x16 \x01(\x05\x12\x10\n\x08\x62\x62ox_vz1\x18\x17 \x01(\x05\x12\x10\n\x08\x62\x62ox_vx2\x18\x18 \x01(\x05\x12\x10\n\x08\x62\x62ox_vy2\x18\x19 \x01(\x05\x12\x10\n\x08\x62\x62ox_vz2\x18\x1a \x01(\x05\x12\x10\n\x08\x62\x62ox_vx3\x18\x1b \x01(\x05\x12\x10\n\x08\x62\x62ox_vy3\x18\x1c \x01(\x05\x12\x10\n\x08\x62\x62ox_vz3\x18\x1d \x01(\x05\x12\x10\n\x08\x62\x62ox_vx4\x18\x1e \x01(\x05\x12\x10\n\x08\x62\x62ox_vy4\x18\x1f \x01(\x05\x12\x10\n\x08\x62\x62ox_vz4\x18  \x01(\x05\x1a\x88\x01\n\tTrackInfo\x12\x10\n\x08track_id\x18\x01 \x01(\r\x12\x14\n\x0ctrack_status\x18\x02 \x01(\r\x12\x14\n\x0clap_progress\x18\x03 \x01(\x05\x12\x16\n\x0etrack_progress\x18\x04 \x01(\x05\x12\x0b\n\x03lap\x18\x05 \x01(\r\x12\x18\n\x10\x63urrent_waypoint\x18\x06 \x01(\r\"\xe0\x02\n\x0bModelOutput\x12#\n\x06\x61\x63tion\x18\x01 \x01(\x0b\x32\x13.ModelOutput.Action\x12*\n\nmodel_info\x18\x02 \x01(\x0b\x32\x16.ModelOutput.ModelInfo\x12,\n\x0btrain_flags\x18\x03 \x01(\x0b\x32\x17.ModelOutput.TrainFlags\x1aT\n\x06\x41\x63tion\x12\x12\n\naccelerate\x18\x01 \x01(\x08\x12\r\n\x05\x62rake\x18\x02 \x01(\x08\x12\x12\n\nsteer_left\x18\x03 \x01(\x08\x12\x13\n\x0bsteer_right\x18\x04 \x01(\x08\x1a_\n\tModelInfo\x12\x12\n\ngeneration\x18\x01 \x01(\r\x12\x0f\n\x07species\x18\x02 \x01(\r\x12\x0e\n\x06genome\x18\x03 \x01(\r\x12\x0f\n\x07\x66itness\x18\x04 \x01(\x05\x12\x0c\n\x04step\x18\x05 \x01(\r\x1a\x1b\n\nTrainFlags\x12\r\n\x05reset\x18\x01 \x01(\x08\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'game_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_GAMEINFO']._serialized_start=15
  _globals['_GAMEINFO']._serialized_end=845
  _globals['_GAMEINFO_CARINFO']._serialized_start=106
  _globals['_GAMEINFO_CARINFO']._serialized_end=706
  _globals['_GAMEINFO_TRACKINFO']._serialized_start=709
  _globals['_GAMEINFO_TRACKINFO']._serialized_end=845
  _globals['_MODELOUTPUT']._serialized_start=848
  _globals['_MODELOUTPUT']._serialized_end=1200
  _globals['_MODELOUTPUT_ACTION']._serialized_start=990
  _globals['_MODELOUTPUT_ACTION']._serialized_end=1074
  _globals['_MODELOUTPUT_MODELINFO']._serialized_start=1076
  _globals['_MODELOUTPUT_MODELINFO']._serialized_end=1171
  _globals['_MODELOUTPUT_TRAINFLAGS']._serialized_start=1173
  _globals['_MODELOUTPUT_TRAINFLAGS']._serialized_end=1200
# @@protoc_insertion_point(module_scope)
