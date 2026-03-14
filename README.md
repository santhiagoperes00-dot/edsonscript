-- ============================================================
-- EDSON MODZ V8 - ULTIMATE RAINBOW EDITION (FIXED)
-- DESIGN ULTRA-PROFISSIONAL | SKELETON ESP | AIMBOT UNIVERSAL
-- 100% PERSONALIZADO POR EDSON | RAINBOW EFFECTS REAL
-- ============================================================

-- Carregar Base Estável (Sirius)
local EDSON_LIB = loadstring(game:HttpGet('https://sirius.menu/rayfield'))()

-- Configurações Globais
local Config = {
    AimEnabled = false,
    TeamCheck = false,
    VisibleCheck = true,
    SelectedPart = "Head",
    Smoothness = 4,
    Prediction = 0.12,
    FOVSize = 150,
    FOVVisible = true,
    
    ESPEnabled = false,
    BoxEnabled = true,
    SkeletonEnabled = true,
    NameEnabled = true,
    HealthEnabled = true,
    LineEnabled = true,
    LinePos = "Bottom",
    
    WalkSpeed = 16,
    SpeedEnabled = false,
    NoclipEnabled = false
}

-- Criar Janela Principal Totalmente Personalizada
local Window = EDSON_LIB:CreateWindow({
    Name = "EDSON MODZ V8",
    LoadingTitle = "EDSON MODZ V8",
    LoadingSubtitle = "by EDSON",
    ShowText = "EDSON", 
    ConfigurationSaving = {
        Enabled = true,
        FolderName = "EdsonModz",
        FileName = "ConfigV8"
    },
    Discord = {
        Enabled = false,
        Invite = "noinvitelink",
        RememberJoins = true
    },
    KeySystem = false
})

-- SISTEMA DE PERSONALIZAÇÃO ÚNICO (SEM LOOP DE ABERTURA)
task.spawn(function()
    local CoreGui = game:GetService("CoreGui")
    local Players = game:GetService("Players")
    local LocalPlayer = Players.LocalPlayer
    
    -- Aguardar o carregamento da UI
    task.wait(2)
    
    local MainUI = CoreGui:FindFirstChild("Rayfield") or CoreGui:FindFirstChild("EDSON")
    if MainUI then
        MainUI.Name = "EDSON"
        
        -- Efeito Rainbow Estável
        task.spawn(function()
            while task.wait() do
                pcall(function()
                    local hue = tick() % 5 / 5
                    local rainbowColor = Color3.fromHSV(hue, 1, 1)
                    
                    -- 1. Título Principal
                    local Title = MainUI:FindFirstChild("Main", true):FindFirstChild("Title", true)
                    if Title and Title:IsA("TextLabel") then
                        Title.Text = "EDSON MODZ V8"
                        Title.TextColor3 = rainbowColor
                    end
                    
                    -- 2. Botão "EDSON" (Mobile)
                    local ShowButton = MainUI:FindFirstChild("Open", true) or MainUI:FindFirstChild("Show", true)
                    if ShowButton and ShowButton:FindFirstChildOfClass("TextLabel") then
                        local label = ShowButton:FindFirstChildOfClass("TextLabel")
                        label.Text = "EDSON"
                        label.TextColor3 = rainbowColor
                    end
                    
                    -- 3. Varredura de Textos (Remover "Rayfield UI" e aplicar Rainbow no "EDSON")
                    for _, textLabel in pairs(MainUI:GetDescendants()) do
                        if textLabel:IsA("TextLabel") then
                            -- Substituir qualquer menção a Rayfield UI ou Configuration Rayfield por EDSON
                            if textLabel.Text:find("Rayfield UI") or textLabel.Text:find("Rayfield") or textLabel.Text:find("Configuration") then
                                textLabel.Text = textLabel.Text:gsub("Rayfield UI", "EDSON"):gsub("Rayfield", "EDSON"):gsub("Configuration", "EDSON CONFIG")
                            end
                            
                            -- Aplicar Rainbow se o texto for EDSON
                            if textLabel.Text:find("EDSON") then
                                textLabel.TextColor3 = rainbowColor
                            end
                        end
                    end
                end)
            end
        end)
    end
end)

-- ============================================================
-- BOTÕES FLUTUANTES (ESTILO SWITCH VERMELHO)
-- ============================================================

local function CreateFloatingSwitch(name, flag, positionY, callback)
    local CoreGui = game:GetService("CoreGui")
    local screenGui = CoreGui:FindFirstChild("EDSON_SWITCHES") or Instance.new("ScreenGui", CoreGui)
    screenGui.Name = "EDSON_SWITCHES"
    
    local frame = Instance.new("Frame", screenGui)
    frame.Size = UDim2.new(0, 120, 0, 50)
    frame.Position = UDim2.new(0.5, positionY, 0, 10)
    frame.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
    frame.BorderSizePixel = 2
    frame.BorderColor3 = Color3.fromRGB(200, 0, 0)
    
    local corner = Instance.new("UICorner", frame)
    corner.CornerRadius = UDim.new(0, 8)
    
    local label = Instance.new("TextLabel", frame)
    label.Size = UDim2.new(1, 0, 0.5, 0)
    label.BackgroundTransparency = 1
    label.Text = name
    label.TextColor3 = Color3.new(1, 1, 1)
    label.Font = Enum.Font.GothamBold
    label.TextSize = 12
    
    local switch = Instance.new("TextButton", frame)
    switch.Size = UDim2.new(0, 50, 0, 20)
    switch.Position = UDim2.new(0.5, -25, 0.6, 0)
    switch.BackgroundColor3 = Color3.fromRGB(50, 50, 50)
    switch.Text = ""
    switch.AutoButtonColor = false
    
    local switchCorner = Instance.new("UICorner", switch)
    switchCorner.CornerRadius = UDim.new(1, 0)
    
    local knob = Instance.new("Frame", switch)
    knob.Size = UDim2.new(0, 18, 0, 18)
    knob.Position = UDim2.new(0, 1, 0.5, -9)
    knob.BackgroundColor3 = Color3.new(1, 1, 1)
    
    local knobCorner = Instance.new("UICorner", knob)
    knobCorner.CornerRadius = UDim.new(1, 0)
    
    local enabled = false
    switch.MouseButton1Click:Connect(function()
        enabled = not enabled
        if enabled then
            switch.BackgroundColor3 = Color3.fromRGB(200, 0, 0)
            knob:TweenPosition(UDim2.new(1, -19, 0.5, -9), "Out", "Quad", 0.2)
        else
            switch.BackgroundColor3 = Color3.fromRGB(50, 50, 50)
            knob:TweenPosition(UDim2.new(0, 1, 0.5, -9), "Out", "Quad", 0.2)
        end
        callback(enabled)
    end)
    
    -- Efeito Rainbow no Nome do Botão
    task.spawn(function()
        while task.wait() do
            local hue = tick() % 5 / 5
            label.TextColor3 = Color3.fromHSV(hue, 1, 1)
        end
    end)
    
    -- Tornar Arrastável
    local dragging, dragInput, dragStart, startPos
    frame.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
            dragging = true
            dragStart = input.Position
            startPos = frame.Position
            input.Changed:Connect(function()
                if input.UserInputState == Enum.UserInputState.End then
                    dragging = false
                end
            end)
        end
    end)
    frame.InputChanged:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseMovement or input.UserInputType.Touch then
            dragInput = input
        end
    end)
    game:GetService("UserInputService").InputChanged:Connect(function(input)
        if input == dragInput and dragging then
            local delta = input.Position - dragStart
            frame.Position = UDim2.new(startPos.X.Scale, startPos.X.Offset + delta.X, startPos.Y.Scale, startPos.Y.Offset + delta.Y)
        end
    end)
end

-- Criar Botões Flutuantes
CreateFloatingSwitch("EDSON SPEED", "SpeedEnabled", -130, function(v) Config.SpeedEnabled = v end)
CreateFloatingSwitch("EDSON NOCLIP", "NoclipEnabled", 10, function(v) Config.NoclipEnabled = v end)

-- Abas
local AimTab = Window:CreateTab("AIMBOT", "target")
local VisualTab = Window:CreateTab("VISUAL", "eye")
local MiscTab = Window:CreateTab("MISC", "settings")

-- Seção Aimbot
AimTab:CreateSection("Combate de Elite - EDSON")

AimTab:CreateToggle({
    Name = "Ativar Aimbot (EDSON)",
    CurrentValue = false,
    Flag = "AimEnabled",
    Callback = function(Value)
        Config.AimEnabled = Value
    end,
})

AimTab:CreateToggle({
    Name = "Team Check",
    CurrentValue = false,
    Flag = "TeamCheck",
    Callback = function(Value)
        Config.TeamCheck = Value
    end,
})

AimTab:CreateToggle({
    Name = "Wall Check",
    CurrentValue = true,
    Flag = "VisibleCheck",
    Callback = function(Value)
        Config.VisibleCheck = Value
    end,
})

AimTab:CreateDropdown({
    Name = "Parte do Alvo",
    Options = {"Head", "HumanoidRootPart", "UpperTorso"},
    CurrentOption = {"Head"},
    MultipleOptions = false,
    Flag = "TargetPart",
    Callback = function(Option)
        Config.SelectedPart = Option[1]
    end,
})

AimTab:CreateSlider({
    Name = "Suavidade (Smoothness)",
    Range = {1, 20},
    Increment = 1,
    Suffix = "x",
    CurrentValue = 4,
    Flag = "Smoothness",
    Callback = function(Value)
        Config.Smoothness = Value
    end,
})

AimTab:CreateSlider({
    Name = "Tamanho do FOV",
    Range = {10, 600},
    Increment = 10,
    Suffix = "px",
    CurrentValue = 150,
    Flag = "FOVSize",
    Callback = function(Value)
        Config.FOVSize = Value
    end,
})

AimTab:CreateToggle({
    Name = "Mostrar FOV",
    CurrentValue = true,
    Flag = "FOVVisible",
    Callback = function(Value)
        Config.FOVVisible = Value
    end,
})

-- Seção Visual
VisualTab:CreateSection("Visão Avançada - EDSON")

VisualTab:CreateToggle({
    Name = "Ativar ESP",
    CurrentValue = false,
    Flag = "ESPEnabled",
    Callback = function(Value)
        Config.ESPEnabled = Value
    end,
})

VisualTab:CreateToggle({
    Name = "Box ESP",
    CurrentValue = true,
    Flag = "BoxEnabled",
    Callback = function(Value)
        Config.BoxEnabled = Value
    end,
})

VisualTab:CreateToggle({
    Name = "Skeleton ESP",
    CurrentValue = true,
    Flag = "SkeletonEnabled",
    Callback = function(Value)
        Config.SkeletonEnabled = Value
    end,
})

VisualTab:CreateToggle({
    Name = "Nome ESP (Branco)",
    CurrentValue = true,
    Flag = "NameEnabled",
    Callback = function(Value)
        Config.NameEnabled = Value
    end,
})

VisualTab:CreateToggle({
    Name = "Vida ESP",
    CurrentValue = true,
    Flag = "HealthEnabled",
    Callback = function(Value)
        Config.HealthEnabled = Value
    end,
})

VisualTab:CreateToggle({
    Name = "Linha ESP (Tracers)",
    CurrentValue = true,
    Flag = "LineEnabled",
    Callback = function(Value)
        Config.LineEnabled = Value
    end,
})

VisualTab:CreateDropdown({
    Name = "Posição da Linha",
    Options = {"Bottom", "Middle", "Top"},
    CurrentOption = {"Bottom"},
    MultipleOptions = false,
    Flag = "LinePos",
    Callback = function(Option)
        Config.LinePos = Option[1]
    end,
})

-- Seção Misc
MiscTab:CreateSection("Outras Funções - EDSON")

MiscTab:CreateSlider({
    Name = "Velocidade",
    Range = {16, 300},
    Increment = 1,
    Suffix = "ws",
    CurrentValue = 16,
    Flag = "WalkSpeed",
    Callback = function(Value)
        Config.WalkSpeed = Value
    end,
})

-- ============================================================
-- LÓGICA DE AIMBOT, ESP E MOVIMENTAÇÃO
-- ============================================================

local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")
local Camera = workspace.CurrentCamera

-- FOV Circle
local FOV_Circle = Drawing.new("Circle")
FOV_Circle.Thickness = 1.5
FOV_Circle.NumSides = 64
FOV_Circle.Color = Color3.fromRGB(130, 50, 255)
FOV_Circle.Filled = false

local function IsVisible(part, char)
    local parts = Camera:GetPartsObscuringTarget({part.Position}, {game:GetService("Players").LocalPlayer.Character, char})
    return #parts == 0
end

local function GetClosest()
    local closest, dist = nil, Config.FOVSize
    for _, p in ipairs(game:GetService("Players"):GetPlayers()) do
        if p ~= game:GetService("Players").LocalPlayer and (not Config.TeamCheck or p.Team ~= game:GetService("Players").LocalPlayer.Team) then
            local char = p.Character
            if char and char:FindFirstChild(Config.SelectedPart) and char:FindFirstChild("Humanoid") and char.Humanoid.Health > 0 then
                local part = char[Config.SelectedPart]
                local screenPos, onScreen = Camera:WorldToViewportPoint(part.Position)
                if onScreen then
                    local mag = (Vector2.new(Camera.ViewportSize.X/2, Camera.ViewportSize.Y/2) - Vector2.new(screenPos.X, screenPos.Y)).Magnitude
                    if mag < dist then
                        if not Config.VisibleCheck or IsVisible(part, char) then
                            dist = mag; closest = p
                        end
                    end
                end
            end
        end
    end
    return closest
end

local ESPs = {}
local function createESP(p)
    pcall(function()
        ESPs[p] = {
            Box = {Drawing.new("Line"), Drawing.new("Line"), Drawing.new("Line"), Drawing.new("Line")},
            Skeleton = {},
            Name = Drawing.new("Text"),
            Health = Drawing.new("Square"),
            HealthBar = Drawing.new("Square"),
            Line = Drawing.new("Line")
        }
        ESPs[p].Name.Size = 14; ESPs[p].Name.Center = true; ESPs[p].Name.Outline = true; ESPs[p].Name.Color = Color3.new(1,1,1)
        ESPs[p].Line.Thickness = 1; ESPs[p].Line.Color = Color3.new(1,1,1)
        for _, v in pairs(ESPs[p].Box) do v.Thickness = 1; v.Color = Color3.new(1,1,1); v.Visible = false end
        ESPs[p].Health.Filled = true; ESPs[p].Health.Color = Color3.new(0,0,0); ESPs[p].Health.Transparency = 0.5
        ESPs[p].HealthBar.Filled = true; ESPs[p].HealthBar.Color = Color3.fromRGB(46, 204, 113)
        for i=1, 10 do
            local line = Drawing.new("Line"); line.Thickness = 1.5; line.Color = Color3.new(1,1,1); line.Visible = false
            table.insert(ESPs[p].Skeleton, line)
        end
    end)
end

RunService.RenderStepped:Connect(function()
    local center = Vector2.new(Camera.ViewportSize.X/2, Camera.ViewportSize.Y/2)
    local localPlayer = game:GetService("Players").LocalPlayer
    local char = localPlayer.Character
    
    -- Atualizar FOV
    FOV_Circle.Position = center
    FOV_Circle.Radius = Config.FOVSize
    FOV_Circle.Visible = Config.AimEnabled and Config.FOVVisible

    -- Lógica Aimbot
    if Config.AimEnabled and (UserInputService:IsMouseButtonPressed(Enum.UserInputType.MouseButton2) or UserInputService:IsMouseButtonPressed(Enum.UserInputType.Touch)) then
        local target = GetClosest()
        if target then
            local part = target.Character[Config.SelectedPart]
            local pos = Camera:WorldToViewportPoint(part.Position + (part.Velocity * Config.Prediction))
            mousemoverel((pos.X - center.X)/Config.Smoothness, (pos.Y - center.Y)/Config.Smoothness)
        end
    end

    -- Lógica ESP
    for p, esp in pairs(ESPs) do
        local pChar = p.Character
        if Config.ESPEnabled and pChar and pChar:FindFirstChild("HumanoidRootPart") and pChar.Humanoid.Health > 0 then
            local rootPart = pChar.HumanoidRootPart
            local pos, onScreen = Camera:WorldToViewportPoint(rootPart.Position)
            if onScreen then
                local h = math.abs(Camera:WorldToViewportPoint(pChar.Head.Position + Vector3.new(0, 0.5, 0)).Y - Camera:WorldToViewportPoint(rootPart.Position - Vector3.new(0, 3, 0)).Y)
                local w = h * 0.6
                
                local visible = IsVisible(rootPart, pChar)
                local espColor = visible and Color3.fromRGB(0, 255, 0) or Color3.fromRGB(255, 0, 0)
                
                if Config.BoxEnabled then
                    local l, t = pos.X - w/2, pos.Y - h/2
                    esp.Box[1].Visible = true; esp.Box[1].From = Vector2.new(l, t); esp.Box[1].To = Vector2.new(l + w, t); esp.Box[1].Color = espColor
                    esp.Box[2].Visible = true; esp.Box[2].From = Vector2.new(l, t + h); esp.Box[2].To = Vector2.new(l + w, t + h); esp.Box[2].Color = espColor
                    esp.Box[3].Visible = true; esp.Box[3].From = Vector2.new(l, t); esp.Box[3].To = Vector2.new(l, t + h); esp.Box[3].Color = espColor
                    esp.Box[4].Visible = true; esp.Box[4].From = Vector2.new(l + w, t); esp.Box[4].To = Vector2.new(l + w, t + h); esp.Box[4].Color = espColor
                else for _, v in pairs(esp.Box) do v.Visible = false end end
                
                if Config.NameEnabled then 
                    esp.Name.Visible = true; esp.Name.Position = Vector2.new(pos.X, pos.Y - h/2 - 15); esp.Name.Text = p.Name 
                else esp.Name.Visible = false end
                
                if Config.HealthEnabled then
                    local bh = h * (pChar.Humanoid.Health/pChar.Humanoid.MaxHealth)
                    esp.Health.Visible = true; esp.Health.Position = Vector2.new(pos.X - w/2 - 6, pos.Y - h/2); esp.Health.Size = Vector2.new(4, h)
                    esp.HealthBar.Visible = true; esp.HealthBar.Position = Vector2.new(pos.X - w/2 - 6, pos.Y + h/2 - bh); esp.HealthBar.Size = Vector2.new(4, bh)
                    esp.HealthBar.Color = Color3.fromHSV(pChar.Humanoid.Health/pChar.Humanoid.MaxHealth * 0.3, 1, 1)
                else esp.Health.Visible = false; esp.HealthBar.Visible = false end
                
                if Config.LineEnabled then 
                    local fromPos = center
                    if Config.LinePos == "Bottom" then fromPos = Vector2.new(Camera.ViewportSize.X/2, Camera.ViewportSize.Y)
                    elseif Config.LinePos == "Top" then fromPos = Vector2.new(Camera.ViewportSize.X/2, 0) end
                    esp.Line.Visible = true; esp.Line.From = fromPos; esp.Line.To = Vector2.new(pos.X, pos.Y + h/2); esp.Line.Color = espColor
                else esp.Line.Visible = false end
                
                if Config.SkeletonEnabled then
                    local pParts = {pChar:FindFirstChild("Head"), pChar:FindFirstChild("UpperTorso") or pChar:FindFirstChild("Torso"), pChar:FindFirstChild("LowerTorso") or pChar:FindFirstChild("Torso"), pChar:FindFirstChild("LeftUpperArm") or pChar:FindFirstChild("Left Arm"), pChar:FindFirstChild("LeftLowerArm") or pChar:FindFirstChild("Left Arm"), pChar:FindFirstChild("RightUpperArm") or pChar:FindFirstChild("Right Arm"), pChar:FindFirstChild("RightLowerArm") or pChar:FindFirstChild("Right Arm"), pChar:FindFirstChild("LeftUpperLeg") or pChar:FindFirstChild("Left Leg"), pChar:FindFirstChild("LeftLowerLeg") or pChar:FindFirstChild("Left Leg"), pChar:FindFirstChild("RightUpperLeg") or pChar:FindFirstChild("Right Leg"), pChar:FindFirstChild("RightLowerLeg") or pChar:FindFirstChild("Right Leg")}
                    local connections = {{1,2}, {2,3}, {2,4}, {4,5}, {2,6}, {6,7}, {3,8}, {8,9}, {3,10}, {10,11}}
                    for i, conn in ipairs(connections) do
                        local p1, p2 = pParts[conn[1]], pParts[conn[2]]
                        if p1 and p2 then
                            local v1, o1 = Camera:WorldToViewportPoint(p1.Position); local v2, o2 = Camera:WorldToViewportPoint(p2.Position)
                            if o1 and o2 then esp.Skeleton[i].Visible = true; esp.Skeleton[i].From = Vector2.new(v1.X, v1.Y); esp.Skeleton[i].To = Vector2.new(v2.X, v2.Y); esp.Skeleton[i].Color = espColor else esp.Skeleton[i].Visible = false end
                        else esp.Skeleton[i].Visible = false end
                    end
                else for _, v in pairs(esp.Skeleton) do v.Visible = false end end
            else 
                for _, v in pairs(esp) do if type(v) == "table" then for _, x in pairs(v) do x.Visible = false end else v.Visible = false end end 
            end
        else 
            for _, v in pairs(esp) do if type(v) == "table" then for _, x in pairs(v) do x.Visible = false end else v.Visible = false end end 
        end
    end
    
    -- Speed Hack
    if Config.SpeedEnabled and char and char:FindFirstChild("Humanoid") then 
        char.Humanoid.WalkSpeed = Config.WalkSpeed 
    end
    
    -- Noclip (Atravessar Paredes)
    if Config.NoclipEnabled and char then
        for _, v in pairs(char:GetDescendants()) do
            if v:IsA("BasePart") then
                v.CanCollide = false
            end
        end
    end
end)

game:GetService("Players").PlayerAdded:Connect(createESP)
for _, p in ipairs(game:GetService("Players"):GetPlayers()) do if p ~= game:GetService("Players").LocalPlayer then createESP(p) end end

EDSON_LIB:Notify({
    Title = "EDSON MODZ V8",
    Content = "Bem-vindo, EDSON! Tudo carregado e personalizado.",
    Duration = 5,
    Image = "check-circle",
})
