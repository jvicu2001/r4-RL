local pb = require "pb"
local protoc = require "protoc"

mem = PCSX.getMemPtr()

-- Load proto message
local p = protoc.new()
local protoSchemaFile = Support.File.open("proto/game.proto")
local protoSchemaSize = protoSchemaFile:size()
local protoSchemaBuffer = protoSchemaFile:read(protoSchemaSize)
local protoSchemaData = p:compile(tostring(protoSchemaBuffer))

protoSchemaFile:close()
pb.load(protoSchemaData)

udp_client = luv.new_udp({family="inet"})

last_frame = readValue(mem, 0x800ac064, "uint32_t*")

time_old = os.time()
packets_sent = 0

local last_drift_timeout = 0

function sendGameData()
    if (imgui.CollapsingHeader("Game Capture", ImGuiTreeNodeFlags_None)) then
        toggledCaptureGame, activeCaptureGame = imgui.Checkbox("Capture Game info", activeCaptureGame)
        paused = readValue(mem, 0x800f4e18, "uint16_t*")

        if activeCaptureGame and paused==0 then
            curr_frame = readValue(mem, 0x800ac064, "uint32_t*")
            if last_frame ~= curr_frame then    -- Enables us to send 30 packets per second
                last_frame=curr_frame
                -- pprint(curr_frame)
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

                -- Game Info
                game_info["car_info"] = car_info
                game_info["track_info"] = track_info


                local bytes = pb.encode("GameInfo", game_info)

                luv.udp_send(udp_client, bytes, "127.0.0.1", 7651, function (err)
                    assert(not err, err)
                    -- pprint("Packet sent.")
                    -- packets_sent = packets_sent + 1
                end)

                -- time_new = os.time()
                -- if time_new ~= time_old then
                --     pprint("Packets sent last second: ", packets_sent)
                --     packets_sent = 0
                --     time_old = time_new
                -- end
                
            end
        end
    end
end