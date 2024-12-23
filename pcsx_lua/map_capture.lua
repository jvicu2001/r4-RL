local pb = require "pb"
local protoc = require "protoc"

mem = PCSX.getMemPtr()

local lastColl = nil
local currColl = nil

pprint("Map Capture module loaded")

-- Load proto message
local p = protoc.new()
local protoSchemaFile = Support.File.open("proto/track.proto")
local protoSchemaSize = protoSchemaFile:size()
local protoSchemaBuffer = protoSchemaFile:read(protoSchemaSize)
local protoSchemaData = p:compile(tostring(protoSchemaBuffer))

protoSchemaFile:close()
pb.load(protoSchemaData)

-- pprint(protoSchemaData)

udp_client = luv.new_udp({family="inet"})
-- luv.udp_bind(udp_client, "127.0.0.1", 7650)

function mapCapture()
    if (imgui.CollapsingHeader("Track capture", ImGuiTreeNodeFlags_None)) then
        toggledCaptureMap, activeCaptureMap = imgui.Checkbox("Capture track", activeCaptureMap)

        if activeCaptureMap then
            -- Check if a collision has happened in this frame
            lastColl = currColl
            currColl = readValue(mem, 0x800ac250, "uint8_t*")

            if (currColl > 0) and (lastColl == 0) then   -- If a new collision was detected this frame, capture data
                local out_data = {}
                out_data["track_id"] = readValue(mem, 0x800ac800, "uint8_t*")
                out_data["x_pos"] = readValue(mem, 0x800ac0d0, "int32_t*")
                out_data["y_pos"] = readValue(mem, 0x800ac0d4, "int32_t*")
                out_data["z_pos"] = readValue(mem, 0x800ac0d8, "int32_t*")
                out_data["lap_progress"] = readValue(mem, 0x800ac23c, "int32_t*")
                out_data["center_distance"] = readValue(mem, 0x800ac222, "int16_t*")
                wrong_way = readValue(mem, 0x800ac29a, "uint8_t*")==1
                right_side_collision = readValue(mem, 0x800ac250, "uint8_t*")==2
                if (right_side_collision) and (not wrong_way) then
                    out_data["side"] = 1
                else
                    out_data["side"] = 0
                end

                pprint("Collision detected")
                pprint(out_data)
                local bytes = pb.encode("TrackPoint", out_data)
                -- pprint(pb.tohex(bytes))

                luv.udp_send(udp_client, bytes, "127.0.0.1", 7650, function (err)
                    assert(not err, err)
                    pprint("Packet sent.")
                end)
            end
        end
    end
end