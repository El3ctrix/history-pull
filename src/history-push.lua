-- To run this line of code is necessary lua5.1
-- lua5.1 history-pull.lua 
local socket = require("socket")

-- Bind to local host and 5555 port
local server = assert(socket.bind("5555",0))

--[[
while 1 do
    local client = server:accept()
    client:settimeout(10)

    local line, err = client:receive()
    if not err then client:send(line .. "\n") end
    client:close()
end
--]]
local client = server:accept()
print("Conenction established")
client:settimeout(10)

local line, err = client:receive()
if not err then client:send("Done!\n") end
print(line .. "\n")
client:close()
