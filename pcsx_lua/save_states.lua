local savestate_name = ""

function SaveStateDialog()
    local shoow = imgui.Begin("Save State", true)
    changed, savestate_name = imgui.extra.InputText("Save State Name", savestate_name)
    if imgui.Button("Save State") then
        local savestate = PCSX.createSaveState()
        local file = Support.File.open("savestates/"..savestate_name..".slice", "TRUNCATE")
        file:writeMoveSlice(savestate)
        file:close()
    end
    if imgui.Button("Load State") then
        local file = Support.File.open("savestates/"..savestate_name..".slice", "READ")
        PCSX.loadSaveState(file)
        file:close()
    end
    imgui.End()
end