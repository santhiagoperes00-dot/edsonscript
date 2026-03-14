-- ============================================================
-- EDSON MODZ V8 - RAYFIELD PERSONALIZED EDITION
-- DESIGN ULTRA-PROFISSIONAL | SKELETON ESP | AIMBOT UNIVERSAL
-- CUSTOMIZED BY EDSON | RAINBOW MIRROR EFFECT
-- ============================================================

-- Carregar Rayfield Library (Base estável)
local Rayfield = loadstring(game:HttpGet('https://sirius.menu/rayfield'))()

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
    
    WalkSpeed = 16,
    SpeedEnabled = false
}

-- Criar Janela Principal Personalizada
local Window = Rayfield:CreateWindow({
    Name = "EDSON MODZ V8",
    LoadingTitle = "EDSON MODZ V8",
    LoadingSubtitle = "by EDSON",
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

-- EFEITO RAINBOW MIRROR NO TÍTULO (Tentativa de personalização visual na UI da Rayfield)
task.spawn(function()
    while task.wait() do
        pcall(function()
            local CoreGui = game:GetService("CoreGui")
            local MainFrame = CoreGui:FindFirstChild("Rayfield") or CoreGui:FindFirstChild("EDSON")
            if MainFrame then
                local Title = MainFrame:FindFirstChild("Main", true):FindFirstChild("Title", true)
                if Title and Title:IsA("TextLabel") then
                    Title.Text = "EDSON MODZ V8"
                    local hue = tick() % 5 / 5
                    Title.TextColor3 = Color3.fromHSV(hue, 1, 1)
                end
            end
        end)
    end
end)

-- Abas
local AimTab = Window:CreateTab("AIMBOT", "target")
local VisualTab = Window:CreateTab("VISUAL", "eye")
local MiscTab = Window:CreateTab("MISC", "settings")

-- Seção Aimbot
AimTab:CreateSection("Combate de Elite")

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
VisualTab:CreateSection("Visão Avançada")

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
    Name = "Nome ESP (Texto Branco)",
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
    Name = "Linha ESP (Centro)",
    CurrentValue = true,
    Flag = "LineEnabled",
    Callback = function(Value)
        Config.LineEnabled = Value
    end,
})

-- Seção Misc
MiscTab:CreateSection("Outras Funções")

MiscTab:CreateToggle({
    Name = "Ativar Speed Hack",
    CurrentValue = false,
    Flag = "SpeedEnabled",
    Callback = function(Value)
        Config.SpeedEnabled = Value
    end,
})

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
-- LÓGICA DE AIMBOT E ESP (ALTA PERFORMANCE)
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
                        if not Config.VisibleCheck or #Camera:GetPartsObscuringTarget({part.Position}, {game:GetService("Players").LocalPlayer.Character, char}) == 0 then
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
        local char = p.Character
        if Config.ESPEnabled and char and char:FindFirstChild("HumanoidRootPart") and char.Humanoid.Health > 0 then
            local pos, onScreen = Camera:WorldToViewportPoint(char.HumanoidRootPart.Position)
            if onScreen then
                local h = math.abs(Camera:WorldToViewportPoint(char.Head.Position + Vector3.new(0, 0.5, 0)).Y - Camera:WorldToViewportPoint(char.HumanoidRootPart.Position - Vector3.new(0, 3, 0)).Y)
                local w = h * 0.6
                
                -- Box
                if Config.BoxEnabled then
                    local l, t = pos.X - w/2, pos.Y - h/2
                    esp.Box[1].Visible = true; esp.Box[1].From = Vector2.new(l, t); esp.Box[1].To = Vector2.new(l + w, t)
                    esp.Box[2].Visible = true; esp.Box[2].From = Vector2.new(l, t + h); esp.Box[2].To = Vector2.new(l + w, t + h)
                    esp.Box[3].Visible = true; esp.Box[3].From = Vector2.new(l, t); esp.Box[3].To = Vector2.new(l, t + h)
                    esp.Box[4].Visible = true; esp.Box[4].From = Vector2.new(l + w, t); esp.Box[4].To = Vector2.new(l + w, t + h)
                else for _, v in pairs(esp.Box) do v.Visible = false end end
                
                -- Name
                if Config.NameEnabled then 
                    esp.Name.Visible = true; esp.Name.Position = Vector2.new(pos.X, pos.Y - h/2 - 15); esp.Name.Text = p.Name 
                else esp.Name.Visible = false end
                
                -- Health
                if Config.HealthEnabled then
                    local bh = h * (char.Humanoid.Health/char.Humanoid.MaxHealth)
                    esp.Health.Visible = true; esp.Health.Position = Vector2.new(pos.X - w/2 - 6, pos.Y - h/2); esp.Health.Size = Vector2.new(4, h)
                    esp.HealthBar.Visible = true; esp.HealthBar.Position = Vector2.new(pos.X - w/2 - 6, pos.Y + h/2 - bh); esp.HealthBar.Size = Vector2.new(4, bh)
                else esp.Health.Visible = false; esp.HealthBar.Visible = false end
                
                -- Line
                if Config.LineEnabled then 
                    esp.Line.Visible = true; esp.Line.From = center; esp.Line.To = Vector2.new(pos.X, pos.Y + h/2) 
                else esp.Line.Visible = false end
                
                -- Skeleton
                if Config.SkeletonEnabled then
                    local parts = {char:FindFirstChild("Head"), char:FindFirstChild("UpperTorso") or char:FindFirstChild("Torso"), char:FindFirstChild("LowerTorso") or char:FindFirstChild("Torso"), char:FindFirstChild("LeftUpperArm") or char:FindFirstChild("Left Arm"), char:FindFirstChild("LeftLowerArm") or char:FindFirstChild("Left Arm"), char:FindFirstChild("RightUpperArm") or char:FindFirstChild("Right Arm"), char:FindFirstChild("RightLowerArm") or char:FindFirstChild("Right Arm"), char:FindFirstChild("LeftUpperLeg") or char:FindFirstChild("Left Leg"), char:FindFirstChild("LeftLowerLeg") or char:FindFirstChild("Left Leg"), char:FindFirstChild("RightUpperLeg") or char:FindFirstChild("Right Leg"), char:FindFirstChild("RightLowerLeg") or char:FindFirstChild("Right Leg")}
                    local connections = {{1,2}, {2,3}, {2,4}, {4,5}, {2,6}, {6,7}, {3,8}, {8,9}, {3,10}, {10,11}}
                    for i, conn in ipairs(connections) do
                        local p1, p2 = parts[conn[1]], parts[conn[2]]
                        if p1 and p2 then
                            local v1, o1 = Camera:WorldToViewportPoint(p1.Position); local v2, o2 = Camera:WorldToViewportPoint(p2.Position)
                            if o1 and o2 then esp.Skeleton[i].Visible = true; esp.Skeleton[i].From = Vector2.new(v1.X, v1.Y); esp.Skeleton[i].To = Vector2.new(v2.X, v2.Y) else esp.Skeleton[i].Visible = false end
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
    if Config.SpeedEnabled and game:GetService("Players").LocalPlayer.Character and game:GetService("Players").LocalPlayer.Character:FindFirstChild("Humanoid") then 
        game:GetService("Players").LocalPlayer.Character.Humanoid.WalkSpeed = Config.WalkSpeed 
    end
end)

game:GetService("Players").PlayerAdded:Connect(createESP)
for _, p in ipairs(game:GetService("Players"):GetPlayers()) do if p ~= game:GetService("Players").LocalPlayer then createESP(p) end end

Rayfield:Notify({
    Title = "EDSON MODZ V8",
    Content = "Bem-vindo de volta, EDSON! Script carregado com sucesso.",
    Duration = 5,
    Image = "check-circle",
})
