-- ============================================================
-- EDSON MODZ V8 - UNIVERSAL EXECUTION EDITION
-- COMPATIBILIDADE TOTAL: PC & MOBILE (SOLARA, DELTA, FLUXUS, ETC)
-- AIMBOT UNIVERSAL | SKELETON ESP | REALISTIC BOX
-- ============================================================

-- Limpeza de instâncias anteriores (Prevenção de Erros)
local oldUI = game:GetService("CoreGui"):FindFirstChild("EdsonModzV8") or game:GetService("Players").LocalPlayer:WaitForChild("PlayerGui"):FindFirstChild("EdsonModzV8")
if oldUI then oldUI:Destroy() end

local TweenService    = game:GetService("TweenService")
local UserInputService = game:GetService("UserInputService")
local Players         = game:GetService("Players")
local RunService      = game:GetService("RunService")
local Camera          = workspace.CurrentCamera
local LocalPlayer     = Players.LocalPlayer

-- ==================== CONFIGURAÇÕES GLOBAIS ====================
local Config = {
    AimEnabled      = false,
    AimMode         = "Legit",
    TeamCheck       = false,
    VisibleCheck    = true,
    SelectedPart    = "Head",
    Smoothness      = 4,
    Prediction      = 0.12,
    FOVSize         = 150,
    FOVVisible      = true,
    TriggerKey      = "MouseButton2",

    ESPEnabled      = false,
    BoxEnabled      = true,
    SkeletonEnabled = true,
    NameEnabled     = true,
    HealthEnabled   = true,
    LineEnabled     = true,
    
    Platform        = "PC",
    SkeletonColor   = Color3.fromRGB(255, 255, 255),
    NameColor       = Color3.fromRGB(255, 255, 255),
    BoxColor        = Color3.fromRGB(255, 255, 255),
}

local Colors = {
    Primary     = Color3.fromRGB(130, 50, 255),
    Accent      = Color3.fromRGB(200, 150, 255),
    Success     = Color3.fromRGB(46, 204, 113),
    Danger      = Color3.fromRGB(231, 76, 60),
    Background  = Color3.fromRGB(15, 15, 22),
    Surface     = Color3.fromRGB(25, 25, 35),
    Text        = Color3.fromRGB(255, 255, 255),
}

-- ==================== SCREENUI (MÉTODO UNIVERSAL) ====================
local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Name = "EdsonModzV8"
ScreenGui.ResetOnSpawn = false
ScreenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling

-- Tenta CoreGui, se falhar vai pro PlayerGui (Garante que apareça!)
local success, err = pcall(function()
    ScreenGui.Parent = game:GetService("CoreGui")
end)
if not success then
    ScreenGui.Parent = LocalPlayer:WaitForChild("PlayerGui")
end

-- Funções de UI
local function addCorner(obj, radius)
    local c = Instance.new("UICorner")
    c.CornerRadius = UDim.new(0, radius or 10)
    c.Parent = obj
end

local function addStroke(obj, thickness, color, transparency)
    local s = Instance.new("UIStroke")
    s.Thickness = thickness or 1
    s.Color = color or Colors.Primary
    s.Transparency = transparency or 0.5
    s.Parent = obj
end

-- ==================== TELA DE SELEÇÃO ====================
local SelectFrame = Instance.new("Frame", ScreenGui)
SelectFrame.Size = UDim2.new(0, 360, 0, 220)
SelectFrame.Position = UDim2.new(0.5, -180, 0.5, -110)
SelectFrame.BackgroundColor3 = Colors.Background
SelectFrame.BorderSizePixel = 0
addCorner(SelectFrame, 15)
addStroke(SelectFrame, 2, Colors.Primary, 0.4)

local SelectTitle = Instance.new("TextLabel", SelectFrame)
SelectTitle.Size = UDim2.new(1, 0, 0, 50)
SelectTitle.Text = "EDSON MODZ V8 - PLATAFORMA"
SelectTitle.TextColor3 = Colors.Text
SelectTitle.Font = Enum.Font.GothamBold
SelectTitle.TextSize = 16
SelectTitle.BackgroundTransparency = 1

local function createSelectBtn(text, icon, pos, platform)
    local btn = Instance.new("TextButton", SelectFrame)
    btn.Size = UDim2.new(0, 140, 0, 100)
    btn.Position = pos
    btn.Text = icon .. "\n\n" .. text
    btn.Font = Enum.Font.GothamBold
    btn.TextSize = 13
    btn.TextColor3 = Colors.Text
    btn.BackgroundColor3 = Colors.Surface
    btn.BackgroundTransparency = 0.3
    addCorner(btn, 12)
    addStroke(btn, 1, Colors.Primary, 0.6)

    btn.MouseButton1Click:Connect(function()
        Config.Platform = platform
        if platform == "Mobile" then
            Config.TriggerKey = "Touch"
            Config.Smoothness = 2
            Config.FOVSize = 120
        end
        SelectFrame.Visible = false
        _G.InitEdsonScript()
    end)
end

createSelectBtn("PC / DESKTOP", "💻", UDim2.new(0, 30, 0, 70), "PC")
createSelectBtn("MOBILE / CELULAR", "📱", UDim2.new(0, 190, 0, 70), "Mobile")

-- ==================== SCRIPT PRINCIPAL ====================
_G.InitEdsonScript = function()
    local MainSize = Config.Platform == "Mobile" and UDim2.new(0, 460, 0, 360) or UDim2.new(0, 540, 0, 440)
    local Main = Instance.new("Frame", ScreenGui)
    Main.Name = "Main"
    Main.Size = MainSize
    Main.Position = UDim2.new(0.5, -MainSize.X.Offset/2, 0.5, -MainSize.Y.Offset/2)
    Main.BackgroundColor3 = Colors.Background
    Main.BackgroundTransparency = 0.15
    Main.Active = true
    Main.Draggable = true
    addCorner(Main, 18)
    addStroke(Main, 2, Colors.Primary, 0.4)

    -- TÍTULO RAINBOW
    local UserBtn = Instance.new("TextButton", Main)
    UserBtn.Size = UDim2.new(1, -40, 0, 50)
    UserBtn.Position = UDim2.new(0, 20, 0, 5)
    UserBtn.Text = "EDSON MODZ"
    UserBtn.BackgroundTransparency = 1
    UserBtn.TextColor3 = Color3.new(1, 1, 1)
    UserBtn.Font = Enum.Font.GothamBold
    UserBtn.TextSize = Config.Platform == "Mobile" and 22 or 26
    UserBtn.TextXAlignment = Enum.TextXAlignment.Left

    local RainbowGradient = Instance.new("UIGradient", UserBtn)
    RainbowGradient.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0,   Color3.fromRGB(255, 0, 0)),
        ColorSequenceKeypoint.new(0.5, Color3.fromRGB(0, 255, 255)),
        ColorSequenceKeypoint.new(1,   Color3.fromRGB(255, 0, 255))
    })
    RunService.RenderStepped:Connect(function() RainbowGradient.Offset = Vector2.new(tick() % 2 / 2, 0) end)

    -- Botão Minimizar
    local MinBtn = Instance.new("TextButton", Main)
    MinBtn.Size = UDim2.new(0, 30, 0, 30)
    MinBtn.Position = UDim2.new(1, -40, 0, 10)
    MinBtn.Text = "—"
    MinBtn.Font = Enum.Font.GothamBold
    MinBtn.TextColor3 = Colors.Text
    MinBtn.BackgroundColor3 = Colors.Surface
    addCorner(MinBtn, 8)

    local Minimized = false
    MinBtn.MouseButton1Click:Connect(function()
        Minimized = not Minimized
        if Minimized then
            TweenService:Create(Main, TweenInfo.new(0.4, Enum.EasingStyle.Back, Enum.EasingDirection.In), {Size = UDim2.new(0, 180, 0, 50)}):Play()
            MinBtn.Text = "+"
            UserBtn.TextXAlignment = Enum.TextXAlignment.Center
            Main:FindFirstChild("Side").Visible = false
            Main:FindFirstChild("Content").Visible = false
        else
            TweenService:Create(Main, TweenInfo.new(0.4, Enum.EasingStyle.Back, Enum.EasingDirection.Out), {Size = MainSize}):Play()
            MinBtn.Text = "—"
            UserBtn.TextXAlignment = Enum.TextXAlignment.Left
            Main:FindFirstChild("Side").Visible = true
            Main:FindFirstChild("Content").Visible = true
        end
    end)

    -- SIDEBAR
    local Side = Instance.new("Frame", Main)
    Side.Name = "Side"
    Side.Size = UDim2.new(0, Config.Platform == "Mobile" and 110 or 140, 1, -70)
    Side.Position = UDim2.new(0, 10, 0, 60)
    Side.BackgroundColor3 = Colors.Surface
    Side.BackgroundTransparency = 0.3
    addCorner(Side, 15)

    local Content = Instance.new("Frame", Main)
    Content.Name = "Content"
    Content.Position = UDim2.new(0, Side.Size.X.Offset + 20, 0, 60)
    Content.Size = UDim2.new(1, -(Side.Size.X.Offset + 30), 1, -70)
    Content.BackgroundTransparency = 1

    local function createTab(parent)
        local tab = Instance.new("ScrollingFrame", parent)
        tab.Size = UDim2.new(1, 0, 1, 0)
        tab.BackgroundTransparency = 1
        tab.ScrollBarThickness = 2
        tab.Visible = false
        tab.AutomaticCanvasSize = Enum.AutomaticSize.Y
        local list = Instance.new("UIListLayout", tab)
        list.Padding = UDim.new(0, 8)
        list.SortOrder = Enum.SortOrder.LayoutOrder
        return tab
    end

    local AimTab = createTab(Content); AimTab.Visible = true
    local VisualTab = createTab(Content)
    local MiscTab = createTab(Content)

    local function createNav(text, icon, y, tab)
        local btn = Instance.new("TextButton", Side)
        btn.Size = UDim2.new(1, -16, 0, 40)
        btn.Position = UDim2.new(0, 8, 0, y)
        btn.Text = icon .. " " .. text
        btn.Font = Enum.Font.GothamBold
        btn.TextSize = 11
        btn.TextColor3 = Colors.Text
        btn.BackgroundColor3 = Colors.Surface
        btn.BackgroundTransparency = 0.5
        addCorner(btn, 8)
        btn.MouseButton1Click:Connect(function()
            AimTab.Visible = false; VisualTab.Visible = false; MiscTab.Visible = false
            tab.Visible = true
        end)
    end
    createNav("AIMBOT", "🎯", 15, AimTab)
    createNav("VISUAL", "👁️", 65, VisualTab)
    createNav("MISC", "🚀", 115, MiscTab)

    -- UI Helpers
    local function createSection(parent, title, height)
        local sec = Instance.new("Frame", parent)
        sec.Size = UDim2.new(1, -10, 0, height or 140)
        sec.BackgroundColor3 = Colors.Surface
        sec.BackgroundTransparency = 0.4
        addCorner(sec, 12)
        local lbl = Instance.new("TextLabel", sec)
        lbl.Size = UDim2.new(1, -20, 0, 25)
        lbl.Position = UDim2.new(0, 10, 0, 5)
        lbl.Text = "» " .. title
        lbl.TextColor3 = Colors.Accent
        lbl.Font = Enum.Font.GothamBold
        lbl.TextSize = 12
        lbl.BackgroundTransparency = 1
        lbl.TextXAlignment = Enum.TextXAlignment.Left
        return sec
    end

    local function createToggle(parent, text, x, y, key)
        local btn = Instance.new("TextButton", parent)
        btn.Size = UDim2.new(0, Config.Platform == "Mobile" and 120 or 160, 0, 32)
        btn.Position = UDim2.new(0, x, 0, y)
        btn.Font = Enum.Font.GothamBold
        btn.TextColor3 = Colors.Text
        btn.TextSize = 10
        addCorner(btn, 8)
        local function update()
            local on = Config[key]
            btn.Text = text .. ": " .. (on and "ON" or "OFF")
            btn.BackgroundColor3 = on and Colors.Success or Colors.Danger
            btn.BackgroundTransparency = 0.2
        end
        btn.MouseButton1Click:Connect(function() Config[key] = not Config[key]; update() end)
        update()
    end

    local function createSlider(parent, label, x, y, min, max, default, key)
        local frame = Instance.new("Frame", parent)
        frame.Size = UDim2.new(1, -20, 0, 45)
        frame.Position = UDim2.new(0, x, 0, y)
        frame.BackgroundTransparency = 1
        local lbl = Instance.new("TextLabel", frame)
        lbl.Size = UDim2.new(1, 0, 0, 15); lbl.Text = label .. ": " .. default; lbl.TextColor3 = Colors.Text; lbl.BackgroundTransparency = 1; lbl.Font = Enum.Font.Gotham; lbl.TextSize = 10; lbl.TextXAlignment = Enum.TextXAlignment.Left
        local track = Instance.new("Frame", frame); track.Size = UDim2.new(1, 0, 0, 4); track.Position = UDim2.new(0, 0, 0, 25); track.BackgroundColor3 = Colors.Surface; addCorner(track, 2)
        local fill = Instance.new("Frame", track); fill.Size = UDim2.new((default-min)/(max-min), 0, 1, 0); fill.BackgroundColor3 = Colors.Primary; addCorner(fill, 2)
        local knob = Instance.new("Frame", track); knob.Size = UDim2.new(0, 14, 0, 14); knob.Position = UDim2.new(fill.Size.X.Scale, -7, 0.5, -7); knob.BackgroundColor3 = Colors.Accent; addCorner(knob, 7)
        local dragging = false
        knob.InputBegan:Connect(function(i) if i.UserInputType == Enum.UserInputType.MouseButton1 or i.UserInputType == Enum.UserInputType.Touch then dragging = true end end)
        knob.InputEnded:Connect(function(i) if i.UserInputType == Enum.UserInputType.MouseButton1 or i.UserInputType == Enum.UserInputType.Touch then dragging = false end end)
        UserInputService.InputChanged:Connect(function(i)
            if dragging and (i.UserInputType == Enum.UserInputType.MouseMovement or i.UserInputType == Enum.UserInputType.Touch) then
                local newX = math.clamp((i.Position.X - track.AbsolutePosition.X) / track.AbsoluteSize.X, 0, 1)
                local value = math.floor(min + (max - min) * newX + 0.5)
                Config[key] = value
                lbl.Text = label .. ": " .. value
                fill.Size = UDim2.new(newX, 0, 1, 0)
                knob.Position = UDim2.new(newX, -7, 0.5, -7)
            end
        end)
    end

    -- ABAS CONTENT
    local s1 = createSection(AimTab, "AIMBOT", 220)
    createToggle(s1, "Enable", 10, 35, "AimEnabled")
    createToggle(s1, "Team Check", Config.Platform == "Mobile" and 140 or 180, 35, "TeamCheck")
    createToggle(s1, "Wall Check", 10, 75, "VisibleCheck")
    createToggle(s1, "Show FOV", Config.Platform == "Mobile" and 140 or 180, 75, "FOVVisible")
    createSlider(s1, "FOV Size", 10, 115, 10, 600, Config.FOVSize, "FOVSize")
    createSlider(s1, "Smoothness", 10, 165, 1, 20, Config.Smoothness, "Smoothness")

    local s2 = createSection(VisualTab, "ESP", 220)
    createToggle(s2, "Enable ESP", 10, 35, "ESPEnabled")
    createToggle(s2, "Skeleton", Config.Platform == "Mobile" and 140 or 180, 35, "SkeletonEnabled")
    createToggle(s2, "Box", 10, 75, "BoxEnabled")
    createToggle(s2, "Name", Config.Platform == "Mobile" and 140 or 180, 75, "NameEnabled")
    createToggle(s2, "Health", 10, 115, "HealthEnabled")
    createToggle(s2, "Line", Config.Platform == "Mobile" and 140 or 180, 115, "LineEnabled")

    local s3 = createSection(MiscTab, "MISC", 100)
    createSlider(s3, "WalkSpeed", 10, 35, 16, 250, 16, "WalkSpeed")

    -- LÓGICA DO AIMBOT
    local FOV_Circle = Drawing.new("Circle")
    FOV_Circle.Thickness = 1.5; FOV_Circle.NumSides = 64; FOV_Circle.Color = Colors.Primary; FOV_Circle.Filled = false

    local function GetClosestPlayer()
        local closest, closestDist = nil, Config.FOVSize
        for _, p in ipairs(Players:GetPlayers()) do
            if p ~= LocalPlayer and (not Config.TeamCheck or p.Team ~= LocalPlayer.Team) then
                local char = p.Character
                if char and char:FindFirstChild(Config.SelectedPart) and char:FindFirstChild("Humanoid") and char.Humanoid.Health > 0 then
                    local part = char[Config.SelectedPart]
                    local screenPos, onScreen = Camera:WorldToViewportPoint(part.Position)
                    if onScreen then
                        local viewport = Camera.ViewportSize
                        local center = Vector2.new(viewport.X / 2, viewport.Y / 2)
                        local dist = (center - Vector2.new(screenPos.X, screenPos.Y)).Magnitude
                        if dist < closestDist then
                            if not Config.VisibleCheck or #Camera:GetPartsObscuringTarget({part.Position}, {LocalPlayer.Character, char}) == 0 then
                                closestDist = dist
                                closest = p
                            end
                        end
                    end
                end
            end
        end
        return closest
    end

    -- LÓGICA DO ESP
    local ESPObjects = {}
    local function createESP(p)
        if ESPObjects[p] then return end
        local esp = {
            Box = {Drawing.new("Line"), Drawing.new("Line"), Drawing.new("Line"), Drawing.new("Line")},
            Skeleton = {},
            Name = Drawing.new("Text"),
            Health = Drawing.new("Square"),
            HealthBar = Drawing.new("Square"),
            Line = Drawing.new("Line")
        }
        esp.Name.Size = 14; esp.Name.Center = true; esp.Name.Outline = true; esp.Name.Color = Config.NameColor
        esp.Line.Thickness = 1.5; esp.Line.Color = Config.BoxColor
        for _, v in pairs(esp.Box) do v.Thickness = 1.5; v.Color = Config.BoxColor; v.Visible = false end
        esp.Health.Filled = true; esp.Health.Color = Color3.fromRGB(0,0,0); esp.Health.Transparency = 0.5
        esp.HealthBar.Filled = true; esp.HealthBar.Color = Colors.Success
        for i=1, 10 do
            local line = Drawing.new("Line"); line.Thickness = 2; line.Color = Config.SkeletonColor; line.Visible = false
            table.insert(esp.Skeleton, line)
        end
        ESPObjects[p] = esp
    end

    -- LOOP PRINCIPAL
    RunService.RenderStepped:Connect(function()
        local viewport = Camera.ViewportSize
        local center = Vector2.new(viewport.X / 2, viewport.Y / 2)
        FOV_Circle.Position = center; FOV_Circle.Radius = Config.FOVSize; FOV_Circle.Visible = Config.AimEnabled and Config.FOVVisible

        -- Aimbot
        local isAiming = (Config.Platform == "Mobile" and Config.AimEnabled) or (Config.AimEnabled and UserInputService:IsMouseButtonPressed(Enum.UserInputType[Config.TriggerKey]))
        if isAiming then
            local target = GetClosestPlayer()
            if target then
                local part = target.Character[Config.SelectedPart]
                local pos = Camera:WorldToViewportPoint(part.Position + (part.Velocity * Config.Prediction))
                mousemoverel((pos.X - center.X) / Config.Smoothness, (pos.Y - center.Y) / Config.Smoothness)
            end
        end

        -- ESP
        for p, esp in pairs(ESPObjects) do
            local char = p.Character
            if Config.ESPEnabled and char and char:FindFirstChild("HumanoidRootPart") and char:FindFirstChild("Humanoid") and char.Humanoid.Health > 0 then
                local root = char.HumanoidRootPart
                local pos, onScreen = Camera:WorldToViewportPoint(root.Position)
                if onScreen then
                    local headPos = Camera:WorldToViewportPoint(char.Head.Position + Vector3.new(0, 0.5, 0))
                    local legPos = Camera:WorldToViewportPoint(root.Position - Vector3.new(0, 3, 0))
                    local h = math.abs(headPos.Y - legPos.Y)
                    local w = h * 0.6
                    
                    if Config.BoxEnabled then
                        local left, top = pos.X - w/2, pos.Y - h/2
                        esp.Box[1].Visible = true; esp.Box[1].From = Vector2.new(left, top); esp.Box[1].To = Vector2.new(left + w, top)
                        esp.Box[2].Visible = true; esp.Box[2].From = Vector2.new(left, top + h); esp.Box[2].To = Vector2.new(left + w, top + h)
                        esp.Box[3].Visible = true; esp.Box[3].From = Vector2.new(left, top); esp.Box[3].To = Vector2.new(left, top + h)
                        esp.Box[4].Visible = true; esp.Box[4].From = Vector2.new(left + w, top); esp.Box[4].To = Vector2.new(left + w, top + h)
                    else for _, v in pairs(esp.Box) do v.Visible = false end end

                    if Config.NameEnabled then esp.Name.Visible = true; esp.Name.Position = Vector2.new(pos.X, pos.Y - h/2 - 15); esp.Name.Text = p.Name else esp.Name.Visible = false end
                    if Config.HealthEnabled then
                        local barH = h * (char.Humanoid.Health / char.Humanoid.MaxHealth)
                        esp.Health.Visible = true; esp.Health.Position = Vector2.new(pos.X - w/2 - 6, pos.Y - h/2); esp.Health.Size = Vector2.new(4, h)
                        esp.HealthBar.Visible = true; esp.HealthBar.Position = Vector2.new(pos.X - w/2 - 6, pos.Y + h/2 - barH); esp.HealthBar.Size = Vector2.new(4, barH)
                        esp.HealthBar.Color = Color3.fromHSV(char.Humanoid.Health/100 * 0.3, 1, 1)
                    else esp.Health.Visible = false; esp.HealthBar.Visible = false end
                    if Config.LineEnabled then esp.Line.Visible = true; esp.Line.From = center; esp.Line.To = Vector2.new(pos.X, pos.Y + h/2) else esp.Line.Visible = false end
                    if Config.SkeletonEnabled then
                        local parts = {char:FindFirstChild("Head"), char:FindFirstChild("UpperTorso") or char:FindFirstChild("Torso"), char:FindFirstChild("LowerTorso") or char:FindFirstChild("Torso"), char:FindFirstChild("LeftUpperArm") or char:FindFirstChild("Left Arm"), char:FindFirstChild("LeftLowerArm") or char:FindFirstChild("Left Arm"), char:FindFirstChild("RightUpperArm") or char:FindFirstChild("Right Arm"), char:FindFirstChild("RightLowerArm") or char:FindFirstChild("Right Arm"), char:FindFirstChild("LeftUpperLeg") or char:FindFirstChild("Left Leg"), char:FindFirstChild("LeftLowerLeg") or char:FindFirstChild("Left Leg"), char:FindFirstChild("RightUpperLeg") or char:FindFirstChild("Right Leg"), char:FindFirstChild("RightLowerLeg") or char:FindFirstChild("Right Leg")}
                        local connections = {{1,2}, {2,3}, {2,4}, {4,5}, {2,6}, {6,7}, {3,8}, {8,9}, {3,10}, {10,11}}
                        for i, conn in ipairs(connections) do
                            local p1, p2 = parts[conn[1]], parts[conn[2]]
                            if p1 and p2 then
                                local v1, o1 = Camera:WorldToViewportPoint(p1.Position); local v2, o2 = Camera:WorldToViewportPoint(p2.Position)
                                if o1 and o2 then esp.Skeleton[i].Visible = true; esp.Skeleton[i].From = Vector2.new(v1.X, v1.Y); esp.Skeleton[i].To = Vector2.new(v2.X, v2.Y) else esp.Skeleton[i].Visible = false end
                            else esp.Skeleton[i].Visible = false end
                        end
                    else for _, v in pairs(esp.Skeleton) do v.Visible = false end end
                else for _, v in pairs(esp) do if type(v) == "table" then for _, x in pairs(v) do x.Visible = false end else v.Visible = false end end end
            else for _, v in pairs(esp) do if type(v) == "table" then for _, x in pairs(v) do x.Visible = false end else v.Visible = false end end end
        end
        if LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("Humanoid") then LocalPlayer.Character.Humanoid.WalkSpeed = Config.WalkSpeed end
    end)

    Players.PlayerAdded:Connect(createESP)
    for _, p in ipairs(Players:GetPlayers()) do if p ~= LocalPlayer then createESP(p) end end
    Players.PlayerRemoving:Connect(function(p) if ESPObjects[p] then for _, v in pairs(ESPObjects[p]) do if type(v) == "table" then for _, x in pairs(v) do x:Remove() end else v:Remove() end end ESPObjects[p] = nil end end)
}

print("EDSON MODZ V8 CARREGADO COM SUCESSO!")
