local env = {
    debug = {
        getinfo=debug.getinfo
    },
    bit32 = bit32
}

io.write([[
    
  __   __  _______  ______    __   __  ___   _  _______ 
 |  | |  ||   _   ||    _ |  |  | |  ||   | | ||   _   |
 |  |_|  ||  |_|  ||   | ||  |  | |  ||   |_| ||  |_|  |
 |       ||       ||   |_||_ |  |_|  ||      _||       |
 |       ||       ||    __  ||       ||     |_ |       |
 |   _   ||   _   ||   |  | ||       ||    _  ||   _   |
 |__| |__||__| |__||___|  |_||_______||___| |_||__| |__|

]])
io.write('> ')
io.flush()

local input = io.read()

local code = string.format([[
function check_flag(s)
    -- REDACTED
end

local result = ''
if check_flag('%s') then
    result = 'Correct!'
else
    result = 'Nope.'
end

return result
]], input)

io.write(code)

local src, err = load(code, nil, 't', env)
if not src then
    io.write('Error: ' .. err .. '\n')
else
    local output = {pcall(src)}
    if output[1] then
        io.write(output[2] .. '\n')
    else
        io.write('Error: ' .. output[2] .. '\n')
    end
end
io.flush()