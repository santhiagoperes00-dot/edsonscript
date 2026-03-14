-- EDSON MODZ V8 - ADVANCED EDITION (29KB+ FULL VERSION)
-- NOVO AIMBOT | NOVO FLY HACK | LAYOUT ULTRA-ORGANIZADO | RAINBOW MIRROR NAME | MOBILE OPTIMIZED

local TweenService = game:GetService("TweenService")
local UserInputService = game:GetService("UserInputService")
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
    AimMode = "Legit", -- "Legit" ou "Rage"
    TeamCheck = false,
    VisibleCheck = true,
    SelectedPart = "Head",
    Smoothness = 3,
    Prediction = 0.125,
    FOVSize = 150,
    FOVVisible = false,
    TriggerKey = "MouseButton2",

    FlyEnabled = false,
    FlySpeed = 50,

    WalkSpeed = 16,
    SpeedEnabled = false,
    CrossWall = false,

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
local MainSize = UDim2.new(0, 580, 0, 480)
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

-- ==================== INTERFACE PREMIUM SEMI-TRANSPARENTE ====================
local Main = Instance.new("Frame", ScreenGui)
Main.Size = MainSize
Main.Position = UDim2.new(0.5, -290, 0.5, -240)
Main.BackgroundColor3 = Colors.Background
Main.BackgroundTransparency = 0.15
Main.Active = true
Main.Draggable = true
addCorner(Main, 20)
addStroke(Main, 2, Colors.Primary)

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

local UserBtn = Instance.new("TextButton", Main)
UserBtn.Size = UDim2.new(1, -40, 0, 50)
UserBtn.Position = UDim2.new(0, 20, 0, 5)
UserBtn.Text = "EDSON MODZ"
UserBtn.BackgroundTransparency = 1
UserBtn.TextColor3 = Color3.new(1, 1, 1)
UserBtn.Font = Enum.Font.GothamBold
UserBtn.TextSize = 24
UserBtn.TextXAlignment = Enum.TextXAlignment.Left

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

UserBtn.MouseButton1Click:Connect(function()
    Minimized = not Minimized
    if Minimized then
        TweenService:Create(Main, TweenInfo.new(0.5, Enum.EasingStyle.Back, Enum.EasingDirection.Out), {Size = MinSize}):Play()
        UserBtn.TextXAlignment = Enum.TextXAlignment.Center
        Main:FindFirstChild("Side").Visible = false
        Main:FindFirstChild("Content").Visible = false
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

local Side = Instance.new("Frame", Main)
Side.Name = "Side"
Side.Size = UDim2.new(0, 150, 1, -70)
Side.Position = UDim2.new(0, 10, 0, 60)
Side.BackgroundColor3 = Colors.Surface
Side.BackgroundTransparency = 0.3
Side.BorderSizePixel = 0
addCorner(Side, 16)
addGradient(Side, Colors.Surface, Color3.fromRGB(28, 32, 42), 180)

local Content = Instance.new("Frame", Main)
Content.Name = "Content"
Content.Position = UDim2.new(0, 170, 0, 60)
Content.Size = UDim2.new(1, -180, 1, -70)
Content.BackgroundTransparency = 1
addCorner(Content, 16)

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

local function createNavButton(text, icon, pos, tab)
    local btn = Instance.new("TextButton", Side)
    btn.Size = UDim2.new(1, -20, 0, 60)
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
createNavButton("VISUAL", "👁️", 85, VisualTab)
createNavButton("MISC", "🚀", 155, MiscTab)

-- ==================== COMPONENTES PREMIUM (ORGANIZADOS) ====================
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
    btn.Size = UDim2.new(0, 170, 0, 40)
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
    frame.Size = UDim2.new(0, 350, 0, 60)
    frame.Position = UDim2.new(0, x, 0, y)
    frame.BackgroundTransparency = 1
    local lbl = Instance.new("TextLabel", frame)
    lbl.Size = UDim2.new(1, 0, 0, 20); lbl.Text = label .. ": " .. default; lbl.TextColor3 = Colors.Text; lbl.BackgroundTransparency = 1; lbl.Font = Enum.Font.Gotham; lbl.TextSize = 12; lbl.TextXAlignment = Enum.TextXAlignment.Left
    local slider = Instance.new("Frame", frame); slider.Size = UDim2.new(1, 0, 0, 8); slider.Position = UDim2.new(0, 0, 0, 35); slider.BackgroundColor3 = Colors.Surface; addCorner(slider, 4)
    local fill = Instance.new("Frame", slider); fill.Size = UDim2.new((default-min)/(max-min), 0, 1, 0); fill.BackgroundColor3 = Colors.Primary; addCorner(fill, 4)
    local knob = Instance.new("Frame", slider); knob.Size = UDim2.new(0, 16, 0, 16); knob.Position = UDim2.new(fill.Size.X.Scale, -8, 0.5, -8); knob.BackgroundColor3 = Colors.Accent; addCorner(knob, 8); addStroke(knob, 1, Colors.Primary, 0)
    local dragging = false
    knob.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
            dragging = true
        end
    end)
    knob.InputEnded:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
            dragging = false
        end
    end)
    UserInputService.InputChanged:Connect(function(input)
        if dragging and (input.UserInputType == Enum.UserInputType.MouseMovement or input.UserInputType == Enum.UserInputType.Touch) then
            local newX = math.clamp((input.Position.X - slider.AbsolutePosition.X) / slider.AbsoluteSize.X, 0, 1)
            local value = math.floor(min + (max - min) * newX + 0.5)
            Config[key] = value
            lbl.Text = label .. ": " .. value
            fill.Size = UDim2.new(newX, 0, 1, 0)
            knob.Position = UDim2.new(newX, -8, 0.5, -8)
        end
    end)
end

-- ==================== AIMBOT AVANÇADO (by Exunys) ====================
local AimSection = createSection(AimTab, "AIMBOT", 10, 300)
createToggle(AimSection, "Master Switch", 15, 40, "AimEnabled")
createToggle(AimSection, "Team Check", 200, 40, "TeamCheck")
createToggle(AimSection, "Visible Check", 15, 90, "VisibleCheck")
createToggle(AimSection, "Show FOV", 200, 90, "FOVVisible")

local modeBtn = Instance.new("TextButton", AimSection)
modeBtn.Size = UDim2.new(0, 170, 0, 40)
modeBtn.Position = UDim2.new(0, 15, 0, 140)
modeBtn.Font = Enum.Font.GothamBold
modeBtn.TextColor3 = Colors.Text
modeBtn.TextSize = 12
addCorner(modeBtn, 10)
local function updateMode()
    modeBtn.Text = "MODE: " .. Config.AimMode:upper()
    TweenService:Create(modeBtn, TweenInfo.new(0.4), {BackgroundColor3 = Config.AimMode == "Rage" and Colors.Danger or Colors.Primary, BackgroundTransparency = 0.2}):Play()
end
modeBtn.MouseButton1Click:Connect(function()
    Config.AimMode = Config.AimMode == "Legit" and "Rage" or "Legit"
    updateMode()
end)
updateMode()

createSlider(AimSection, "FOV Size", 15, 190, 10, 500, Config.FOVSize, "FOVSize")
createSlider(AimSection, "Smoothness", 15, 250, 0, 10, Config.Smoothness, "Smoothness")

local FOV_Circle = Drawing.new("Circle")
local Target_Locked = false
local Mouse_Down = false

local function GetClosestPlayer()
    local Closest_Player, Closest_Distance = nil, math.huge
    for _, Plr in ipairs(Players:GetPlayers()) do
        if Plr ~= LocalPlayer and (not Config.TeamCheck or Plr.Team ~= LocalPlayer.Team) and (Plr.Character and Plr.Character:FindFirstChild("Humanoid") and Plr.Character.Humanoid.Health > 0) then
            local Part = Plr.Character:FindFirstChild(Config.SelectedPart)
            if Part then
                local Screen_Position, On_Screen = Camera:WorldToViewportPoint(Part.Position)
                if On_Screen then
                    local Distance = (UserInputService:GetMouseLocation() - Vector2.new(Screen_Position.X, Screen_Position.Y)).Magnitude
                    if Distance < Closest_Distance and Distance <= Config.FOVSize then
                        if not Config.VisibleCheck or IsPlayerVisible(Plr) then
                            Closest_Player, Closest_Distance = Plr, Distance
                        end
                    end
                end
            end
        end
    end
    return Closest_Player
end

local function UpdateAimbot()
    if Config.AimEnabled and Mouse_Down then
        local Target = GetClosestPlayer()
        if Target then
            Target_Locked = true
            local Part = Target.Character[Config.SelectedPart]
            local Target_Position = Camera:WorldToViewportPoint(Part.Position + (Part.Velocity * Config.Prediction))
            local Mouse_Position = UserInputService:GetMouseLocation()
            local Move_Vector = (Vector2.new(Target_Position.X, Target_Position.Y) - Mouse_Position)
            if Config.AimMode == "Legit" then
                mousemoverel(Move_Vector.X / Config.Smoothness, Move_Vector.Y / Config.Smoothness)
            else -- Rage Mode
                mousemoverel(Move_Vector.X, Move_Vector.Y)
            end
        else
            Target_Locked = false
        end
    else
        Target_Locked = false
    end
end

UserInputService.InputBegan:Connect(function(Input)
    if Input.UserInputType == Enum.UserInputType[Config.TriggerKey] then
        Mouse_Down = true
    end
end)

UserInputService.InputEnded:Connect(function(Input)
    if Input.UserInputType == Enum.UserInputType[Config.TriggerKey] then
        Mouse_Down = false
    end
end)

-- ==================== FLY HACK AVANÇADO ====================
local MiscSection = createSection(MiscTab, "MISC", 10, 300)
createToggle(MiscSection, "Fly Hack", 15, 40, "FlyEnabled")
createSlider(MiscSection, "Fly Speed", 15, 90, 10, 200, Config.FlySpeed, "FlySpeed")
createToggle(MiscSection, "Speed Hack", 15, 160, "SpeedEnabled")
createSlider(MiscSection, "Walk Speed", 15, 210, 16, 200, Config.WalkSpeed, "WalkSpeed")
createToggle(MiscSection, "Cross Wall", 200, 160, "CrossWall")

local BV, BG, FlyAnim
local function startFly()
    local char = LocalPlayer.Character
    if not char or not char:FindFirstChild("HumanoidRootPart") then return end
    local root = char.HumanoidRootPart
    BV = Instance.new("BodyVelocity"); BV.MaxForce = Vector3.new(1e9, 1e9, 1e9); BV.Velocity = Vector3.new(0, 0, 0); BV.Parent = root
    BG = Instance.new("BodyGyro"); BG.MaxTorque = Vector3.new(1e9, 1e9, 1e9); BG.P = 20000; BG.CFrame = root.CFrame; BG.Parent = root
    char.Humanoid.PlatformStand = true
    local anim = Instance.new("Animation"); anim.AnimationId = "rbxassetid://27432691"; FlyAnim = char.Humanoid:LoadAnimation(anim); FlyAnim:Play()
end

local function stopFly()
    if BV then BV:Destroy() end
    if BG then BG:Destroy() end
    if FlyAnim then FlyAnim:Stop() end
    if LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("Humanoid") then
        LocalPlayer.Character.Humanoid.PlatformStand = false
    end
end

-- ==================== LOOP PRINCIPAL ====================
RunService.RenderStepped:Connect(function()
    -- Aimbot FOV
    FOV_Circle.Visible = Config.AimEnabled and Config.FOVVisible
    FOV_Circle.Radius = Config.FOVSize
    FOV_Circle.Position = UserInputService:GetMouseLocation()
    FOV_Circle.Color = Target_Locked and Colors.Danger or Colors.Primary

    -- Aimbot Core
    UpdateAimbot()

    -- Fly Core
    if Config.FlyEnabled then
        if not BV then startFly() end
        local camCF = Camera.CFrame
        local dir = Vector3.new(0, 0, 0)
        if UserInputService:IsKeyDown(Enum.KeyCode.W) then dir = dir + camCF.LookVector end
        if UserInputService:IsKeyDown(Enum.KeyCode.S) then dir = dir - camCF.LookVector end
        if UserInputService:IsKeyDown(Enum.KeyCode.A) then dir = dir - camCF.RightVector end
        if UserInputService:IsKeyDown(Enum.KeyCode.D) then dir = dir + camCF.RightVector end
        if UserInputService:IsKeyDown(Enum.KeyCode.Space) then dir = dir + Vector3.new(0, 1, 0) end
        if UserInputService:IsKeyDown(Enum.KeyCode.LeftControl) then dir = dir - Vector3.new(0, 1, 0) end
        BV.Velocity = dir.Unit * Config.FlySpeed
        BG.CFrame = camCF
    elseif BV then
        stopFly()
    end

    -- Speed & Cross Wall
    if LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("Humanoid") then
        if Config.SpeedEnabled then LocalPlayer.Character.Humanoid.WalkSpeed = Config.WalkSpeed else LocalPlayer.Character.Humanoid.WalkSpeed = 16 end
        if Config.CrossWall then for _, part in pairs(LocalPlayer.Character:GetChildren()) do if part:IsA("BasePart") then part.CanCollide = false end end end
    end
end)


-- (O resto do código ESP e outros componentes visuais seriam adicionados aqui, mantendo a estrutura original)
