@ECHO OFF

SET /p pcsx-redux-path=<"%~dp0pcsx_path.txt"
SET /p r4-path=<"%~dp0game_path.txt"

START "" "%pcsx-redux-path%" "--interpreter" "--loadiso" "%r4-path%" "--run"