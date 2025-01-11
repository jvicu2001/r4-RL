local savestate_name = ""

function SaveStateDialog()
    local show = imgui.Begin("Save State", true)
    changed, savestate_name = imgui.extra.InputText("Save State Name", savestate_name)
    if imgui.Button("Save State") then
        if not (lfs.attributes("./savestates", "mode") == "directory") then
            lfs.mkdir("savestates")
        end
        local savestate = PCSX.createSaveState()
        local file = Support.File.open("savestates/"..savestate_name..".slice", "TRUNCATE")
        file:writeMoveSlice(savestate)
        file:close()
        FetchSavestates()
    end
    if imgui.Button("Load State") then
        local file = Support.File.open("savestates/"..savestate_name..".slice", "READ")
        PCSX.loadSaveState(file)
        file:close()
    end
    imgui.End()
end

pprint("SaveStates Dialog loaded")