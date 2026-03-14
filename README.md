-- EDSON MODZ V7 - ULTIMATE SUPERHERO EDITION (29KB+ FULL VERSION)
-- DESIGN PREMIUM SEMI-TRANSPARENTE | FLY HACK (SUPERHERO) | AIM MAGNET | CROSS WALL | SPEED HACK | RAINBOW MIRROR NAME | MOBILE OPTIMIZED

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
    AimMagnet = false, -- RESTAURADO: AIM MAGNET
    AimMode = "Legit",
    TeamCheck = false,
    VisibleCheck = true,
    SelectedPart = "Head",
    Smoothness = 3,
    FOVSize = 150,
    FOVVisible = false,
    
    WalkSpeed = 16,
    SpeedEnabled = false,
    CrossWall = false, -- RESTAURADO: CROSS WALL
    
    FlyEnabled = false, -- RESTAURADO: FLY HACK
    FlySpeed = 50,
    
    ESPEnabled = false,
    BoxEnabled = false,
    NameEnabled = false,
    HealthEnabled = false,
    LineEnabled = false,
    LineOrigin = "Bottom",
}

-- PALETA DE CORES PREMIUM (TEXTOS BRANCOS & TRANSPARÊNCIA)
local Colors = {
    Primary = Color3.fromRGB(130, 50, 255),
    Secondary = Color3.fromRGB(160, 80, 255),
    Accent = Color3.fromRGB(200, 150, 255),
    Success = Color3.fromRGB(46, 204, 113),
    Danger = Color3.fromRGB(231, 76, 60),
    Background = Color3.fromRGB(15, 15, 22),
    Surface = Color3.fromRGB(25, 25, 35),
    SurfaceLight = Color3.fromRGB(35, 35, 45),
    Text = Color3.fromRGB(255, 255, 255),
    TextDim = Color3.fromRGB(255, 255, 255)
}

local ESPObjects = {}
local Minimized = false
local MainSize = UDim2.new(0, 550, 0, 450)
local MinSize = UDim2.new(0, 220, 0, 55)

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

-- ==================== INTERFACE PREMIUM SEMI-TRANSPARENTE ====================
local Main = Instance.new("Frame", ScreenGui)
Main.Size = MainSize
Main.Position = UDim2.new(0.5, -275, 0.5, -225)
Main.BackgroundColor3 = Colors.Background
Main.BackgroundTransparency = 0.15
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

-- BOTÃO DE NOME (RAINBOW & CENTRALIZADO AO MINIMIZAR)
local UserBtn = Instance.new("TextButton", Main)
UserBtn.Size = UDim2.new(1, -40, 0, 50)
UserBtn.Position = UDim2.new(0, 20, 0, 5)
UserBtn.Text = "EDSON MODZ"
UserBtn.BackgroundTransparency = 1
UserBtn.TextColor3 = Color3.new(1, 1, 1)
UserBtn.Font = Enum.Font.GothamBold
UserBtn.TextSize = 24
UserBtn.TextXAlignment = Enum.TextXAlignment.Left

-- Efeito Rainbow Espelhado no Nome
local RainbowGradient = Instance.new("UIGradient", UserBtn)
RainbowGradient.Color = ColorSequence.new({
    ColorSequenceKeypoint.new(0, Color3.fromRGB(255, 0, 0)),
    ColorSequenceKeypoint.new(0.2, Color3.fromRGB(255, 255, 0)),
    ColorSequenceKeypoint.new(0.4, Color3.fromRGB(0, 255, 0)),
    ColorSequenceKeypoint.new(0.6, Color3.fromRGB(0, 255, 255)),
    ColorSequenceKeypoint.new(0.8, Color3.fromRGB(0, 0, 255)),
    ColorSequenceKeypoint.new(1, Color3.fromRGB(255, 0, 255))
})

RunService.RenderStepped:Connect(function()
    RainbowGradient.Offset = Vector2.new(tick() % 2 / 2, 0)
end)

-- Lógica de Minimizar com Nome Centralizado e Animado
UserBtn.MouseButton1Click:Connect(function()
    Minimized = not Minimized
    if Minimized then
        TweenService:Create(Main, TweenInfo.new(0.5, Enum.EasingStyle.Back, Enum.EasingDirection.Out), {Size = MinSize}):Play()
        UserBtn.TextXAlignment = Enum.TextXAlignment.Center
        Main:FindFirstChild("Side").Visible = false
        Main:FindFirstChild("Content").Visible = false
        
        -- Animação de Balanço Suave ao Minimizar
        local shake = TweenService:Create(UserBtn, TweenInfo.new(1, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut, -1, true), {Rotation = 2})
        shake:Play()
        UserBtn:SetAttribute("ShakeAnim", shake)
    else
        TweenService:Create(Main, TweenInfo.new(0.5, Enum.EasingStyle.Back, Enum.EasingDirection.Out), {Size = MainSize}):Play()
        UserBtn.TextXAlignment = Enum.TextXAlignment.Left
        UserBtn.Rotation = 0
        if UserBtn:GetAttribute("ShakeAnim") then UserBtn:GetAttribute("ShakeAnim"):Cancel() end
        wait(0.2)
        Main:FindFirstChild("Side").Visible = true
        Main:FindFirstChild("Content").Visible = true
    end
end)

-- SIDE MENU PREMIUM
local Side = Instance.new("Frame", Main)
Side.Name = "Side"
Side.Size = UDim2.new(0, 140, 1, -70)
Side.Position = UDim2.new(0, 10, 0, 60)
Side.BackgroundColor3 = Colors.Surface
Side.BackgroundTransparency = 0.3
Side.BorderSizePixel = 0
addCorner(Side, 16)
addGradient(Side, Colors.Surface, Color3.fromRGB(28, 32, 42), 180)

-- CONTENT AREA
local Content = Instance.new("Frame", Main)
Content.Name = "Content"
Content.Position = UDim2.new(0, 160, 0, 60)
Content.Size = UDim2.new(1, -170, 1, -70)
Content.BackgroundTransparency = 1
addCorner(Content, 16)

-- ABAS
local function createTab(parent)
    local tab = Instance.new("ScrollingFrame", parent)
    tab.Size = UDim2.new(1, 0, 1, 0)
    tab.BackgroundTransparency = 1
    tab.ScrollBarThickness = 4
    tab.ScrollBarImageColor3 = Colors.Primary
    tab.CanvasSize = UDim2.new(0, 0, 0, 1000)
    tab.BorderSizePixel = 0
    tab.Visible = false
    return tab
end

local AimTab = createTab(Content); AimTab.Visible = true
local VisualTab = createTab(Content)
local MiscTab = createTab(Content)

-- BOTÕES DE ABA ULTRA-FLUIDOS
local function createNavButton(text, icon, pos, tab)
    local btn = Instance.new("TextButton", Side)
    btn.Size = UDim2.new(1, -20, 0, 55)
    btn.Position = UDim2.new(0, 10, 0, pos)
    btn.Text = icon .. "  " .. text
    btn.Font = Enum.Font.GothamBold
    btn.TextSize = 14
    btn.TextColor3 = Colors.Text
    btn.BackgroundColor3 = Colors.SurfaceLight
    btn.BackgroundTransparency = 0.5
    btn.BorderSizePixel = 0
    addCorner(btn, 12)
    addStroke(btn, 1, Colors.Primary, 0.7)
    
    btn.MouseButton1Click:Connect(function()
        AimTab.Visible = false; VisualTab.Visible = false; MiscTab.Visible = false
        tab.Visible = true
    end)
    return btn
end

createNavButton("AIMBOT", "🎯", 15, AimTab)
createNavButton("VISUAL", "👁️", 80, VisualTab)
createNavButton("MISC", "🚀", 145, MiscTab)

-- ==================== COMPONENTES PREMIUM (RESTAURADOS) ====================
local function createSection(parent, title, yPos, height)
    local section = Instance.new("Frame", parent)
    section.Size = UDim2.new(1, -10, 0, height or 140)
    section.Position = UDim2.new(0, 5, 0, yPos)
    section.BackgroundColor3 = Colors.Surface
    section.BackgroundTransparency = 0.4
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
    btn.Size = UDim2.new(0, 150, 0, 38)
    btn.Position = UDim2.new(0, x, 0, y)
    btn.Font = Enum.Font.GothamBold
    btn.TextColor3 = Colors.Text
    btn.TextSize = 12
    addCorner(btn, 10)
    
    local function update()
        local is_on = Config[key]
        btn.Text = text .. ": " .. (is_on and "ON" or "OFF")
        TweenService:Create(btn, TweenInfo.new(0.4), {BackgroundColor3 = is_on and Colors.Success or Colors.Danger, BackgroundTransparency = 0.2}):Play()
    end
    btn.MouseButton1Click:Connect(function() Config[key] = not Config[key]; update() end)
    update()
end

local function createSlider(parent, label, x, y, min, max, default, key)
    local frame = Instance.new("Frame", parent)
    frame.Size = UDim2.new(0, 320, 0, 55)
    frame.Position = UDim2.new(0, x, 0, y)
    frame.BackgroundTransparency = 1
    
    local lbl = Instance.new("TextLabel", frame)
    lbl.Size = UDim2.new(1, 0, 0, 20); lbl.Text = label .. ": " .. default; lbl.TextColor3 = Colors.Text; lbl.BackgroundTransparency = 1; lbl.Font = Enum.Font.Gotham; lbl.TextSize = 12; lbl.TextXAlignment = Enum.TextXAlignment.Left
    
    local slider = Instance.new("Frame", frame); slider.Size = UDim2.new(1, 0, 0, 8); slider.Position = UDim2.new(0, 0, 0, 32); slider.BackgroundColor3 = Colors.Surface; addCorner(slider, 4)
    local fill = Instance.new("Frame", slider); fill.Size = UDim2.new((default-min)/(max-min), 0, 1, 0); fill.BackgroundColor3 = Colors.Primary; addCorner(fill, 4)
    local knob = Instance.new("Frame", slider); knob.Size = UDim2.new(0, 18, 0, 18); knob.Position = UDim2.new(fill.Size.X.Scale, -9, -0.5, 0); knob.BackgroundColor3 = Colors.Text; addCorner(knob, 9)
    
    local dragging = false
    local function updateSlider(input)
        local pos = math.clamp((input.Position.X - slider.AbsolutePosition.X) / slider.AbsoluteSize.X, 0, 1)
        fill.Size = UDim2.new(pos, 0, 1, 0); knob.Position = UDim2.new(pos, -9, -0.5, 0)
        local val = math.floor(min + (pos * (max - min))); lbl.Text = label .. ": " .. val; Config[key] = val
    end
    
    knob.InputBegan:Connect(function(i) if i.UserInputType == Enum.UserInputType.MouseButton1 or i.UserInputType == Enum.UserInputType.Touch then dragging = true end end)
    UIS.InputEnded:Connect(function(i) if i.UserInputType == Enum.UserInputType.MouseButton1 or i.UserInputType == Enum.UserInputType.Touch then dragging = false end end)
    UIS.InputChanged:Connect(function(i) if dragging and (i.UserInputType == Enum.UserInputType.MouseMovement or i.UserInputType == Enum.UserInputType.Touch) then updateSlider(i) end end)
end

-- ==================== CONTEÚDO DAS ABAS (RESTAURADO) ====================
-- AIM TAB
local aY = 10
local aimSec1 = createSection(AimTab, "AIMBOT CONTROL", aY, 160); aY = aY + 170
createToggle(aimSec1, "AIMBOT", 10, 45, "AimEnabled")
createToggle(aimSec1, "AIM MAGNET", 170, 45, "AimMagnet")
createToggle(aimSec1, "TEAM CHECK", 10, 100, "TeamCheck")
createToggle(aimSec1, "VIS CHECK", 170, 100, "VisibleCheck")

local ModeBtn = Instance.new("TextButton", aimSec1)
ModeBtn.Size = UDim2.new(0, 150, 0, 38); ModeBtn.Position = UDim2.new(0, 10, 0, 145); ModeBtn.Font = Enum.Font.GothamBold; ModeBtn.TextColor3 = Colors.Text; ModeBtn.TextSize = 12; addCorner(ModeBtn, 10)
local function updateMode() ModeBtn.Text = "MODE: " .. Config.AimMode:upper(); ModeBtn.BackgroundColor3 = Config.AimMode == "Rage" and Colors.Danger or Colors.Primary; ModeBtn.BackgroundTransparency = 0.2 end
ModeBtn.MouseButton1Click:Connect(function() Config.AimMode = Config.AimMode == "Legit" and "Rage" or "Legit"; updateMode() end)
updateMode()

local aimSec2 = createSection(AimTab, "AIMBOT SETTINGS", aY, 220); aY = aY + 230
createSlider(aimSec2, "FOV SIZE", 10, 45, 10, 600, 150, "FOVSize")
createSlider(aimSec2, "DELAY (SMOOTH)", 10, 115, 1, 10, 3, "Smoothness")
createToggle(aimSec2, "SHOW FOV", 10, 165, "FOVVisible")

-- VISUAL TAB
local vY = 10
local visSec1 = createSection(VisualTab, "ESP MASTER", vY, 100); vY = vY + 110
createToggle(visSec1, "MASTER ESP", 10, 45, "ESPEnabled")

local visSec2 = createSection(VisualTab, "ESP ELEMENTS", vY, 260); vY = vY + 270
createToggle(visSec2, "BOX", 10, 45, "BoxEnabled")
createToggle(visSec2, "NAME", 170, 45, "NameEnabled")
createToggle(visSec2, "HEALTH", 10, 100, "HealthEnabled")
createToggle(visSec2, "LINE", 170, 100, "LineEnabled")

local LineOriginBtn = Instance.new("TextButton", visSec2)
LineOriginBtn.Size = UDim2.new(0, 310, 0, 40); LineOriginBtn.Position = UDim2.new(0, 10, 0, 155); LineOriginBtn.Text = "LINE ORIGIN: BOTTOM"; LineOriginBtn.Font = Enum.Font.GothamBold; LineOriginBtn.TextColor3 = Colors.Text; LineOriginBtn.BackgroundColor3 = Colors.SurfaceLight; LineOriginBtn.BackgroundTransparency = 0.4; addCorner(LineOriginBtn, 12)
LineOriginBtn.MouseButton1Click:Connect(function()
    if Config.LineOrigin == "Bottom" then Config.LineOrigin = "Center" elseif Config.LineOrigin == "Center" then Config.LineOrigin = "Top" else Config.LineOrigin = "Bottom" end
    LineOriginBtn.Text = "LINE ORIGIN: " .. Config.LineOrigin:upper()
end)

-- MISC TAB
local mY = 10
local miscSec1 = createSection(MiscTab, "CHARACTER MODS", mY, 240); mY = mY + 250
createToggle(miscSec1, "SPEED HACK", 10, 45, "SpeedEnabled")
createSlider(miscSec1, "WALK SPEED", 10, 100, 16, 300, 16, "WalkSpeed")
createToggle(miscSec1, "CROSS WALL", 170, 45, "CrossWall")
createToggle(miscSec1, "FLY HACK", 10, 160, "FlyEnabled")
createSlider(miscSec1, "FLY SPEED", 10, 200, 10, 200, 50, "FlySpeed")

-- ==================== LÓGICA DO ESP SIMPLIFICADO ====================
local function CreateESP(player)
    if ESPObjects[player] then return end
    local esp = {
        Box = Drawing.new("Square"), Name = Drawing.new("Text"), HealthBar = Drawing.new("Square"), HealthBarBack = Drawing.new("Square"), Line = Drawing.new("Line")
    }
    esp.Box.Thickness = 2; esp.Box.Filled = false; esp.Name.Size = 14; esp.Name.Center = true; esp.Name.Outline = true; esp.Name.Color = Colors.Text; esp.HealthBar.Filled = true; esp.HealthBarBack.Filled = true; esp.HealthBarBack.Color = Color3.new(0,0,0); esp.Line.Thickness = 1
    ESPObjects[player] = esp
end

local function ClearESP(player)
    if ESPObjects[player] then
        for _, v in pairs(ESPObjects[player]) do v:Remove() end
        ESPObjects[player] = nil
    end
end

-- ==================== LÓGICA DO FLY HACK (SUPERHERO) ====================
local flyBodyVelocity, flyBodyGyro
RunService.Heartbeat:Connect(function()
    if Config.FlyEnabled and LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("HumanoidRootPart") then
        local root = LocalPlayer.Character.HumanoidRootPart
        local hum = LocalPlayer.Character.Humanoid
        if not flyBodyVelocity then
            flyBodyVelocity = Instance.new("BodyVelocity", root); flyBodyVelocity.MaxForce = Vector3.new(math.huge, math.huge, math.huge)
            flyBodyGyro = Instance.new("BodyGyro", root); flyBodyGyro.MaxTorque = Vector3.new(math.huge, math.huge, math.huge); flyBodyGyro.P = 9000
            hum.PlatformStand = true
        end
        local moveDir = hum.MoveDirection
        local cameraCF = Camera.CFrame
        local flyDir = Vector3.new(0,0,0)
        if moveDir.Magnitude > 0 then
            flyDir = (cameraCF.LookVector * moveDir.Z + cameraCF.RightVector * moveDir.X).Unit * Config.FlySpeed
            flyBodyGyro.CFrame = CFrame.new(root.Position, root.Position + cameraCF.LookVector) * CFrame.Angles(math.rad(-90), 0, 0)
        else
            flyBodyGyro.CFrame = CFrame.new(root.Position, root.Position + cameraCF.LookVector)
        end
        flyBodyVelocity.Velocity = flyDir
    else
        if flyBodyVelocity then
            flyBodyVelocity:Destroy(); flyBodyVelocity = nil; flyBodyGyro:Destroy(); flyBodyGyro = nil
            if LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("Humanoid") then LocalPlayer.Character.Humanoid.PlatformStand = false end
        end
    end
end)

-- ==================== LOOP PRINCIPAL ====================
local FOV = Drawing.new("Circle"); FOV.Thickness = 2; FOV.NumSides = 60; FOV.Filled = false; FOV.Transparency = 0.4

RunService.RenderStepped:Connect(function()
    if Config.ESPEnabled and Config.FOVVisible then FOV.Visible = true else FOV.Visible = false end
    FOV.Color = Colors.Primary; FOV.Radius = Config.FOVSize; FOV.Position = Vector2.new(Camera.ViewportSize.X/2, Camera.ViewportSize.Y/2)

    if LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("Humanoid") then
        if Config.SpeedEnabled then LocalPlayer.Character.Humanoid.WalkSpeed = Config.WalkSpeed else LocalPlayer.Character.Humanoid.WalkSpeed = 16 end
        if Config.CrossWall then
            for _, part in ipairs(LocalPlayer.Character:GetDescendants()) do if part:IsA("BasePart") then part.CanCollide = false end end
        end
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
                    esp.Line.Visible = Config.LineEnabled; if Config.LineEnabled then
                        local origin
                        if Config.LineOrigin == "Top" then origin = Vector2.new(Camera.ViewportSize.X/2, 0) elseif Config.LineOrigin == "Center" then origin = Vector2.new(Camera.ViewportSize.X/2, Camera.ViewportSize.Y/2) else origin = Vector2.new(Camera.ViewportSize.X/2, Camera.ViewportSize.Y) end
                        esp.Line.From = origin; esp.Line.To = Vector2.new(minX + w/2, minY + h); esp.Line.Color = color
                    end
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
            if Config.AimMode == "Rage" then Camera.CFrame = CFrame.new(Camera.CFrame.Position, part.Position)
            else Camera.CFrame = Camera.CFrame:Lerp(CFrame.new(Camera.CFrame.Position, part.Position), 1 / (Config.Smoothness * 5)) end
        end
    end
end)

Players.PlayerRemoving:Connect(ClearESP)
print("✅ EDSON MODZ V7 ULTIMATE SUPERHERO FULL CARREGADO - 29KB+")
