-- ============================================================
-- EDSON MODZ V8 - ULTIMATE ANIMATED PREMIUM EDITION
-- DESIGN FLUIDO | SKELETON ESP | AIMBOT UNIVERSAL
-- RAINBOW MIRROR NAME | CLICK-TO-EXPAND (ANIMATED)
-- ============================================================

-- Serviços Essenciais
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")
local TweenService = game:GetService("TweenService")
local Camera = workspace.CurrentCamera
local LocalPlayer = Players.LocalPlayer

-- Proteção de Execução
if _G.EdsonModzLoaded then
    local old = game:GetService("CoreGui"):FindFirstChild("EdsonModzV8") or game:GetService("Players").LocalPlayer:WaitForChild("PlayerGui"):FindFirstChild("EdsonModzV8")
    if old then old:Destroy() end
end
_G.EdsonModzLoaded = true

-- Configurações (Simples e Diretas)
local Config = {
    AimEnabled = false,
    TeamCheck = false,
    VisibleCheck = true,
    SelectedPart = "Head",
    Smoothness = 4,
    Prediction = 0.12,
    FOVSize = 150,
    FOVVisible = true,
    TriggerKey = "MouseButton2",

    ESPEnabled = false,
    BoxEnabled = true,
    SkeletonEnabled = true,
    NameEnabled = true,
    HealthEnabled = true,
    LineEnabled = true,
    
    Platform = "PC",
    WalkSpeed = 16,
    SpeedEnabled = false
}

-- Paleta de Cores Premium
local Colors = {
    Primary = Color3.fromRGB(130, 50, 255),
    Background = Color3.fromRGB(15, 15, 22),
    Surface = Color3.fromRGB(25, 25, 35),
    Text = Color3.fromRGB(255, 255, 255),
    Success = Color3.fromRGB(46, 204, 113),
    Danger = Color3.fromRGB(231, 76, 60),
    Accent = Color3.fromRGB(200, 150, 255)
}

-- Criar ScreenGui de Forma Segura
local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Name = "EdsonModzV8"
ScreenGui.ResetOnSpawn = false
ScreenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling

local pcall_success = pcall(function()
    ScreenGui.Parent = game:GetService("CoreGui")
end)
if not pcall_success then
    ScreenGui.Parent = LocalPlayer:WaitForChild("PlayerGui")
end

-- Helpers de UI
local function addCorner(obj, radius)
    local c = Instance.new("UICorner")
    c.CornerRadius = UDim.new(0, radius or 12)
    c.Parent = obj
end

-- TELA DE SELEÇÃO INICIAL (Obrigatória para definir PC/Mobile)
local SelectFrame = Instance.new("Frame", ScreenGui)
SelectFrame.Size = UDim2.new(0, 360, 0, 220)
SelectFrame.Position = UDim2.new(0.5, -180, 0.5, -110)
SelectFrame.BackgroundColor3 = Colors.Background
SelectFrame.BackgroundTransparency = 0.1
addCorner(SelectFrame, 20)

local SelectTitle = Instance.new("TextLabel", SelectFrame)
SelectTitle.Size = UDim2.new(1, 0, 0, 60)
SelectTitle.Text = "EDSON MODZ V8 - PLATAFORMA"
SelectTitle.TextColor3 = Colors.Text
SelectTitle.Font = Enum.Font.GothamBold
SelectTitle.TextSize = 18
SelectTitle.BackgroundTransparency = 1

local function createSelectBtn(text, pos, platform)
    local btn = Instance.new("TextButton", SelectFrame)
    btn.Size = UDim2.new(0, 140, 0, 100)
    btn.Position = pos
    btn.Text = text
    btn.Font = Enum.Font.GothamBold
    btn.TextSize = 14
    btn.TextColor3 = Colors.Text
    btn.BackgroundColor3 = Colors.Surface
    btn.BackgroundTransparency = 0.4
    addCorner(btn, 15)

    btn.MouseButton1Click:Connect(function()
        Config.Platform = platform
        if platform == "Mobile" then
            Config.Smoothness = 2
            Config.FOVSize = 120
        end
        SelectFrame:Destroy()
        _G.InitPremiumMenu()
    end)
end

createSelectBtn("PC / DESKTOP", UDim2.new(0, 30, 0, 80), "PC")
createSelectBtn("MOBILE / CELULAR", UDim2.new(0, 190, 0, 80), "Mobile")

-- MENU PRINCIPAL (COM ANIMAÇÕES)
_G.InitPremiumMenu = function()
    local MainSize = Config.Platform == "Mobile" and UDim2.new(0, 480, 0, 360) or UDim2.new(0, 560, 0, 440)
    local MinimizedSize = UDim2.new(0, 220, 0, 55)
    
    local Main = Instance.new("Frame", ScreenGui)
    Main.Name = "Main"
    Main.Size = MinimizedSize -- Começa minimizado
    Main.Position = UDim2.new(0.5, -110, 0.1, 0)
    Main.BackgroundColor3 = Colors.Background
    Main.BackgroundTransparency = 0.2
    Main.Active = true
    Main.Draggable = true
    Main.ClipsDescendants = true
    addCorner(Main, 15)

    -- Título Rainbow Mirror (Botão de Expansão)
    local TitleBtn = Instance.new("TextButton", Main)
    TitleBtn.Name = "TitleBtn"
    TitleBtn.Size = UDim2.new(1, 0, 0, 55)
    TitleBtn.Position = UDim2.new(0, 0, 0, 0)
    TitleBtn.Text = "EDSON MODZ"
    TitleBtn.BackgroundTransparency = 1
    TitleBtn.TextColor3 = Color3.new(1, 1, 1)
    TitleBtn.Font = Enum.Font.GothamBold
    TitleBtn.TextSize = 24
    TitleBtn.AutoButtonColor = false

    local RainbowGradient = Instance.new("UIGradient", TitleBtn)
    RainbowGradient.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0, Color3.fromRGB(255, 0, 0)),
        ColorSequenceKeypoint.new(0.2, Color3.fromRGB(255, 255, 0)),
        ColorSequenceKeypoint.new(0.4, Color3.fromRGB(0, 255, 0)),
        ColorSequenceKeypoint.new(0.6, Color3.fromRGB(0, 255, 255)),
        ColorSequenceKeypoint.new(0.8, Color3.fromRGB(0, 0, 255)),
        ColorSequenceKeypoint.new(1, Color3.fromRGB(255, 0, 255))
    })
    RunService.RenderStepped:Connect(function() RainbowGradient.Offset = Vector2.new(tick() % 2 / 2, 0) end)

    -- Container do Conteúdo
    local Container = Instance.new("Frame", Main)
    Container.Name = "Container"
    Container.Size = UDim2.new(1, 0, 1, -55)
    Container.Position = UDim2.new(0, 0, 0, 55)
    Container.BackgroundTransparency = 1
    Container.Visible = false

    -- Sidebar
    local Side = Instance.new("Frame", Container)
    Side.Size = UDim2.new(0, 130, 1, -20)
    Side.Position = UDim2.new(0, 15, 0, 5)
    Side.BackgroundColor3 = Colors.Surface
    Side.BackgroundTransparency = 0.4
    addCorner(Side, 15)

    -- Conteúdo Principal
    local Content = Instance.new("Frame", Container)
    Content.Size = UDim2.new(1, -170, 1, -20)
    Content.Position = UDim2.new(0, 155, 0, 5)
    Content.BackgroundTransparency = 1

    -- Lógica de Minimizar/Expandir com Animação
    local IsMinimized = true
    TitleBtn.MouseButton1Click:Connect(function()
        IsMinimized = not IsMinimized
        if IsMinimized then
            Container.Visible = false
            TweenService:Create(Main, TweenInfo.new(0.5, Enum.EasingStyle.Quart, Enum.EasingDirection.Out), {
                Size = MinimizedSize,
                BackgroundTransparency = 0.2
            }):Play()
        else
            TweenService:Create(Main, TweenInfo.new(0.5, Enum.EasingStyle.Quart, Enum.EasingDirection.Out), {
                Size = MainSize,
                BackgroundTransparency = 0.1
            }):Play()
            task.delay(0.2, function() Container.Visible = true end)
        end
    end)

    -- Sistema de Abas
    local function createTab(parent)
        local tab = Instance.new("ScrollingFrame", parent)
        tab.Size = UDim2.new(1, 0, 1, 0)
        tab.BackgroundTransparency = 1
        tab.Visible = false
        tab.ScrollBarThickness = 0
        tab.AutomaticCanvasSize = Enum.AutomaticSize.Y
        local list = Instance.new("UIListLayout", tab)
        list.Padding = UDim.new(0, 10)
        list.SortOrder = Enum.SortOrder.LayoutOrder
        return tab
    end

    local AimTab = createTab(Content); AimTab.Visible = true
    local VisualTab = createTab(Content)
    local MiscTab = createTab(Content)

    local function createNav(text, y, tab)
        local btn = Instance.new("TextButton", Side)
        btn.Size = UDim2.new(1, -20, 0, 45)
        btn.Position = UDim2.new(0, 10, 0, y)
        btn.Text = text
        btn.Font = Enum.Font.GothamBold
        btn.TextSize = 12
        btn.TextColor3 = Colors.Text
        btn.BackgroundColor3 = Colors.Surface
        btn.BackgroundTransparency = 0.6
        addCorner(btn, 10)
        
        btn.MouseButton1Click:Connect(function()
            AimTab.Visible = false; VisualTab.Visible = false; MiscTab.Visible = false
            tab.Visible = true
        end)
    end
    createNav("AIMBOT", 20, AimTab)
    createNav("VISUAL", 75, VisualTab)
    createNav("MISC", 130, MiscTab)

    -- Componentes UI (Toggles e Sliders)
    local function createToggle(parent, text, key)
        local frame = Instance.new("Frame", parent)
        frame.Size = UDim2.new(1, -5, 0, 45)
        frame.BackgroundColor3 = Colors.Surface
        frame.BackgroundTransparency = 0.5
        addCorner(frame, 10)

        local lbl = Instance.new("TextLabel", frame)
        lbl.Size = UDim2.new(1, -60, 1, 0)
        lbl.Position = UDim2.new(0, 15, 0, 0)
        lbl.Text = text
        lbl.TextColor3 = Colors.Text
        lbl.Font = Enum.Font.GothamBold
        lbl.TextSize = 12
        lbl.BackgroundTransparency = 1
        lbl.TextXAlignment = Enum.TextXAlignment.Left

        local toggle = Instance.new("TextButton", frame)
        toggle.Size = UDim2.new(0, 45, 0, 25)
        toggle.Position = UDim2.new(1, -55, 0.5, -12)
        toggle.Text = ""
        addCorner(toggle, 12)

        local function update()
            local on = Config[key]
            TweenService:Create(toggle, TweenInfo.new(0.3), {
                BackgroundColor3 = on and Colors.Success or Colors.Danger
            }):Play()
        end
        toggle.MouseButton1Click:Connect(function() Config[key] = not Config[key]; update() end)
        update()
    end

    local function createSlider(parent, label, min, max, key)
        local frame = Instance.new("Frame", parent)
        frame.Size = UDim2.new(1, -5, 0, 60)
        frame.BackgroundColor3 = Colors.Surface
        frame.BackgroundTransparency = 0.5
        addCorner(frame, 10)

        local lbl = Instance.new("TextLabel", frame)
        lbl.Size = UDim2.new(1, -30, 0, 30)
        lbl.Position = UDim2.new(0, 15, 0, 5)
        lbl.Text = label .. ": " .. Config[key]
        lbl.TextColor3 = Colors.Text
        lbl.Font = Enum.Font.GothamBold
        lbl.TextSize = 11
        lbl.BackgroundTransparency = 1
        lbl.TextXAlignment = Enum.TextXAlignment.Left

        local track = Instance.new("Frame", frame)
        track.Size = UDim2.new(1, -30, 0, 6)
        track.Position = UDim2.new(0, 15, 0, 40)
        track.BackgroundColor3 = Colors.Background
        addCorner(track, 3)

        local fill = Instance.new("Frame", track)
        fill.Size = UDim2.new((Config[key]-min)/(max-min), 0, 1, 0)
        fill.BackgroundColor3 = Colors.Primary
        addCorner(fill, 3)

        local function move()
            local newX = math.clamp((UserInputService:GetMouseLocation().X - track.AbsolutePosition.X) / track.AbsoluteSize.X, 0, 1)
            local val = math.floor(min + (max - min) * newX + 0.5)
            Config[key] = val
            lbl.Text = label .. ": " .. val
            fill.Size = UDim2.new(newX, 0, 1, 0)
        end

        track.InputBegan:Connect(function(i)
            if i.UserInputType == Enum.UserInputType.MouseButton1 or i.UserInputType == Enum.UserInputType.Touch then
                local conn; conn = RunService.RenderStepped:Connect(move)
                UserInputService.InputEnded:Connect(function(input)
                    if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then conn:Disconnect() end
                end)
            end
        end)
    end

    -- Montar Tabs
    createToggle(AimTab, "Ativar Aimbot", "AimEnabled")
    createToggle(AimTab, "Team Check", "TeamCheck")
    createToggle(AimTab, "Wall Check", "VisibleCheck")
    createToggle(AimTab, "Mostrar FOV", "FOVVisible")
    createSlider(AimTab, "Tamanho FOV", 10, 600, "FOVSize")
    createSlider(AimTab, "Suavidade", 1, 20, "Smoothness")

    createToggle(VisualTab, "Ativar ESP", "ESPEnabled")
    createToggle(VisualTab, "Box ESP", "BoxEnabled")
    createToggle(VisualTab, "Nome ESP", "NameEnabled")
    createToggle(VisualTab, "Vida ESP", "HealthEnabled")
    createToggle(VisualTab, "Linha ESP", "LineEnabled")
    createToggle(VisualTab, "Skeleton ESP", "SkeletonEnabled")

    createToggle(MiscTab, "Ativar Speed", "SpeedEnabled")
    createSlider(MiscTab, "Velocidade", 16, 250, "WalkSpeed")

    -- LÓGICA DE AIMBOT E ESP (ESTÁVEL)
    local FOV_Circle = nil
    pcall(function()
        FOV_Circle = Drawing.new("Circle")
        FOV_Circle.Thickness = 1.5
        FOV_Circle.NumSides = 64
        FOV_Circle.Color = Colors.Primary
        FOV_Circle.Filled = false
    end)

    local function GetClosest()
        local closest, dist = nil, Config.FOVSize
        for _, p in ipairs(Players:GetPlayers()) do
            if p ~= LocalPlayer and (not Config.TeamCheck or p.Team ~= LocalPlayer.Team) then
                local char = p.Character
                if char and char:FindFirstChild(Config.SelectedPart) and char:FindFirstChild("Humanoid") and char.Humanoid.Health > 0 then
                    local part = char[Config.SelectedPart]
                    local screenPos, onScreen = Camera:WorldToViewportPoint(part.Position)
                    if onScreen then
                        local mag = (Vector2.new(Camera.ViewportSize.X/2, Camera.ViewportSize.Y/2) - Vector2.new(screenPos.X, screenPos.Y)).Magnitude
                        if mag < dist then
                            if not Config.VisibleCheck or #Camera:GetPartsObscuringTarget({part.Position}, {LocalPlayer.Character, char}) == 0 then
                                dist = mag; closest = p
                            end
                        end
                    end
                end
            end
        end
        return closest
    end

    local ESPs = {}
    local function createESP(p)
        pcall(function()
            ESPs[p] = {
                Box = {Drawing.new("Line"), Drawing.new("Line"), Drawing.new("Line"), Drawing.new("Line")},
                Skeleton = {},
                Name = Drawing.new("Text"),
                Health = Drawing.new("Square"),
                HealthBar = Drawing.new("Square"),
                Line = Drawing.new("Line")
            }
            ESPs[p].Name.Size = 14; ESPs[p].Name.Center = true; ESPs[p].Name.Outline = true; ESPs[p].Name.Color = Color3.new(1,1,1)
            ESPs[p].Line.Thickness = 1; ESPs[p].Line.Color = Color3.new(1,1,1)
            for _, v in pairs(ESPs[p].Box) do v.Thickness = 1; v.Color = Color3.new(1,1,1) end
            ESPs[p].Health.Filled = true; ESPs[p].Health.Color = Color3.new(0,0,0); ESPs[p].Health.Transparency = 0.5
            ESPs[p].HealthBar.Filled = true; ESPs[p].HealthBar.Color = Colors.Success
            for i=1, 10 do
                local line = Drawing.new("Line"); line.Thickness = 1.5; line.Color = Color3.new(1,1,1); line.Visible = false
                table.insert(ESPs[p].Skeleton, line)
            end
        end)
    end

    RunService.RenderStepped:Connect(function()
        local center = Vector2.new(Camera.ViewportSize.X/2, Camera.ViewportSize.Y/2)
        if FOV_Circle then
            FOV_Circle.Position = center
            FOV_Circle.Radius = Config.FOVSize
            FOV_Circle.Visible = Config.AimEnabled and Config.FOVVisible
        end

        if Config.AimEnabled and (Config.Platform == "Mobile" or UserInputService:IsMouseButtonPressed(Enum.UserInputType.MouseButton2)) then
            local target = GetClosest()
            if target then
                local part = target.Character[Config.SelectedPart]
                local pos = Camera:WorldToViewportPoint(part.Position + (part.Velocity * Config.Prediction))
                mousemoverel((pos.X - center.X)/Config.Smoothness, (pos.Y - center.Y)/Config.Smoothness)
            end
        end

        for p, esp in pairs(ESPs) do
            local char = p.Character
            if Config.ESPEnabled and char and char:FindFirstChild("HumanoidRootPart") and char.Humanoid.Health > 0 then
                local pos, onScreen = Camera:WorldToViewportPoint(char.HumanoidRootPart.Position)
                if onScreen then
                    local h = math.abs(Camera:WorldToViewportPoint(char.Head.Position + Vector3.new(0, 0.5, 0)).Y - Camera:WorldToViewportPoint(char.HumanoidRootPart.Position - Vector3.new(0, 3, 0)).Y)
                    local w = h * 0.6
                    if Config.BoxEnabled then
                        local l, t = pos.X - w/2, pos.Y - h/2
                        esp.Box[1].Visible = true; esp.Box[1].From = Vector2.new(l, t); esp.Box[1].To = Vector2.new(l + w, t)
                        esp.Box[2].Visible = true; esp.Box[2].From = Vector2.new(l, t + h); esp.Box[2].To = Vector2.new(l + w, t + h)
                        esp.Box[3].Visible = true; esp.Box[3].From = Vector2.new(l, t); esp.Box[3].To = Vector2.new(l, t + h)
                        esp.Box[4].Visible = true; esp.Box[4].From = Vector2.new(l + w, t); esp.Box[4].To = Vector2.new(l + w, t + h)
                    else for _, v in pairs(esp.Box) do v.Visible = false end end
                    if Config.NameEnabled then esp.Name.Visible = true; esp.Name.Position = Vector2.new(pos.X, pos.Y - h/2 - 15); esp.Name.Text = p.Name else esp.Name.Visible = false end
                    if Config.HealthEnabled then
                        local bh = h * (char.Humanoid.Health/char.Humanoid.MaxHealth)
                        esp.Health.Visible = true; esp.Health.Position = Vector2.new(pos.X - w/2 - 6, pos.Y - h/2); esp.Health.Size = Vector2.new(4, h)
                        esp.HealthBar.Visible = true; esp.HealthBar.Position = Vector2.new(pos.X - w/2 - 6, pos.Y + h/2 - bh); esp.HealthBar.Size = Vector2.new(4, bh)
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
        if Config.SpeedEnabled and LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("Humanoid") then LocalPlayer.Character.Humanoid.WalkSpeed = Config.WalkSpeed end
    end)

    Players.PlayerAdded:Connect(createESP)
    for _, p in ipairs(Players:GetPlayers()) do if p ~= LocalPlayer then createESP(p) end end
}
