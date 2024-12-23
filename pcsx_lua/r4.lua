pprint("R4 Info script loaded sucessfully")
PCSX.pauseEmulator()

loadfile("pcsx_lua/memory.lua")()
loadfile("pcsx_lua/map_capture.lua")()
loadfile("pcsx_lua/send_car_data.lua")()

local function reload()
  PCSX.pauseEmulator()
  loadfile("pcsx_lua/r4.lua")()
end




mem = PCSX.getMemPtr()
function carInfo()
  if (imgui.CollapsingHeader("Car", ImGuiTreeNodeFlags_None)) then
    -- Car data
    doSliderInt(mem, 0x800ac100, "Car Pitch", -100, 100, "int16_t*")            -- Car pitch, Forward/Backward inclination
    doSliderInt(mem, 0x800ac104, "Car Applied Direction", 0, 4096, "uint16_t*") -- Car's applied forward angle. Smoothly interpolates to 0x800ac340 when manually changed
    doSliderInt(mem, 0x800ac340, "Car Intended Direction", 0, 4096, "uint16_t*")-- Car's real forward angle where the car wants to go. Snaps to appplied direction after drift


    doSliderInt(mem, 0x800ac32a, "Current Gear", 0, 6, "uint16_t*")         -- Car's current engaged gear
    -- doSliderShort(mem, 0x800ac28d, "Current Gear", 0, 6)                 -- Clones 0x800ac23a

    doSliderInt(mem, 0x800f4e20, "Visible RPM", 0, 20000, "uint16_t*")      -- Car's current RPM, derived from somewhere else.
    doSliderInt(mem, 0x800ac32c, "RPM", 0, 20000, "uint16_t*")              -- Car's actual RPM, without lower-end jiggle
    
    doSliderInt(mem, 0x800ac288, "Applied Speed", -32768, 32767, "int16_t*")-- Car actual speed

    doSliderInt(mem, 0x800ac25e, "Car Tilt", -60, 60, "int16_t*")           -- Car visual tilt
  end
end

function carWorldInfo()
  if (imgui.CollapsingHeader("Car World info", ImGuiTreeNodeFlags_None)) then
    doSliderInt(mem, 0x801fff58, "Car Camera X Position", -40000, 40000, "int32_t*")    -- Car's Camera X Position


    doSliderInt(mem, 0x801fff5c, "Car Camera Y Position", -32768, 32767, "int16_t*")    -- Car's Camera Y Position, twitches when rear view mirror present.
    
    -- First set of car coordinates
    doSliderInt(mem, 0x800ac0c0, "Car Xa Position", -40000, 40000, "int32_t*")    -- Car's X position relative to the map.
    doSliderInt(mem, 0x800ac0c4, "Car Ya Position", -40000, 40000, "int32_t*")    -- Car's Y position relative to the map.
    doSliderInt(mem, 0x800ac0c8, "Car Za Position", -40000, 40000, "int32_t*")    -- Car's Z position relative to the map.

    -- Second set of car coordinates, These one's X and Z don't go into the negatives.
    doSliderInt(mem, 0x800ac0d0, "Car Xb Position", -40000, 40000, "int32_t*")    -- Car's X position relative to the map.
    doSliderInt(mem, 0x800ac0d4, "Car Yb Position", -40000, 40000, "int32_t*")    -- Car's Y position relative to the map.
    doSliderInt(mem, 0x800ac0d8, "Car Zb Position", -40000, 40000, "int32_t*")    -- Car's Z position relative to the map.
    -- doSliderInt(mem, 0x800ac128, "Car Z Position", -32768, 32767)       -- Car's Z position relative to the map. Goes blank after frame is rendered, then syncs from 0x800ac0c8
    -- doSliderInt(mem, 0x800ac180, "Car Z Position", -32768, 32767)       -- Car's Z position relative to the map. Only updates from 0x800ac0c8 when the screen updates

  end
end

function carWheelInfo()
  if (imgui.CollapsingHeader("Car Wheel info", ImGuiTreeNodeFlags_None)) then 
    imgui.BeginDisabled()
    
    imgui.BeginTable("Wheel traction", 2, imgui.constant.TableFlags.Resizable)

    -- Track OOBounds friction loss

    imgui.TableNextRow()
    imgui.TableSetColumnIndex(0)
    imgui.RadioButton("FL", readValue(mem, 0x800ac2a0, "uint8_t*")==1)
    imgui.TableSetColumnIndex(1)
    imgui.RadioButton("FR", readValue(mem, 0x800ac2a1, "uint8_t*")==1)
    imgui.TableNextRow()
    imgui.TableSetColumnIndex(0)
    imgui.RadioButton("RL", readValue(mem, 0x800ac2a2, "uint8_t*")==1)
    imgui.TableSetColumnIndex(1)
    imgui.RadioButton("RR", readValue(mem, 0x800ac2a3, "uint8_t*")==1)
    imgui.EndTable()

    imgui.EndDisabled()
  end
end

-- Check in what corner the car collided.
function carCollisionInfo()
  if (imgui.CollapsingHeader("Car Collision info", ImGuiTreeNodeFlags_None)) then 
    collisionValue = readValue(mem, 0x800ac250, "uint8_t*")
    collisionType = {"None", "FL", "FR", "RL", "RR"}

    imgui.BeginDisabled()
    imgui.BeginTable("Car Collision", 2, imgui.constant.TableFlags.Resizable)

    imgui.TableNextRow()
    imgui.TableSetColumnIndex(0)
    imgui.RadioButton("FL", collisionValue==1)
    imgui.TableSetColumnIndex(1)
    imgui.RadioButton("FR", collisionValue==2)
    imgui.TableNextRow()
    imgui.TableSetColumnIndex(0)
    imgui.RadioButton("RL", collisionValue==3)
    imgui.TableSetColumnIndex(1)
    imgui.RadioButton("RR", collisionValue==4)
    imgui.EndTable()

    imgui.EndDisabled()
  end
end


function trackInfo()
  if (imgui.CollapsingHeader("Track", ImGuiTreeNodeFlags_None)) then
    -- doSliderInt(mem, 0x800ac23c, "Track Progression", 0, 0x0fffffff, "uint32_t*")    -- Increments when the car goes forward. Decreases when the car goes the wrong way.
    -- doSliderInt(mem, 0x800ac240, "Track Progression (loops)", -32768, 32767) -- Clones 0x800ac23c mid-frame
    imgui.BeginDisabled()
    doSliderInt(mem, 0x800ac800, "Track ID", 0, 15, "uint8_t*") -- Track id, reversed track have different ids than normal tracks
    imgui.RadioButton("Wrong way", readValue(mem, 0x800ac29a, "uint8_t*")==1)
    imgui.EndDisabled()
    doSliderInt(mem, 0x800f684c, "Track Progression", -10000, 0x0fffffff, "int32_t*") -- Track progression for the whole race. Doesn't reset on new laps.

    doSliderInt(mem, 0x800ac35a, "Lap count", 0, 6, "uint16_t*")                            -- Shows current lap
    doSliderInt(mem, 0x800ac23c, "Lap time / TT Lap Progress", 0, 0x000fffff, "uint32_t*")  -- Shows current lap's time
    doSliderInt(mem, 0x800ac29e, "Current Position -1", 0, 7, "uint16_t*")                  -- Show car's current position

    doSliderInt(mem, 0x800ac222, "Distance from track center", -2000, 2000, "int16_t*")     -- Car distance from the center of the trackInfo
  end
end


function DrawImguiFrame()
  local show = imgui.Begin("R4", true)
  if not show then imgui.End() return end

  if (imgui.Button("Reload")) then
    reload()
  end

  -- Car info Table
  imgui.BeginTable("Car info", 2, imgui.constant.TableFlags.Resizable)
  imgui.TableNextRow()
  imgui.TableSetColumnIndex(0)
  carInfo()
  imgui.TableSetColumnIndex(1)
  carWorldInfo()

  imgui.BeginTable("Wheels", 2, imgui.constant.TableFlags.Resizable)
  imgui.TableNextRow()
  imgui.TableSetColumnIndex(0)
  carWheelInfo()
  imgui.TableSetColumnIndex(1)
  carCollisionInfo()
  imgui.EndTable()

  imgui.EndTable()


  -- Track info table
  imgui.BeginTable("Track info", 2, imgui.constant.TableFlags.Resizable)
  imgui.TableNextRow()
  imgui.TableSetColumnIndex(0)
  trackInfo()
  imgui.EndTable()

  -- Track capture table
  imgui.BeginTable("Data capture", 2, imgui.constant.TableFlags.Resizable)
  imgui.TableNextRow()
  imgui.TableSetColumnIndex(0)
  mapCapture()
  imgui.TableSetColumnIndex(1)
  sendCarData()
  imgui.EndTable()
  imgui.End()
end

PCSX.resumeEmulator()