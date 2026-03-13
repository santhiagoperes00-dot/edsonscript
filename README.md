-- EDSON SCRIPT V5 - ULTIMATE EDITION
-- COR: AZUL FORTE | ESP DETALHADO | BOX CORRIGIDA | VIDA GRUDADA

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

-- VARIÁVEIS GLOBAIS
local AimMode = "Legit"
local AimEnabled = false
local ESPEnabled = false
local TeamCheck = false
local SelectedPart = "Head"
local Smoothness = 0.3
local FOVSize = 150
local FOVVisible = false
local MainColor = Color3.fromRGB(0, 100, 255) -- AZUL FORTE
local Minimized = false
local VisibleCheck = true
local MainSize = UDim2.new(0,480,0,400)
local MinSize = UDim2.new(0,480,0,40)

-- VARIÁVEIS ESP (CONFIGURAÇÕES)
local BoxEnabled = false
local NameEnabled = false
local HealthEnabled = false
local DistEnabled = false
local SkeletonEnabled = false
local ESPObjects = {}

-- FUNÇÕES DE UTILIDADE
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
    if not VisibleCheck then return true end
    if not player or not player.Character then return false end
    
    local character = player.Character
    local head = character:FindFirstChild("Head")
    local root = character:FindFirstChild("HumanoidRootPart")
    
    if not head or not root then return false end
    
    local origin = Camera.CFrame.Position
    local direction = (head.Position - origin).Unit * (head.Position - origin).Magnitude
    
    local raycastParams = RaycastParams.new()
    raycastParams.FilterDescendantsInstances = {LocalPlayer.Character, character}
    raycastParams.FilterType = Enum.RaycastFilterType.Blacklist
    
    local result = workspace:Raycast(origin, direction, raycastParams)
    
    return result == nil
end

-- MAIN FRAME
local Main = Instance.new("Frame")
Main.Parent = ScreenGui
Main.Size = MainSize
Main.Position = UDim2.new(0.5,-240,0.5,-200)
Main.BackgroundColor3 = Color3.fromRGB(18, 18, 22)
Main.Active = true
Main.Draggable = true
addCorner(Main, 12)
addStroke(Main, 1, Color3.fromRGB(60,60,60))

-- TOP BAR
local Top = Instance.new("Frame")
Top.Parent = Main
Top.Size = UDim2.new(1,0,0,45)
Top.BackgroundColor3 = MainColor
Top.BorderSizePixel = 0
addCorner(Top, 12)

local Title = Instance.new("TextLabel")
Title.Parent = Top
Title.Size = UDim2.new(1,-80,1,0)
Title.Position = UDim2.new(0,15,0,0)
Title.Text = "⚡ EDSON SCRIPT V5 ⚡"
Title.BackgroundTransparency = 1
Title.TextColor3 = Color3.new(1,1,1)
Title.Font = Enum.Font.GothamBold
Title.TextSize = 18
Title.TextXAlignment = Enum.TextXAlignment.Left

local MinimizeBtn = Instance.new("TextButton")
MinimizeBtn.Parent = Top
MinimizeBtn.Size = UDim2.new(0,30,0,30)
MinimizeBtn.Position = UDim2.new(1,-70,0.5,-15)
MinimizeBtn.BackgroundColor3 = Color3.fromRGB(255,255,255)
MinimizeBtn.BackgroundTransparency = 0.9
MinimizeBtn.Text = "−"
MinimizeBtn.TextColor3 = Color3.new(1,1,1)
MinimizeBtn.TextSize = 20
MinimizeBtn.Font = Enum.Font.GothamBold
addCorner(MinimizeBtn, 8)

local CloseBtn = Instance.new("TextButton")
CloseBtn.Parent = Top
CloseBtn.Size = UDim2.new(0,30,0,30)
CloseBtn.Position = UDim2.new(1,-35,0.5,-15)
CloseBtn.BackgroundColor3 = Color3.fromRGB(255,70,70)
CloseBtn.BackgroundTransparency = 0.2
CloseBtn.Text = "✕"
CloseBtn.TextColor3 = Color3.new(1,1,1)
CloseBtn.TextSize = 16
CloseBtn.Font = Enum.Font.GothamBold
addCorner(CloseBtn, 8)

CloseBtn.MouseButton1Click:Connect(function()
    ScreenGui:Destroy()
end)

-- SIDE MENU
local Side = Instance.new("Frame")
Side.Parent = Main
Side.Size = UDim2.new(0,110,1,-45)
Side.Position = UDim2.new(0,0,0,45)
Side.BackgroundColor3 = Color3.fromRGB(24, 24, 30)
Side.BorderSizePixel = 0
addCorner(Side, 12)

-- CONTENT AREA
local Content = Instance.new("Frame")
Content.Parent = Main
Content.Position = UDim2.new(0,110,0,45)
Content.Size = UDim2.new(1,-110,1,-45)
Content.BackgroundColor3 = Color3.fromRGB(18, 18, 22)
Content.BorderSizePixel = 0
addCorner(Content, 12)

-- ABAS
local AimTab = Instance.new("ScrollingFrame")
AimTab.Parent = Content
AimTab.Size = UDim2.new(1,0,1,0)
AimTab.BackgroundTransparency = 1
AimTab.ScrollBarThickness = 4
AimTab.ScrollBarImageColor3 = MainColor
AimTab.CanvasSize = UDim2.new(0,0,0,500)
AimTab.BorderSizePixel = 0

local VisualTab = Instance.new("ScrollingFrame")
VisualTab.Parent = Content
VisualTab.Size = UDim2.new(1,0,1,0)
VisualTab.BackgroundTransparency = 1
VisualTab.ScrollBarThickness = 4
VisualTab.ScrollBarImageColor3 = MainColor
VisualTab.CanvasSize = UDim2.new(0,0,0,500)
VisualTab.BorderSizePixel = 0
VisualTab.Visible = false

local SettingsTab = Instance.new("ScrollingFrame")
SettingsTab.Parent = Content
SettingsTab.Size = UDim2.new(1,0,1,0)
SettingsTab.BackgroundTransparency = 1
SettingsTab.ScrollBarThickness = 4
SettingsTab.ScrollBarImageColor3 = MainColor
SettingsTab.CanvasSize = UDim2.new(0,0,0,300)
SettingsTab.BorderSizePixel = 0
SettingsTab.Visible = false

-- BOTÕES DAS ABAS
local function createTabButton(emoji, name, pos)
    local b = Instance.new("TextButton")
    b.Parent = Side
    b.Size = UDim2.new(1,-10,0,60)
    b.Position = UDim2.new(0,5,0,pos)
    b.Text = emoji .. "  " .. name
    b.Font = Enum.Font.GothamBold
    b.TextColor3 = Color3.new(0.9,0.9,0.9)
    b.BackgroundColor3 = Color3.fromRGB(30, 30, 36)
    b.BorderSizePixel = 0
    addCorner(b, 8)
    
    b.MouseEnter:Connect(function()
        TweenService:Create(b, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(45, 45, 52)}):Play()
    end)
    b.MouseLeave:Connect(function()
        TweenService:Create(b, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(30, 30, 36)}):Play()
    end)
    
    return b
end

local AimButton = createTabButton("🎯", "AIM", 10)
local VisualButton = createTabButton("👁️", "VISUAL", 80)
local SettingsButton = createTabButton("⚙️", "SET", 150)

-- FUNÇÃO TROCAR ABA
local function switch(tab)
    AimTab.Visible = false
    VisualTab.Visible = false
    SettingsTab.Visible = false
    tab.Visible = true
end

AimButton.MouseButton1Click:Connect(function() switch(AimTab) end)
VisualButton.MouseButton1Click:Connect(function() switch(VisualTab) end)
SettingsButton.MouseButton1Click:Connect(function() switch(SettingsTab) end)

-- FUNÇÃO MINIMIZAR
MinimizeBtn.MouseButton1Click:Connect(function()
    Minimized = not Minimized
    
    if Minimized then
        TweenService:Create(Main, TweenInfo.new(0.3), {Size = MinSize}):Play()
        MinimizeBtn.Text = "+"
        Side.Visible = false
        Content.Visible = false
    else
        TweenService:Create(Main, TweenInfo.new(0.3), {Size = MainSize}):Play()
        MinimizeBtn.Text = "−"
        wait(0.3)
        Side.Visible = true
        Content.Visible = true
    end
end)

-- FUNÇÃO PARA CRIAR BOTÕES (ORGANIZADOS EM GRID)
local function createButton(parent, text, x, y, width, color)
    local btn = Instance.new("TextButton")
    btn.Parent = parent
    btn.Size = UDim2.new(0, width or 140, 0, 35)
    btn.Position = UDim2.new(0, x, 0, y)
    btn.Text = text
    btn.Font = Enum.Font.GothamBold
    btn.TextColor3 = Color3.new(1,1,1)
    btn.BackgroundColor3 = color or Color3.fromRGB(60,60,70)
    btn.BorderSizePixel = 0
    addCorner(btn, 6)
    return btn
end

-- FUNÇÃO PARA CRIAR SLIDER
local function createSlider(parent, label, x, y, minVal, maxVal, defaultVal, callback)
    local lbl = Instance.new("TextLabel")
    lbl.Parent = parent
    lbl.Size = UDim2.new(0,200,0,20)
    lbl.Position = UDim2.new(0, x, 0, y)
    lbl.Text = label .. ": " .. defaultVal
    lbl.TextColor3 = Color3.new(1,1,1)
    lbl.BackgroundTransparency = 1
    lbl.Font = Enum.Font.Gotham
    lbl.TextXAlignment = Enum.TextXAlignment.Left
    
    local slider = Instance.new("Frame")
    slider.Parent = parent
    slider.Size = UDim2.new(0,200,0,4)
    slider.Position = UDim2.new(0, x, 0, y + 25)
    slider.BackgroundColor3 = Color3.fromRGB(60,60,70)
    addCorner(slider, 2)
    
    local fill = Instance.new("Frame")
    fill.Parent = slider
    fill.Size = UDim2.new((defaultVal-minVal)/(maxVal-minVal),0,1,0)
    fill.BackgroundColor3 = MainColor
    addCorner(fill, 2)
    
    local knob = Instance.new("Frame")
    knob.Parent = slider
    knob.Size = UDim2.new(0,12,0,12)
    knob.Position = UDim2.new(fill.Size.X.Scale, -6, -1, 0)
    knob.BackgroundColor3 = MainColor
    addCorner(knob, 6)
    
    local dragging = false
    
    knob.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 then
            dragging = true
        end
    end)
    
    UIS.InputEnded:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 then
            dragging = false
        end
    end)
    
    UIS.InputChanged:Connect(function(input)
        if dragging and input.UserInputType == Enum.UserInputType.MouseMovement then
            local pos = math.clamp(
                (input.Position.X - slider.AbsolutePosition.X) / slider.AbsoluteSize.X,
                0, 1
            )
            fill.Size = UDim2.new(pos,0,1,0)
            knob.Position = UDim2.new(pos, -6, -1, 0)
            
            local value = minVal + (pos * (maxVal - minVal))
            lbl.Text = label .. ": " .. math.floor(value)
            callback(value)
        end
    end)
    
    return slider
end

-- ==================== ABA AIM ====================
local aimTitle = Instance.new("TextLabel")
aimTitle.Parent = AimTab
aimTitle.Size = UDim2.new(1,0,0,30)
aimTitle.Position = UDim2.new(0,10,0,10)
aimTitle.Text = "🎯 AIMBOT CONFIGURATIONS"
aimTitle.TextColor3 = MainColor
aimTitle.BackgroundTransparency = 1
aimTitle.Font = Enum.Font.GothamBold
aimTitle.TextSize = 18
aimTitle.TextXAlignment = Enum.TextXAlignment.Left

local AimToggle = createButton(AimTab, "AIMBOT: OFF", 10, 50, 160, Color3.fromRGB(220, 40, 80))
AimToggle.MouseButton1Click:Connect(function()
    AimEnabled = not AimEnabled
    AimToggle.Text = AimEnabled and "AIMBOT: ON" or "AIMBOT: OFF"
    AimToggle.BackgroundColor3 = AimEnabled and Color3.fromRGB(50, 200, 50) or Color3.fromRGB(220, 40, 80)
end)

local ModeToggle = createButton(AimTab, "MODE: LEGIT", 180, 50, 160)
ModeToggle.MouseButton1Click:Connect(function()
    AimMode = (AimMode == "Legit") and "Rage" or "Legit"
    ModeToggle.Text = "MODE: " .. AimMode:upper()
end)

local TeamToggle = createButton(AimTab, "TEAM CHECK: OFF", 10, 95, 160)
TeamToggle.MouseButton1Click:Connect(function()
    TeamCheck = not TeamCheck
    TeamToggle.Text = TeamCheck and "TEAM CHECK: ON" or "TEAM CHECK: OFF"
end)

local VisToggle = createButton(AimTab, "VIS CHECK: ON", 180, 95, 160)
VisToggle.MouseButton1Click:Connect(function()
    VisibleCheck = not VisibleCheck
    VisToggle.Text = VisibleCheck and "VIS CHECK: ON" or "VIS CHECK: OFF"
end)

createSlider(AimTab, "SMOOTHNESS", 10, 150, 1, 10, 3, function(v) Smoothness = v/10 end)
createSlider(AimTab, "FOV SIZE", 10, 210, 10, 500, 150, function(v) FOVSize = v end)

local FOVToggle = createButton(AimTab, "SHOW FOV: OFF", 10, 270, 160)
FOVToggle.MouseButton1Click:Connect(function()
    FOVVisible = not FOVVisible
    FOVToggle.Text = FOVVisible and "SHOW FOV: ON" or "SHOW FOV: OFF"
end)

-- ==================== ABA VISUAL ====================
local visualTitle = Instance.new("TextLabel")
visualTitle.Parent = VisualTab
visualTitle.Size = UDim2.new(1,0,0,30)
visualTitle.Position = UDim2.new(0,10,0,10)
visualTitle.Text = "👁️ VISUAL CONFIGURATIONS"
visualTitle.TextColor3 = MainColor
visualTitle.BackgroundTransparency = 1
visualTitle.Font = Enum.Font.GothamBold
visualTitle.TextSize = 18
visualTitle.TextXAlignment = Enum.TextXAlignment.Left

local ESPToggle = createButton(VisualTab, "MASTER ESP: OFF", 10, 50, 160, Color3.fromRGB(220, 40, 80))
ESPToggle.MouseButton1Click:Connect(function()
    ESPEnabled = not ESPEnabled
    ESPToggle.Text = ESPEnabled and "MASTER ESP: ON" or "MASTER ESP: OFF"
    ESPToggle.BackgroundColor3 = ESPEnabled and Color3.fromRGB(50, 200, 50) or Color3.fromRGB(220, 40, 80)
end)

local BoxToggle = createButton(VisualTab, "BOX: OFF", 10, 95, 160)
BoxToggle.MouseButton1Click:Connect(function()
    BoxEnabled = not BoxEnabled
    BoxToggle.Text = BoxEnabled and "BOX: ON" or "BOX: OFF"
end)

local NameToggle = createButton(VisualTab, "NAME: OFF", 180, 95, 160)
NameToggle.MouseButton1Click:Connect(function()
    NameEnabled = not NameEnabled
    NameToggle.Text = NameEnabled and "NAME: ON" or "NAME: OFF"
end)

local HealthToggle = createButton(VisualTab, "HEALTH: OFF", 10, 140, 160)
HealthToggle.MouseButton1Click:Connect(function()
    HealthEnabled = not HealthEnabled
    HealthToggle.Text = HealthEnabled and "HEALTH: ON" or "HEALTH: OFF"
end)

local DistToggle = createButton(VisualTab, "DISTANCE: OFF", 180, 140, 160)
DistToggle.MouseButton1Click:Connect(function()
    DistEnabled = not DistEnabled
    DistToggle.Text = DistEnabled and "DISTANCE: ON" or "DISTANCE: OFF"
end)

local SkelToggle = createButton(VisualTab, "SKELETON: OFF", 10, 185, 160)
SkelToggle.MouseButton1Click:Connect(function()
    SkeletonEnabled = not SkeletonEnabled
    SkelToggle.Text = SkeletonEnabled and "SKELETON: ON" or "SKELETON: OFF"
end)

-- ==================== ABA SETTINGS ====================
local settingsTitle = Instance.new("TextLabel")
settingsTitle.Parent = SettingsTab
settingsTitle.Size = UDim2.new(1,0,0,30)
settingsTitle.Position = UDim2.new(0,10,0,10)
settingsTitle.Text = "⚙️ GLOBAL SETTINGS"
settingsTitle.TextColor3 = MainColor
settingsTitle.BackgroundTransparency = 1
settingsTitle.Font = Enum.Font.GothamBold
settingsTitle.TextSize = 18
settingsTitle.TextXAlignment = Enum.TextXAlignment.Left

local colorDisplay = Instance.new("Frame")
colorDisplay.Parent = SettingsTab
colorDisplay.Size = UDim2.new(0,40,0,40)
colorDisplay.Position = UDim2.new(0,10,0,50)
colorDisplay.BackgroundColor3 = MainColor
addCorner(colorDisplay, 8)
addStroke(colorDisplay, 2, Color3.new(1,1,1))

local colorBtn = createButton(SettingsTab, "MUDAR COR", 60, 50, 150, Color3.fromRGB(60,60,70))
local colors = {Color3.fromRGB(0, 100, 255), Color3.fromRGB(220, 40, 80), Color3.fromRGB(50, 200, 50), Color3.fromRGB(255, 140, 0), Color3.fromRGB(180, 0, 255)}
local colorIndex = 1
colorBtn.MouseButton1Click:Connect(function()
    colorIndex = colorIndex % #colors + 1
    MainColor = colors[colorIndex]
    Top.BackgroundColor3 = MainColor
    colorDisplay.BackgroundColor3 = MainColor
    aimTitle.TextColor3 = MainColor
    visualTitle.TextColor3 = MainColor
    settingsTitle.TextColor3 = MainColor
end)

-- ==================== FOV CIRCLE ====================
local FOV = Drawing.new("Circle")
FOV.Thickness = 1
FOV.NumSides = 60
FOV.Radius = FOVSize
FOV.Filled = false
FOV.Transparency = 0.8
FOV.Color = MainColor
FOV.Visible = false

-- ==================== FUNÇÕES DO AIMBOT ====================
local function IsPlayerValid(player)
    if not player or player == LocalPlayer then return false end
    if not player.Character or not player.Character:FindFirstChild("Humanoid") then return false end
    local hum = player.Character.Humanoid
    if hum.Health <= 0 then return false end
    if TeamCheck and player.Team == LocalPlayer.Team then return false end
    if VisibleCheck and not IsPlayerVisible(player) then return false end
    return true
end

local function GetClosestPlayerToCrosshair()
    local center = Vector2.new(Camera.ViewportSize.X / 2, Camera.ViewportSize.Y / 2)
    local closest = nil
    local shortestDist = FOVSize
    for _, player in ipairs(Players:GetPlayers()) do
        if IsPlayerValid(player) then
            local char = player.Character
            local part = char:FindFirstChild(SelectedPart) or char:FindFirstChild("Head")
            if part then
                local vector, onScreen = Camera:WorldToViewportPoint(part.Position)
                if onScreen then
                    local dist = (Vector2.new(vector.X, vector.Y) - center).Magnitude
                    if dist < shortestDist then
                        shortestDist = dist
                        closest = player
                    end
                end
            end
        end
    end
    return closest
end

RunService.RenderStepped:Connect(function()
    FOV.Radius = FOVSize
    FOV.Visible = FOVVisible
    FOV.Position = Vector2.new(Camera.ViewportSize.X / 2, Camera.ViewportSize.Y / 2)
    FOV.Color = MainColor
    
    if AimEnabled then
        local target = GetClosestPlayerToCrosshair()
        if target then
            local char = target.Character
            local part = char:FindFirstChild(SelectedPart) or char:FindFirstChild("Head")
            if part then
                local targetPos = part.Position
                local camPos = Camera.CFrame.Position
                if AimMode == "Legit" then
                    local direction = (targetPos - camPos).Unit
                    local newCF = CFrame.lookAt(camPos, camPos + direction)
                    Camera.CFrame = Camera.CFrame:Lerp(newCF, Smoothness)
                else
                    Camera.CFrame = CFrame.lookAt(camPos, targetPos)
                end
            end
        end
    end
end)

-- ==================== FUNÇÕES DO ESP (CORRIGIDAS) ====================
local function CreateESPForPlayer(player)
    if ESPObjects[player] then return end
    local esp = {
        Box = Drawing.new("Square"),
        Name = Drawing.new("Text"),
        HealthText = Drawing.new("Text"),
        HealthBar = Drawing.new("Square"),
        HealthBarBack = Drawing.new("Square"),
        Distance = Drawing.new("Text"),
        Skeleton = {}
    }
    esp.Box.Thickness = 2
    esp.Box.Filled = false
    esp.Name.Size = 16
    esp.Name.Center = true
    esp.Name.Outline = true
    esp.HealthText.Size = 14
    esp.HealthText.Center = true
    esp.HealthText.Outline = true
    esp.HealthBar.Thickness = 1
    esp.HealthBar.Filled = true
    esp.HealthBarBack.Thickness = 1
    esp.HealthBarBack.Filled = true
    esp.HealthBarBack.Color = Color3.new(0,0,0)
    esp.Distance.Size = 12
    esp.Distance.Center = true
    esp.Distance.Outline = true
    ESPObjects[player] = esp
end

local function ClearESPForPlayer(player)
    if ESPObjects[player] then
        local esp = ESPObjects[player]
        esp.Box:Remove()
        esp.Name:Remove()
        esp.HealthText:Remove()
        esp.HealthBar:Remove()
        esp.HealthBarBack:Remove()
        esp.Distance:Remove()
        for _, line in ipairs(esp.Skeleton) do line:Remove() end
        ESPObjects[player] = nil
    end
end

local function DrawSkeleton(player, esp, color)
    local char = player.Character
    if not char then return end
    local parts = {
        Head = char:FindFirstChild("Head"),
        UpperTorso = char:FindFirstChild("UpperTorso") or char:FindFirstChild("Torso"),
        LowerTorso = char:FindFirstChild("LowerTorso") or char:FindFirstChild("HumanoidRootPart"),
        LeftUpperArm = char:FindFirstChild("LeftUpperArm") or char:FindFirstChild("Left Arm"),
        LeftLowerArm = char:FindFirstChild("LeftLowerArm") or char:FindFirstChild("Left Arm"),
        LeftHand = char:FindFirstChild("LeftHand") or char:FindFirstChild("Left Arm"),
        RightUpperArm = char:FindFirstChild("RightUpperArm") or char:FindFirstChild("Right Arm"),
        RightLowerArm = char:FindFirstChild("RightLowerArm") or char:FindFirstChild("Right Arm"),
        RightHand = char:FindFirstChild("RightHand") or char:FindFirstChild("Right Arm"),
        LeftUpperLeg = char:FindFirstChild("LeftUpperLeg") or char:FindFirstChild("Left Leg"),
        LeftLowerLeg = char:FindFirstChild("LeftLowerLeg") or char:FindFirstChild("Left Leg"),
        LeftFoot = char:FindFirstChild("LeftFoot") or char:FindFirstChild("Left Leg"),
        RightUpperLeg = char:FindFirstChild("RightUpperLeg") or char:FindFirstChild("Right Leg"),
        RightLowerLeg = char:FindFirstChild("RightLowerLeg") or char:FindFirstChild("Right Leg"),
        RightFoot = char:FindFirstChild("RightFoot") or char:FindFirstChild("Right Leg")
    }
    local connections = {
        {"Head", "UpperTorso"}, {"UpperTorso", "LowerTorso"},
        {"UpperTorso", "LeftUpperArm"}, {"LeftUpperArm", "LeftLowerArm"}, {"LeftLowerArm", "LeftHand"},
        {"UpperTorso", "RightUpperArm"}, {"RightUpperArm", "RightLowerArm"}, {"RightLowerArm", "RightHand"},
        {"LowerTorso", "LeftUpperLeg"}, {"LeftUpperLeg", "LeftLowerLeg"}, {"LeftLowerLeg", "LeftFoot"},
        {"LowerTorso", "RightUpperLeg"}, {"RightUpperLeg", "RightLowerLeg"}, {"RightLowerLeg", "RightFoot"}
    }
    while #esp.Skeleton < #connections do
        local line = Drawing.new("Line")
        line.Thickness = 2
        line.Transparency = 0.6
        table.insert(esp.Skeleton, line)
    end
    for i, conn in ipairs(connections) do
        local p1, p2 = parts[conn[1]], parts[conn[2]]
        if p1 and p2 then
            local pos1, vis1 = Camera:WorldToViewportPoint(p1.Position)
            local pos2, vis2 = Camera:WorldToViewportPoint(p2.Position)
            if vis1 and vis2 then
                esp.Skeleton[i].From = Vector2.new(pos1.X, pos1.Y)
                esp.Skeleton[i].To = Vector2.new(pos2.X, pos2.Y)
                esp.Skeleton[i].Color = color
                esp.Skeleton[i].Visible = true
                continue
            end
        end
        esp.Skeleton[i].Visible = false
    end
end

RunService.RenderStepped:Connect(function()
    if not ESPEnabled then
        for player, _ in pairs(ESPObjects) do ClearESPForPlayer(player) end
        return
    end
    for _, player in ipairs(Players:GetPlayers()) do
        if player ~= LocalPlayer and player.Character and player.Character:FindFirstChild("Humanoid") and player.Character.Humanoid.Health > 0 then
            if not ESPObjects[player] then CreateESPForPlayer(player) end
            local esp = ESPObjects[player]
            local char = player.Character
            local hum = char.Humanoid
            local root = char:FindFirstChild("HumanoidRootPart")
            local head = char:FindFirstChild("Head")
            if root and head then
                local rootPos, rootVis = Camera:WorldToViewportPoint(root.Position)
                local headPos, headVis = Camera:WorldToViewportPoint(head.Position)
                if rootVis and headVis then
                    local height = math.abs(headPos.Y - rootPos.Y) * 1.5
                    local width = height * 0.6
                    local boxX, boxY = rootPos.X - width/2, rootPos.Y - height/2
                    local color = IsPlayerVisible(player) and Color3.new(0,1,0) or MainColor
                    
                    esp.Box.Visible = BoxEnabled
                    if BoxEnabled then
                        esp.Box.Size = Vector2.new(width, height)
                        esp.Box.Position = Vector2.new(boxX, boxY)
                        esp.Box.Color = color
                    end
                    
                    esp.Name.Visible = NameEnabled
                    if NameEnabled then
                        esp.Name.Text = player.Name
                        esp.Name.Position = Vector2.new(rootPos.X, boxY - 20)
                        esp.Name.Color = Color3.new(1,1,1)
                    end
                    
                    esp.HealthBar.Visible = HealthEnabled
                    esp.HealthBarBack.Visible = HealthEnabled
                    if HealthEnabled then
                        local hpPct = hum.Health / hum.MaxHealth
                        esp.HealthBarBack.Size = Vector2.new(width, 4)
                        esp.HealthBarBack.Position = Vector2.new(boxX, boxY + height + 2)
                        esp.HealthBar.Size = Vector2.new(width * hpPct, 4)
                        esp.HealthBar.Position = Vector2.new(boxX, boxY + height + 2)
                        esp.HealthBar.Color = Color3.fromHSV(hpPct/3, 1, 1)
                    end
                    
                    esp.Distance.Visible = DistEnabled
                    if DistEnabled then
                        local dist = (Camera.CFrame.Position - root.Position).Magnitude
                        esp.Distance.Text = math.floor(dist) .. "m"
                        esp.Distance.Position = Vector2.new(rootPos.X, boxY + height + (HealthEnabled and 8 or 2))
                    end
                    
                    if SkeletonEnabled then DrawSkeleton(player, esp, color)
                    else for _, l in ipairs(esp.Skeleton) do l.Visible = false end end
                    continue
                end
            end
            ClearESPForPlayer(player)
        elseif ESPObjects[player] then
            ClearESPForPlayer(player)
        end
    end
end)

Players.PlayerRemoving:Connect(ClearESPForPlayer)
print("✅ EDSON SCRIPT V5 COMPLETO CARREGADO")
