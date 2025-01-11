local function reload()
    PCSX.pauseEmulator()
    loadfile("pcsx_lua/r4_save_files.lua")()
end

local initial_sector = 0
local size = 0
local filename = ""


function SaveDataFrame()
    local show = imgui.Begin("Save R4.BIN Files", true)
    if not show then imgui.End() return end

    if (imgui.Button("Reload")) then
      reload()
    end

    imgui.Separator()

    if (imgui.Button("Save R4.BIN")) then
        local iso = PCSX.getCurrentIso()

        local data = iso:createReader():open("R4.BIN;1")
        
        local new_file = Support.File.open(
            "extracted/R4.BIN", 
            "CREATE")

        new_file:write(data:read(data:size()))
        new_file:close()
        data:close()
    end

    imgui.Separator()

    -- Replace with TextWrapped once available
    imgui.TextUnformatted('Use the printed "CdRead Invoked" sector value \nand the first "CdPosToInt Invoked" final_sector value after the "CdRead" \non console here.')

    _, initial_sector = imgui.InputInt("Initial sector", initial_sector, 1, 100, "%d")

    _, size = imgui.InputInt("Size in sectors", size, 1, 10, "%d")

    _, filename = imgui.extra.InputText("Filename", filename)

    if imgui.Button("Save") then
        local iso = PCSX.getCurrentIso()

        local data = iso:createReader():open("R4.BIN;1")

        -- 412 is the R4.BIN sector offset on USA image, obtained experimentally
        local start_offset = initial_sector-412

        local new_file = Support.File.open(
            string.format("extracted/%d-%d_%s.dmp", initial_sector, initial_sector+size-1, filename), 
            "CREATE")
        new_file:write(data:readAt(size*2048, start_offset*2048))
        new_file:close()
        data:close()
    end
    imgui.End()
end

if not (lfs.attributes("./extracted", "mode") == "directory") then
    lfs.mkdir("extracted")
end

PCSX.resumeEmulator()
pprint("SaveData module loaded")