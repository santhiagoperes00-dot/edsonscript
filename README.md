-- EDSON SCRIPT V5 - ULTIMATE EDITION (VERSÃO DEFINITIVA)
-- COR: AZUL FORTE | ESP REALISTA COM CABEÇA | BOX AJUSTADA | VIDA NA LATERAL | BOTÕES VERDES | MENU COMPLETO

local TweenService = game:GetService("TweenService")
local UIS = game:GetService("UserInputService")
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local Camera = workspace.CurrentCamera
local LocalPlayer = Players.LocalPlayer

local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Parent = game.CoreGui
ScreenGui.ResetOnSpawn = false
ScreenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
ScreenGui.DisplayOrder = 999

-- ==================== CONFIGURAÇÕES GLOBAIS ====================
local Config = {
    AimEnabled = false,
    AimMode = "Legit",
    TeamCheck = false,
    VisibleCheck = true,
    SelectedPart = "Head",
    Smoothness = 0.3,
    FOVSize = 150,
    FOVVisible = false,
    
    ESPEnabled = false,
    BoxEnabled = false,
    NameEnabled = false,
    HealthEnabled = false,
    DistEnabled = false,
    SkeletonEnabled = false,
}

local MainColor = Color3.fromRGB(0, 100, 255) -- AZUL FORTE
local OnColor = Color3.fromRGB(46, 204, 113) -- VERDE
local OffColor = Color3.fromRGB(231, 76, 60) -- VERMELHO
local ESPObjects = {}

-- ==================== FUNÇÕES DE UTILIDADE ====================
local function addCorner(obj, radius)
    local corner = Instance.new("UICorner")
    corner.CornerRadius = UDim.new(0, radius)
    corner.Parent = obj
end

local function addStroke(obj, thickness, color)
    local stroke = Instance.new("UIStroke")
    stroke.Thickness = thickness
    stroke.Color = color or Color3.new(0,0,0)
    stroke.Transparency = 0.5
    stroke.Parent = obj
end

local function IsPlayerVisible(player)
    if not Config.VisibleCheck then return true end
    if not player or not player.Character then return false end
    local head = player.Character:FindFirstChild("Head")
    if not head then return false end
    
    local origin = Camera.CFrame.Position
    local direction = (head.Position - origin).Unit * (head.Position - origin).Magnitude
    local raycastParams = RaycastParams.new()
    raycastParams.FilterDescendantsInstances = {LocalPlayer.Character, player.Character}
    raycastParams.FilterType = Enum.RaycastFilterType.Blacklist
    
    local result = workspace:Raycast(origin, direction, raycastParams)
    return result == nil
end

-- ==================== INTERFACE (MENU) ====================
local Main = Instance.new("Frame", ScreenGui)
Main.Size = UDim2.new(0, 480, 0, 400)
Main.Position = UDim2.new(0.5, -240, 0.5, -200)
Main.BackgroundColor3 = Color3.fromRGB(18, 18, 22)
Main.Active = true
Main.Draggable = true
addCorner(Main, 12)
addStroke(Main, 1, Color3.fromRGB(60, 60, 60))

local Top = Instance.new("Frame", Main)
Top.Size = UDim2.new(1, 0, 0, 45)
Top.BackgroundColor3 = MainColor
addCorner(Top, 12)

local Title = Instance.new("TextLabel", Top)
Title.Size = UDim2.new(1, -80, 1, 0)
Title.Position = UDim2.new(0, 15, 0, 0)
Title.Text = "⚡ EDSON SCRIPT V5 ULTIMATE ⚡"
Title.BackgroundTransparency = 1
Title.TextColor3 = Color3.new(1, 1, 1)
Title.Font = Enum.Font.GothamBold
Title.TextSize = 18
Title.TextXAlignment = Enum.TextXAlignment.Left

local Side = Instance.new("Frame", Main)
Side.Size = UDim2.new(0, 110, 1, -45)
Side.Position = UDim2.new(0, 0, 0, 45)
Side.BackgroundColor3 = Color3.fromRGB(24, 24, 30)
addCorner(Side, 12)

local Content = Instance.new("Frame", Main)
Content.Position = UDim2.new(0, 110, 0, 45)
Content.Size = UDim2.new(1, -110, 1, -45)
Content.BackgroundTransparency = 1

local AimTab = Instance.new("ScrollingFrame", Content)
AimTab.Size = UDim2.new(1, 0, 1, 0)
AimTab.BackgroundTransparency = 1
AimTab.ScrollBarThickness = 4
AimTab.CanvasSize = UDim2.new(0,0,0,500)
AimTab.Visible = true

local VisualTab = Instance.new("ScrollingFrame", Content)
VisualTab.Size = UDim2.new(1, 0, 1, 0)
VisualTab.BackgroundTransparency = 1
VisualTab.ScrollBarThickness = 4
VisualTab.CanvasSize = UDim2.new(0,0,0,500)
VisualTab.Visible = false

local SettingsTab = Instance.new("ScrollingFrame", Content)
SettingsTab.Size = UDim2.new(1, 0, 1, 0)
SettingsTab.BackgroundTransparency = 1
SettingsTab.ScrollBarThickness = 4
SettingsTab.CanvasSize = UDim2.new(0,0,0,300)
SettingsTab.Visible = false

-- BOTÕES DE ABA
local function createTabBtn(text, pos, tab)
    local b = Instance.new("TextButton", Side)
    b.Size = UDim2.new(1, -10, 0, 50)
    b.Position = UDim2.new(0, 5, 0, pos)
    b.Text = text
    b.Font = Enum.Font.GothamBold
    b.TextColor3 = Color3.new(1,1,1)
    b.BackgroundColor3 = Color3.fromRGB(35, 35, 42)
    addCorner(b, 8)
    b.MouseButton1Click:Connect(function()
        AimTab.Visible = false
        VisualTab.Visible = false
        SettingsTab.Visible = false
        tab.Visible = true
    end)
end
createTabBtn("🎯 AIM", 10, AimTab)
createTabBtn("👁️ VISUAL", 70, VisualTab)
createTabBtn("⚙️ SET", 130, SettingsTab)

-- FUNÇÃO TOGGLE COM FEEDBACK VERDE
local function createToggle(parent, text, x, y, width, key)
    local btn = Instance.new("TextButton", parent)
    btn.Size = UDim2.new(0, width or 160, 0, 35)
    btn.Position = UDim2.new(0, x, 0, y)
    btn.Font = Enum.Font.GothamBold
    btn.TextColor3 = Color3.new(1,1,1)
    addCorner(btn, 6)
    
    local function update()
        btn.Text = text .. ": " .. (Config[key] and "ON" or "OFF")
        btn.BackgroundColor3 = Config[key] and OnColor or OffColor
    end
    btn.MouseButton1Click:Connect(function() Config[key] = not Config[key]; update() end)
    update()
end

-- FUNÇÃO SLIDER RESTAURADA
local function createSlider(parent, label, x, y, minVal, maxVal, defaultVal, callback)
    local lbl = Instance.new("TextLabel", parent)
    lbl.Size = UDim2.new(0,200,0,20)
    lbl.Position = UDim2.new(0, x, 0, y)
    lbl.Text = label .. ": " .. defaultVal
    lbl.TextColor3 = Color3.new(1,1,1)
    lbl.BackgroundTransparency = 1
    lbl.Font = Enum.Font.Gotham
    lbl.TextXAlignment = Enum.TextXAlignment.Left
    
    local slider = Instance.new("Frame", parent)
    slider.Size = UDim2.new(0,200,0,4)
    slider.Position = UDim2.new(0, x, 0, y + 25)
    slider.BackgroundColor3 = Color3.fromRGB(60,60,70)
    addCorner(slider, 2)
    
    local fill = Instance.new("Frame", slider)
    fill.Size = UDim2.new((defaultVal-minVal)/(maxVal-minVal),0,1,0)
    fill.BackgroundColor3 = MainColor
    addCorner(fill, 2)
    
    local knob = Instance.new("Frame", slider)
    knob.Size = UDim2.new(0,12,0,12)
    knob.Position = UDim2.new(fill.Size.X.Scale, -6, -1, 0)
    knob.BackgroundColor3 = MainColor
    addCorner(knob, 6)
    
    local dragging = false
    knob.InputBegan:Connect(function(input) if input.UserInputType == Enum.UserInputType.MouseButton1 then dragging = true end end)
    UIS.InputEnded:Connect(function(input) if input.UserInputType == Enum.UserInputType.MouseButton1 then dragging = false end end)
    UIS.InputChanged:Connect(function(input)
        if dragging and input.UserInputType == Enum.UserInputType.MouseMovement then
            local pos = math.clamp((input.Position.X - slider.AbsolutePosition.X) / slider.AbsoluteSize.X, 0, 1)
            fill.Size = UDim2.new(pos,0,1,0)
            knob.Position = UDim2.new(pos, -6, -1, 0)
            local value = minVal + (pos * (maxVal - minVal))
            lbl.Text = label .. ": " .. math.floor(value)
            callback(value)
        end
    end)
end

-- BOTÕES AIM
createToggle(AimTab, "AIMBOT", 10, 10, 330, "AimEnabled")
local ModeBtn = Instance.new("TextButton", AimTab)
ModeBtn.Size = UDim2.new(0, 160, 0, 35)
ModeBtn.Position = UDim2.new(0, 10, 0, 55)
ModeBtn.Text = "MODE: LEGIT"
ModeBtn.Font = Enum.Font.GothamBold
ModeBtn.TextColor3 = Color3.new(1,1,1)
ModeBtn.BackgroundColor3 = Color3.fromRGB(60,60,70)
addCorner(ModeBtn, 6)
ModeBtn.MouseButton1Click:Connect(function()
    Config.AimMode = (Config.AimMode == "Legit") and "Rage" or "Legit"
    ModeBtn.Text = "MODE: " .. Config.AimMode:upper()
end)

createToggle(AimTab, "TEAM CHECK", 180, 55, 160, "TeamCheck")
createToggle(AimTab, "VIS CHECK", 10, 100, 160, "VisibleCheck")
createToggle(AimTab, "SHOW FOV", 180, 100, 160, "FOVVisible")
createSlider(AimTab, "SMOOTHNESS", 10, 150, 1, 10, 3, function(v) Config.Smoothness = v/10 end)
createSlider(AimTab, "FOV SIZE", 10, 210, 10, 500, 150, function(v) Config.FOVSize = v end)

-- BOTÕES VISUAL
createToggle(VisualTab, "MASTER ESP", 10, 10, 330, "ESPEnabled")
createToggle(VisualTab, "BOX", 10, 55, 160, "BoxEnabled")
createToggle(VisualTab, "SKELETON", 180, 55, 160, "SkeletonEnabled")
createToggle(VisualTab, "NAME", 10, 100, 160, "NameEnabled")
createToggle(VisualTab, "HEALTH", 180, 100, 160, "HealthEnabled")
createToggle(VisualTab, "DISTANCE", 10, 145, 160, "DistEnabled")

-- BOTÕES SETTINGS (COLOR PICKER RESTAURADO)
local colorBtn = Instance.new("TextButton", SettingsTab)
colorBtn.Size = UDim2.new(0, 330, 0, 35)
colorBtn.Position = UDim2.new(0, 10, 0, 10)
colorBtn.Text = "MUDAR COR DO MENU"
colorBtn.Font = Enum.Font.GothamBold
colorBtn.TextColor3 = Color3.new(1,1,1)
colorBtn.BackgroundColor3 = MainColor
addCorner(colorBtn, 6)
local colors = {Color3.fromRGB(0, 100, 255), Color3.fromRGB(220, 40, 80), Color3.fromRGB(50, 200, 50), Color3.fromRGB(255, 140, 0), Color3.fromRGB(180, 0, 255)}
local colorIdx = 1
colorBtn.MouseButton1Click:Connect(function()
    colorIdx = colorIdx % #colors + 1
    MainColor = colors[colorIdx]
    Top.BackgroundColor3 = MainColor
    colorBtn.BackgroundColor3 = MainColor
end)

-- ==================== LÓGICA DO ESP ====================
local function CreateESP(player)
    if ESPObjects[player] then return end
    local esp = {
        Box = Drawing.new("Square"),
        Name = Drawing.new("Text"),
        Dist = Drawing.new("Text"),
        HealthBar = Drawing.new("Square"),
        HealthBarBack = Drawing.new("Square"),
        Skeleton = {},
        HeadCircle = Drawing.new("Circle")
    }
    esp.Box.Thickness = 2; esp.Box.Filled = false
    esp.Name.Size = 14; esp.Name.Center = true; esp.Name.Outline = true
    esp.Dist.Size = 12; esp.Dist.Center = true; esp.Dist.Outline = true
    esp.HealthBar.Filled = true; esp.HealthBarBack.Filled = true; esp.HealthBarBack.Color = Color3.new(0,0,0)
    esp.HeadCircle.Thickness = 2; esp.HeadCircle.Filled = false; esp.HeadCircle.NumSides = 12
    ESPObjects[player] = esp
end

local function ClearESP(player)
    if ESPObjects[player] then
        for _, v in pairs(ESPObjects[player]) do
            if type(v) == "table" then for _, l in ipairs(v) do l:Remove() end else v:Remove() end
        end
        ESPObjects[player] = nil
    end
end

local SkeletonConnections = {
    {"Head", "UpperTorso"}, {"UpperTorso", "LowerTorso"},
    {"UpperTorso", "LeftUpperArm"}, {"LeftUpperArm", "LeftLowerArm"}, {"LeftLowerArm", "LeftHand"},
    {"UpperTorso", "RightUpperArm"}, {"RightUpperArm", "RightLowerArm"}, {"RightLowerArm", "RightHand"},
    {"LowerTorso", "LeftUpperLeg"}, {"LeftUpperLeg", "LeftLowerLeg"}, {"LeftLowerLeg", "LeftFoot"},
    {"LowerTorso", "RightUpperLeg"}, {"RightUpperLeg", "RightLowerLeg"}, {"RightLowerLeg", "RightFoot"}
}

local function DrawSkeleton(char, esp, color)
    -- Cabeça (Círculo)
    local head = char:FindFirstChild("Head")
    if head then
        local pos, vis = Camera:WorldToViewportPoint(head.Position)
        if vis then
            local dist = (Camera.CFrame.Position - head.Position).Magnitude
            esp.HeadCircle.Radius = math.clamp(500 / dist, 2, 15)
            esp.HeadCircle.Position = Vector2.new(pos.X, pos.Y)
            esp.HeadCircle.Color = color
            esp.HeadCircle.Visible = true
        else esp.HeadCircle.Visible = false end
    else esp.HeadCircle.Visible = false end

    -- Linhas do corpo
    while #esp.Skeleton < #SkeletonConnections do
        local l = Drawing.new("Line"); l.Thickness = 2; table.insert(esp.Skeleton, l)
    end
    for i, conn in ipairs(SkeletonConnections) do
        local p1, p2 = char:FindFirstChild(conn[1]), char:FindFirstChild(conn[2])
        if p1 and p2 then
            local pos1, vis1 = Camera:WorldToViewportPoint(p1.Position)
            local pos2, vis2 = Camera:WorldToViewportPoint(p2.Position)
            if vis1 and vis2 then
                esp.Skeleton[i].From = Vector2.new(pos1.X, pos1.Y)
                esp.Skeleton[i].To = Vector2.new(pos2.X, pos2.Y)
                esp.Skeleton[i].Color = color; esp.Skeleton[i].Visible = true
                continue
            end
        end
        esp.Skeleton[i].Visible = false
    end
end

-- ==================== LOOP PRINCIPAL ====================
local FOV = Drawing.new("Circle")
FOV.Thickness = 1; FOV.NumSides = 60; FOV.Filled = false; FOV.Transparency = 0.7

RunService.RenderStepped:Connect(function()
    FOV.Radius = Config.FOVSize; FOV.Visible = Config.FOVVisible; FOV.Color = MainColor
    FOV.Position = Vector2.new(Camera.ViewportSize.X/2, Camera.ViewportSize.Y/2)

    if not Config.ESPEnabled then
        for p, _ in pairs(ESPObjects) do ClearESP(p) end
    else
        for _, player in ipairs(Players:GetPlayers()) do
            local char = player.Character
            local hum = char and char:FindFirstChildOfClass("Humanoid")
            if player ~= LocalPlayer and hum and hum.Health > 0 then
                if not ESPObjects[player] then CreateESP(player) end
                local esp = ESPObjects[player]
                
                -- Cálculo da Box Perfeita
                local minX, minY = math.huge, math.huge
                local maxX, maxY = -math.huge, -math.huge
                local onScreen = false
                for _, part in ipairs(char:GetChildren()) do
                    if part:IsA("BasePart") then
                        local pos, vis = Camera:WorldToViewportPoint(part.Position)
                        if vis then
                            onScreen = true
                            minX = math.min(minX, pos.X); minY = math.min(minY, pos.Y)
                            maxX = math.max(maxX, pos.X); maxY = math.max(maxY, pos.Y)
                        end
                    end
                end

                if onScreen then
                    local w, h = maxX - minX, maxY - minY
                    local color = IsPlayerVisible(player) and OnColor or MainColor
                    
                    esp.Box.Visible = Config.BoxEnabled
                    if Config.BoxEnabled then
                        esp.Box.Size = Vector2.new(w, h); esp.Box.Position = Vector2.new(minX, minY); esp.Box.Color = color
                    end
                    
                    esp.HealthBar.Visible = Config.HealthEnabled
                    esp.HealthBarBack.Visible = Config.HealthEnabled
                    if Config.HealthEnabled then
                        local hp = hum.Health / hum.MaxHealth
                        esp.HealthBarBack.Size = Vector2.new(4, h); esp.HealthBarBack.Position = Vector2.new(minX - 6, minY)
                        esp.HealthBar.Size = Vector2.new(4, h * hp); esp.HealthBar.Position = Vector2.new(minX - 6, minY + (h - h * hp))
                        esp.HealthBar.Color = Color3.fromHSV(hp/3, 1, 1)
                    end
                    
                    esp.Name.Visible = Config.NameEnabled
                    if Config.NameEnabled then
                        esp.Name.Text = player.Name; esp.Name.Position = Vector2.new(minX + w/2, minY - 16)
                    end
                    
                    esp.Dist.Visible = Config.DistEnabled
                    if Config.DistEnabled then
                        local d = (Camera.CFrame.Position - char.HumanoidRootPart.Position).Magnitude
                        esp.Dist.Text = math.floor(d) .. "m"; esp.Dist.Position = Vector2.new(minX + w/2, minY + h + 5)
                    end
                    
                    if Config.SkeletonEnabled then DrawSkeleton(char, esp, color) else
                        esp.HeadCircle.Visible = false
                        for _, l in ipairs(esp.Skeleton) do l.Visible = false end
                    end
                else ClearESP(player) end
            elseif ESPObjects[player] then ClearESP(player) end
        end
    end

    -- AIMBOT LOOP
    if Config.AimEnabled then
        local center = Vector2.new(Camera.ViewportSize.X/2, Camera.ViewportSize.Y/2)
        local target = nil
        local shortest = Config.FOVSize
        for _, p in ipairs(Players:GetPlayers()) do
            if p ~= LocalPlayer and p.Character and p.Character:FindFirstChild("Humanoid") and p.Character.Humanoid.Health > 0 then
                if Config.TeamCheck and p.Team == LocalPlayer.Team then continue end
                if Config.VisibleCheck and not IsPlayerVisible(p) then continue end
                local part = p.Character:FindFirstChild(Config.SelectedPart) or p.Character:FindFirstChild("Head")
                if part then
                    local pos, vis = Camera:WorldToViewportPoint(part.Position)
                    if vis then
                        local dist = (Vector2.new(pos.X, pos.Y) - center).Magnitude
                        if dist < shortest then shortest = dist; target = part end
                    end
                end
            end
        end
        if target then
            if Config.AimMode == "Legit" then
                Camera.CFrame = Camera.CFrame:Lerp(CFrame.new(Camera.CFrame.Position, target.Position), Config.Smoothness)
            else
                Camera.CFrame = CFrame.new(Camera.CFrame.Position, target.Position)
            end
        end
    end
end)

Players.PlayerRemoving:Connect(ClearESP)
print("✅ EDSON SCRIPT V5 ULTIMATE DEFINITIVO CARREGADO")
