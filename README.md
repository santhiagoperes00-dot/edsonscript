-- EDSON MODZ V7 - ULTIMATE PROFESSIONAL EDITION
-- DESIGN PREMIUM | AIM MAGNET | SPEED HACK | ESP LINHA CONFIGURÁVEL | PERFIL | ESQUELETO REALISTA

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
    AimMagnet = false, -- NOVO: AIM MAGNET
    AimMode = "Legit",
    TeamCheck = false,
    VisibleCheck = true,
    SelectedPart = "Head",
    Smoothness = 0.3,
    FOVSize = 150,
    FOVVisible = false,
    
    WalkSpeed = 16, -- NOVO: SPEED HACK
    SpeedEnabled = false,
    
    ESPEnabled = false,
    BoxEnabled = false,
    NameEnabled = false,
    HealthEnabled = false,
    DistEnabled = false,
    SkeletonEnabled = false,
    LineEnabled = false,
    LineOrigin = "Bottom", -- Opções: "Top", "Center", "Bottom"
}

-- PALETA DE CORES PROFISSIONAL
local Colors = {
    Primary = Color3.fromRGB(130, 50, 255),  -- Roxo Vibrante
    Secondary = Color3.fromRGB(160, 80, 255),
    Accent = Color3.fromRGB(200, 150, 255),
    Success = Color3.fromRGB(46, 204, 113),
    Danger = Color3.fromRGB(231, 76, 60),
    Background = Color3.fromRGB(15, 15, 22),
    Surface = Color3.fromRGB(25, 25, 35),
    SurfaceLight = Color3.fromRGB(35, 35, 45),
    Text = Color3.fromRGB(255, 255, 255),
    TextDim = Color3.fromRGB(180, 180, 190)
}

local ESPObjects = {}
local Minimized = false
local MainSize = UDim2.new(0, 600, 0, 520)
local MinSize = UDim2.new(0, 600, 0, 70)

-- ==================== FUNÇÕES DE UTILIDADE ====================
local function addCorner(obj, radius)
    local corner = Instance.new("UICorner")
    corner.CornerRadius = UDim.new(0, radius)
    corner.Parent = obj
end

local function addStroke(obj, thickness, color, transparency)
    local stroke = Instance.new("UIStroke")
    stroke.Thickness = thickness
    stroke.Color = color or Colors.Primary
    stroke.Transparency = transparency or 0.5
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
Main.Active = true
Main.Draggable = true
addCorner(Main, 20)
addStroke(Main, 2, Colors.Primary)

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
Top.BorderSizePixel = 0
addCorner(Top, 20)
addGradient(Top, Colors.Surface, Colors.SurfaceLight, 90)

-- IMAGEM DE PERFIL (FOTO DO EDSON)
local ProfileImg = Instance.new("ImageLabel", Top)
ProfileImg.Size = UDim2.new(0, 50, 0, 50)
ProfileImg.Position = UDim2.new(0, 15, 0.5, -25)
ProfileImg.Image = "https://files.manuscdn.com/user_upload_by_module/session_file/310519663331117583/cxWdFRZwnhgWlwHS.jpg"
ProfileImg.BackgroundTransparency = 1
addCorner(ProfileImg, 25)
addStroke(ProfileImg, 2, Colors.Primary)

local Title = Instance.new("TextLabel", Top)
Title.Size = UDim2.new(1, -150, 1, 0)
Title.Position = UDim2.new(0, 80, 0, 0)
Title.Text = "EDSON MODZ V7"
Title.BackgroundTransparency = 1
Title.TextColor3 = Colors.Text
Title.Font = Enum.Font.GothamBold
Title.TextSize = 26
Title.TextXAlignment = Enum.TextXAlignment.Left

local SubTitle = Instance.new("TextLabel", Top)
SubTitle.Size = UDim2.new(1, -150, 0, 20)
SubTitle.Position = UDim2.new(0, 80, 0.5, 12)
SubTitle.Text = "ULTIMATE PROFESSIONAL EDITION"
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
    btn.BorderSizePixel = 0
    addCorner(btn, 12)
    addStroke(btn, 1, Colors.TextDim, 0.5)
    return btn
end

local MinimizeBtn = createTopButton(Top, "−", -100, Colors.SurfaceLight)
local CloseBtn = createTopButton(Top, "✕", -45, Colors.Danger)

CloseBtn.MouseButton1Click:Connect(function() ScreenGui:Destroy() end)

-- SIDE MENU
local Side = Instance.new("Frame", Main)
Side.Size = UDim2.new(0, 160, 1, -70)
Side.Position = UDim2.new(0, 0, 0, 70)
Side.BackgroundColor3 = Colors.Surface
Side.BorderSizePixel = 0
addCorner(Side, 16)
addGradient(Side, Colors.Surface, Color3.fromRGB(28, 32, 42), 180)

-- CONTENT AREA
local Content = Instance.new("Frame", Main)
Content.Position = UDim2.new(0, 160, 0, 70)
Content.Size = UDim2.new(1, -160, 1, -70)
Content.BackgroundTransparency = 1
addCorner(Content, 16)

-- ABAS
local function createTab(parent)
    local tab = Instance.new("ScrollingFrame", parent)
    tab.Size = UDim2.new(1, -20, 1, -20)
    tab.Position = UDim2.new(0, 10, 0, 10)
    tab.BackgroundTransparency = 1
    tab.ScrollBarThickness = 4
    tab.ScrollBarImageColor3 = Colors.Primary
    tab.CanvasSize = UDim2.new(0, 0, 0, 900)
    tab.BorderSizePixel = 0
    tab.Visible = false
    return tab
end

local AimTab = createTab(Content); AimTab.Visible = true
local VisualTab = createTab(Content)
local MiscTab = createTab(Content)
local SettingsTab = createTab(Content)

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
    btn.BorderSizePixel = 0
    addCorner(btn, 14)
    addStroke(btn, 1, Colors.Primary, 0.7)
    
    btn.MouseButton1Click:Connect(function()
        AimTab.Visible = false; VisualTab.Visible = false; MiscTab.Visible = false; SettingsTab.Visible = false
        tab.Visible = true
    end)
    return btn
end

createNavButton("AIM", "🎯", 15, AimTab)
createNavButton("VISUAL", "👁️", 85, VisualTab)
createNavButton("MISC", "🚀", 155, MiscTab)
createNavButton("SETTINGS", "⚙️", 225, SettingsTab)

-- FUNÇÃO MINIMIZAR
MinimizeBtn.MouseButton1Click:Connect(function()
    Minimized = not Minimized
    if Minimized then
        TweenService:Create(Main, TweenInfo.new(0.4), {Size = MinSize}):Play()
        MinimizeBtn.Text = "+"
        Side.Visible = false; Content.Visible = false
    else
        TweenService:Create(Main, TweenInfo.new(0.4), {Size = MainSize}):Play()
        MinimizeBtn.Text = "−"
        wait(0.2)
        Side.Visible = true; Content.Visible = true
    end
end)

-- ==================== COMPONENTES PREMIUM ====================
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
    sectionTitle.TextColor3 = Colors.Accent
    sectionTitle.Font = Enum.Font.GothamBold
    sectionTitle.TextSize = 14
    sectionTitle.BackgroundTransparency = 1
    sectionTitle.TextXAlignment = Enum.TextXAlignment.Left
    return section
end

local function createToggle(parent, text, x, y, key)
    local btn = Instance.new("TextButton", parent)
    btn.Size = UDim2.new(0, 140, 0, 35)
    btn.Position = UDim2.new(0, x, 0, y)
    btn.Font = Enum.Font.GothamBold
    btn.TextColor3 = Colors.Text
    btn.TextSize = 12
    addCorner(btn, 10)
    
    local function update()
        local is_on = Config[key]
        btn.Text = text .. ": " .. (is_on and "ON" or "OFF")
        TweenService:Create(btn, TweenInfo.new(0.3), {BackgroundColor3 = is_on and Colors.Success or Colors.Danger}):Play()
    end
    btn.MouseButton1Click:Connect(function() Config[key] = not Config[key]; update() end)
    update()
end

local function createSlider(parent, label, x, y, min, max, default, key)
    local frame = Instance.new("Frame", parent)
    frame.Size = UDim2.new(0, 300, 0, 50)
    frame.Position = UDim2.new(0, x, 0, y)
    frame.BackgroundTransparency = 1
    
    local lbl = Instance.new("TextLabel", frame)
    lbl.Size = UDim2.new(1, 0, 0, 20); lbl.Text = label .. ": " .. default; lbl.TextColor3 = Colors.Text; lbl.BackgroundTransparency = 1; lbl.Font = Enum.Font.Gotham; lbl.TextSize = 12; lbl.TextXAlignment = Enum.TextXAlignment.Left
    
    local slider = Instance.new("Frame", frame); slider.Size = UDim2.new(1, 0, 0, 6); slider.Position = UDim2.new(0, 0, 0, 30); slider.BackgroundColor3 = Colors.Surface; addCorner(slider, 3)
    local fill = Instance.new("Frame", slider); fill.Size = UDim2.new((default-min)/(max-min), 0, 1, 0); fill.BackgroundColor3 = Colors.Primary; addCorner(fill, 3)
    local knob = Instance.new("Frame", slider); knob.Size = UDim2.new(0, 14, 0, 14); knob.Position = UDim2.new(fill.Size.X.Scale, -7, -0.5, 0); knob.BackgroundColor3 = Colors.Text; addCorner(knob, 7)
    
    local dragging = false
    knob.InputBegan:Connect(function(i) if i.UserInputType == Enum.UserInputType.MouseButton1 then dragging = true end end)
    UIS.InputEnded:Connect(function(i) if i.UserInputType == Enum.UserInputType.MouseButton1 then dragging = false end end)
    UIS.InputChanged:Connect(function(i)
        if dragging and i.UserInputType == Enum.UserInputType.MouseMovement then
            local pos = math.clamp((i.Position.X - slider.AbsolutePosition.X) / slider.AbsoluteSize.X, 0, 1)
            fill.Size = UDim2.new(pos, 0, 1, 0); knob.Position = UDim2.new(pos, -7, -0.5, 0)
            local val = math.floor(min + (pos * (max - min))); lbl.Text = label .. ": " .. val; Config[key] = val
        end
    end)
end

-- ==================== CONTEÚDO DAS ABAS ====================
-- AIM TAB
local aY = 10
local aimSec1 = createSection(AimTab, "AIMBOT CONTROL", aY, 140); aY = aY + 150
createToggle(aimSec1, "AIMBOT", 10, 45, "AimEnabled")
createToggle(aimSec1, "AIM MAGNET", 160, 45, "AimMagnet")
createToggle(aimSec1, "TEAM CHECK", 10, 90, "TeamCheck")
createToggle(aimSec1, "VIS CHECK", 160, 90, "VisibleCheck")

local aimSec2 = createSection(AimTab, "AIMBOT SETTINGS", aY, 180); aY = aY + 190
createSlider(aimSec2, "FOV SIZE", 10, 45, 10, 600, 150, "FOVSize")
createSlider(aimSec2, "SMOOTHNESS", 10, 105, 1, 10, 3, "Smoothness")
createToggle(aimSec2, "SHOW FOV", 10, 140, "FOVVisible")

-- VISUAL TAB
local vY = 10
local visSec1 = createSection(VisualTab, "ESP MASTER", vY, 90); vY = vY + 100
createToggle(visSec1, "MASTER ESP", 10, 45, "ESPEnabled")

local visSec2 = createSection(VisualTab, "ESP ELEMENTS", vY, 220); vY = vY + 230
createToggle(visSec2, "BOX", 10, 45, "BoxEnabled")
createToggle(visSec2, "NAME", 160, 45, "NameEnabled")
createToggle(visSec2, "HEALTH", 10, 90, "HealthEnabled")
createToggle(visSec2, "DISTANCE", 160, 90, "DistEnabled")
createToggle(visSec2, "SKELETON", 10, 135, "SkeletonEnabled")
createToggle(visSec2, "LINE", 160, 135, "LineEnabled")

local LineOriginBtn = Instance.new("TextButton", visSec2)
LineOriginBtn.Size = UDim2.new(0, 300, 0, 30); LineOriginBtn.Position = UDim2.new(0, 10, 0, 180); LineOriginBtn.Text = "LINE ORIGIN: BOTTOM"; LineOriginBtn.Font = Enum.Font.GothamBold; LineOriginBtn.TextColor3 = Colors.Text; LineOriginBtn.BackgroundColor3 = Colors.SurfaceLight; addCorner(LineOriginBtn, 8)
LineOriginBtn.MouseButton1Click:Connect(function()
    if Config.LineOrigin == "Bottom" then Config.LineOrigin = "Center" elseif Config.LineOrigin == "Center" then Config.LineOrigin = "Top" else Config.LineOrigin = "Bottom" end
    LineOriginBtn.Text = "LINE ORIGIN: " .. Config.LineOrigin:upper()
end)

-- MISC TAB
local mY = 10
local miscSec1 = createSection(MiscTab, "CHARACTER MODS", mY, 150); mY = mY + 160
createToggle(miscSec1, "SPEED HACK", 10, 45, "SpeedEnabled")
createSlider(miscSec1, "WALK SPEED", 10, 90, 16, 300, 16, "WalkSpeed")

-- SETTINGS TAB (COLOR PICKER)
local sY = 10
local setSec1 = createSection(SettingsTab, "THEME SETTINGS", sY, 100); sY = sY + 110
local colorColors = {Colors.Primary, Color3.fromRGB(0, 150, 255), Color3.fromRGB(46, 204, 113), Color3.fromRGB(255, 100, 100), Color3.fromRGB(255, 170, 50)}
for i, color in ipairs(colorColors) do
    local cBtn = Instance.new("TextButton", setSec1); cBtn.Size = UDim2.new(0, 50, 0, 40); cBtn.Position = UDim2.new(0, 10 + (i-1)*60, 0, 45); cBtn.Text = ""; cBtn.BackgroundColor3 = color; addCorner(cBtn, 10)
    cBtn.MouseButton1Click:Connect(function() Colors.Primary = color; Top.BackgroundColor3 = Colors.Surface; glowStroke.Color = color:Lerp(Color3.new(1,1,1), 0.5) end)
end

-- ==================== LÓGICA DO ESP ====================
local function CreateESP(player)
    if ESPObjects[player] then return end
    local esp = {
        Box = Drawing.new("Square"), Name = Drawing.new("Text"), Dist = Drawing.new("Text"), HealthBar = Drawing.new("Square"), HealthBarBack = Drawing.new("Square"), Line = Drawing.new("Line"), Skeleton = {}, HeadCircle = Drawing.new("Circle")
    }
    esp.Box.Thickness = 2; esp.Box.Filled = false; esp.Name.Size = 14; esp.Name.Center = true; esp.Name.Outline = true; esp.Dist.Size = 12; esp.Dist.Center = true; esp.Dist.Outline = true; esp.HealthBar.Filled = true; esp.HealthBarBack.Filled = true; esp.HealthBarBack.Color = Color3.new(0,0,0); esp.Line.Thickness = 1; esp.HeadCircle.Thickness = 2; esp.HeadCircle.NumSides = 12
    ESPObjects[player] = esp
end

local function ClearESP(player)
    if ESPObjects[player] then
        for _, v in pairs(ESPObjects[player]) do if type(v) == "table" then for _, l in ipairs(v) do l:Remove() end else v:Remove() end end
        ESPObjects[player] = nil
    end
end

local SkeletonConnections = {
    {"Head", "UpperTorso"}, {"UpperTorso", "LowerTorso"}, {"UpperTorso", "LeftUpperArm"}, {"LeftUpperArm", "LeftLowerArm"}, {"LeftLowerArm", "LeftHand"}, {"UpperTorso", "RightUpperArm"}, {"RightUpperArm", "RightLowerArm"}, {"RightLowerArm", "RightHand"}, {"LowerTorso", "LeftUpperLeg"}, {"LeftUpperLeg", "LeftLowerLeg"}, {"LeftLowerLeg", "LeftFoot"}, {"LowerTorso", "RightUpperLeg"}, {"RightUpperLeg", "RightLowerLeg"}, {"RightLowerLeg", "RightFoot"}
}

-- ==================== LOOP PRINCIPAL ====================
local FOV = Drawing.new("Circle"); FOV.Thickness = 2; FOV.NumSides = 60; FOV.Filled = false; FOV.Transparency = 0.4

RunService.RenderStepped:Connect(function()
    FOV.Color = Colors.Primary; FOV.Radius = Config.FOVSize; FOV.Visible = Config.FOVVisible; FOV.Position = Vector2.new(Camera.ViewportSize.X/2, Camera.ViewportSize.Y/2)

    if Config.SpeedEnabled and LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("Humanoid") then
        LocalPlayer.Character.Humanoid.WalkSpeed = Config.WalkSpeed
    elseif LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("Humanoid") then
        LocalPlayer.Character.Humanoid.WalkSpeed = 16
    end

    if not Config.ESPEnabled then
        for p, _ in pairs(ESPObjects) do ClearESP(p) end
    else
        for _, player in ipairs(Players:GetPlayers()) do
            local char = player.Character
            local hum = char and char:FindFirstChildOfClass("Humanoid")
            if player ~= LocalPlayer and hum and hum.Health > 0 then
                if not ESPObjects[player] then CreateESP(player) end
                local esp = ESPObjects[player]
                local minX, minY, maxX, maxY, onScreen = math.huge, math.huge, -math.huge, -math.huge, false
                for _, part in ipairs(char:GetChildren()) do
                    if part:IsA("BasePart") then
                        local pos, vis = Camera:WorldToViewportPoint(part.Position)
                        if vis then onScreen = true; minX = math.min(minX, pos.X); minY = math.min(minY, pos.Y); maxX = math.max(maxX, pos.X); maxY = math.max(maxY, pos.Y) end
                    end
                end
                if onScreen then
                    local w, h = maxX - minX, maxY - minY
                    local color = IsPlayerVisible(player) and Colors.Success or Colors.Primary
                    esp.Box.Visible = Config.BoxEnabled; if Config.BoxEnabled then esp.Box.Size = Vector2.new(w, h); esp.Box.Position = Vector2.new(minX, minY); esp.Box.Color = color end
                    esp.HealthBar.Visible = Config.HealthEnabled; esp.HealthBarBack.Visible = Config.HealthEnabled
                    if Config.HealthEnabled then
                        local hp = hum.Health / hum.MaxHealth
                        esp.HealthBarBack.Size = Vector2.new(4, h); esp.HealthBarBack.Position = Vector2.new(minX - 6, minY)
                        esp.HealthBar.Size = Vector2.new(4, h * hp); esp.HealthBar.Position = Vector2.new(minX - 6, minY + (h - h * hp)); esp.HealthBar.Color = Color3.fromHSV(hp/3, 1, 1)
                    end
                    esp.Name.Visible = Config.NameEnabled; if Config.NameEnabled then esp.Name.Text = player.Name; esp.Name.Position = Vector2.new(minX + w/2, minY - 16) end
                    esp.Dist.Visible = Config.DistEnabled; if Config.DistEnabled then local d = (Camera.CFrame.Position - char.HumanoidRootPart.Position).Magnitude; esp.Dist.Text = math.floor(d) .. "m"; esp.Dist.Position = Vector2.new(minX + w/2, minY + h + 5) end
                    esp.Line.Visible = Config.LineEnabled; if Config.LineEnabled then
                        local origin
                        if Config.LineOrigin == "Top" then origin = Vector2.new(Camera.ViewportSize.X/2, 0) elseif Config.LineOrigin == "Center" then origin = Vector2.new(Camera.ViewportSize.X/2, Camera.ViewportSize.Y/2) else origin = Vector2.new(Camera.ViewportSize.X/2, Camera.ViewportSize.Y) end
                        esp.Line.From = origin; esp.Line.To = Vector2.new(minX + w/2, minY + h); esp.Line.Color = color
                    end
                    if Config.SkeletonEnabled then
                        local head = char:FindFirstChild("Head")
                        if head then
                            local hpos, hvis = Camera:WorldToViewportPoint(head.Position)
                            if hvis then esp.HeadCircle.Radius = math.clamp(500 / (Camera.CFrame.Position - head.Position).Magnitude, 2, 15); esp.HeadCircle.Position = Vector2.new(hpos.X, hpos.Y); esp.HeadCircle.Color = color; esp.HeadCircle.Visible = true else esp.HeadCircle.Visible = false end
                        end
                        while #esp.Skeleton < #SkeletonConnections do table.insert(esp.Skeleton, Drawing.new("Line")) end
                        for i, conn in ipairs(SkeletonConnections) do
                            local p1, p2 = char:FindFirstChild(conn[1]), char:FindFirstChild(conn[2])
                            if p1 and p2 then
                                local pos1, vis1 = Camera:WorldToViewportPoint(p1.Position)
                                local pos2, vis2 = Camera:WorldToViewportPoint(p2.Position)
                                if vis1 and vis2 then esp.Skeleton[i].From = Vector2.new(pos1.X, pos1.Y); esp.Skeleton[i].To = Vector2.new(pos2.X, pos2.Y); esp.Skeleton[i].Color = color; esp.Skeleton[i].Visible = true; continue end
                            end
                            esp.Skeleton[i].Visible = false
                        end
                    else esp.HeadCircle.Visible = false; for _, l in ipairs(esp.Skeleton) do l.Visible = false end end
                else ClearESP(player) end
            elseif ESPObjects[player] then ClearESP(player) end
        end
    end

    if Config.AimEnabled then
        local target, shortest = nil, Config.FOVSize
        for _, p in ipairs(Players:GetPlayers()) do
            if p ~= LocalPlayer and p.Character and p.Character:FindFirstChild("Humanoid") and p.Character.Humanoid.Health > 0 then
                if Config.TeamCheck and p.Team == LocalPlayer.Team then continue end
                local part = p.Character:FindFirstChild(Config.SelectedPart) or p.Character:FindFirstChild("Head")
                if part then
                    local pos, vis = Camera:WorldToViewportPoint(part.Position)
                    local dist = (Vector2.new(pos.X, pos.Y) - Vector2.new(Camera.ViewportSize.X/2, Camera.ViewportSize.Y/2)).Magnitude
                    if dist < shortest then if Config.VisibleCheck and not IsPlayerVisible(p) and not Config.AimMagnet then continue end; shortest = dist; target = p end
                end
            end
        end
        if target then
            local part = target.Character[Config.SelectedPart]
            if Config.AimMagnet then Camera.CFrame = Camera.CFrame:Lerp(CFrame.new(Camera.CFrame.Position, part.Position), 0.5)
            else Camera.CFrame = Camera.CFrame:Lerp(CFrame.new(Camera.CFrame.Position, part.Position), Config.Smoothness) end
        end
    end
end)

Players.PlayerRemoving:Connect(ClearESP)
print("✅ EDSON MODZ V7 ULTIMATE PROFESSIONAL CARREGADO - 29KB+")
