mem = PCSX.getMemPtr()

local printf = function(s,...)
  return pprint(s:format(...))
end

-- Read strings in memory byte by byte until a 0x00 is found.
local function readStringFromMem(address)
  local out_string = ""
  local current_address = address

  local read_byte = readValue(mem, current_address, "uint8_t*")
  while read_byte ~= 0 do
    out_string = out_string .. string.char(read_byte)
    current_address = current_address + 1
    read_byte = readValue(mem, current_address, "uint8_t*")
  end

  return out_string
end

local function print_1()
  local regs = PCSX.getRegisters()
  local a0_s = readStringFromMem(regs.GPR.n.a0)

  -- Remove size modifier as it's not supported by Lua
  -- May cause wrong reads
  a0_s, _ = string.gsub(a0_s, "%%l", "%%")

  -- These should work for all but one print in R4, where there are
  -- 4 specifiers and I can't figure where are all the pointers.
  local param_register_list = {regs.GPR.n.a1, regs.GPR.n.a2, regs.GPR.n.a3}
  local params = {}
  local param_count = 0

  -- Match the specifiers and cast the parameter reads accordingly
  for w in string.gmatch(a0_s, "%%%d*([dxs])") do
    param_count = param_count + 1
    if (string.find(w, "[dx]") == 1) then
      params[param_count] = readValue(mem, param_register_list[param_count], "uint32_t*")
    else
      params[param_count] = readStringFromMem(param_register_list[param_count])
    end
  end

  printf(a0_s, table.unpack(params))
end

r4_printf_bp = PCSX.addBreakpoint(0x8001e844, 'Exec', 4, "Print", function(address, width, cause)
  local success, msg = pcall(function()
    print_1()
  end)
  if not success then
      print('Error while running Lua breakpoint callback: ' .. msg)
  end
end)

r4_print_bp = PCSX.addBreakpoint(0x800965b8, 'Exec', 4, "Print", function(address, width, cause)
  pprint(readStringFromMem(PCSX.getRegisters().GPR.n.a0))
end)

r4_CdRead_log = PCSX.addBreakpoint(0x8008f0d0, 'Exec', 4, "CdRead", function(address, width, cause)
  local regs = PCSX.getRegisters().GPR.n
  pprint(string.format("CdRead Invoked: sectors: %d, buf: 0x%x, mode:0x%x", regs.a0, regs.a1, regs.a2))
end)

r4_CdSearchFile_log = PCSX.addBreakpoint(0x8008e060, 'Exec', 4, "CdSearchFile", function(address, width, cause)
  local regs = PCSX.getRegisters().GPR.n
  local ra = regs.ra
  pprint("CdSearchFile Invoked")

  -- local CdSearchFileReturn = PCSX.addBreakpoint(ra, 'Exec', 4, "CdSearchFile_Return", function(address, width, cause)
  --   pprint(string.format("CdSearchFile result: 0x%x", regs.v0))
  -- end)

end)

r4_CdPosToInt_log = PCSX.addBreakpoint(0x8008c880, 'Exec', 4, "CdPosToInt", function(address, width, cause)
  local a0 = PCSX.getRegisters().GPR.n.a0

  -- For some reason these numbers are in hex but shown as dec
  -- 0-9 is used and a-f is skipped
  local minutes = tonumber(string.format("%x", readValue(mem, a0, "uint8_t*")))
  local seconds = tonumber(string.format("%x", readValue(mem, a0 + 0x1, "uint8_t*")))
  local sector = tonumber(string.format("%x", readValue(mem, a0 + 0x2, "uint8_t*")))
  local track = tonumber(string.format("%x", readValue(mem, a0 + 0x3, "uint8_t*")))

  local final_sector = (minutes*60*75) + (seconds * 75) + sector - 75

  local s_out = string.format("CdPosToInt Invoked: minute: %d, second: %d, sector: %d, track: %d, final_sector: %d", minutes, seconds, sector, track, final_sector)
  pprint(s_out)
end)