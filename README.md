-- EDSON SCRIPT V5 - ULTIMATE EDITION (VERSÃO DEFINITIVA)
-- COR: AZUL FORTE | ESP REALISTA COM CABEÇA | BOX AJUSTADA | VIDA NA LATERAL | BOTÕES VERDES | MENU COMPLETO
-- LAYOUT PROFISSIONAL COM FUNDO TRANSPARENTE E BOTÃO DE MINIMIZAR

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
local Minimized = false
local MainSize = UDim2.new(0, 480, 0, 400)
local MinSize = UDim2.new(0, 480, 0, 45)

-- ==================== FUNÇÕES DE UTILIDADE ====================
local function addCorner(obj, radius)
    local corner = Instance.new("UICorner")
    corner.CornerRadius = UDim.new(0, radius)
    corner.Parent = obj
end

local function addStroke(obj, thickness, color, transparency)
    local stroke = Instance.new("UIStroke")
    stroke.Thickness = thickness
    stroke.Color = color or Color3.new(0,0,0)
    stroke.Transparency = transparency or 0.5
    stroke.Parent = obj
end

local function addShadow(obj, transparency, offset)
    local shadow = Instance.new("ImageLabel")
    shadow.Name = "Shadow"
    shadow.Parent = obj
    shadow.BackgroundTransparency = 1
    shadow.Position = UDim2.new(0, -5, 0, -5)
    shadow.Size = UDim2.new(1, 10, 1, 10)
    shadow.Image = "rbxasset://textures/ui/GuiImagePlaceholder.png"
    shadow.ImageColor3 = Color3.new(0, 0, 0)
    shadow.ImageTransparency = transparency or 0.7
    shadow.ScaleType = Enum.ScaleType.Slice
    shadow.SliceCenter = Rect.new(10, 10, 10, 10)
    shadow.ZIndex = obj.ZIndex - 1
end

local function createGradient(obj, color1, color2)
    local gradient = Instance.new("UIGradient")
    gradient.Color = ColorSequence.new({ColorSequenceKeypoint.new(0, color1), ColorSequenceKeypoint.new(1, color2)})
    gradient.Rotation = 90
    gradient.Parent = obj
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
Main.Size = MainSize
Main.Position = UDim2.new(0.5, -240, 0.5, -200)
Main.BackgroundColor3 = Color3.fromRGB(15, 15, 18)
Main.BackgroundTransparency = 0.1
Main.Active = true
Main.Draggable = true
addCorner(Main, 16)
addStroke(Main, 1.5, Color3.fromRGB(80, 80, 90), 0.3)
createGradient(Main, Color3.fromRGB(25, 25, 30), Color3.fromRGB(10, 10, 12))

-- Efeito de brilho nas bordas
local Glow = Instance.new("Frame", Main)
Glow.Size = UDim2.new(1, 4, 1, 4)
Glow.Position = UDim2.new(0, -2, 0, -2)
Glow.BackgroundTransparency = 1
Glow.BorderSizePixel = 0
local glowCorner = Instance.new("UICorner")
glowCorner.CornerRadius = UDim.new(0, 18)
glowCorner.Parent = Glow
local glowStroke = Instance.new("UIStroke")
glowStroke.Thickness = 2
glowStroke.Color = MainColor
glowStroke.Transparency = 0.8
glowStroke.Parent = Glow

-- TOP BAR COM EFEITO MODERNO
local Top = Instance.new("Frame", Main)
Top.Size = UDim2.new(1, 0, 0, 50)
Top.BackgroundColor3 = MainColor
Top.BackgroundTransparency = 0.05
Top.BorderSizePixel = 0
addCorner(Top, 16)
createGradient(Top, MainColor, MainColor:Lerp(Color3.new(1,1,1), 0.2))

-- Ícone decorativo
local Icon = Instance.new("ImageLabel", Top)
Icon.Size = UDim2.new(0, 30, 0, 30)
Icon.Position = UDim2.new(0, 15, 0.5, -15)
Icon.BackgroundTransparency = 1
Icon.Image = "rbxasset://textures/ui/GuiImagePlaceholder.png"
Icon.ImageColor3 = Color3.new(1, 1, 1)
Icon.ImageTransparency = 0.2

local Title = Instance.new("TextLabel", Top)
Title.Size = UDim2.new(1, -100, 1, 0)
Title.Position = UDim2.new(0, 50, 0, 0)
Title.Text = "⚡ EDSON SCRIPT V5 ⚡"
Title.BackgroundTransparency = 1
Title.TextColor3 = Color3.new(1, 1, 1)
Title.Font = Enum.Font.GothamBold
Title.TextSize = 20
Title.TextXAlignment = Enum.TextXAlignment.Left
Title.TextStrokeTransparency = 0.5
Title.TextStrokeColor3 = Color3.new(0,0,0)

-- BOTÕES DA TOP BAR
local MinimizeBtn = Instance.new("TextButton", Top)
MinimizeBtn.Size = UDim2.new(0, 35, 0, 35)
MinimizeBtn.Position = UDim2.new(1, -80, 0.5, -17.5)
MinimizeBtn.BackgroundColor3 = Color3.fromRGB(255, 255, 255)
MinimizeBtn.BackgroundTransparency = 0.85
MinimizeBtn.Text = "−"
MinimizeBtn.TextColor3 = Color3.new(1, 1, 1)
MinimizeBtn.TextSize = 24
MinimizeBtn.Font = Enum.Font.GothamBold
addCorner(MinimizeBtn, 10)
addStroke(MinimizeBtn, 1, Color3.new(1,1,1), 0.7)

local CloseBtn = Instance.new("TextButton", Top)
CloseBtn.Size = UDim2.new(0, 35, 0, 35)
CloseBtn.Position = UDim2.new(1, -40, 0.5, -17.5)
CloseBtn.BackgroundColor3 = Color3.fromRGB(255, 70, 70)
CloseBtn.BackgroundTransparency = 0.2
CloseBtn.Text = "✕"
CloseBtn.TextColor3 = Color3.new(1, 1, 1)
CloseBtn.TextSize = 18
CloseBtn.Font = Enum.Font.GothamBold
addCorner(CloseBtn, 10)
addStroke(CloseBtn, 1, Color3.new(1,1,1), 0.3)

CloseBtn.MouseButton1Click:Connect(function()
    ScreenGui:Destroy()
end)

-- FUNÇÃO MINIMIZAR
MinimizeBtn.MouseButton1Click:Connect(function()
    Minimized = not Minimized
    
    if Minimized then
        TweenService:Create(Main, TweenInfo.new(0.4, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), {
            Size = MinSize,
            BackgroundTransparency = 0.2
        }):Play()
        MinimizeBtn.Text = "+"
        Side.Visible = false
        Content.Visible = false
    else
        TweenService:Create(Main, TweenInfo.new(0.4, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), {
            Size = MainSize,
            BackgroundTransparency = 0.1
        }):Play()
        MinimizeBtn.Text = "−"
        wait(0.2)
        Side.Visible = true
        Content.Visible = true
    end
end)

-- SIDE MENU MODERNO
local Side = Instance.new("Frame", Main)
Side.Size = UDim2.new(0, 120, 1, -50)
Side.Position = UDim2.new(0, 0, 0, 50)
Side.BackgroundColor3 = Color3.fromRGB(20, 20, 24)
Side.BackgroundTransparency = 0.1
Side.BorderSizePixel = 0
addCorner(Side, 12)
createGradient(Side, Color3.fromRGB(25, 25, 30), Color3.fromRGB(15, 15, 18))

-- Linha divisória
local Divider = Instance.new("Frame", Side)
Divider.Size = UDim2.new(1, -20, 0, 1)
Divider.Position = UDim2.new(0, 10, 1, -1)
Divider.BackgroundColor3 = Color3.fromRGB(80, 80, 90)
Divider.BackgroundTransparency = 0.5
addCorner(Divider, 1)

-- CONTENT AREA
local Content = Instance.new("Frame", Main)
Content.Position = UDim2.new(0, 120, 0, 50)
Content.Size = UDim2.new(1, -120, 1, -50)
Content.BackgroundTransparency = 1

-- ABAS
local AimTab = Instance.new("ScrollingFrame", Content)
AimTab.Size = UDim2.new(1, -20, 1, -20)
AimTab.Position = UDim2.new(0, 10, 0, 10)
AimTab.BackgroundTransparency = 1
AimTab.ScrollBarThickness = 4
AimTab.ScrollBarImageColor3 = MainColor
AimTab.CanvasSize = UDim2.new(0,0,0,500)
AimTab.Visible = true
AimTab.BorderSizePixel = 0

local VisualTab = Instance.new("ScrollingFrame", Content)
VisualTab.Size = UDim2.new(1, -20, 1, -20)
VisualTab.Position = UDim2.new(0, 10, 0, 10)
VisualTab.BackgroundTransparency = 1
VisualTab.ScrollBarThickness = 4
VisualTab.ScrollBarImageColor3 = MainColor
VisualTab.CanvasSize = UDim2.new(0,0,0,500)
VisualTab.Visible = false
VisualTab.BorderSizePixel = 0

local SettingsTab = Instance.new("ScrollingFrame", Content)
SettingsTab.Size = UDim2.new(1, -20, 1, -20)
SettingsTab.Position = UDim2.new(0, 10, 0, 10)
SettingsTab.BackgroundTransparency = 1
SettingsTab.ScrollBarThickness = 4
SettingsTab.ScrollBarImageColor3 = MainColor
SettingsTab.CanvasSize = UDim2.new(0,0,0,300)
SettingsTab.Visible = false
SettingsTab.BorderSizePixel = 0

-- BOTÕES DE ABA COM EFEITO MODERNO
local function createTabBtn(text, pos, tab)
    local b = Instance.new("TextButton", Side)
    b.Size = UDim2.new(1, -20, 0, 55)
    b.Position = UDim2.new(0, 10, 0, pos)
    b.Text = text
    b.Font = Enum.Font.GothamBold
    b.TextSize = 16
    b.TextColor3 = Color3.new(0.9,0.9,0.9)
    b.BackgroundColor3 = Color3.fromRGB(30, 30, 36)
    b.BackgroundTransparency = 0.2
    b.BorderSizePixel = 0
    addCorner(b, 12)
    addStroke(b, 1, Color3.fromRGB(60, 60, 70), 0.3)
    
    -- Efeito hover
    b.MouseEnter:Connect(function()
        TweenService:Create(b, TweenInfo.new(0.2), {
            BackgroundColor3 = Color3.fromRGB(45, 45, 52),
            BackgroundTransparency = 0.1,
            TextColor3 = Color3.new(1,1,1)
        }):Play()
    end)
    b.MouseLeave:Connect(function()
        TweenService:Create(b, TweenInfo.new(0.2), {
            BackgroundColor3 = Color3.fromRGB(30, 30, 36),
            BackgroundTransparency = 0.2,
            TextColor3 = Color3.new(0.9,0.9,0.9)
        }):Play()
    end)
    
    b.MouseButton1Click:Connect(function()
        AimTab.Visible = false
        VisualTab.Visible = false
        SettingsTab.Visible = false
        tab.Visible = true
        
        -- Efeito de clique
        TweenService:Create(b, TweenInfo.new(0.1), {BackgroundColor3 = MainColor}):Play()
        wait(0.1)
        TweenService:Create(b, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(45, 45, 52)}):Play()
    end)
end

createTabBtn("🎯 AIM", 15, AimTab)
createTabBtn("👁️ VISUAL", 80, VisualTab)
createTabBtn("⚙️ SETTINGS", 145, SettingsTab)

-- FUNÇÃO TOGGLE COM EFEITO MODERNO
local function createToggle(parent, text, x, y, width, key)
    local btn = Instance.new("TextButton", parent)
    btn.Size = UDim2.new(0, width or 160, 0, 40)
    btn.Position = UDim2.new(0, x, 0, y)
    btn.Font = Enum.Font.GothamBold
    btn.TextSize = 14
    btn.TextColor3 = Color3.new(1,1,1)
    btn.BorderSizePixel = 0
    addCorner(btn, 10)
    addStroke(btn, 1, Color3.fromRGB(0,0,0), 0.3)
    
    local function update()
        btn.Text = text .. ": " .. (Config[key] and "ON" or "OFF")
        btn.BackgroundColor3 = Config[key] and OnColor or OffColor
        btn.BackgroundTransparency = 0.1
    end
    
    btn.MouseButton1Click:Connect(function()
        Config[key] = not Config[key]
        update()
        
        -- Efeito de clique
        TweenService:Create(btn, TweenInfo.new(0.1), {BackgroundTransparency = 0}):Play()
        wait(0.1)
        TweenService:Create(btn, TweenInfo.new(0.2), {BackgroundTransparency = 0.1}):Play()
    end)
    
    -- Efeito hover
    btn.MouseEnter:Connect(function()
        TweenService:Create(btn, TweenInfo.new(0.2), {BackgroundTransparency = 0}):Play()
    end)
    btn.MouseLeave:Connect(function()
        TweenService:Create(btn, TweenInfo.new(0.2), {BackgroundTransparency = 0.1}):Play()
    end)
    
    update()
end

-- FUNÇÃO SLIDER COM DESIGN MODERNO
local function createSlider(parent, label, x, y, minVal, maxVal, defaultVal, callback)
    local lbl = Instance.new("TextLabel", parent)
    lbl.Size = UDim2.new(0,200,0,20)
    lbl.Position = UDim2.new(0, x, 0, y)
    lbl.Text = label .. ": " .. defaultVal
    lbl.TextColor3 = Color3.new(1,1,1)
    lbl.BackgroundTransparency = 1
    lbl.Font = Enum.Font.Gotham
    lbl.TextXAlignment = Enum.TextXAlignment.Left
    lbl.TextStrokeTransparency = 0.5
    
    local slider = Instance.new("Frame", parent)
    slider.Size = UDim2.new(0,200,0,6)
    slider.Position = UDim2.new(0, x, 0, y + 25)
    slider.BackgroundColor3 = Color3.fromRGB(40, 40, 45)
    slider.BackgroundTransparency = 0.3
    addCorner(slider, 3)
    addStroke(slider, 1, Color3.fromRGB(0,0,0), 0.5)
    
    local fill = Instance.new("Frame", slider)
    fill.Size = UDim2.new((defaultVal-minVal)/(maxVal-minVal),0,1,0)
    fill.BackgroundColor3 = MainColor
    addCorner(fill, 3)
    createGradient(fill, MainColor, MainColor:Lerp(Color3.new(1,1,1), 0.3))
    
    local knob = Instance.new("Frame", slider)
    knob.Size = UDim2.new(0, 16, 0, 16)
    knob.Position = UDim2.new(fill.Size.X.Scale, -8, -0.5, -5)
    knob.BackgroundColor3 = MainColor
    addCorner(knob, 8)
    addStroke(knob, 1.5, Color3.new(1,1,1), 0.3)
    
    local dragging = false
    knob.InputBegan:Connect(function(input) 
        if input.UserInputType == Enum.UserInputType.MouseButton1 then 
            dragging = true
            TweenService:Create(knob, TweenInfo.new(0.1), {Size = UDim2.new(0,20,0,20)}):Play()
        end 
    end)
    
    UIS.InputEnded:Connect(function(input) 
        if input.UserInputType == Enum.UserInputType.MouseButton1 then 
            dragging = false
            TweenService:Create(knob, TweenInfo.new(0.2), {Size = UDim2.new(0,16,0,16)}):Play()
        end 
    end)
    
    UIS.InputChanged:Connect(function(input)
        if dragging and input.UserInputType == Enum.UserInputType.MouseMovement then
            local pos = math.clamp((input.Position.X - slider.AbsolutePosition.X) / slider.AbsoluteSize.X, 0, 1)
            fill.Size = UDim2.new(pos,0,1,0)
            knob.Position = UDim2.new(pos, -8, -0.5, -5)
            local value = minVal + (pos * (maxVal - minVal))
            lbl.Text = label .. ": " .. math.floor(value)
            callback(value)
        end
    end)
end

-- BOTÕES AIM
createToggle(AimTab, "AIMBOT", 10, 10, 320, "AimEnabled")

local ModeBtn = Instance.new("TextButton", AimTab)
ModeBtn.Size = UDim2.new(0, 155, 0, 40)
ModeBtn.Position = UDim2.new(0, 10, 0, 60)
ModeBtn.Text = "MODE: LEGIT"
ModeBtn.Font = Enum.Font.GothamBold
ModeBtn.TextSize = 14
ModeBtn.TextColor3 = Color3.new(1,1,1)
ModeBtn.BackgroundColor3 = Color3.fromRGB(50, 50, 55)
ModeBtn.BackgroundTransparency = 0.1
ModeBtn.BorderSizePixel = 0
addCorner(ModeBtn, 10)
addStroke(ModeBtn, 1, Color3.fromRGB(0,0,0), 0.3)

ModeBtn.MouseButton1Click:Connect(function()
    Config.AimMode = (Config.AimMode == "Legit") and "Rage" or "Legit"
    ModeBtn.Text = "MODE: " .. Config.AimMode:upper()
    
    -- Efeito de clique
    TweenService:Create(ModeBtn, TweenInfo.new(0.1), {BackgroundColor3 = MainColor}):Play()
    wait(0.1)
    TweenService:Create(ModeBtn, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(50, 50, 55)}):Play()
end)

createToggle(AimTab, "TEAM", 175, 60, 155, "TeamCheck")
createToggle(AimTab, "VISIBLE", 10, 110, 155, "VisibleCheck")
createToggle(AimTab, "SHOW FOV", 175, 110, 155, "FOVVisible")
createSlider(AimTab, "SMOOTHNESS", 10, 165, 1, 10, 3, function(v) Config.Smoothness = v/10 end)
createSlider(AimTab, "FOV SIZE", 10, 230, 10, 500, 150, function(v) Config.FOVSize = v end)

-- BOTÕES VISUAL
createToggle(VisualTab, "MASTER ESP", 10, 10, 320, "ESPEnabled")
createToggle(VisualTab, "BOX", 10, 60, 155, "BoxEnabled")
createToggle(VisualTab, "SKELETON", 175, 60, 155, "SkeletonEnabled")
createToggle(VisualTab, "NAME", 10, 110, 155, "NameEnabled")
createToggle(VisualTab, "HEALTH", 175, 110, 155, "HealthEnabled")
createToggle(VisualTab, "DISTANCE", 10, 160, 155, "DistEnabled")

-- BOTÕES SETTINGS (COLOR PICKER)
local colorBtn = Instance.new("TextButton", SettingsTab)
colorBtn.Size = UDim2.new(0, 320, 0, 45)
colorBtn.Position = UDim2.new(0, 10, 0, 10)
colorBtn.Text = "🎨 MUDAR COR DO MENU"
colorBtn.Font = Enum.Font.GothamBold
colorBtn.TextSize = 16
colorBtn.TextColor3 = Color3.new(1,1,1)
colorBtn.BackgroundColor3 = MainColor
colorBtn.BackgroundTransparency = 0.1
colorBtn.BorderSizePixel = 0
addCorner(colorBtn, 12)
addStroke(colorBtn, 1.5, Color3.new(1,1,1), 0.3)
createGradient(colorBtn, MainColor, MainColor:Lerp(Color3.new(1,1,1), 0.2))

local colors = {
    Color3.fromRGB(0, 100, 255),   -- Azul
    Color3.fromRGB(220, 40, 80),   -- Rosa
    Color3.fromRGB(50, 200, 50),   -- Verde
    Color3.fromRGB(255, 140, 0),   -- Laranja
    Color3.fromRGB(180, 0, 255)    -- Roxo
}
local colorIdx = 1

colorBtn.MouseButton1Click:Connect(function()
    colorIdx = colorIdx % #colors + 1
    MainColor = colors[colorIdx]
    Top.BackgroundColor3 = MainColor
    colorBtn.BackgroundColor3 = MainColor
    Glow.UIStroke.Color = MainColor
    
    -- Atualizar gradientes
    createGradient(Top, MainColor, MainColor:Lerp(Color3.new(1,1,1), 0.2))
    createGradient(colorBtn, MainColor, MainColor:Lerp(Color3.new(1,1,1), 0.2))
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
FOV.Thickness = 2
FOV.NumSides = 60
FOV.Filled = false
FOV.Transparency = 0.5
FOV.Color = MainColor

RunService.RenderStepped:Connect(function()
    -- Atualizar cor do FOV
    FOV.Color = MainColor
    
    FOV.Radius = Config.FOVSize
    FOV.Visible = Config.FOVVisible
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
                        esp.Box.Size = Vector2.new(w, h)
                        esp.Box.Position = Vector2.new(minX, minY)
                        esp.Box.Color = color
                    end
                    
                    esp.HealthBar.Visible = Config.HealthEnabled
                    esp.HealthBarBack.Visible = Config.HealthEnabled
                    if Config.HealthEnabled then
                        local hp = hum.Health / hum.MaxHealth
                        esp.HealthBarBack.Size = Vector2.new(4, h)
                        esp.HealthBarBack.Position = Vector2.new(minX - 6, minY)
                        esp.HealthBar.Size = Vector2.new(4, h * hp)
                        esp.HealthBar.Position = Vector2.new(minX - 6, minY + (h - h * hp))
                        esp.HealthBar.Color = Color3.fromHSV(hp/3, 1, 1)
                    end
                    
                    esp.Name.Visible = Config.NameEnabled
                    if Config.NameEnabled then
                        esp.Name.Text = player.Name
                        esp.Name.Position = Vector2.new(minX + w/2, minY - 16)
                    end
                    
                    esp.Dist.Visible = Config.DistEnabled
                    if Config.DistEnabled then
                        local d = (Camera.CFrame.Position - char.HumanoidRootPart.Position).Magnitude
                        esp.Dist.Text = math.floor(d) .. "m"
                        esp.Dist.Position = Vector2.new(minX + w/2, minY + h + 5)
                    end
                    
                    if Config.SkeletonEnabled then 
                        DrawSkeleton(char, esp, color) 
                    else
                        esp.HeadCircle.Visible = false
                        for _, l in ipairs(esp.Skeleton) do l.Visible = false end
                    end
                else 
                    ClearESP(player) 
                end
            elseif ESPObjects[player] then 
                ClearESP(player) 
            end
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
print("✅ LAYOUT PROFISSIONAL ATIVADO | BOTÃO DE MINIMIZAR | FUNDO TRANSPARENTE")
