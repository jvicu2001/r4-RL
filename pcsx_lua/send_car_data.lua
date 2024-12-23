local pb = require "pb"
local protoc = require "protoc"

mem = PCSX.getMemPtr()

-- Load proto message
local p = protoc.new()
local protoSchemaFile = Support.File.open("proto/car.proto")
local protoSchemaSize = protoSchemaFile:size()
local protoSchemaBuffer = protoSchemaFile:read(protoSchemaSize)
local protoSchemaData = p:compile(tostring(protoSchemaBuffer))

protoSchemaFile:close()
pb.load(protoSchemaData)

udp_client = luv.new_udp({family="inet"})

last_frame = readValue(mem, 0x800ac064, "uint32_t*")

time_old = os.time()
packets_sent = 0

function sendCarData()
    if (imgui.CollapsingHeader("Car Capture", ImGuiTreeNodeFlags_None)) then
        toggledCapture, activeCapture = imgui.Checkbox("Capture car info", activeCapture)
        paused = readValue(mem, 0x800f4e18, "uint16_t*")

        if activeCapture and paused==0 then
            curr_frame = readValue(mem, 0x800ac064, "uint32_t*")
            if last_frame ~= curr_frame then    -- Enables us to send 30 packets per second
                last_frame=curr_frame
                -- pprint(curr_frame)
                local out_data = {}   -- If a new collision was detected this frame, capture data
                out_data["x_pos"] = readValue(mem, 0x800ac0d0, "int32_t*")
                out_data["y_pos"] = readValue(mem, 0x800ac0d4, "int32_t*")
                out_data["z_pos"] = readValue(mem, 0x800ac0d8, "int32_t*")
                out_data["applied_direction"] = readValue(mem, 0x800ac104, "uint16_t*")
                out_data["intended_direction"] = readValue(mem, 0x800ac340, "uint16_t*")

                out_data["speed"] = readValue(mem, 0x800ac288, "int16_t*")
                out_data["rpm"] = readValue(mem, 0x800ac32c, "uint16_t*")
                out_data["gear"] = readValue(mem, 0x800ac32a, "uint16_t*")

                local bytes = pb.encode("CarInfo", out_data)

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