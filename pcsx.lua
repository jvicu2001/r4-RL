function loadScripts()
    loadfile("pcsx_lua/r4_prints.lua", "bt")()
    loadfile("pcsx_lua/r4_save_files.lua", "bt")()
    loadfile("pcsx_lua/r4.lua", "bt")()
end

loadScripts()