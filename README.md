-- EDSON SCRIPT V6 - PROFESSIONAL ULTIMATE EDITION
-- DESIGN PREMIUM | LAYOUT CORRIGIDO | ESP LINHA ADICIONADO

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
    LineEnabled = false, -- NOVA OPÇÃO: ESP LINHA
}

-- PALETA DE CORES PROFISSIONAL
local Colors = {
    Primary = Color3.fromRGB(98, 114, 164),  -- Roxo acinzentado elegante
    Secondary = Color3.fromRGB(139, 155, 205), -- Roxo claro
    Accent = Color3.fromRGB(192, 203, 245),   -- Lilás suave
    Success = Color3.fromRGB(80, 200, 120),    -- Verde menta
    Danger = Color3.fromRGB(255, 107, 107),    -- Vermelho suave
    Background = Color3.fromRGB(22, 25, 35),   -- Azul muito escuro
    Surface = Color3.fromRGB(32, 36, 48),      -- Azul escuro
    SurfaceLight = Color3.fromRGB(42, 47, 62), -- Azul médio
    Text = Color3.fromRGB(230, 235, 245),      -- Branco azulado
    TextDim = Color3.fromRGB(160, 170, 190)    -- Cinza azulado
}

local ESPObjects = {}
local Minimized = false
local MainSize = UDim2.new(0, 600, 0, 520) -- Aumentado para acomodar nova opção
local MinSize = UDim2.new(0, 600, 0, 50)

-- ==================== FUNÇÕES DE UTILIDADE ====================
local function addCorner(obj, radius)
    local corner = Instance.new("UICorner")
    corner.CornerRadius = UDim.new(0, radius)
    corner.Parent = obj
end

local function addStroke(obj, thickness, color, transparency)
    local stroke = Instance.new("UIStroke")
    stroke.Thickness = thickness
    stroke.Color = color or Colors.TextDim
    stroke.Transparency = transparency or 0.7
    stroke.Parent = obj
end

local function addGradient(obj, color1, color2, rotation)
    local gradient = Instance.new("UIGradient")
    gradient.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0, color1),
        ColorSequenceKeypoint.new(1, color2)
    })
    gradient.Rotation = rotation or 90
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

-- ==================== INTERFACE PREMIUM ====================
local Main = Instance.new("Frame", ScreenGui)
Main.Size = MainSize
Main.Position = UDim2.new(0.5, -300, 0.5, -260)
Main.BackgroundColor3 = Colors.Background
Main.BackgroundTransparency = 0.05
Main.Active = true
Main.Draggable = true
addCorner(Main, 20)
addStroke(Main, 1.5, Colors.Primary, 0.6)

-- Efeito de brilho nas bordas
local GlowBorder = Instance.new("Frame", Main)
GlowBorder.Size = UDim2.new(1, 4, 1, 4)
GlowBorder.Position = UDim2.new(0, -2, 0, -2)
GlowBorder.BackgroundTransparency = 1
addCorner(GlowBorder, 22)
local glowStroke = Instance.new("UIStroke")
glowStroke.Thickness = 2
glowStroke.Color = Colors.Accent
glowStroke.Transparency = 0.8
glowStroke.Parent = GlowBorder

-- TOP BAR PREMIUM
local Top = Instance.new("Frame", Main)
Top.Size = UDim2.new(1, 0, 0, 70)
Top.BackgroundColor3 = Colors.Surface
Top.BackgroundTransparency = 0.1
Top.BorderSizePixel = 0
addCorner(Top, 20)
addGradient(Top, Colors.Surface, Colors.SurfaceLight, 90)

local Title = Instance.new("TextLabel", Top)
Title.Size = UDim2.new(1, -120, 1, 0)
Title.Position = UDim2.new(0, 20, 0, 0)
Title.Text = "EDSON SCRIPT V6"
Title.BackgroundTransparency = 1
Title.TextColor3 = Colors.Text
Title.Font = Enum.Font.GothamBold
Title.TextSize = 28
Title.TextXAlignment = Enum.TextXAlignment.Left
Title.TextStrokeTransparency = 0.3
Title.TextStrokeColor3 = Colors.Primary

local SubTitle = Instance.new("TextLabel", Top)
SubTitle.Size = UDim2.new(1, -120, 0, 20)
SubTitle.Position = UDim2.new(0, 20, 0.5, 12)
SubTitle.Text = "PROFESSIONAL EDITION"
SubTitle.BackgroundTransparency = 1
SubTitle.TextColor3 = Colors.TextDim
SubTitle.Font = Enum.Font.Gotham
SubTitle.TextSize = 14
SubTitle.TextXAlignment = Enum.TextXAlignment.Left

-- BOTÕES DA TOP BAR
local function createTopButton(parent, text, posX, color)
    local btn = Instance.new("TextButton", parent)
    btn.Size = UDim2.new(0, 45, 0, 45)
    btn.Position = UDim2.new(1, posX, 0.5, -22.5)
    btn.Text = text
    btn.Font = Enum.Font.GothamBold
    btn.TextSize = 24
    btn.TextColor3 = Colors.Text
    btn.BackgroundColor3 = color or Colors.SurfaceLight
    btn.BackgroundTransparency = 0.3
    btn.BorderSizePixel = 0
    addCorner(btn, 12)
    addStroke(btn, 1, Colors.TextDim, 0.5)
    
    btn.MouseEnter:Connect(function()
        TweenService:Create(btn, TweenInfo.new(0.2), {
            BackgroundTransparency = 0.1,
            BackgroundColor3 = color or Colors.Accent
        }):Play()
    end)
    
    btn.MouseLeave:Connect(function()
        TweenService:Create(btn, TweenInfo.new(0.2), {
            BackgroundTransparency = 0.3,
            BackgroundColor3 = color or Colors.SurfaceLight
        }):Play()
    end)
    
    return btn
end

local MinimizeBtn = createTopButton(Top, "−", -100, Colors.SurfaceLight)
local CloseBtn = createTopButton(Top, "✕", -45, Colors.Danger)

CloseBtn.MouseButton1Click:Connect(function()
    ScreenGui:Destroy()
end)

-- SIDE MENU
local Side = Instance.new("Frame", Main)
Side.Size = UDim2.new(0, 160, 1, -70)
Side.Position = UDim2.new(0, 0, 0, 70)
Side.BackgroundColor3 = Colors.Surface
Side.BackgroundTransparency = 0.15
Side.BorderSizePixel = 0
addCorner(Side, 16)
addGradient(Side, Colors.Surface, Color3.fromRGB(28, 32, 42), 180)

-- CONTENT AREA
local Content = Instance.new("Frame", Main)
Content.Position = UDim2.new(0, 160, 0, 70)
Content.Size = UDim2.new(1, -160, 1, -70)
Content.BackgroundColor3 = Colors.Background
Content.BackgroundTransparency = 0.2
Content.BorderSizePixel = 0
addCorner(Content, 16)

-- ABAS
local function createTab(parent)
    local tab = Instance.new("ScrollingFrame", parent)
    tab.Size = UDim2.new(1, -20, 1, -20)
    tab.Position = UDim2.new(0, 10, 0, 10)
    tab.BackgroundTransparency = 1
    tab.ScrollBarThickness = 4
    tab.ScrollBarImageColor3 = Colors.Primary
    tab.CanvasSize = UDim2.new(0, 0, 0, 850)
    tab.BorderSizePixel = 0
    tab.ScrollingEnabled = true
    tab.ScrollBarImageTransparency = 0.5
    return tab
end

local AimTab = createTab(Content)
AimTab.Visible = true

local VisualTab = createTab(Content)
VisualTab.Visible = false

local SettingsTab = createTab(Content)
SettingsTab.Visible = false

-- BOTÕES DE ABA
local function createNavButton(text, icon, pos, tab)
    local btn = Instance.new("TextButton", Side)
    btn.Size = UDim2.new(1, -20, 0, 60)
    btn.Position = UDim2.new(0, 10, 0, pos)
    btn.Text = icon .. "  " .. text
    btn.Font = Enum.Font.GothamBold
    btn.TextSize = 18
    btn.TextColor3 = Colors.TextDim
    btn.BackgroundColor3 = Colors.SurfaceLight
    btn.BackgroundTransparency = 0.3
    btn.BorderSizePixel = 0
    addCorner(btn, 14)
    addStroke(btn, 1, Colors.Primary, 0.7)
    
    btn.MouseEnter:Connect(function()
        TweenService:Create(btn, TweenInfo.new(0.2), {
            BackgroundTransparency = 0.1,
            TextColor3 = Colors.Text,
            BackgroundColor3 = Colors.Primary
        }):Play()
    end)
    
    btn.MouseLeave:Connect(function()
        TweenService:Create(btn, TweenInfo.new(0.2), {
            BackgroundTransparency = 0.3,
            TextColor3 = Colors.TextDim,
            BackgroundColor3 = Colors.SurfaceLight
        }):Play()
    end)
    
    btn.MouseButton1Click:Connect(function()
        AimTab.Visible = false
        VisualTab.Visible = false
        SettingsTab.Visible = false
        tab.Visible = true
    end)
    
    return btn
end

local AimNav = createNavButton("AIM", "🎯", 15, AimTab)
local VisualNav = createNavButton("VISUAL", "👁️", 85, VisualTab)
local SettingsNav = createNavButton("SETTINGS", "⚙️", 155, SettingsTab)

-- FUNÇÃO MINIMIZAR
MinimizeBtn.MouseButton1Click:Connect(function()
    Minimized = not Minimized
    
    if Minimized then
        TweenService:Create(Main, TweenInfo.new(0.4), {Size = MinSize}):Play()
        MinimizeBtn.Text = "+"
        Side.Visible = false
        Content.Visible = false
    else
        TweenService:Create(Main, TweenInfo.new(0.4), {Size = MainSize}):Play()
        MinimizeBtn.Text = "−"
        wait(0.2)
        Side.Visible = true
        Content.Visible = true
    end
end)

-- ==================== COMPONENTES REUTILIZÁVEIS ====================

-- FUNÇÃO PARA CRIAR SEÇÕES ORGANIZADAS
local function createSection(parent, title, yPos, height)
    local section = Instance.new("Frame", parent)
    section.Size = UDim2.new(1, -20, 0, height or 140)
    section.Position = UDim2.new(0, 10, 0, yPos)
    section.BackgroundColor3 = Colors.Surface
    section.BackgroundTransparency = 0.3
    section.BorderSizePixel = 0
    addCorner(section, 16)
    addStroke(section, 1, Colors.Primary, 0.8)
    
    local sectionTitle = Instance.new("TextLabel", section)
    sectionTitle.Size = UDim2.new(1, -20, 0, 30)
    sectionTitle.Position = UDim2.new(0, 10, 0, 5)
    sectionTitle.Text = title
    sectionTitle.BackgroundTransparency = 1
    sectionTitle.TextColor3 = Colors.Accent
    sectionTitle.Font = Enum.Font.GothamBold
    sectionTitle.TextSize = 16
    sectionTitle.TextXAlignment = Enum.TextXAlignment.Left
    
    local divider = Instance.new("Frame", section)
    divider.Size = UDim2.new(1, -20, 0, 1)
    divider.Position = UDim2.new(0, 10, 0, 35)
    divider.BackgroundColor3 = Colors.Primary
    divider.BackgroundTransparency = 0.5
    addCorner(divider, 1)
    
    return section
end

-- FUNÇÃO TOGGLE PADRÃO
local function createToggle(parent, text, x, y, key)
    local btn = Instance.new("TextButton", parent)
    btn.Size = UDim2.new(0, 140, 0, 35)
    btn.Position = UDim2.new(0, x, 0, y)
    btn.Font = Enum.Font.GothamBold
    btn.TextSize = 14
    btn.TextColor3 = Colors.Text
    btn.BackgroundColor3 = Colors.SurfaceLight
    btn.BackgroundTransparency = 0.2
    btn.BorderSizePixel = 0
    addCorner(btn, 10)
    addStroke(btn, 1, Colors.Primary, 0.6)
    
    local function update()
        btn.Text = text .. ": " .. (Config[key] and "ON" or "OFF")
        btn.BackgroundColor3 = Config[key] and Colors.Success or Colors.SurfaceLight
    end
    
    btn.MouseButton1Click:Connect(function()
        Config[key] = not Config[key]
        update()
    end)
    
    update()
    return btn
end

-- FUNÇÃO SLIDER PADRÃO
local function createSlider(parent, label, x, y, minVal, maxVal, defaultVal, callback)
    local container = Instance.new("Frame", parent)
    container.Size = UDim2.new(0, 220, 0, 50)
    container.Position = UDim2.new(0, x, 0, y)
    container.BackgroundTransparency = 1
    
    local lbl = Instance.new("TextLabel", container)
    lbl.Size = UDim2.new(1, 0, 0, 20)
    lbl.Text = label .. ": " .. defaultVal
    lbl.TextColor3 = Colors.Text
    lbl.BackgroundTransparency = 1
    lbl.Font = Enum.Font.Gotham
    lbl.TextXAlignment = Enum.TextXAlignment.Left
    
    local sliderBg = Instance.new("Frame", container)
    sliderBg.Size = UDim2.new(1, 0, 0, 6)
    sliderBg.Position = UDim2.new(0, 0, 0, 25)
    sliderBg.BackgroundColor3 = Colors.SurfaceLight
    sliderBg.BackgroundTransparency = 0.3
    addCorner(sliderBg, 3)
    addStroke(sliderBg, 1, Colors.Primary, 0.7)
    
    local fill = Instance.new("Frame", sliderBg)
    fill.Size = UDim2.new((defaultVal-minVal)/(maxVal-minVal), 0, 1, 0)
    fill.BackgroundColor3 = Colors.Primary
    addCorner(fill, 3)
    addGradient(fill, Colors.Primary, Colors.Accent, 90)
    
    local knob = Instance.new("Frame", sliderBg)
    knob.Size = UDim2.new(0, 16, 0, 16)
    knob.Position = UDim2.new(fill.Size.X.Scale, -8, -0.5, -5)
    knob.BackgroundColor3 = Colors.Text
    addCorner(knob, 8)
    addStroke(knob, 1.5, Colors.Primary, 0.3)
    
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
            local pos = math.clamp((input.Position.X - sliderBg.AbsolutePosition.X) / sliderBg.AbsoluteSize.X, 0, 1)
            fill.Size = UDim2.new(pos, 0, 1, 0)
            knob.Position = UDim2.new(pos, -8, -0.5, -5)
            local value = minVal + (pos * (maxVal - minVal))
            lbl.Text = label .. ": " .. math.floor(value)
            callback(value)
        end
    end)
    
    return container
end

-- FUNÇÃO DROPDOWN PADRÃO
local function createDropdown(parent, label, x, y, options, callback)
    local container = Instance.new("Frame", parent)
    container.Size = UDim2.new(0, 220, 0, 50)
    container.Position = UDim2.new(0, x, 0, y)
    container.BackgroundTransparency = 1
    
    local lbl = Instance.new("TextLabel", container)
    lbl.Size = UDim2.new(1, 0, 0, 20)
    lbl.Text = label
    lbl.TextColor3 = Colors.Text
    lbl.BackgroundTransparency = 1
    lbl.Font = Enum.Font.Gotham
    lbl.TextXAlignment = Enum.TextXAlignment.Left
    
    local btn = Instance.new("TextButton", container)
    btn.Size = UDim2.new(1, 0, 0, 30)
    btn.Position = UDim2.new(0, 0, 0, 20)
    btn.Text = options[1]
    btn.Font = Enum.Font.GothamBold
    btn.TextColor3 = Colors.Text
    btn.BackgroundColor3 = Colors.SurfaceLight
    btn.BackgroundTransparency = 0.2
    btn.BorderSizePixel = 0
    addCorner(btn, 10)
    addStroke(btn, 1, Colors.Primary, 0.6)
    
    local idx = 1
    btn.MouseButton1Click:Connect(function()
        idx = idx % #options + 1
        btn.Text = options[idx]
        callback(options[idx])
    end)
end

-- ==================== CONTEÚDO DA AIM TAB ====================
local yPos = 10

-- Seção 1: Aimbot Principal
local aimSection1 = createSection(AimTab, "AIMBOT PRIMARY", yPos, 130)
yPos = yPos + 140

createToggle(aimSection1, "AIMBOT", 10, 45, "AimEnabled")

local modeBtn = Instance.new("TextButton", aimSection1)
modeBtn.Size = UDim2.new(0, 140, 0, 35)
modeBtn.Position = UDim2.new(0, 160, 0, 45)
modeBtn.Text = "MODE: LEGIT"
modeBtn.Font = Enum.Font.GothamBold
modeBtn.TextColor3 = Colors.Text
modeBtn.BackgroundColor3 = Colors.SurfaceLight
modeBtn.BackgroundTransparency = 0.2
modeBtn.BorderSizePixel = 0
addCorner(modeBtn, 10)
addStroke(modeBtn, 1, Colors.Primary, 0.6)

modeBtn.MouseButton1Click:Connect(function()
    Config.AimMode = (Config.AimMode == "Legit") and "Rage" or "Legit"
    modeBtn.Text = "MODE: " .. Config.AimMode:upper()
end)

createToggle(aimSection1, "TEAM", 10, 85, "TeamCheck")
createToggle(aimSection1, "VISIBLE", 160, 85, "VisibleCheck")

-- Seção 2: FOV
local aimSection2 = createSection(AimTab, "FIELD OF VIEW", yPos, 130)
yPos = yPos + 140

createToggle(aimSection2, "SHOW FOV", 10, 45, "FOVVisible")
createSlider(aimSection2, "FOV SIZE", 160, 45, 50, 300, 150, function(v) Config.FOVSize = v end)

-- Seção 3: Avançado
local aimSection3 = createSection(AimTab, "ADVANCED", yPos, 130)
yPos = yPos + 140

createSlider(aimSection3, "SMOOTHNESS", 10, 45, 1, 20, 3, function(v) Config.Smoothness = v/10 end)
createDropdown(aimSection3, "TARGET PART", 240, 45, {"Head", "Torso", "Root"}, function(part)
    Config.SelectedPart = part == "Head" and "Head" or (part == "Torso" and "Torso" or "HumanoidRootPart")
end)

-- ==================== CONTEÚDO DA VISUAL TAB ====================
local vYPos = 10

-- Seção 1: ESP Master
local visSection1 = createSection(VisualTab, "ESP MASTER CONTROL", vYPos, 90)
vYPos = vYPos + 100

createToggle(visSection1, "MASTER ESP", 10, 45, "ESPEnabled")

-- Seção 2: Elementos ESP
local visSection2 = createSection(VisualTab, "ESP ELEMENTS", vYPos, 210) -- Aumentado para 210px
vYPos = vYPos + 220

createToggle(visSection2, "BOX", 10, 45, "BoxEnabled")
createToggle(visSection2, "NAME", 160, 45, "NameEnabled")
createToggle(visSection2, "HEALTH", 10, 85, "HealthEnabled")
createToggle(visSection2, "DISTANCE", 160, 85, "DistEnabled")
createToggle(visSection2, "SKELETON", 10, 125, "SkeletonEnabled")
createToggle(visSection2, "LINE", 160, 125, "LineEnabled") -- NOVA OPÇÃO: ESP LINHA

-- ==================== CONTEÚDO DA SETTINGS TAB ====================
local sYPos = 10

-- Seção 1: Interface
local setSection1 = createSection(SettingsTab, "INTERFACE CUSTOMIZATION", sYPos, 150)
sYPos = sYPos + 160

-- Color Picker
local colorLabel = Instance.new("TextLabel", setSection1)
colorLabel.Size = UDim2.new(0, 100, 0, 25)
colorLabel.Position = UDim2.new(0, 10, 0, 45)
colorLabel.Text = "THEME COLOR"
colorLabel.TextColor3 = Colors.Text
colorLabel.BackgroundTransparency = 1
colorLabel.Font = Enum.Font.GothamBold
colorLabel.TextXAlignment = Enum.TextXAlignment.Left

local colors = {
    {Color3.fromRGB(98, 114, 164), "ROXO"},
    {Color3.fromRGB(0, 150, 255), "AZUL"},
    {Color3.fromRGB(50, 200, 120), "VERDE"},
    {Color3.fromRGB(255, 100, 100), "VERMELHO"},
    {Color3.fromRGB(255, 170, 50), "LARANJA"}
}

local colorIdx = 1

local function updateThemeColor(color)
    Colors.Primary = color
    Colors.Secondary = color:Lerp(Color3.new(1,1,1), 0.3)
    Colors.Accent = color:Lerp(Color3.new(1,1,1), 0.5)
    
    Top.BackgroundColor3 = Colors.Surface
    glowStroke.Color = Colors.Accent
    AimTab.ScrollBarImageColor3 = Colors.Primary
    VisualTab.ScrollBarImageColor3 = Colors.Primary
    SettingsTab.ScrollBarImageColor3 = Colors.Primary
end

for i, colorData in ipairs(colors) do
    local colorBtn = Instance.new("TextButton", setSection1)
    colorBtn.Size = UDim2.new(0, 45, 0, 30)
    colorBtn.Position = UDim2.new(0, 120 + (i-1) * 55, 0, 45)
    colorBtn.Text = ""
    colorBtn.BackgroundColor3 = colorData[1]
    colorBtn.BorderSizePixel = 0
    addCorner(colorBtn, 8)
    addStroke(colorBtn, 1.5, Colors.Text, 0.3)
    
    colorBtn.MouseButton1Click:Connect(function()
        updateThemeColor(colorData[1])
    end)
end

-- ==================== LÓGICA DO ESP ====================
local function CreateESP(player)
    if ESPObjects[player] then return end
    local esp = {
        Box = Drawing.new("Square"),
        Name = Drawing.new("Text"),
        Dist = Drawing.new("Text"),
        HealthBar = Drawing.new("Square"),
        HealthBarBack = Drawing.new("Square"),
        Line = Drawing.new("Line"), -- NOVO: Linha ESP
        Skeleton = {},
        HeadCircle = Drawing.new("Circle")
    }
    
    -- Box
    esp.Box.Thickness = 2
    esp.Box.Filled = false
    
    -- Name
    esp.Name.Size = 14
    esp.Name.Center = true
    esp.Name.Outline = true
    esp.Name.Color = Colors.Text
    
    -- Distance
    esp.Dist.Size = 12
    esp.Dist.Center = true
    esp.Dist.Outline = true
    esp.Dist.Color = Colors.TextDim
    
    -- Health
    esp.HealthBar.Filled = true
    esp.HealthBarBack.Filled = true
    esp.HealthBarBack.Color = Color3.new(0,0,0)
    
    -- Head Circle
    esp.HeadCircle.Thickness = 2
    esp.HeadCircle.Filled = false
    esp.HeadCircle.NumSides = 12
    
    -- LINE ESP (NOVO)
    esp.Line.Thickness = 2
    esp.Line.Color = Colors.Primary
    esp.Line.Transparency = 0.3
    
    ESPObjects[player] = esp
end

local function ClearESP(player)
    if ESPObjects[player] then
        for _, v in pairs(ESPObjects[player]) do
            if type(v) == "table" then
                for _, l in ipairs(v) do l:Remove() end
            else
                v:Remove()
            end
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
    local head = char:FindFirstChild("Head")
    if head then
        local pos, vis = Camera:WorldToViewportPoint(head.Position)
        if vis then
            local dist = (Camera.CFrame.Position - head.Position).Magnitude
            esp.HeadCircle.Radius = math.clamp(500 / dist, 2, 15)
            esp.HeadCircle.Position = Vector2.new(pos.X, pos.Y)
            esp.HeadCircle.Color = color
            esp.HeadCircle.Visible = true
        else
            esp.HeadCircle.Visible = false
        end
    else
        esp.HeadCircle.Visible = false
    end

    while #esp.Skeleton < #SkeletonConnections do
        local l = Drawing.new("Line")
        l.Thickness = 2
        table.insert(esp.Skeleton, l)
    end
    
    for i, conn in ipairs(SkeletonConnections) do
        local p1, p2 = char:FindFirstChild(conn[1]), char:FindFirstChild(conn[2])
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

-- ==================== LOOP PRINCIPAL ====================
local FOV = Drawing.new("Circle")
FOV.Thickness = 2
FOV.NumSides = 60
FOV.Filled = false
FOV.Transparency = 0.4
FOV.Color = Colors.Primary

RunService.RenderStepped:Connect(function()
    FOV.Color = Colors.Primary
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
                
                local minX, minY = math.huge, math.huge
                local maxX, maxY = -math.huge, -math.huge
                local onScreen = false
                local rootPart = char:FindFirstChild("HumanoidRootPart") or char:FindFirstChild("Head")
                
                for _, part in ipairs(char:GetChildren()) do
                    if part:IsA("BasePart") then
                        local pos, vis = Camera:WorldToViewportPoint(part.Position)
                        if vis then
                            onScreen = true
                            minX = math.min(minX, pos.X)
                            minY = math.min(minY, pos.Y)
                            maxX = math.max(maxX, pos.X)
                            maxY = math.max(maxY, pos.Y)
                        end
                    end
                end

                if onScreen and rootPart then
                    local w, h = maxX - minX, maxY - minY
                    local color = IsPlayerVisible(player) and Colors.Success or Colors.Primary
                    
                    -- BOX ESP
                    esp.Box.Visible = Config.BoxEnabled
                    if Config.BoxEnabled then
                        esp.Box.Size = Vector2.new(w, h)
                        esp.Box.Position = Vector2.new(minX, minY)
                        esp.Box.Color = color
                    end
                    
                    -- HEALTH BAR
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
                    
                    -- NAME ESP
                    esp.Name.Visible = Config.NameEnabled
                    if Config.NameEnabled then
                        esp.Name.Text = player.Name
                        esp.Name.Position = Vector2.new(minX + w/2, minY - 16)
                    end
                    
                    -- DISTANCE ESP
                    esp.Dist.Visible = Config.DistEnabled
                    if Config.DistEnabled then
                        local d = (Camera.CFrame.Position - rootPart.Position).Magnitude
                        esp.Dist.Text = math.floor(d) .. "m"
                        esp.Dist.Position = Vector2.new(minX + w/2, minY + h + 5)
                    end
                    
                    -- SKELETON ESP
                    if Config.SkeletonEnabled then
                        DrawSkeleton(char, esp, color)
                    else
                        esp.HeadCircle.Visible = false
                        for _, l in ipairs(esp.Skeleton) do l.Visible = false end
                    end
                    
                    -- LINE ESP (NOVO)
                    esp.Line.Visible = Config.LineEnabled
                    if Config.LineEnabled then
                        local rootPos, rootVis = Camera:WorldToViewportPoint(rootPart.Position)
                        if rootVis then
                            local screenCenter = Vector2.new(Camera.ViewportSize.X/2, Camera.ViewportSize.Y)
                            esp.Line.From = Vector2.new(rootPos.X, rootPos.Y)
                            esp.Line.To = screenCenter
                            esp.Line.Color = color
                        else
                            esp.Line.Visible = false
                        end
                    end
                    
                else
                    esp.Box.Visible = false
                    esp.Name.Visible = false
                    esp.Dist.Visible = false
                    esp.HealthBar.Visible = false
                    esp.HealthBarBack.Visible = false
                    esp.Line.Visible = false
                    esp.HeadCircle.Visible = false
                    for _, l in ipairs(esp.Skeleton) do l.Visible = false end
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
                        if dist < shortest then
                            shortest = dist
                            target = part
                        end
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

print("✅ EDSON SCRIPT V6 - ESP LINHA ADICIONADO")
print("✅ Agora com LINE ESP (linha do chão até o jogador)")
