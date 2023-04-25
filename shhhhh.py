-- Options
getgenv().autofarm = true
getgenv().serverhop = true -- for public servers

if not game:IsLoaded() then
    game.Loaded:wait()
end
rconsoleclear()
local queueonteleport = (syn and syn.queue_on_teleport) or queue_on_teleport or (fluxus and fluxus.queue_on_teleport) or nil
if serverhop and queueonteleport then
    queueonteleport([[loadstring(game:HttpGetAsync('https://raw.githubusercontent.com/ImMejor35/Test-Script/main/shhhhh.py'))()]])
end

if not isfolder('Flooded Logs') then
    makefolder('Flooded Logs')
end
if not isfile('Flooded Logs/Stats.txt') then
    writefile('Stats.txt','0, ')
end
local function log(wins, Time)
    if serverhop then
        appendfile('Flooded Logs/Stats.txt',tostring(wins).."|"..tostring(Time).."\n")
    end
end

local gameModes = {"Easy", "Medium", "Hard"}
local winsGained = 0
local StartClock = os.clock()
log(winsGained, os.clock() - StartClock)

-- Constants
local LP = game:GetService("Players").LocalPlayer
local RunService = game:GetService("RunService")
local wait = task.wait

local function getThing(mode, thing)
    local mode = workspace[mode]
    local thing = thing:lower()
    if thing == "entry" then
        return mode.Entry.LiftEntry
    elseif thing == "info" then
        return mode.Info
    elseif thing == "exit" then
        return mode:WaitForChild('Main'):WaitForChild('Exit')
    end
end

local function getRoot()
    return (LP.Character or LP.CharacterAdded:Wait()) and LP.Character:WaitForChild("HumanoidRootPart")
end

local function touchPart(part)
    local root = getRoot()
    firetouchinterest(root, part, 0)
    firetouchinterest(root, part, 1)
end

local function playGame(mode)
    -- Enters Lift
    touchPart(getThing(mode, 'entry'))
    -- Wait until game start
    repeat
        wait()
    until LP.Ingame.Value == 1
    -- Spam touch exit until win
    repeat
        wait()
        touchPart(getThing(mode, 'exit'))
    until LP.Ingame.Value == 0
    winsGained += 1
    log(winsGained, os.clock() - StartClock)
end
local function serverhop()
    loadstring(game:HttpGetAsync('https://raw.githubusercontent.com/Morples/Server-hop/main/Script'))()
end
RunService.Heartbeat:Connect(function()
    if autofarm and LP.Ingame.Value == 0 and LP.Waiting.Value == 0 then
        for _, mode in ipairs(gameModes) do
            local infoval = getThing(mode, 'info').Value
            if infoval == "Game is Ready!" or infoval:lower():match('intermission') then
                playGame(mode)
                if not serverhop then
                    rconsoleprint("Gained", winsGained, "wins so far!")
                end
                break
            end
        end
        if serverhop then
            serverhop()
        end
    end
end)
