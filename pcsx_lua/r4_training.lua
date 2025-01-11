local pb = require "pb"
local protoc = require "protoc"

loadfile("pcsx_lua/memory.lua")()

mem = PCSX.getMemPtr()

TrainingPortSend = 7652
TrainingPortReceive = 7653

SaveStates = {}
CurrentSaveStateIndex = 1

function FetchSavestates()
    for name in lfs.dir("./savestates") do
        if name ~= "." and name ~= ".." then
            table.insert(SaveStates, name)
        end
    end
end

FetchSavestates()

local function selectNewSaveState()
    local SaveStatePoolSize = table.getn(SaveStates)

    -- Choose a random save state
    CurrentSaveStateIndex = math.random(1, SaveStatePoolSize)
end

selectNewSaveState()

-- Load proto message
local p = protoc.new()
local protoSchemaFile = Support.File.open("proto/game.proto")
local protoSchemaSize = protoSchemaFile:size()
local protoSchemaBuffer = protoSchemaFile:read(protoSchemaSize)
local protoSchemaData = p:compile(tostring(protoSchemaBuffer))

protoSchemaFile:close()
pb.load(protoSchemaData)

udp_train_client = luv.new_udp({family="inet"})
luv.udp_bind(udp_train_client, "127.0.0.1", TrainingPortReceive, {reuseaddr=true})

last_frame = readValue(mem, 0x800ac064, "uint32_t*")

local waiting_for_response = false

local function sendGameState()
    local car_info = {}
    local track_info = {}
    local game_info = {}

    -- Car Info
    car_info["x_pos"] = readValue(mem, 0x800ac0d0, "int32_t*")
    car_info["y_pos"] = readValue(mem, 0x800ac0d4, "int32_t*")
    car_info["z_pos"] = readValue(mem, 0x800ac0d8, "int32_t*")
    car_info["applied_direction"] = readValue(mem, 0x800ac104, "uint16_t*")
    car_info["intended_direction"] = readValue(mem, 0x800ac340, "uint16_t*")

    car_info["speed"] = readValue(mem, 0x800ac288, "int16_t*")
    car_info["rpm"] = readValue(mem, 0x800ac32c, "uint16_t*")
    car_info["gear"] = readValue(mem, 0x800ac32a, "uint8_t*")

    car_info["gear_timeout"] = readValue(mem, 0x800ac2dc, "uint8_t*")
    car_info["accel_lifted_timer"] = readValue(mem, 0x800ac2f8, "uint8_t*")

    car_info["collided"] = (readValue(mem, 0x800ac250, "uint8_t*") ~= 0)

    car_info["tracktion_loss_fl"] = (readValue(mem, 0x800ac2a0, "uint8_t*")==1)
    car_info["tracktion_loss_fr"] = (readValue(mem, 0x800ac2a1, "uint8_t*")==1)
    car_info["tracktion_loss_rl"] = (readValue(mem, 0x800ac2a2, "uint8_t*")==1)
    car_info["tracktion_loss_rr"] = (readValue(mem, 0x800ac2a3, "uint8_t*")==1)

    car_info["wrong_way"] = (readValue(mem, 0x800ac29a, "uint8_t*")==1)

    car_info["free_fall"] = (readValue(mem, 0x800ac269, "uint8_t*")==1)

    local drift_timeout = readValue(mem, 0x800ac2fc, "int32_t*")
    if readValue(mem, 0x800ac348, "uint8_t*") ~= 2 then
        drift_timeout = 0
    end
    car_info["drift_timeout"] = drift_timeout
    last_drift_timeout = drift_timeout

    ---- Bounding box
    car_info["bbox_vx1"] = readValue(mem, 0x800ac138, "int32_t*")
    car_info["bbox_vy1"] = readValue(mem, 0x800ac13c, "int32_t*")
    car_info["bbox_vz1"] = readValue(mem, 0x800ac140, "int32_t*")

    car_info["bbox_vx2"] = readValue(mem, 0x800ac148, "int32_t*")
    car_info["bbox_vy2"] = readValue(mem, 0x800ac14c, "int32_t*")
    car_info["bbox_vz2"] = readValue(mem, 0x800ac150, "int32_t*")

    car_info["bbox_vx3"] = readValue(mem, 0x800ac158, "int32_t*")
    car_info["bbox_vy3"] = readValue(mem, 0x800ac15c, "int32_t*")
    car_info["bbox_vz3"] = readValue(mem, 0x800ac160, "int32_t*")

    car_info["bbox_vx4"] = readValue(mem, 0x800ac168, "int32_t*")
    car_info["bbox_vy4"] = readValue(mem, 0x800ac16c, "int32_t*")
    car_info["bbox_vz4"] = readValue(mem, 0x800ac170, "int32_t*")

    -- Track Info
    track_info["track_id"] = readValue(mem, 0x800ac800, "uint8_t*")
    track_info["track_status"] = readValue(mem, 0x800ff860, "uint8_t*")

    track_info["lap_progress"] = readValue(mem, 0x800ac23c, "int32_t*")
    track_info["track_progress"] = readValue(mem, 0x800f684c, "int32_t*")

    track_info["lap"] = readValue(mem, 0x800ac35a, "uint16_t*")

    track_info["current_waypoint"] = readValue(mem, 0x800ac1a0, "uint16_t*")

    track_info["center_distance"] = readValue(mem, 0x800ac222, "int16_t*")

    -- Game Info
    game_info["car_info"] = car_info
    game_info["track_info"] = track_info


    local bytes = pb.encode("GameInfo", game_info)

    luv.udp_send(udp_train_client, bytes, "127.0.0.1", TrainingPortSend, function (err)
        assert(not err, err)
    end)
end

train_generation = 0
train_genome = 0
train_species = 0
train_fitness = 0
train_step = 0

current_actions = {}

function gameModelResponseCallback(err, data, addr)
    if data then

        pprint("Received data from training module.")
        waiting_for_response = false
        local modelResponse = pb.decode("ModelOutput", data)


        -- Reset session on genome change
        if modelResponse['train_flags']['reset'] then
            if modelResponse['train_flags']['change_savestate'] then
                selectNewSaveState()
            end
            local file = Support.File.open("savestates/"..SaveStates[CurrentSaveStateIndex], "READ")
            PCSX.loadSaveState(file)
            file:close()
            PCSX.resumeEmulator()
            pprint("Resetting session")
            return
        end

        local actions = modelResponse["action"]

        if actions["accelerate"] then
            PCSX.SIO0.slots[1].pads[1].setOverride(PCSX.CONSTS.PAD.BUTTON.CROSS)
        else
            PCSX.SIO0.slots[1].pads[1].clearOverride(PCSX.CONSTS.PAD.BUTTON.CROSS)
        end

        -- if actions["brake"] then
        --     PCSX.SIO0.slots[1].pads[1].setOverride(PCSX.CONSTS.PAD.BUTTON.SQUARE)
        -- else
        --     PCSX.SIO0.slots[1].pads[1].clearOverride(PCSX.CONSTS.PAD.BUTTON.SQUARE)
        -- end

        if actions["steer_left"] then
            PCSX.SIO0.slots[1].pads[1].setOverride(PCSX.CONSTS.PAD.BUTTON.LEFT)
        else
            PCSX.SIO0.slots[1].pads[1].clearOverride(PCSX.CONSTS.PAD.BUTTON.LEFT)
        end

        if actions["steer_right"] then
            PCSX.SIO0.slots[1].pads[1].setOverride(PCSX.CONSTS.PAD.BUTTON.RIGHT)
        else
            PCSX.SIO0.slots[1].pads[1].clearOverride(PCSX.CONSTS.PAD.BUTTON.RIGHT)
        end

        -- if actions["shift_up"] then
        --     PCSX.SIO0.slots[1].pads[1].setOverride(PCSX.CONSTS.PAD.BUTTON.R1)
        -- else
        --     PCSX.SIO0.slots[1].pads[1].clearOverride(PCSX.CONSTS.PAD.BUTTON.R1)
        -- end

        -- if actions["shift_down"] then
        --     PCSX.SIO0.slots[1].pads[1].setOverride(PCSX.CONSTS.PAD.BUTTON.L1)
        -- else
        --     PCSX.SIO0.slots[1].pads[1].clearOverride(PCSX.CONSTS.PAD.BUTTON.L1)
        -- end

        PCSX.resumeEmulator()

        -- Get current genome info
        train_generation = modelResponse['model_info']['generation']
        train_species = modelResponse['model_info']['species']
        train_genome = modelResponse['model_info']['genome']
        train_fitness = modelResponse['model_info']['fitness']
        train_step = modelResponse['model_info']['step']

        current_actions = actions
    end
end

local timeSinceLastSend = 0

function SendGameDataTraining()
    local show = imgui.Begin("Training", true)
    toggledCaptureTrain, activeCaptureTrain = imgui.Checkbox("Connect to training module", activeCaptureTrain)

    imgui.TextUnformatted("Generation: "..train_generation)
    imgui.TextUnformatted("Species: "..train_species)
    imgui.TextUnformatted("Genome: "..train_genome)
    imgui.TextUnformatted("Fitness: "..train_fitness)
    imgui.TextUnformatted("Step: "..train_step)
    if table.getn(SaveStates) > 0 then
        imgui.TextUnformatted("Save state: "..SaveStates[CurrentSaveStateIndex])
    else
        imgui.TextUnformatted("There are no savestates available.")
    end

    imgui.Separator()

    imgui.TextUnformatted("Model output")
    imgui.BeginDisabled()
    imgui.RadioButton("Accelerate", current_actions["accelerate"])
    -- imgui.RadioButton("Brake", current_actions["brake"])
    imgui.RadioButton("Steer left", current_actions["steer_left"])
    imgui.RadioButton("Steer right", current_actions["steer_right"])
    -- imgui.RadioButton("Shift up", current_actions["shift_up"])
    -- imgui.RadioButton("Shift down", current_actions["shift_down"])
    imgui.EndDisabled()

    if waiting_for_response then
        PCSX.pauseEmulator()
    else
        PCSX.resumeEmulator()
    end

    paused = readValue(mem, 0x800f4e18, "uint16_t*")

    if toggledCaptureTrain then
        if activeCaptureTrain then
            -- Send activation packet
            udp_wake_client = luv.new_udp({family="inet"})
            luv.udp_send(udp_wake_client, "ready", "127.0.0.1", 7650, function (err)
                assert(not err, err)
                luv.close(udp_wake_client)
            end)
        else
            waiting_for_response = false
            luv.udp_recv_stop(udp_train_client)
        end

    elseif activeCaptureTrain and paused==0 and waiting_for_response == false then
        curr_frame = readValue(mem, 0x800ac064, "uint32_t*")
        if last_frame ~= curr_frame then    -- Enables us to send 30 packets per second
            last_frame=curr_frame
            timeSinceLastSend = 0
            pprint("Sending game state" .. curr_frame)
            sendGameState()
            waiting_for_response = true
            luv.udp_recv_start(udp_train_client, gameModelResponseCallback)
        else
            timeSinceLastSend = timeSinceLastSend + 1

            -- If the game hasn't sent any data in 120 loops, reload savestate
            if timeSinceLastSend > 120 then
                local file = Support.File.open("savestates/"..SaveStates[CurrentSaveStateIndex], "READ")
                PCSX.loadSaveState(file)
                file:close()
                PCSX.resumeEmulator()
            end
        end
        pprint("Time since last send: "..timeSinceLastSend)
    end
    imgui.End()
end