-- Options
getgenv().autofarm = true
getgenv().serverhop = true -- for public servers

if not game:IsLoaded() then
    game.Loaded:wait()
end

local queueonteleport = (syn and syn.queue_on_teleport) or queue_on_teleport or (fluxus and fluxus.queue_on_teleport) or nil
if serverhop and queueonteleport then
    queueonteleport([[loadstring(game:HttpGetAsync('https://raw.githubusercontent.com/ImMejor35/Test-Script/main/shhhhh.py'))()]])
end

if not isfolder('Flooded Logs') then
    makefolder('Flooded Logs')
    writefile('Stats','')
end

local function log(wins, Time)
    if serverhop then
        appendfile('Stats',tostring(wins).."|"..tostring(Time).."\n")
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
    -- Wait till game start efficiently?
    for i = 1,3 do
        getThing(mode, 'info').Changed:wait()
    end
    -- Spam touch exit till it wins
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
            if getThing(mode, 'info').Value == "Game is Ready!" then
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
