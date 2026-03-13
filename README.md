-- EDSON SCRIPT V5 - ULTIMATE EDITION
-- COR: AZUL FORTE | ESP DETALHADO | BOX CORRIGIDA

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

-- VARIÁVEIS ESP
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

-- AIM MODE (Linha 1)
local legitBtn = createButton(AimTab, "LEGIT", 10, 50, 130, Color3.fromRGB(0,150,0))
local rageBtn = createButton(AimTab, "RAGE", 150, 50, 130, Color3.fromRGB(150,0,0))

-- AIM TOGGLE (Linha 2)
local aimToggle = createButton(AimTab, "🔫 AIMBOT: OFF", 10, 100, 270, Color3.fromRGB(60,60,70))

aimToggle.MouseButton1Click:Connect(function()
    AimEnabled = not AimEnabled
    aimToggle.Text = AimEnabled and "🔫 AIMBOT: ON" or "🔫 AIMBOT: OFF"
    aimToggle.BackgroundColor3 = AimEnabled and Color3.fromRGB(0,150,0) or Color3.fromRGB(60,60,70)
end)

-- TEAM CHECK + VISIBLE CHECK (Linha 3)
local teamToggle = createButton(AimTab, "🛡️ TEAM: OFF", 10, 150, 130, Color3.fromRGB(60,60,70))
local visibleToggle = createButton(AimTab, "👁️ VISIBLE: ON", 150, 150, 130, Color3.fromRGB(0,150,0))

teamToggle.MouseButton1Click:Connect(function()
    TeamCheck = not TeamCheck
    teamToggle.Text = TeamCheck and "🛡️ TEAM: ON" or "🛡️ TEAM: OFF"
    teamToggle.BackgroundColor3 = TeamCheck and Color3.fromRGB(0,150,0) or Color3.fromRGB(60,60,70)
end)

visibleToggle.MouseButton1Click:Connect(function()
    VisibleCheck = not VisibleCheck
    visibleToggle.Text = VisibleCheck and "👁️ VISIBLE: ON" or "👁️ VISIBLE: OFF"
    visibleToggle.BackgroundColor3 = VisibleCheck and Color3.fromRGB(0,150,0) or Color3.fromRGB(60,60,70)
end)

-- TARGET PART + FOV TOGGLE (Linha 4)
local partLabel = Instance.new("TextLabel")
partLabel.Parent = AimTab
partLabel.Size = UDim2.new(0,40,0,25)
partLabel.Position = UDim2.new(0,10,0,200)
partLabel.Text = "PART:"
partLabel.TextColor3 = Color3.new(1,1,1)
partLabel.BackgroundTransparency = 1

local partBtn = createButton(AimTab, "Head", 55, 200, 85, Color3.fromRGB(80,80,90))
local fovToggle = createButton(AimTab, "🔵 FOV: OFF", 150, 200, 130, Color3.fromRGB(60,60,70))

local parts = {"Head", "Root"}
local currentPart = 1

partBtn.MouseButton1Click:Connect(function()
    currentPart = currentPart % #parts + 1
    SelectedPart = currentPart == 1 and "Head" or "HumanoidRootPart"
    partBtn.Text = SelectedPart == "Head" and "Head" or "Root"
end)

-- FOV CIRCLE
local FOV = Instance.new("Frame")
FOV.Parent = ScreenGui
FOV.Size = UDim2.new(0,150,0,150)
FOV.Position = UDim2.new(0.5,-75,0.5,-75)
FOV.BackgroundTransparency = 1
FOV.BorderColor3 = MainColor
FOV.BorderSizePixel = 2
FOV.Visible = false
FOV.ZIndex = 10
addCorner(FOV, 75)

fovToggle.MouseButton1Click:Connect(function()
    FOVVisible = not FOVVisible
    FOV.Visible = FOVVisible
    fovToggle.Text = FOVVisible and "🔵 FOV: ON" or "🔵 FOV: OFF"
    fovToggle.BackgroundColor3 = FOVVisible and Color3.fromRGB(0,150,0) or Color3.fromRGB(60,60,70)
end)

-- FOV SLIDER
createSlider(AimTab, "FOV SIZE", 10, 240, 50, 250, 150, function(val)
    FOVSize = val
    FOV.Size = UDim2.new(0,val,0,val)
    FOV.Position = UDim2.new(0.5,-val/2,0.5,-val/2)
end)

-- SMOOTHNESS SLIDER
createSlider(AimTab, "SMOOTHNESS", 10, 300, 0.1, 1, 0.3, function(val)
    Smoothness = val
end)

-- AIM MODE SWITCH
legitBtn.MouseButton1Click:Connect(function()
    AimMode = "Legit"
    legitBtn.BackgroundColor3 = Color3.fromRGB(0,150,0)
    rageBtn.BackgroundColor3 = Color3.fromRGB(150,0,0)
end)

rageBtn.MouseButton1Click:Connect(function()
    AimMode = "Rage"
    rageBtn.BackgroundColor3 = Color3.fromRGB(0,150,0)
    legitBtn.BackgroundColor3 = Color3.fromRGB(150,0,0)
end)

-- ==================== ABA VISUAL ====================
local visualTitle = Instance.new("TextLabel")
visualTitle.Parent = VisualTab
visualTitle.Size = UDim2.new(1,0,0,30)
visualTitle.Position = UDim2.new(0,10,0,10)
visualTitle.Text = "👁️ ESP CONFIGURATIONS"
visualTitle.TextColor3 = MainColor
visualTitle.BackgroundTransparency = 1
visualTitle.Font = Enum.Font.GothamBold
visualTitle.TextSize = 18
visualTitle.TextXAlignment = Enum.TextXAlignment.Left

-- ESP TOGGLE (Linha 1)
local espToggle = createButton(VisualTab, "🔄 ESP: OFF", 10, 50, 270, Color3.fromRGB(60,60,70))

espToggle.MouseButton1Click:Connect(function()
    ESPEnabled = not ESPEnabled
    espToggle.Text = ESPEnabled and "🔄 ESP: ON" or "🔄 ESP: OFF"
    espToggle.BackgroundColor3 = ESPEnabled and Color3.fromRGB(0,150,0) or Color3.fromRGB(60,60,70)
    
    if ESPEnabled then
        CreateESPForAll()
    else
        ClearAllESP()
    end
end)

-- BOX + NAME (Linha 2)
local boxToggle = createButton(VisualTab, "📦 BOX: ON", 10, 100, 130, Color3.fromRGB(0,150,0))
local nameToggle = createButton(VisualTab, "🏷️ NAME: ON", 150, 100, 130, Color3.fromRGB(0,150,0))
local BoxEnabled = true
local NameEnabled = true

boxToggle.MouseButton1Click:Connect(function()
    BoxEnabled = not BoxEnabled
    boxToggle.Text = BoxEnabled and "📦 BOX: ON" or "📦 BOX: OFF"
    boxToggle.BackgroundColor3 = BoxEnabled and Color3.fromRGB(0,150,0) or Color3.fromRGB(60,60,70)
end)

nameToggle.MouseButton1Click:Connect(function()
    NameEnabled = not NameEnabled
    nameToggle.Text = NameEnabled and "🏷️ NAME: ON" or "🏷️ NAME: OFF"
    nameToggle.BackgroundColor3 = NameEnabled and Color3.fromRGB(0,150,0) or Color3.fromRGB(60,60,70)
end)

-- HEALTH + DISTANCE (Linha 3)
local healthToggle = createButton(VisualTab, "❤️ HEALTH: ON", 10, 150, 130, Color3.fromRGB(0,150,0))
local distToggle = createButton(VisualTab, "📏 DIST: ON", 150, 150, 130, Color3.fromRGB(0,150,0))
local HealthEnabled = true
local DistEnabled = true

healthToggle.MouseButton1Click:Connect(function()
    HealthEnabled = not HealthEnabled
    healthToggle.Text = HealthEnabled and "❤️ HEALTH: ON" or "❤️ HEALTH: OFF"
    healthToggle.BackgroundColor3 = HealthEnabled and Color3.fromRGB(0,150,0) or Color3.fromRGB(60,60,70)
end)

distToggle.MouseButton1Click:Connect(function()
    DistEnabled = not DistEnabled
    distToggle.Text = DistEnabled and "📏 DIST: ON" or "📏 DIST: OFF"
    distToggle.BackgroundColor3 = DistEnabled and Color3.fromRGB(0,150,0) or Color3.fromRGB(60,60,70)
end)

-- SKELETON TOGGLE (Linha 4)
local skeletonToggle = createButton(VisualTab, "🦴 SKELETON: OFF", 10, 200, 270, Color3.fromRGB(60,60,70))
local SkeletonEnabled = false

skeletonToggle.MouseButton1Click:Connect(function()
    SkeletonEnabled = not SkeletonEnabled
    skeletonToggle.Text = SkeletonEnabled and "🦴 SKELETON: ON" or "🦴 SKELETON: OFF"
    skeletonToggle.BackgroundColor3 = SkeletonEnabled and Color3.fromRGB(0,150,0) or Color3.fromRGB(60,60,70)
end)

-- ==================== ABA SETTINGS ====================
local settingsTitle = Instance.new("TextLabel")
settingsTitle.Parent = SettingsTab
settingsTitle.Size = UDim2.new(1,0,0,30)
settingsTitle.Position = UDim2.new(0,10,0,10)
settingsTitle.Text = "⚙️ CONFIGURAÇÕES"
settingsTitle.TextColor3 = MainColor
settingsTitle.BackgroundTransparency = 1
settingsTitle.Font = Enum.Font.GothamBold
settingsTitle.TextSize = 18
settingsTitle.TextXAlignment = Enum.TextXAlignment.Left

-- COR DO PAINEL
local colorDisplay = Instance.new("Frame")
colorDisplay.Parent = SettingsTab
colorDisplay.Size = UDim2.new(0,40,0,40)
colorDisplay.Position = UDim2.new(0,10,0,50)
colorDisplay.BackgroundColor3 = MainColor
addCorner(colorDisplay, 8)
addStroke(colorDisplay, 2, Color3.new(1,1,1))

local colorBtn = createButton(SettingsTab, "MUDAR COR", 60, 50, 150, Color3.fromRGB(60,60,70))

local colors = {
    Color3.fromRGB(0, 100, 255),  -- Azul Forte (principal)
    Color3.fromRGB(220, 40, 80),  -- Rosa
    Color3.fromRGB(50, 200, 50),  -- Verde
    Color3.fromRGB(255, 140, 0),  -- Laranja
    Color3.fromRGB(180, 0, 255)   -- Roxo
}
local colorIndex = 1

colorBtn.MouseButton1Click:Connect(function()
    colorIndex = colorIndex % #colors + 1
    MainColor = colors[colorIndex]
    
    Top.BackgroundColor3 = MainColor
    colorDisplay.BackgroundColor3 = MainColor
    FOV.BorderColor3 = MainColor
    AimTab.ScrollBarImageColor3 = MainColor
    VisualTab.ScrollBarImageColor3 = MainColor
    SettingsTab.ScrollBarImageColor3 = MainColor
    aimTitle.TextColor3 = MainColor
    visualTitle.TextColor3 = MainColor
    settingsTitle.TextColor3 = MainColor
end)

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

-- AIMBOT LOOP
RunService.RenderStepped:Connect(function()
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

-- ==================== FUNÇÕES DO ESP ====================
local function CreateESPForPlayer(player)
    if ESPObjects[player] then return end
    
    local esp = {
        Box = Drawing.new("Square"),
        Name = Drawing.new("Text"),
        Health = Drawing.new("Text"),
        Distance = Drawing.new("Text"),
        Skeleton = {}
    }
    
    -- Box
    esp.Box.Visible = false
    esp.Box.Thickness = 2
    esp.Box.Color = MainColor
    esp.Box.Filled = false
    esp.Box.Transparency = 1
    
    -- Name
    esp.Name.Visible = false
    esp.Name.Size = 16
    esp.Name.Center = true
    esp.Name.Outline = true
    esp.Name.Color = Color3.new(1,1,1)
    
    -- Health
    esp.Health.Visible = false
    esp.Health.Size = 14
    esp.Health.Center = true
    esp.Health.Outline = true
    
    -- Distance
    esp.Distance.Visible = false
    esp.Distance.Size = 12
    esp.Distance.Center = true
    esp.Distance.Outline = true
    esp.Distance.Color = Color3.new(1,1,1)
    
    -- Skeleton (15 linhas para esqueleto completo)
    for i = 1, 15 do
        local line = Drawing.new("Line")
        line.Visible = false
        line.Thickness = 2
        line.Color = MainColor
        line.Transparency = 0.5
        table.insert(esp.Skeleton, line)
    end
    
    ESPObjects[player] = esp
end

local function CreateESPForAll()
    for _, player in ipairs(Players:GetPlayers()) do
        if player ~= LocalPlayer then
            CreateESPForPlayer(player)
        end
    end
end

local function ClearAllESP()
    for player, esp in pairs(ESPObjects) do
        if esp.Box then esp.Box:Remove() end
        if esp.Name then esp.Name:Remove() end
        if esp.Health then esp.Health:Remove() end
        if esp.Distance then esp.Distance:Remove() end
        for _, line in ipairs(esp.Skeleton) do
            line:Remove()
        end
    end
    ESPObjects = {}
end

-- FUNÇÃO PARA DESENHAR ESQUELETO COMPLETO
local function DrawSkeleton(player)
    local char = player.Character
    if not char then return end
    
    local esp = ESPObjects[player]
    if not esp then return end
    
    -- Mapeamento de partes do corpo (R6 e R15)
    local parts = {
        Head = char:FindFirstChild("Head"),
        Neck = char:FindFirstChild("Neck") or char:FindFirstChild("Head"),
        
        Torso = char:FindFirstChild("Torso") or char:FindFirstChild("UpperTorso"),
        Waist = char:FindFirstChild("HumanoidRootPart") or char:FindFirstChild("LowerTorso"),
        
        LeftArm = char:FindFirstChild("Left Arm") or char:FindFirstChild("LeftUpperArm"),
        LeftForearm = char:FindFirstChild("LeftForearm") or char:FindFirstChild("LeftLowerArm"),
        LeftHand = char:FindFirstChild("LeftHand") or char:FindFirstChild("Left Arm"),
        
        RightArm = char:FindFirstChild("Right Arm") or char:FindFirstChild("RightUpperArm"),
        RightForearm = char:FindFirstChild("RightForearm") or char:FindFirstChild("RightLowerArm"),
        RightHand = char:FindFirstChild("RightHand") or char:FindFirstChild("Right Arm"),
        
        LeftLeg = char:FindFirstChild("Left Leg") or char:FindFirstChild("LeftUpperLeg"),
        LeftCalf = char:FindFirstChild("LeftCalf") or char:FindFirstChild("LeftLowerLeg"),
        LeftFoot = char:FindFirstChild("LeftFoot") or char:FindFirstChild("Left Leg"),
        
        RightLeg = char:FindFirstChild("Right Leg") or char:FindFirstChild("RightUpperLeg"),
        RightCalf = char:FindFirstChild("RightCalf") or char:FindFirstChild("RightLowerLeg"),
        RightFoot = char:FindFirstChild("RightFoot") or char:FindFirstChild("Right Leg")
    }
    
    -- Verifica se tem as partes principais
    if not parts.Head or not parts.Torso then return end
    
    -- Obtém posições na tela
    local positions = {}
    local allVisible = true
    
    for name, part in pairs(parts) do
        if part then
            local pos, vis = Camera:WorldToViewportPoint(part.Position)
            positions[name] = pos
            if not vis then allVisible = false end
        end
    end
    
    if not allVisible then
        for _, line in ipairs(esp.Skeleton) do
            line.Visible = false
        end
        return
    end
    
    -- Conexões do esqueleto (15 linhas)
    local connections = {
        -- Cabeça e pescoço
        {positions.Head, positions.Neck},
        {positions.Neck, positions.Torso},
        
        -- Coluna
        {positions.Torso, positions.Waist},
        
        -- Braço esquerdo
        {positions.Torso, positions.LeftArm},
        {positions.LeftArm, positions.LeftForearm or positions.LeftArm},
        {positions.LeftForearm or positions.LeftArm, positions.LeftHand},
        
        -- Braço direito
        {positions.Torso, positions.RightArm},
        {positions.RightArm, positions.RightForearm or positions.RightArm},
        {positions.RightForearm or positions.RightArm, positions.RightHand},
        
        -- Perna esquerda
        {positions.Waist, positions.LeftLeg},
        {positions.LeftLeg, positions.LeftCalf or positions.LeftLeg},
        {positions.LeftCalf or positions.LeftLeg, positions.LeftFoot},
        
        -- Perna direita
        {positions.Waist, positions.RightLeg},
        {positions.RightLeg, positions.RightCalf or positions.RightLeg},
        {positions.RightCalf or positions.RightLeg, positions.RightFoot}
    }
    
    -- Desenha as linhas
    for i, connection in ipairs(connections) do
        if i <= #esp.Skeleton and connection[1] and connection[2] then
            esp.Skeleton[i].From = Vector2.new(connection[1].X, connection[1].Y)
            esp.Skeleton[i].To = Vector2.new(connection[2].X, connection[2].Y)
            esp.Skeleton[i].Visible = true
            esp.Skeleton[i].Color = MainColor
        end
    end
    
    -- Esconde linhas não usadas
    for i = #connections + 1, #esp.Skeleton do
        esp.Skeleton[i].Visible = false
    end
end

-- LOOP PRINCIPAL DO ESP
RunService.RenderStepped:Connect(function()
    if not ESPEnabled then 
        for _, esp in pairs(ESPObjects) do
            esp.Box.Visible = false
            esp.Name.Visible = false
            esp.Health.Visible = false
            esp.Distance.Visible = false
            for _, line in ipairs(esp.Skeleton) do
                line.Visible = false
            end
        end
        return 
    end
    
    for player, esp in pairs(ESPObjects) do
        if player and player.Character and player.Character:FindFirstChild("Humanoid") then
            local char = player.Character
            local hum = char.Humanoid
            local root = char:FindFirstChild("HumanoidRootPart")
            local head = char:FindFirstChild("Head")
            
            if root and head and hum and hum.Health > 0 then
                local rootPos, rootOnScreen = Camera:WorldToViewportPoint(root.Position)
                local headPos, headOnScreen = Camera:WorldToViewportPoint(head.Position)
                
                if rootOnScreen and headOnScreen then
                    -- Calcula tamanho do box
                    local distance = (root.Position - Camera.CFrame.Position).Magnitude
                    local boxHeight = math.clamp(5500 / distance, 45, 180)
                    local boxWidth = boxHeight * 0.55
                    
                    -- POSIÇÃO CORRETA DO BOX (dos pés à cabeça)
                    local boxY = headPos.Y - boxHeight - 5
                    local boxX = rootPos.X - boxWidth/2
                    
                    -- BOX - CORRIGIDA: agora fica ao redor do corpo
                    if BoxEnabled then
                        esp.Box.Visible = true
                        esp.Box.Size = Vector2.new(boxWidth, boxHeight)
                        esp.Box.Position = Vector2.new(boxX, boxY)
                        esp.Box.Color = MainColor
                    else
                        esp.Box.Visible = false
                    end
                    
                    -- NAME
                    if NameEnabled then
                        esp.Name.Visible = true
                        esp.Name.Text = player.Name
                        esp.Name.Position = Vector2.new(rootPos.X, boxY - 18)
                    else
                        esp.Name.Visible = false
                    end
                    
                    -- HEALTH
                    if HealthEnabled then
                        local healthPercent = hum.Health / hum.MaxHealth
                        esp.Health.Visible = true
                        esp.Health.Text = string.format("%.0f HP", hum.Health)
                        esp.Health.Position = Vector2.new(rootPos.X, boxY + boxHeight + 5)
                        esp.Health.Color = Color3.new(1 - healthPercent, healthPercent, 0)
                    else
                        esp.Health.Visible = false
                    end
                    
                    -- DISTANCE
                    if DistEnabled then
                        esp.Distance.Visible = true
                        esp.Distance.Text = math.floor(distance) .. "m"
                        esp.Distance.Position = Vector2.new(rootPos.X, boxY + boxHeight + 23)
                    else
                        esp.Distance.Visible = false
                    end
                    
                    -- SKELETON
                    if SkeletonEnabled then
                        DrawSkeleton(player)
                    else
                        for _, line in ipairs(esp.Skeleton) do
                            line.Visible = false
                        end
                    end
                else
                    esp.Box.Visible = false
                    esp.Name.Visible = false
                    esp.Health.Visible = false
                    esp.Distance.Visible = false
                    for _, line in ipairs(esp.Skeleton) do
                        line.Visible = false
                    end
                end
            else
                esp.Box.Visible = false
                esp.Name.Visible = false
                esp.Health.Visible = false
                esp.Distance.Visible = false
                for _, line in ipairs(esp.Skeleton) do
                    line.Visible = false
                end
            end
        end
    end
end)

-- EVENTOS DE JOGADOR
Players.PlayerAdded:Connect(function(player)
    player.CharacterAdded:Connect(function()
        if ESPEnabled then
            CreateESPForPlayer(player)
        end
    end)
end)

Players.PlayerRemoving:Connect(function(player)
    if ESPObjects[player] then
        local esp = ESPObjects[player]
        if esp.Box then esp.Box:Remove() end
        if esp.Name then esp.Name:Remove() end
        if esp.Health then esp.Health:Remove() end
        if esp.Distance then esp.Distance:Remove() end
        for _, line in ipairs(esp.Skeleton) do
            line:Remove()
        end
        ESPObjects[player] = nil
    end
end)

-- CRIAR ESP INICIAL
CreateESPForAll()

print("✅ EDSON SCRIPT V5 CARREGADO - COR AZUL FORTE | ESP DETALHADO")
