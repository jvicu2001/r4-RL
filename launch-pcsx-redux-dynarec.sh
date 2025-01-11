pcsx_path=$(<pcsx_path.txt)
game_path=$(<game_path.txt)

$pcsx_path "--dynarec" "--loadiso" "$game_path" "--run" &