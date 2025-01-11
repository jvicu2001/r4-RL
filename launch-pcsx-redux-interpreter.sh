pcsx_path=$(<pcsx_path.txt)
game_path=$(<game_path.txt)

$pcsx_path "--interpreter" "--loadiso" "$game_path" "--run" &