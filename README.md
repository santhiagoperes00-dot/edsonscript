-- EDSON SCRIPT V6 - PROFESSIONAL ULTIMATE EDITION
-- DESIGN PREMIUM | PALETA DE CORES SOFISTICADA | LAYOUT PERFEITO

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
local MainSize = UDim2.new(0, 520, 0, 450)
local MinSize = UDim2.new(0, 520, 0, 50)

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

local function addShadow(obj, transparency, offset)
    local shadow = Instance.new("ImageLabel")
    shadow.Name = "Shadow"
    shadow.Parent = obj
    shadow.BackgroundTransparency = 1
    shadow.Position = UDim2.new(0, -10, 0, -10)
    shadow.Size = UDim2.new(1, 20, 1, 20)
    shadow.Image = "rbxasset://textures/ui/GuiImagePlaceholder.png"
    shadow.ImageColor3 = Color3.new(0, 0, 0)
    shadow.ImageTransparency = transparency or 0.8
    shadow.ScaleType = Enum.ScaleType.Slice
    shadow.SliceCenter = Rect.new(10, 10, 10, 10)
    shadow.ZIndex = obj.ZIndex - 1
end

local function createBlurEffect(parent, size)
    local blur = Instance.new("Frame")
    blur.Name = "Blur"
    blur.Parent = parent
    blur.Size = UDim2.new(1, 0, 1, 0)
    blur.BackgroundColor3 = Color3.new(1, 1, 1)
    blur.BackgroundTransparency = 0.95
    blur.ZIndex = parent.ZIndex + 1
    blur.BorderSizePixel = 0
    return blur
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
Main.Position = UDim2.new(0.5, -260, 0.5, -225)
Main.BackgroundColor3 = Colors.Background
Main.BackgroundTransparency = 0.05
Main.Active = true
Main.Draggable = true
addCorner(Main, 20)
addStroke(Main, 1.5, Colors.Primary, 0.6)
addShadow(Main, 0.7)

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

-- Efeito de brilho interno
local InnerGlow = Instance.new("Frame", Main)
InnerGlow.Size = UDim2.new(1, -2, 1, -2)
InnerGlow.Position = UDim2.new(0, 1, 0, 1)
InnerGlow.BackgroundTransparency = 1
addCorner(InnerGlow, 19)
local innerStroke = Instance.new("UIStroke")
innerStroke.Thickness = 1
innerStroke.Color = Colors.Text
innerStroke.Transparency = 0.9
innerStroke.Parent = InnerGlow

-- TOP BAR PREMIUM
local Top = Instance.new("Frame", Main)
Top.Size = UDim2.new(1, 0, 0, 60)
Top.BackgroundColor3 = Colors.Surface
Top.BackgroundTransparency = 0.1
Top.BorderSizePixel = 0
addCorner(Top, 20)
addGradient(Top, Colors.Surface, Colors.SurfaceLight, 90)

-- Logo/Ícone
local Logo = Instance.new("ImageLabel", Top)
Logo.Size = UDim2.new(0, 40, 0, 40)
Logo.Position = UDim2.new(0, 15, 0.5, -20)
Logo.BackgroundTransparency = 1
Logo.Image = "rbxasset://textures/ui/GuiImagePlaceholder.png"
Logo.ImageColor3 = Colors.Accent
Logo.ImageTransparency = 0.2

local Title = Instance.new("TextLabel", Top)
Title.Size = UDim2.new(1, -120, 1, 0)
Title.Position = UDim2.new(0, 65, 0, 0)
Title.Text = "EDSON SCRIPT V6"
Title.BackgroundTransparency = 1
Title.TextColor3 = Colors.Text
Title.Font = Enum.Font.GothamBold
Title.TextSize = 24
Title.TextXAlignment = Enum.TextXAlignment.Left
Title.TextStrokeTransparency = 0.3
Title.TextStrokeColor3 = Colors.Primary

local SubTitle = Instance.new("TextLabel", Top)
SubTitle.Size = UDim2.new(1, -120, 0, 20)
SubTitle.Position = UDim2.new(0, 65, 0.5, 8)
SubTitle.Text = "PROFESSIONAL EDITION"
SubTitle.BackgroundTransparency = 1
SubTitle.TextColor3 = Colors.TextDim
SubTitle.Font = Enum.Font.Gotham
SubTitle.TextSize = 12
SubTitle.TextXAlignment = Enum.TextXAlignment.Left

-- BOTÕES DA TOP BAR
local function createTopButton(parent, text, posX, color)
    local btn = Instance.new("TextButton", parent)
    btn.Size = UDim2.new(0, 40, 0, 40)
    btn.Position = UDim2.new(1, posX, 0.5, -20)
    btn.Text = text
    btn.Font = Enum.Font.GothamBold
    btn.TextSize = 22
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

local MinimizeBtn = createTopButton(Top, "−", -90, Colors.SurfaceLight)
local CloseBtn = createTopButton(Top, "✕", -40, Colors.Danger)

CloseBtn.MouseButton1Click:Connect(function()
    ScreenGui:Destroy()
end)

-- SIDE MENU LUXUOSO
local Side = Instance.new("Frame", Main)
Side.Size = UDim2.new(0, 140, 1, -60)
Side.Position = UDim2.new(0, 0, 0, 60)
Side.BackgroundColor3 = Colors.Surface
Side.BackgroundTransparency = 0.15
Side.BorderSizePixel = 0
addCorner(Side, 16)
addGradient(Side, Colors.Surface, Color3.fromRGB(28, 32, 42), 180)

-- Linha decorativa
local SideLine = Instance.new("Frame", Side)
SideLine.Size = UDim2.new(1, -30, 0, 1)
SideLine.Position = UDim2.new(0, 15, 1, -15)
SideLine.BackgroundColor3 = Colors.Primary
SideLine.BackgroundTransparency = 0.5
addCorner(SideLine, 1)

-- CONTENT AREA COM EFEITO GLASSMORPHISM
local Content = Instance.new("Frame", Main)
Content.Position = UDim2.new(0, 140, 0, 60)
Content.Size = UDim2.new(1, -140, 1, -60)
Content.BackgroundColor3 = Colors.Background
Content.BackgroundTransparency = 0.2
Content.BorderSizePixel = 0
addCorner(Content, 16)

-- Efeito glassmorphism
local GlassEffect = Instance.new("Frame", Content)
GlassEffect.Size = UDim2.new(1, -2, 1, -2)
GlassEffect.Position = UDim2.new(0, 1, 0, 1)
GlassEffect.BackgroundColor3 = Colors.Text
GlassEffect.BackgroundTransparency = 0.95
GlassEffect.BorderSizePixel = 0
addCorner(GlassEffect, 15)

-- ABAS COM DESIGN MODERNO
local function createTab(parent)
    local tab = Instance.new("ScrollingFrame", parent)
    tab.Size = UDim2.new(1, -30, 1, -30)
    tab.Position = UDim2.new(0, 15, 0, 15)
    tab.BackgroundTransparency = 1
    tab.ScrollBarThickness = 4
    tab.ScrollBarImageColor3 = Colors.Primary
    tab.CanvasSize = UDim2.new(0, 0, 0, 600)
    tab.BorderSizePixel = 0
    tab.AutomaticCanvasSize = Enum.AutomaticSize.Y
    return tab
end

local AimTab = createTab(Content)
AimTab.Visible = true

local VisualTab = createTab(Content)
VisualTab.Visible = false

local SettingsTab = createTab(Content)
SettingsTab.Visible = false

-- BOTÕES DE ABA COM ÍCONES
local function createNavButton(text, icon, pos, tab)
    local btn = Instance.new("TextButton", Side)
    btn.Size = UDim2.new(1, -20, 0, 55)
    btn.Position = UDim2.new(0, 10, 0, pos)
    btn.Text = icon .. "  " .. text
    btn.Font = Enum.Font.GothamBold
    btn.TextSize = 16
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
        
        TweenService:Create(btn, TweenInfo.new(0.1), {
            BackgroundColor3 = Colors.Accent,
            TextColor3 = Colors.Text
        }):Play()
        wait(0.1)
        TweenService:Create(btn, TweenInfo.new(0.2), {
            BackgroundColor3 = Colors.Primary
        }):Play()
    end)
    
    return btn
end

local AimNav = createNavButton("AIM", "🎯", 15, AimTab)
local VisualNav = createNavButton("VISUAL", "👁️", 80, VisualTab)
local SettingsNav = createNavButton("SETTINGS", "⚙️", 145, SettingsTab)

-- FUNÇÃO MINIMIZAR
MinimizeBtn.MouseButton1Click:Connect(function()
    Minimized = not Minimized
    
    if Minimized then
        TweenService:Create(Main, TweenInfo.new(0.4, Enum.EasingStyle.Quad), {
            Size = MinSize
        }):Play()
        MinimizeBtn.Text = "+"
        Side.Visible = false
        Content.Visible = false
    else
        TweenService:Create(Main, TweenInfo.new(0.4, Enum.EasingStyle.Quad), {
            Size = MainSize
        }):Play()
        MinimizeBtn.Text = "−"
        wait(0.2)
        Side.Visible = true
        Content.Visible = true
    end
end)

-- FUNÇÃO PARA CRIAR CARDS
local function createCard(parent, title, yPos)
    local card = Instance.new("Frame", parent)
    card.Size = UDim2.new(1, -20, 0, 100)
    card.Position = UDim2.new(0, 10, 0, yPos)
    card.BackgroundColor3 = Colors.Surface
    card.BackgroundTransparency = 0.3
    card.BorderSizePixel = 0
    addCorner(card, 16)
    addStroke(card, 1, Colors.Primary, 0.8)
    
    local cardTitle = Instance.new("TextLabel", card)
    cardTitle.Size = UDim2.new(1, -20, 0, 30)
    cardTitle.Position = UDim2.new(0, 10, 0, 5)
    cardTitle.Text = title
    cardTitle.BackgroundTransparency = 1
    cardTitle.TextColor3 = Colors.Accent
    cardTitle.Font = Enum.Font.GothamBold
    cardTitle.TextSize = 14
    cardTitle.TextXAlignment = Enum.TextXAlignment.Left
    
    local cardLine = Instance.new("Frame", card)
    cardLine.Size = UDim2.new(1, -20, 0, 1)
    cardLine.Position = UDim2.new(0, 10, 0, 35)
    cardLine.BackgroundColor3 = Colors.Primary
    cardLine.BackgroundTransparency = 0.5
    addCorner(cardLine, 1)
    
    return card
end

-- FUNÇÃO TOGGLE PREMIUM
local function createToggle(parent, text, x, y, width, key)
    local btn = Instance.new("TextButton", parent)
    btn.Size = UDim2.new(0, width or 150, 0, 40)
    btn.Position = UDim2.new(0, x, 0, y)
    btn.Font = Enum.Font.GothamBold
    btn.TextSize = 14
    btn.TextColor3 = Colors.Text
    btn.BackgroundColor3 = Colors.SurfaceLight
    btn.BackgroundTransparency = 0.2
    btn.BorderSizePixel = 0
    addCorner(btn, 12)
    addStroke(btn, 1, Colors.Primary, 0.6)
    
    local function update()
        btn.Text = text .. ": " .. (Config[key] and "ON" or "OFF")
        btn.BackgroundColor3 = Config[key] and Colors.Success or Colors.SurfaceLight
    end
    
    btn.MouseButton1Click:Connect(function()
        Config[key] = not Config[key]
        update()
        
        TweenService:Create(btn, TweenInfo.new(0.1), {
            BackgroundColor3 = Colors.Accent,
            Size = UDim2.new(0, (width or 150) + 5, 0, 45)
        }):Play()
        
        wait(0.1)
        
        TweenService:Create(btn, TweenInfo.new(0.2), {
            BackgroundColor3 = Config[key] and Colors.Success or Colors.SurfaceLight,
            Size = UDim2.new(0, width or 150, 0, 40)
        }):Play()
    end)
    
    btn.MouseEnter:Connect(function()
        TweenService:Create(btn, TweenInfo.new(0.2), {
            BackgroundTransparency = 0.05,
            TextColor3 = Colors.Text
        }):Play()
    end)
    
    btn.MouseLeave:Connect(function()
        TweenService:Create(btn, TweenInfo.new(0.2), {
            BackgroundTransparency = 0.2
        }):Play()
    end)
    
    update()
    return btn
end

-- FUNÇÃO SLIDER PREMIUM
local function createSlider(parent, label, x, y, minVal, maxVal, defaultVal, callback)
    local container = Instance.new("Frame", parent)
    container.Size = UDim2.new(0, 200, 0, 50)
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
    knob.Size = UDim2.new(0, 18, 0, 18)
    knob.Position = UDim2.new(fill.Size.X.Scale, -9, -0.5, -6)
    knob.BackgroundColor3 = Colors.Text
    addCorner(knob, 9)
    addStroke(knob, 1.5, Colors.Primary, 0.3)
    
    local dragging = false
    
    knob.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 then
            dragging = true
            TweenService:Create(knob, TweenInfo.new(0.1), {
                Size = UDim2.new(0, 22, 0, 22),
                BackgroundColor3 = Colors.Accent
            }):Play()
        end
    end)
    
    UIS.InputEnded:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 then
            dragging = false
            TweenService:Create(knob, TweenInfo.new(0.2), {
                Size = UDim2.new(0, 18, 0, 18),
                BackgroundColor3 = Colors.Text
            }):Play()
        end
    end)
    
    UIS.InputChanged:Connect(function(input)
        if dragging and input.UserInputType == Enum.UserInputType.MouseMovement then
            local pos = math.clamp((input.Position.X - sliderBg.AbsolutePosition.X) / sliderBg.AbsoluteSize.X, 0, 1)
            fill.Size = UDim2.new(pos, 0, 1, 0)
            knob.Position = UDim2.new(pos, -9, -0.5, -6)
            local value = minVal + (pos * (maxVal - minVal))
            lbl.Text = label .. ": " .. math.floor(value)
            callback(value)
        end
    end)
    
    return container
end

-- FUNÇÃO PARA CRIAR DROPDOWN
local function createDropdown(parent, label, x, y, options, callback)
    local container = Instance.new("Frame", parent)
    container.Size = UDim2.new(0, 200, 0, 50)
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

-- ==================== CONTEÚDO DAS ABAS ====================

-- AIM TAB
local aimCard1 = createCard(AimTab, "AIMBOT CONFIGURATION", 10)
local aimCard2 = createCard(AimTab, "FOV SETTINGS", 120)
local aimCard3 = createCard(AimTab, "ADVANCED", 230)

-- Card 1 - Aimbot
createToggle(aimCard1, "AIMBOT", 10, 45, 160, "AimEnabled")

local modeBtn = Instance.new("TextButton", aimCard1)
modeBtn.Size = UDim2.new(0, 150, 0, 40)
modeBtn.Position = UDim2.new(0, 180, 0, 45)
modeBtn.Text = "MODE: LEGIT"
modeBtn.Font = Enum.Font.GothamBold
modeBtn.TextColor3 = Colors.Text
modeBtn.BackgroundColor3 = Colors.SurfaceLight
modeBtn.BackgroundTransparency = 0.2
modeBtn.BorderSizePixel = 0
addCorner(modeBtn, 12)
addStroke(modeBtn, 1, Colors.Primary, 0.6)

modeBtn.MouseButton1Click:Connect(function()
    Config.AimMode = (Config.AimMode == "Legit") and "Rage" or "Legit"
    modeBtn.Text = "MODE: " .. Config.AimMode:upper()
end)

createToggle(aimCard1, "TEAM", 10, 95, 100, "TeamCheck")
createToggle(aimCard1, "VISIBLE", 120, 95, 100, "VisibleCheck")

-- Card 2 - FOV
createToggle(aimCard2, "SHOW FOV", 10, 45, 160, "FOVVisible")
createSlider(aimCard2, "FOV SIZE", 180, 45, 50, 300, 150, function(v) Config.FOVSize = v end)

-- Card 3 - Advanced
createSlider(aimCard3, "SMOOTHNESS", 10, 45, 1, 20, 3, function(v) Config.Smoothness = v/10 end)
createDropdown(aimCard3, "TARGET PART", 180, 45, {"Head", "Torso", "Root"}, function(part)
    Config.SelectedPart = part == "Head" and "Head" or (part == "Torso" and "Torso" or "HumanoidRootPart")
end)

-- VISUAL TAB
local visualCard1 = createCard(VisualTab, "ESP MASTER CONTROL", 10)
local visualCard2 = createCard(VisualTab, "ESP ELEMENTS", 120)
local visualCard3 = createCard(VisualTab, "VISUAL FEATURES", 230)

createToggle(visualCard1, "MASTER ESP", 10, 45, 300, "ESPEnabled")

createToggle(visualCard2, "BOX", 10, 45, 120, "BoxEnabled")
createToggle(visualCard2, "NAME", 140, 45, 120, "NameEnabled")
createToggle(visualCard2, "HEALTH", 10, 95, 120, "HealthEnabled")
createToggle(visualCard2, "DISTANCE", 140, 95, 120, "DistEnabled")

createToggle(visualCard3, "SKELETON", 10, 45, 160, "SkeletonEnabled")

-- SETTINGS TAB
local settingsCard = createCard(SettingsTab, "INTERFACE CUSTOMIZATION", 10)

-- Color Picker
local colorPicker = Instance.new("Frame", settingsCard)
colorPicker.Size = UDim2.new(1, -20, 0, 100)
colorPicker.Position = UDim2.new(0, 10, 0, 45)
colorPicker.BackgroundTransparency = 1

local colorTitle = Instance.new("TextLabel", colorPicker)
colorTitle.Size = UDim2.new(1, 0, 0, 25)
colorTitle.Text = "THEME COLOR"
colorTitle.TextColor3 = Colors.Text
colorTitle.BackgroundTransparency = 1
colorTitle.Font = Enum.Font.GothamBold
colorTitle.TextXAlignment = Enum.TextXAlignment.Left

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
    SideLine.BackgroundColor3 = Colors.Primary
    AimTab.ScrollBarImageColor3 = Colors.Primary
    VisualTab.ScrollBarImageColor3 = Colors.Primary
    SettingsTab.ScrollBarImageColor3 = Colors.Primary
end

for i, colorData in ipairs(colors) do
    local colorBtn = Instance.new("TextButton", colorPicker)
    colorBtn.Size = UDim2.new(0, 50, 0, 30)
    colorBtn.Position = UDim2.new(0, (i-1) * 60, 0, 30)
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
        Skeleton = {},
        HeadCircle = Drawing.new("Circle")
    }
    esp.Box.Thickness = 2
    esp.Box.Filled = false
    esp.Name.Size = 14
    esp.Name.Center = true
    esp.Name.Outline = true
    esp.Name.Color = Colors.Text
    esp.Dist.Size = 12
    esp.Dist.Center = true
    esp.Dist.Outline = true
    esp.Dist.Color = Colors.TextDim
    esp.HealthBar.Filled = true
    esp.HealthBarBack.Filled = true
    esp.HealthBarBack.Color = Color3.new(0,0,0)
    esp.HeadCircle.Thickness = 2
    esp.HeadCircle.Filled = false
    esp.HeadCircle.NumSides = 12
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

                if onScreen then
                    local w, h = maxX - minX, maxY - minY
                    local color = IsPlayerVisible(player) and Colors.Success or Colors.Primary
                    
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

print("✅ EDSON SCRIPT V6 - PROFESSIONAL ULTIMATE EDITION CARREGADO")
print("✅ DESIGN PREMIUM | PALETA SOFISTICADA | LAYOUT PERFEITO")
