# R4-RL
A project to make a AI agent race in Ridge Racer Type 4.

## Objective
To make an AI agent that can navigate, drive fast and potentially discover strategies and make lap records on Namco® R4: Ridge Racer Type 4™

## How to run
### Prerequisites
`raylib` and `python` must be installed in the system beforehand. Python 3.11 is recommended but newer versions should work.
A copy of PCSX-Redux is needed.
A copy of Ridge Racer Type 4 NTSC-U compatible with PCSX-Redux is required (not provided)

Enter the absolute paths of the PCSX-Redux emulator and the copy of Ridge Racer Type 4 on the `pcsx_path.txt` and `game_path.txt` files respectively.
These are used by the scripts on the root folder to launch the emulator correctly.

### Memory observers and file extractor (in PCSX-Redux)
When opening PCSX-Redux, the pcsx.lua file on the root directory should load automatically, loading the rest of the modules and showing various windows related to the project.

For the first time only, once you load the game in PCSX-Redux, extract the `R4.BIN` file pressing the "Save R4.BIN" button on the "Save R4.BIN Files" window.

### Track info extractor
After extracting the `R4.BIN` file, just run the script with `python extract_tracks.py` on the `python` folder.

### Map viewer
To launch the map viewer, run the

| Normal view | Debug view | 
 :------: | :-------: 
| ![](screenshots/map_viewer_base.png) | ![](screenshots/map_viewer_debug.png) |


#### Controls
- Mouse left click: Draw view.
- Mouse scrool wheel: Zoom in/out.
- Z: Chase car.
- X: Rotate camera with car while chasing.
- C: Toggle distance rays
- V: Toggle between polygon track drawing or line/debug drawing mode.
- B: Toggle drawing only the waypoints visible to the ray colliders


__DO NOT__ run the map viewer while training. They will collide and get the emulator stuck.

### Sector extractor
On PCSX-Redux, there will be a menu called "Save R4.BIN Files". In the Size in sectors field you have to enter the `sectors` number given by the "CdRead Invoked" print in console, and in the Initial sector field you have to enter the `final_sector` number given by the  first "CdPosToInt Invoked" print after the "CdRead" one. You can enter a custom filename.

The saved file will be named `{initial_sector}-{final_sector}_{filename}.dmp` in the `extracted/` folder.

![](screenshots/save_assets_values.png)

### Savestate save/load windows
The savestates that will be used by the RL controller have to be saved with the `Save State` window.

Enter Time Attack mode, choose one or many tracks (non-reverse tracks only, for now), choose a car (must be AT, try staying in a single speed class, and use only one driving class).
In the race, drive the car in various points of the track. Once you're in a particular place you want to test: 
- Pause the emulator (NOT the pause in-game) with F6
- Write an unique savestate name.
- Press the `Save State` button.

It's preferable that the savestates occur within the first lap.

### NEAT controller
First, start the NEAT-python program by running one of these scripts: `launch-neat.bat`(on Windows) or `launch-neat.sh` (on Linux).

While the python program waits for the emulator, start PCSX-Redux, and after the OpenBIOS screen turns green or you see the NAMCO logo, press the `Connect to training module` checkbox on the `Training` window. This will load a savestate and start the training session.

__NEEDS WORK__, genomes that make good progress can be marked as stagnant across savestate changes, consider implementing a custom Stagnation class. Hyperparameters in the `neat_config.ini` file need adjusting too. Also, it can't restore the training sessions saved on checkpoints yet (maybe a GUI for ease of selection?).

## TODO List
- Data collection
    - [x] Find and monitor relevant memory addresses to read
        - [ ] Finding competitor's data in memory could allow for the AI Agent to participate in Grand Prix mode
    - [x] Sample track walls
        - This will allow us to make a simpler model by not needing visual input later
- Wall distance detector
    - [X] Build a simulated enviroment to cast rays to the track walls previously collected.
- AI Agent
    - [x] Choose model (Probably NEAT)
    - [X] Connect the model to PCSX-Redux
        - [x] FIX sometimes the game gets stuck when the savestate is restored.
            - Made a workaround checking if the in-game counter hasn't been updated after 120 draw cycles. If so, load again.
    - [ ] Train and adjust hyperparameters
    - [ ] Draw the model's output to PCSX-Redux screen using NanoVG
        - [x] Provisional drawing with imgui window

# Credits
- Whitehole [@whiteh0le](https://github.com/whiteh0le) for providing the tracks' waypoint offsets and struct, as well as the cars' bounding box, enabling to use accurate track data for the simulation.
- [PCSX-Redux](https://github.com/grumpycoders/pcsx-redux/) for making an amazing emulator with the tools necessary for making this project a reality.