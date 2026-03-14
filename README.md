-- ============================================================
-- EDSON MODZ V8 - ADVANCED EDITION (30KB+ FULL VERSION)
-- AIMBOT UNIVERSAL | ESP COMPLETO | LAYOUT ULTRA-ORGANIZADO
-- RAINBOW MIRROR NAME | MOBILE OPTIMIZED | SEM FLY HACK
-- Algoritmo de Aimbot baseado em Exunys Aimbot V3 (CC0 1.0)
-- ============================================================

local TweenService    = game:GetService("TweenService")
local UserInputService = game:GetService("UserInputService")
local Players         = game:GetService("Players")
local RunService      = game:GetService("RunService")
local Camera          = workspace.CurrentCamera
local LocalPlayer     = Players.LocalPlayer

-- ==================== SCREENUI PRINCIPAL ====================
local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Parent = game.CoreGui
ScreenGui.ResetOnSpawn = false
ScreenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
ScreenGui.DisplayOrder = 999

-- ==================== CONFIGURAÇÕES GLOBAIS ====================
local Config = {
    -- AIMBOT
    AimEnabled      = false,
    AimMode         = "Legit",   -- "Legit" ou "Rage"
    AimLockMode     = "Mouse",   -- "Mouse" (mousemoverel) ou "Camera" (CFrame lock)
    TeamCheck       = false,
    VisibleCheck    = false,
    SelectedPart    = "Head",
    Smoothness      = 5,         -- Legit: quanto maior, mais suave (divisor)
    Prediction      = 0.12,      -- Compensação de movimento (velocity offset)
    FOVSize         = 150,
    FOVVisible      = true,
    TriggerKey      = "MouseButton2",
    AimToggle       = false,     -- true = toggle, false = hold

    -- SPEED
    WalkSpeed       = 16,
    SpeedEnabled    = false,
    CrossWall       = false,

    -- ESP
    ESPEnabled      = false,
    BoxEnabled      = true,
    NameEnabled     = true,
    HealthEnabled   = true,
    LineEnabled     = true,
    LineOrigin      = "Bottom",  -- "Bottom" ou "Center"
    DistanceEnabled = true,
    TracerEnabled   = false,
}

-- ==================== PALETA DE CORES PREMIUM ====================
local Colors = {
    Primary     = Color3.fromRGB(130, 50, 255),
    Secondary   = Color3.fromRGB(160, 80, 255),
    Accent      = Color3.fromRGB(200, 150, 255),
    Success     = Color3.fromRGB(46, 204, 113),
    Danger      = Color3.fromRGB(231, 76, 60),
    Warning     = Color3.fromRGB(241, 196, 15),
    Background  = Color3.fromRGB(15, 15, 22),
    Surface     = Color3.fromRGB(25, 25, 35),
    SurfaceLight = Color3.fromRGB(35, 35, 45),
    Text        = Color3.fromRGB(255, 255, 255),
    TextDim     = Color3.fromRGB(180, 180, 200),
}

local ESPObjects  = {}
local Minimized   = false
local MainSize    = UDim2.new(0, 600, 0, 520)
local MinSize     = UDim2.new(0, 230, 0, 55)

-- ==================== FUNÇÕES DE UTILIDADE ====================
local function addCorner(obj, radius)
    local c = Instance.new("UICorner")
    c.CornerRadius = UDim.new(0, radius or 10)
    c.Parent = obj
    return c
end

local function addStroke(obj, thickness, color, transparency)
    local s = Instance.new("UIStroke")
    s.Thickness = thickness or 1
    s.Color = color or Colors.Primary
    s.Transparency = transparency or 0.5
    s.Parent = obj
    return s
end

local function addGradient(obj, c1, c2, rotation)
    local g = Instance.new("UIGradient")
    g.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0, c1),
        ColorSequenceKeypoint.new(1, c2)
    })
    g.Rotation = rotation or 90
    g.Parent = obj
    return g
end

local function addPadding(obj, top, bottom, left, right)
    local p = Instance.new("UIPadding")
    p.PaddingTop    = UDim.new(0, top    or 4)
    p.PaddingBottom = UDim.new(0, bottom or 4)
    p.PaddingLeft   = UDim.new(0, left   or 8)
    p.PaddingRight  = UDim.new(0, right  or 8)
    p.Parent = obj
    return p
end

-- ==================== INTERFACE PREMIUM SEMI-TRANSPARENTE ====================
local Main = Instance.new("Frame", ScreenGui)
Main.Name = "Main"
Main.Size = MainSize
Main.Position = UDim2.new(0.5, -300, 0.5, -260)
Main.BackgroundColor3 = Colors.Background
Main.BackgroundTransparency = 0.12
Main.Active = true
Main.Draggable = true
addCorner(Main, 20)
addStroke(Main, 2, Colors.Primary, 0.3)

-- Borda de brilho externa
local GlowBorder = Instance.new("Frame", Main)
GlowBorder.Size = UDim2.new(1, 6, 1, 6)
GlowBorder.Position = UDim2.new(0, -3, 0, -3)
GlowBorder.BackgroundTransparency = 1
addCorner(GlowBorder, 23)
local glowStroke = Instance.new("UIStroke")
glowStroke.Thickness = 3
glowStroke.Color = Colors.Accent
glowStroke.Transparency = 0.75
glowStroke.Parent = GlowBorder

-- Linha decorativa no topo
local TopLine = Instance.new("Frame", Main)
TopLine.Size = UDim2.new(0.6, 0, 0, 2)
TopLine.Position = UDim2.new(0.2, 0, 0, 0)
TopLine.BackgroundColor3 = Colors.Accent
TopLine.BackgroundTransparency = 0.3
TopLine.BorderSizePixel = 0
addCorner(TopLine, 2)

-- ==================== TÍTULO RAINBOW ESPELHADO ====================
local UserBtn = Instance.new("TextButton", Main)
UserBtn.Size = UDim2.new(1, -50, 0, 52)
UserBtn.Position = UDim2.new(0, 20, 0, 4)
UserBtn.Text = "✦ EDSON MODZ V8 ✦"
UserBtn.BackgroundTransparency = 1
UserBtn.TextColor3 = Color3.new(1, 1, 1)
UserBtn.Font = Enum.Font.GothamBold
UserBtn.TextSize = 22
UserBtn.TextXAlignment = Enum.TextXAlignment.Left

local RainbowGradient = Instance.new("UIGradient", UserBtn)
RainbowGradient.Color = ColorSequence.new({
    ColorSequenceKeypoint.new(0,   Color3.fromRGB(255, 0,   0)),
    ColorSequenceKeypoint.new(0.17,Color3.fromRGB(255, 165, 0)),
    ColorSequenceKeypoint.new(0.33,Color3.fromRGB(255, 255, 0)),
    ColorSequenceKeypoint.new(0.5, Color3.fromRGB(0,   255, 0)),
    ColorSequenceKeypoint.new(0.67,Color3.fromRGB(0,   0,   255)),
    ColorSequenceKeypoint.new(0.83,Color3.fromRGB(128, 0,   128)),
    ColorSequenceKeypoint.new(1,   Color3.fromRGB(255, 0,   255))
})

-- Subtítulo / versão
local SubTitle = Instance.new("TextLabel", Main)
SubTitle.Size = UDim2.new(1, -50, 0, 18)
SubTitle.Position = UDim2.new(0, 22, 0, 36)
SubTitle.Text = "ADVANCED EDITION  •  ESP + AIMBOT UNIVERSAL"
SubTitle.BackgroundTransparency = 1
SubTitle.TextColor3 = Colors.TextDim
SubTitle.Font = Enum.Font.Gotham
SubTitle.TextSize = 10
SubTitle.TextXAlignment = Enum.TextXAlignment.Left

-- Botão minimizar
local MinBtn = Instance.new("TextButton", Main)
MinBtn.Size = UDim2.new(0, 36, 0, 36)
MinBtn.Position = UDim2.new(1, -46, 0, 8)
MinBtn.Text = "—"
MinBtn.Font = Enum.Font.GothamBold
MinBtn.TextSize = 16
MinBtn.TextColor3 = Colors.Text
MinBtn.BackgroundColor3 = Colors.SurfaceLight
MinBtn.BackgroundTransparency = 0.3
addCorner(MinBtn, 10)
addStroke(MinBtn, 1, Colors.Primary, 0.6)

-- Animação Rainbow no título
RunService.RenderStepped:Connect(function()
    RainbowGradient.Offset = Vector2.new(tick() % 2 / 2, 0)
end)

-- Minimizar / Expandir
MinBtn.MouseButton1Click:Connect(function()
    Minimized = not Minimized
    if Minimized then
        TweenService:Create(Main, TweenInfo.new(0.4, Enum.EasingStyle.Back, Enum.EasingDirection.In), {Size = MinSize}):Play()
        MinBtn.Text = "+"
        task.wait(0.1)
        Main:FindFirstChild("Side").Visible = false
        Main:FindFirstChild("Content").Visible = false
        SubTitle.Visible = false
    else
        TweenService:Create(Main, TweenInfo.new(0.4, Enum.EasingStyle.Back, Enum.EasingDirection.Out), {Size = MainSize}):Play()
        MinBtn.Text = "—"
        task.wait(0.25)
        Main:FindFirstChild("Side").Visible = true
        Main:FindFirstChild("Content").Visible = true
        SubTitle.Visible = true
    end
end)

-- ==================== SIDEBAR DE NAVEGAÇÃO ====================
local Side = Instance.new("Frame", Main)
Side.Name = "Side"
Side.Size = UDim2.new(0, 155, 1, -75)
Side.Position = UDim2.new(0, 10, 0, 65)
Side.BackgroundColor3 = Colors.Surface
Side.BackgroundTransparency = 0.25
Side.BorderSizePixel = 0
addCorner(Side, 16)
addGradient(Side, Colors.Surface, Color3.fromRGB(20, 20, 32), 180)
addStroke(Side, 1, Colors.Primary, 0.7)

-- ==================== ÁREA DE CONTEÚDO ====================
local Content = Instance.new("Frame", Main)
Content.Name = "Content"
Content.Position = UDim2.new(0, 175, 0, 65)
Content.Size = UDim2.new(1, -185, 1, -75)
Content.BackgroundTransparency = 1
addCorner(Content, 16)

-- ==================== ABAS ====================
local function createTab(parent)
    local tab = Instance.new("ScrollingFrame", parent)
    tab.Size = UDim2.new(1, 0, 1, 0)
    tab.BackgroundTransparency = 1
    tab.ScrollBarThickness = 4
    tab.ScrollBarImageColor3 = Colors.Primary
    tab.CanvasSize = UDim2.new(0, 0, 0, 1200)
    tab.BorderSizePixel = 0
    tab.Visible = false
    tab.AutomaticCanvasSize = Enum.AutomaticSize.Y
    return tab
end

local AimTab    = createTab(Content); AimTab.Visible = true
local VisualTab = createTab(Content)
local MiscTab   = createTab(Content)

-- ==================== BOTÕES DE NAVEGAÇÃO ====================
local ActiveTab = AimTab
local NavButtons = {}

local function createNavButton(text, icon, yPos, tab)
    local btn = Instance.new("TextButton", Side)
    btn.Size = UDim2.new(1, -16, 0, 58)
    btn.Position = UDim2.new(0, 8, 0, yPos)
    btn.Text = icon .. "\n" .. text
    btn.Font = Enum.Font.GothamBold
    btn.TextSize = 12
    btn.TextColor3 = Colors.Text
    btn.BackgroundColor3 = Colors.SurfaceLight
    btn.BackgroundTransparency = 0.5
    btn.BorderSizePixel = 0
    addCorner(btn, 12)
    addStroke(btn, 1, Colors.Primary, 0.7)

    btn.MouseButton1Click:Connect(function()
        AimTab.Visible = false
        VisualTab.Visible = false
        MiscTab.Visible = false
        tab.Visible = true
        ActiveTab = tab
        for _, b in pairs(NavButtons) do
            TweenService:Create(b, TweenInfo.new(0.3), {BackgroundTransparency = 0.5}):Play()
        end
        TweenService:Create(btn, TweenInfo.new(0.3), {BackgroundTransparency = 0.1}):Play()
    end)
    NavButtons[#NavButtons + 1] = btn
    return btn
end

createNavButton("AIMBOT", "🎯", 12,  AimTab)
createNavButton("VISUAL", "👁️", 80,  VisualTab)
createNavButton("MISC",   "⚙️", 148, MiscTab)

-- Ativa o primeiro botão visualmente
TweenService:Create(NavButtons[1], TweenInfo.new(0.3), {BackgroundTransparency = 0.1}):Play()

-- Créditos na sidebar
local CredLabel = Instance.new("TextLabel", Side)
CredLabel.Size = UDim2.new(1, -10, 0, 30)
CredLabel.Position = UDim2.new(0, 5, 1, -35)
CredLabel.Text = "by EDSON MODZ"
CredLabel.TextColor3 = Colors.TextDim
CredLabel.Font = Enum.Font.Gotham
CredLabel.TextSize = 10
CredLabel.BackgroundTransparency = 1

-- ==================== COMPONENTES PREMIUM ====================
local function createSection(parent, title, height)
    local section = Instance.new("Frame", parent)
    section.Size = UDim2.new(1, -12, 0, height or 150)
    section.BackgroundColor3 = Colors.Surface
    section.BackgroundTransparency = 0.35
    section.BorderSizePixel = 0
    addCorner(section, 14)
    addStroke(section, 1, Colors.Primary, 0.75)

    local sTitle = Instance.new("TextLabel", section)
    sTitle.Size = UDim2.new(1, -16, 0, 28)
    sTitle.Position = UDim2.new(0, 8, 0, 4)
    sTitle.Text = "▸  " .. title
    sTitle.TextColor3 = Colors.Accent
    sTitle.Font = Enum.Font.GothamBold
    sTitle.TextSize = 13
    sTitle.BackgroundTransparency = 1
    sTitle.TextXAlignment = Enum.TextXAlignment.Left

    local divider = Instance.new("Frame", section)
    divider.Size = UDim2.new(1, -16, 0, 1)
    divider.Position = UDim2.new(0, 8, 0, 32)
    divider.BackgroundColor3 = Colors.Primary
    divider.BackgroundTransparency = 0.7
    divider.BorderSizePixel = 0

    return section
end

local function createToggle(parent, text, x, y, key, callback)
    local btn = Instance.new("TextButton", parent)
    btn.Size = UDim2.new(0, 178, 0, 38)
    btn.Position = UDim2.new(0, x, 0, y)
    btn.Font = Enum.Font.GothamBold
    btn.TextColor3 = Colors.Text
    btn.TextSize = 11
    btn.BorderSizePixel = 0
    addCorner(btn, 10)
    addStroke(btn, 1, Colors.Primary, 0.6)

    local indicator = Instance.new("Frame", btn)
    indicator.Size = UDim2.new(0, 8, 0, 8)
    indicator.Position = UDim2.new(0, 8, 0.5, -4)
    indicator.BorderSizePixel = 0
    addCorner(indicator, 4)

    local function update()
        local on = Config[key]
        btn.Text = "  " .. text .. ": " .. (on and "ON" or "OFF")
        TweenService:Create(btn, TweenInfo.new(0.35), {
            BackgroundColor3 = on and Colors.Success or Colors.Danger,
            BackgroundTransparency = 0.2
        }):Play()
        TweenService:Create(indicator, TweenInfo.new(0.35), {
            BackgroundColor3 = on and Color3.fromRGB(255, 255, 255) or Color3.fromRGB(100, 100, 100)
        }):Play()
    end

    btn.MouseButton1Click:Connect(function()
        Config[key] = not Config[key]
        update()
        if callback then callback(Config[key]) end
    end)
    update()
    return btn
end

local function createSlider(parent, label, x, y, minV, maxV, default, key, callback)
    local frame = Instance.new("Frame", parent)
    frame.Size = UDim2.new(0, 360, 0, 58)
    frame.Position = UDim2.new(0, x, 0, y)
    frame.BackgroundTransparency = 1

    local lbl = Instance.new("TextLabel", frame)
    lbl.Size = UDim2.new(1, 0, 0, 20)
    lbl.Text = label .. ":  " .. default
    lbl.TextColor3 = Colors.Text
    lbl.BackgroundTransparency = 1
    lbl.Font = Enum.Font.Gotham
    lbl.TextSize = 11
    lbl.TextXAlignment = Enum.TextXAlignment.Left

    local track = Instance.new("Frame", frame)
    track.Size = UDim2.new(1, 0, 0, 6)
    track.Position = UDim2.new(0, 0, 0, 36)
    track.BackgroundColor3 = Colors.SurfaceLight
    track.BorderSizePixel = 0
    addCorner(track, 3)

    local fill = Instance.new("Frame", track)
    fill.Size = UDim2.new((default - minV) / (maxV - minV), 0, 1, 0)
    fill.BackgroundColor3 = Colors.Primary
    fill.BorderSizePixel = 0
    addCorner(fill, 3)
    addGradient(fill, Colors.Primary, Colors.Accent, 0)

    local knob = Instance.new("Frame", track)
    knob.Size = UDim2.new(0, 18, 0, 18)
    knob.Position = UDim2.new(fill.Size.X.Scale, -9, 0.5, -9)
    knob.BackgroundColor3 = Color3.fromRGB(255, 255, 255)
    knob.BorderSizePixel = 0
    addCorner(knob, 9)
    addStroke(knob, 2, Colors.Primary, 0.2)

    local dragging = false
    knob.InputBegan:Connect(function(i)
        if i.UserInputType == Enum.UserInputType.MouseButton1 or i.UserInputType == Enum.UserInputType.Touch then
            dragging = true
        end
    end)
    knob.InputEnded:Connect(function(i)
        if i.UserInputType == Enum.UserInputType.MouseButton1 or i.UserInputType == Enum.UserInputType.Touch then
            dragging = false
        end
    end)
    UserInputService.InputChanged:Connect(function(i)
        if dragging and (i.UserInputType == Enum.UserInputType.MouseMovement or i.UserInputType == Enum.UserInputType.Touch) then
            local newX = math.clamp((i.Position.X - track.AbsolutePosition.X) / track.AbsoluteSize.X, 0, 1)
            local value = math.floor(minV + (maxV - minV) * newX + 0.5)
            Config[key] = value
            lbl.Text = label .. ":  " .. value
            fill.Size = UDim2.new(newX, 0, 1, 0)
            knob.Position = UDim2.new(newX, -9, 0.5, -9)
            if callback then callback(value) end
        end
    end)
    return frame
end

local function createDropdown(parent, label, x, y, options, key)
    local frame = Instance.new("Frame", parent)
    frame.Size = UDim2.new(0, 178, 0, 38)
    frame.Position = UDim2.new(0, x, 0, y)
    frame.BackgroundColor3 = Colors.SurfaceLight
    frame.BackgroundTransparency = 0.3
    frame.BorderSizePixel = 0
    addCorner(frame, 10)
    addStroke(frame, 1, Colors.Primary, 0.6)

    local lbl = Instance.new("TextButton", frame)
    lbl.Size = UDim2.new(1, 0, 1, 0)
    lbl.Text = label .. ": " .. Config[key]
    lbl.TextColor3 = Colors.Text
    lbl.Font = Enum.Font.GothamBold
    lbl.TextSize = 11
    lbl.BackgroundTransparency = 1

    local idx = 1
    for i, v in ipairs(options) do
        if v == Config[key] then idx = i end
    end

    lbl.MouseButton1Click:Connect(function()
        idx = idx % #options + 1
        Config[key] = options[idx]
        lbl.Text = label .. ": " .. options[idx]
    end)
    return frame
end

-- ==================== LAYOUT DO AIMBOT ====================
local function buildAimLayout()
    local list = Instance.new("UIListLayout", AimTab)
    list.Padding = UDim.new(0, 8)
    list.SortOrder = Enum.SortOrder.LayoutOrder
    addPadding(AimTab, 6, 6, 6, 6)

    -- Seção: Controles Principais
    local secMain = createSection(AimTab, "CONTROLES PRINCIPAIS", 170)
    secMain.LayoutOrder = 1
    createToggle(secMain, "Master Switch",  8, 40, "AimEnabled")
    createToggle(secMain, "Team Check",   196, 40, "TeamCheck")
    createToggle(secMain, "Wall Check",     8, 88, "VisibleCheck")
    createToggle(secMain, "Show FOV",     196, 88, "FOVVisible")

    -- Modo (Legit / Rage)
    local modeBtn = Instance.new("TextButton", secMain)
    modeBtn.Size = UDim2.new(0, 178, 0, 38)
    modeBtn.Position = UDim2.new(0, 8, 0, 126)
    modeBtn.Font = Enum.Font.GothamBold
    modeBtn.TextColor3 = Colors.Text
    modeBtn.TextSize = 12
    modeBtn.BorderSizePixel = 0
    addCorner(modeBtn, 10)
    addStroke(modeBtn, 1, Colors.Primary, 0.5)
    local function updateMode()
        modeBtn.Text = "⚡ MODE: " .. Config.AimMode:upper()
        TweenService:Create(modeBtn, TweenInfo.new(0.35), {
            BackgroundColor3 = Config.AimMode == "Rage" and Colors.Danger or Colors.Primary,
            BackgroundTransparency = 0.15
        }):Play()
    end
    modeBtn.MouseButton1Click:Connect(function()
        Config.AimMode = Config.AimMode == "Legit" and "Rage" or "Legit"
        updateMode()
    end)
    updateMode()

    -- Lock Mode (Mouse / Camera)
    local lockBtn = Instance.new("TextButton", secMain)
    lockBtn.Size = UDim2.new(0, 178, 0, 38)
    lockBtn.Position = UDim2.new(0, 196, 0, 126)
    lockBtn.Font = Enum.Font.GothamBold
    lockBtn.TextColor3 = Colors.Text
    lockBtn.TextSize = 12
    lockBtn.BorderSizePixel = 0
    addCorner(lockBtn, 10)
    addStroke(lockBtn, 1, Colors.Primary, 0.5)
    local function updateLock()
        lockBtn.Text = "🔒 LOCK: " .. Config.AimLockMode:upper()
        TweenService:Create(lockBtn, TweenInfo.new(0.35), {
            BackgroundColor3 = Config.AimLockMode == "Camera" and Colors.Warning or Colors.Secondary,
            BackgroundTransparency = 0.15
        }):Play()
    end
    lockBtn.MouseButton1Click:Connect(function()
        Config.AimLockMode = Config.AimLockMode == "Mouse" and "Camera" or "Mouse"
        updateLock()
    end)
    updateLock()

    -- Seção: Configurações de Precisão
    local secPrec = createSection(AimTab, "CONFIGURAÇÕES DE PRECISÃO", 200)
    secPrec.LayoutOrder = 2
    createSlider(secPrec, "FOV Radius",   8, 40, 10, 600, Config.FOVSize,    "FOVSize")
    createSlider(secPrec, "Smoothness",   8, 108, 1, 20,  Config.Smoothness, "Smoothness")
    createSlider(secPrec, "Prediction",   8, 176, 0, 50,  math.floor(Config.Prediction * 100), "Prediction")

    -- Seção: Parte Alvo
    local secPart = createSection(AimTab, "PARTE ALVO & TECLA", 100)
    secPart.LayoutOrder = 3
    createDropdown(secPart, "Parte",  8, 40, {"Head", "HumanoidRootPart", "UpperTorso", "LowerTorso"}, "SelectedPart")
    createDropdown(secPart, "Tecla", 196, 40, {"MouseButton2", "MouseButton1", "E", "Q", "F"}, "TriggerKey")
    createToggle(secPart, "Toggle Mode", 8, 88, "AimToggle")
end

-- ==================== LAYOUT DO VISUAL (ESP) ====================
local function buildVisualLayout()
    local list = Instance.new("UIListLayout", VisualTab)
    list.Padding = UDim.new(0, 8)
    list.SortOrder = Enum.SortOrder.LayoutOrder
    addPadding(VisualTab, 6, 6, 6, 6)

    -- Seção: ESP Geral
    local secESP = createSection(VisualTab, "ESP - CONFIGURAÇÕES GERAIS", 130)
    secESP.LayoutOrder = 1
    createToggle(secESP, "ESP Master",   8, 40, "ESPEnabled")
    createToggle(secESP, "Box ESP",    196, 40, "BoxEnabled")
    createToggle(secESP, "Nome",         8, 88, "NameEnabled")
    createToggle(secESP, "Vida",       196, 88, "HealthEnabled")

    -- Seção: Linhas e Tracer
    local secLines = createSection(VisualTab, "LINHAS & TRACER", 130)
    secLines.LayoutOrder = 2
    createToggle(secLines, "Linha",       8, 40, "LineEnabled")
    createToggle(secLines, "Distância", 196, 40, "DistanceEnabled")
    createDropdown(secLines, "Origem",    8, 88, {"Bottom", "Center"}, "LineOrigin")
end

-- ==================== LAYOUT DO MISC ====================
local function buildMiscLayout()
    local list = Instance.new("UIListLayout", MiscTab)
    list.Padding = UDim.new(0, 8)
    list.SortOrder = Enum.SortOrder.LayoutOrder
    addPadding(MiscTab, 6, 6, 6, 6)

    -- Seção: Movimento
    local secMove = createSection(MiscTab, "MOVIMENTO & FÍSICA", 170)
    secMove.LayoutOrder = 1
    createToggle(secMove, "Speed Hack",   8, 40, "SpeedEnabled")
    createToggle(secMove, "Cross Wall", 196, 40, "CrossWall")
    createSlider(secMove, "Walk Speed",   8, 88, 16, 250, Config.WalkSpeed, "WalkSpeed")

    -- Seção: Informações
    local secInfo = createSection(MiscTab, "INFORMAÇÕES DO SISTEMA", 130)
    secInfo.LayoutOrder = 2

    local infoLbl = Instance.new("TextLabel", secInfo)
    infoLbl.Size = UDim2.new(1, -16, 0, 80)
    infoLbl.Position = UDim2.new(0, 8, 0, 38)
    infoLbl.BackgroundTransparency = 1
    infoLbl.TextColor3 = Colors.TextDim
    infoLbl.Font = Enum.Font.Gotham
    infoLbl.TextSize = 11
    infoLbl.TextXAlignment = Enum.TextXAlignment.Left
    infoLbl.TextYAlignment = Enum.TextYAlignment.Top
    infoLbl.TextWrapped = true
    infoLbl.RichText = true

    RunService.RenderStepped:Connect(function()
        local char = LocalPlayer.Character
        local hum  = char and char:FindFirstChildOfClass("Humanoid")
        local fps  = math.floor(1 / RunService.RenderStepped:Wait() * 100) / 100
        infoLbl.Text = string.format(
            "<b>Jogador:</b> %s\n<b>Vida:</b> %s\n<b>Jogo:</b> %s\n<b>Players:</b> %d",
            LocalPlayer.Name,
            hum and math.floor(hum.Health) or "?",
            game.Name,
            #Players:GetPlayers()
        )
    end)
end

buildAimLayout()
buildVisualLayout()
buildMiscLayout()

-- ==================== AIMBOT UNIVERSAL - ALGORITMO AVANÇADO ====================
-- Baseado em Exunys Aimbot V3 (CC0 1.0) com melhorias proprietárias

local FOV_Circle = Drawing.new("Circle")
FOV_Circle.Visible = false
FOV_Circle.Filled = false
FOV_Circle.Thickness = 1.5
FOV_Circle.Color = Colors.Primary
FOV_Circle.NumSides = 64

local FOV_Outline = Drawing.new("Circle")
FOV_Outline.Visible = false
FOV_Outline.Filled = false
FOV_Outline.Thickness = 3
FOV_Outline.Color = Color3.fromRGB(0, 0, 0)
FOV_Outline.NumSides = 64

local AimRunning   = false
local AimLocked    = nil
local AimAnimation = nil

-- Verifica visibilidade (Wall Check)
local function IsVisible(target)
    if not target or not target.Character then return false end
    local part = target.Character:FindFirstChild(Config.SelectedPart)
    if not part then return false end
    local char = LocalPlayer.Character
    local blacklist = {}
    if char then
        for _, v in pairs(char:GetDescendants()) do
            blacklist[#blacklist + 1] = v
        end
    end
    for _, v in pairs(target.Character:GetDescendants()) do
        blacklist[#blacklist + 1] = v
    end
    local obscuring = Camera:GetPartsObscuringTarget({part.Position}, blacklist)
    return #obscuring == 0
end

-- Obtém o jogador mais próximo do centro do FOV
local function GetClosestPlayer()
    local closest, closestDist = nil, Config.FOVSize

    for _, plr in ipairs(Players:GetPlayers()) do
        if plr == LocalPlayer then continue end
        if Config.TeamCheck and plr.Team == LocalPlayer.Team then continue end

        local char = plr.Character
        if not char then continue end

        local hum = char:FindFirstChildOfClass("Humanoid")
        if not hum or hum.Health <= 0 then continue end

        local part = char:FindFirstChild(Config.SelectedPart)
        if not part then continue end

        if Config.VisibleCheck and not IsVisible(plr) then continue end

        local screenPos, onScreen = Camera:WorldToViewportPoint(part.Position)
        if not onScreen then continue end

        local mousePos = UserInputService:GetMouseLocation()
        local dist = (mousePos - Vector2.new(screenPos.X, screenPos.Y)).Magnitude

        if dist < closestDist then
            closestDist = dist
            closest = plr
        end
    end

    return closest
end

-- Cancela o lock atual
local function CancelAimLock()
    AimLocked = nil
    if AimAnimation then
        AimAnimation:Cancel()
        AimAnimation = nil
    end
end

-- Núcleo do Aimbot Universal
local function UpdateAimbot()
    if not Config.AimEnabled or not AimRunning then
        CancelAimLock()
        return
    end

    -- Obtém o alvo mais próximo
    local target = GetClosestPlayer()
    if not target then
        CancelAimLock()
        return
    end

    AimLocked = target
    local char = target.Character
    if not char then CancelAimLock(); return end

    local part = char:FindFirstChild(Config.SelectedPart)
    if not part then CancelAimLock(); return end

    -- Calcula posição com predição de velocidade
    local velocity = part.Velocity or Vector3.new(0, 0, 0)
    local predictedPos = part.Position + (velocity * Config.Prediction)
    local screenPos = Camera:WorldToViewportPoint(predictedPos)
    local mousePos  = UserInputService:GetMouseLocation()

    local deltaX = screenPos.X - mousePos.X
    local deltaY = screenPos.Y - mousePos.Y

    if Config.AimLockMode == "Mouse" then
        -- Modo Mouse (mousemoverel) — funciona em qualquer jogo
        if Config.AimMode == "Rage" then
            -- Rage: mira instantânea, sem suavização
            mousemoverel(deltaX, deltaY)
        else
            -- Legit: suavização progressiva (Smoothness como divisor)
            local smooth = math.max(1, Config.Smoothness)
            mousemoverel(deltaX / smooth, deltaY / smooth)
        end
    else
        -- Modo Camera (CFrame Lock) — mais preciso, porém mais detectável
        if Config.AimMode == "Rage" then
            Camera.CFrame = CFrame.new(Camera.CFrame.Position, predictedPos)
        else
            -- Legit com TweenService para suavidade máxima
            local tweenTime = Config.Smoothness * 0.05
            if AimAnimation then AimAnimation:Cancel() end
            AimAnimation = TweenService:Create(
                Camera,
                TweenInfo.new(tweenTime, Enum.EasingStyle.Sine, Enum.EasingDirection.Out),
                {CFrame = CFrame.new(Camera.CFrame.Position, predictedPos)}
            )
            AimAnimation:Play()
        end
    end
end

-- Controle de tecla de ativação do Aimbot
UserInputService.InputBegan:Connect(function(input)
    if Config.AimToggle then
        local triggerType = Enum.UserInputType[Config.TriggerKey]
        if triggerType and input.UserInputType == triggerType then
            AimRunning = not AimRunning
            if not AimRunning then CancelAimLock() end
        end
    else
        local triggerType = Enum.UserInputType[Config.TriggerKey]
        if triggerType and input.UserInputType == triggerType then
            AimRunning = true
        end
    end
end)

UserInputService.InputEnded:Connect(function(input)
    if not Config.AimToggle then
        local triggerType = Enum.UserInputType[Config.TriggerKey]
        if triggerType and input.UserInputType == triggerType then
            AimRunning = false
            CancelAimLock()
        end
    end
end)

-- ==================== ESP COMPLETO ====================
-- Box, Nome, Vida, Linha, Distância

local function GetHealthColor(health, maxHealth)
    local ratio = health / maxHealth
    if ratio > 0.6 then
        return Color3.fromRGB(46, 204, 113)   -- Verde
    elseif ratio > 0.3 then
        return Color3.fromRGB(241, 196, 15)   -- Amarelo
    else
        return Color3.fromRGB(231, 76, 60)    -- Vermelho
    end
end

local function CreateESPForPlayer(player)
    if ESPObjects[player] then return end

    local esp = {}

    -- Box (4 linhas formando retângulo)
    esp.BoxLines = {}
    for i = 1, 4 do
        local line = Drawing.new("Line")
        line.Visible = false
        line.Thickness = 1.5
        line.Color = Color3.fromRGB(255, 255, 255)
        esp.BoxLines[i] = line
    end

    -- Preenchimento da Box (fundo semi-transparente)
    esp.BoxFill = Drawing.new("Square")
    esp.BoxFill.Visible = false
    esp.BoxFill.Filled = true
    esp.BoxFill.Color = Color3.fromRGB(0, 0, 0)
    esp.BoxFill.Transparency = 0.6

    -- Nome
    esp.Name = Drawing.new("Text")
    esp.Name.Visible = false
    esp.Name.Size = 14
    esp.Name.Font = Drawing.Fonts.UI
    esp.Name.Color = Color3.fromRGB(255, 255, 255)
    esp.Name.Outline = true
    esp.Name.OutlineColor = Color3.fromRGB(0, 0, 0)
    esp.Name.Center = true

    -- Barra de Vida (fundo)
    esp.HealthBarBg = Drawing.new("Square")
    esp.HealthBarBg.Visible = false
    esp.HealthBarBg.Filled = true
    esp.HealthBarBg.Color = Color3.fromRGB(30, 30, 30)

    -- Barra de Vida (preenchimento)
    esp.HealthBar = Drawing.new("Square")
    esp.HealthBar.Visible = false
    esp.HealthBar.Filled = true
    esp.HealthBar.Color = Color3.fromRGB(46, 204, 113)

    -- Texto de Vida
    esp.HealthText = Drawing.new("Text")
    esp.HealthText.Visible = false
    esp.HealthText.Size = 11
    esp.HealthText.Font = Drawing.Fonts.UI
    esp.HealthText.Color = Color3.fromRGB(255, 255, 255)
    esp.HealthText.Outline = true
    esp.HealthText.OutlineColor = Color3.fromRGB(0, 0, 0)
    esp.HealthText.Center = true

    -- Linha (tracer)
    esp.Line = Drawing.new("Line")
    esp.Line.Visible = false
    esp.Line.Thickness = 1.2
    esp.Line.Color = Color3.fromRGB(255, 255, 255)

    -- Distância
    esp.Distance = Drawing.new("Text")
    esp.Distance.Visible = false
    esp.Distance.Size = 11
    esp.Distance.Font = Drawing.Fonts.UI
    esp.Distance.Color = Color3.fromRGB(200, 200, 255)
    esp.Distance.Outline = true
    esp.Distance.OutlineColor = Color3.fromRGB(0, 0, 0)
    esp.Distance.Center = true

    ESPObjects[player] = esp
end

local function RemoveESPForPlayer(player)
    local esp = ESPObjects[player]
    if not esp then return end

    for _, line in pairs(esp.BoxLines) do line:Remove() end
    esp.BoxFill:Remove()
    esp.Name:Remove()
    esp.HealthBarBg:Remove()
    esp.HealthBar:Remove()
    esp.HealthText:Remove()
    esp.Line:Remove()
    esp.Distance:Remove()

    ESPObjects[player] = nil
end

local function UpdateESP()
    for _, player in ipairs(Players:GetPlayers()) do
        if player == LocalPlayer then continue end

        if not ESPObjects[player] then
            CreateESPForPlayer(player)
        end

        local esp = ESPObjects[player]
        if not esp then continue end

        local char = player.Character
        local hum  = char and char:FindFirstChildOfClass("Humanoid")
        local root = char and char:FindFirstChild("HumanoidRootPart")
        local head = char and char:FindFirstChild("Head")

        local visible = Config.ESPEnabled and char and hum and hum.Health > 0 and root and head

        if not visible then
            for _, line in pairs(esp.BoxLines) do line.Visible = false end
            esp.BoxFill.Visible = false
            esp.Name.Visible = false
            esp.HealthBarBg.Visible = false
            esp.HealthBar.Visible = false
            esp.HealthText.Visible = false
            esp.Line.Visible = false
            esp.Distance.Visible = false
            continue
        end

        -- Calcula bounding box 3D -> 2D
        local rootPos = root.Position
        local headPos = head.Position

        local topScreen,    topOnScreen    = Camera:WorldToViewportPoint(headPos + Vector3.new(0, 0.7, 0))
        local bottomScreen, bottomOnScreen = Camera:WorldToViewportPoint(rootPos - Vector3.new(0, 2.8, 0))

        if not topOnScreen or not bottomOnScreen then
            for _, line in pairs(esp.BoxLines) do line.Visible = false end
            esp.BoxFill.Visible = false
            esp.Name.Visible = false
            esp.HealthBarBg.Visible = false
            esp.HealthBar.Visible = false
            esp.HealthText.Visible = false
            esp.Line.Visible = false
            esp.Distance.Visible = false
            continue
        end

        local height = math.abs(topScreen.Y - bottomScreen.Y)
        local width  = height * 0.55
        local centerX = topScreen.X
        local top     = topScreen.Y
        local bottom  = bottomScreen.Y
        local left    = centerX - width / 2
        local right   = centerX + width / 2

        -- Distância ao jogador local
        local localRoot = LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("HumanoidRootPart")
        local dist = localRoot and math.floor((localRoot.Position - rootPos).Magnitude) or 0

        -- Cor baseada na equipe
        local boxColor = Color3.fromRGB(255, 255, 255)
        if Config.TeamCheck and player.Team == LocalPlayer.Team then
            boxColor = Color3.fromRGB(46, 204, 113)
        elseif AimLocked == player then
            boxColor = Color3.fromRGB(231, 76, 60)
        end

        -- BOX ESP
        if Config.BoxEnabled then
            -- Preenchimento
            esp.BoxFill.Visible = true
            esp.BoxFill.Position = Vector2.new(left, top)
            esp.BoxFill.Size = Vector2.new(width, height)

            -- Linhas da box (topo, baixo, esquerda, direita)
            local corners = {
                {Vector2.new(left, top),   Vector2.new(right, top)},   -- topo
                {Vector2.new(left, bottom),Vector2.new(right, bottom)}, -- baixo
                {Vector2.new(left, top),   Vector2.new(left, bottom)},  -- esquerda
                {Vector2.new(right, top),  Vector2.new(right, bottom)}, -- direita
            }
            for i, pts in ipairs(corners) do
                esp.BoxLines[i].Visible = true
                esp.BoxLines[i].From = pts[1]
                esp.BoxLines[i].To   = pts[2]
                esp.BoxLines[i].Color = boxColor
            end
        else
            for _, line in pairs(esp.BoxLines) do line.Visible = false end
            esp.BoxFill.Visible = false
        end

        -- NOME
        if Config.NameEnabled then
            esp.Name.Visible = true
            esp.Name.Position = Vector2.new(centerX, top - 18)
            esp.Name.Text = player.Name
            esp.Name.Color = boxColor
        else
            esp.Name.Visible = false
        end

        -- BARRA DE VIDA
        if Config.HealthEnabled then
            local healthRatio = math.clamp(hum.Health / hum.MaxHealth, 0, 1)
            local barX = left - 7
            local barHeight = height
            local filledH = barHeight * healthRatio

            esp.HealthBarBg.Visible = true
            esp.HealthBarBg.Position = Vector2.new(barX - 2, top)
            esp.HealthBarBg.Size = Vector2.new(5, barHeight)

            esp.HealthBar.Visible = true
            esp.HealthBar.Color = GetHealthColor(hum.Health, hum.MaxHealth)
            esp.HealthBar.Position = Vector2.new(barX - 2, top + (barHeight - filledH))
            esp.HealthBar.Size = Vector2.new(5, filledH)

            esp.HealthText.Visible = true
            esp.HealthText.Position = Vector2.new(barX, bottom + 4)
            esp.HealthText.Text = math.floor(hum.Health) .. "hp"
        else
            esp.HealthBarBg.Visible = false
            esp.HealthBar.Visible = false
            esp.HealthText.Visible = false
        end

        -- LINHA (TRACER)
        if Config.LineEnabled then
            local viewport = Camera.ViewportSize
            local originY = Config.LineOrigin == "Bottom" and viewport.Y or viewport.Y / 2
            esp.Line.Visible = true
            esp.Line.From = Vector2.new(viewport.X / 2, originY)
            esp.Line.To   = Vector2.new(centerX, bottom)
            esp.Line.Color = boxColor
        else
            esp.Line.Visible = false
        end

        -- DISTÂNCIA
        if Config.DistanceEnabled then
            esp.Distance.Visible = true
            esp.Distance.Position = Vector2.new(centerX, bottom + 4)
            esp.Distance.Text = dist .. "m"
        else
            esp.Distance.Visible = false
        end
    end
end

-- Gerencia entrada/saída de jogadores
Players.PlayerAdded:Connect(function(plr)
    task.wait(1)
    CreateESPForPlayer(plr)
end)

Players.PlayerRemoving:Connect(function(plr)
    RemoveESPForPlayer(plr)
end)

-- Inicializa ESP para jogadores já na partida
for _, plr in ipairs(Players:GetPlayers()) do
    if plr ~= LocalPlayer then
        CreateESPForPlayer(plr)
    end
end

-- ==================== LOOP PRINCIPAL ====================
RunService.RenderStepped:Connect(function()
    -- ===== FOV CIRCLE =====
    local fovVisible = Config.AimEnabled and Config.FOVVisible
    FOV_Circle.Visible  = fovVisible
    FOV_Outline.Visible = fovVisible
    if fovVisible then
        local mousePos = UserInputService:GetMouseLocation()
        FOV_Circle.Radius  = Config.FOVSize
        FOV_Outline.Radius = Config.FOVSize + 1
        FOV_Circle.Position  = mousePos
        FOV_Outline.Position = mousePos
        -- Cor muda quando tem alvo travado
        if AimLocked then
            FOV_Circle.Color = Colors.Danger
        else
            -- Efeito rainbow no FOV
            local h = tick() % 5 / 5
            FOV_Circle.Color = Color3.fromHSV(h, 1, 1)
        end
    end

    -- ===== AIMBOT =====
    UpdateAimbot()

    -- ===== ESP =====
    UpdateESP()

    -- ===== SPEED HACK =====
    local char = LocalPlayer.Character
    if char then
        local hum = char:FindFirstChildOfClass("Humanoid")
        if hum then
            hum.WalkSpeed = Config.SpeedEnabled and Config.WalkSpeed or 16
        end

        -- Cross Wall (No Clip)
        if Config.CrossWall then
            for _, part in pairs(char:GetDescendants()) do
                if part:IsA("BasePart") then
                    part.CanCollide = false
                end
            end
        end
    end
end)

-- ==================== EFEITO GLOW PULSANTE NA BORDA ====================
local glowTick = 0
RunService.Heartbeat:Connect(function(dt)
    glowTick = glowTick + dt
    local pulse = math.abs(math.sin(glowTick * 1.5))
    glowStroke.Transparency = 0.5 + pulse * 0.4
    glowStroke.Color = Color3.fromHSV(glowTick % 5 / 5, 0.8, 1)
end)

-- ==================== FIM DO SCRIPT ====================
-- EDSON MODZ V8 - ADVANCED EDITION
-- ESP: Box | Nome | Vida | Linha | Distância
-- AIMBOT: Rage | Legit | Mouse Mode | Camera Mode
-- MISC: Speed Hack | Cross Wall
-- Layout Premium 30KB+ | Rainbow Mirror Name | Semi-Transparente
