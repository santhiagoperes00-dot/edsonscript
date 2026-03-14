-- ============================================================
-- EDSON MODZ V8 - VERSÃO DE COMPATIBILIDADE ABSOLUTA
-- FUNCIONA EM QUALQUER EXECUTOR (SOLARA, DELTA, FLUXUS, ETC)
-- AIMBOT UNIVERSAL | ESP BOX & VIDA | RAINBOW NAME
-- ============================================================

-- Serviços Básicos
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")
local Camera = workspace.CurrentCamera
local LocalPlayer = Players.LocalPlayer

-- Proteção para múltiplos carregamentos
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
    
    ESPEnabled = false,
    BoxEnabled = true,
    NameEnabled = true,
    HealthEnabled = true,
    LineEnabled = true,
    
    Platform = "PC",
    WalkSpeed = 16,
    SpeedEnabled = false
}

-- Cores
local Colors = {
    Primary = Color3.fromRGB(130, 50, 255),
    Background = Color3.fromRGB(15, 15, 22),
    Surface = Color3.fromRGB(25, 25, 35),
    Text = Color3.fromRGB(255, 255, 255),
    Success = Color3.fromRGB(46, 204, 113),
    Danger = Color3.fromRGB(231, 76, 60)
}

-- Interface Principal (Sem UIStroke para evitar erros)
local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Name = "EdsonModzV8"
ScreenGui.ResetOnSpawn = false
ScreenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling

-- Tenta colocar no CoreGui, se não der vai pro PlayerGui (Garante que apareça!)
local pcall_success = pcall(function()
    ScreenGui.Parent = game:GetService("CoreGui")
end)
if not pcall_success then
    ScreenGui.Parent = LocalPlayer:WaitForChild("PlayerGui")
end

-- Função para arredondar cantos (Simples)
local function addCorner(obj, radius)
    local c = Instance.new("UICorner")
    c.CornerRadius = UDim.new(0, radius or 10)
    c.Parent = obj
end

-- TELA DE SELEÇÃO INICIAL (Obrigatória para definir PC/Mobile)
local SelectFrame = Instance.new("Frame", ScreenGui)
SelectFrame.Size = UDim2.new(0, 340, 0, 200)
SelectFrame.Position = UDim2.new(0.5, -170, 0.5, -100)
SelectFrame.BackgroundColor3 = Colors.Background
SelectFrame.BorderSizePixel = 0
addCorner(SelectFrame, 15)

local SelectTitle = Instance.new("TextLabel", SelectFrame)
SelectTitle.Size = UDim2.new(1, 0, 0, 50)
SelectTitle.Text = "EDSON MODZ V8 - SELECIONE"
SelectTitle.TextColor3 = Colors.Text
SelectTitle.Font = Enum.Font.GothamBold
SelectTitle.TextSize = 16
SelectTitle.BackgroundTransparency = 1

local function createSelectBtn(text, pos, platform)
    local btn = Instance.new("TextButton", SelectFrame)
    btn.Size = UDim2.new(0, 130, 0, 80)
    btn.Position = pos
    btn.Text = text
    btn.Font = Enum.Font.GothamBold
    btn.TextSize = 14
    btn.TextColor3 = Colors.Text
    btn.BackgroundColor3 = Colors.Surface
    addCorner(btn, 12)

    btn.MouseButton1Click:Connect(function()
        Config.Platform = platform
        if platform == "Mobile" then
            Config.Smoothness = 2
            Config.FOVSize = 120
        end
        SelectFrame.Visible = false
        _G.StartEdsonMenu()
    end)
end

createSelectBtn("PC / DESKTOP", UDim2.new(0, 30, 0, 70), "PC")
createSelectBtn("MOBILE / CELULAR", UDim2.new(0, 180, 0, 70), "Mobile")

-- MENU PRINCIPAL
_G.StartEdsonMenu = function()
    local MainSize = Config.Platform == "Mobile" and UDim2.new(0, 440, 0, 340) or UDim2.new(0, 520, 0, 420)
    local Main = Instance.new("Frame", ScreenGui)
    Main.Name = "Main"
    Main.Size = MainSize
    Main.Position = UDim2.new(0.5, -MainSize.X.Offset/2, 0.5, -MainSize.Y.Offset/2)
    Main.BackgroundColor3 = Colors.Background
    Main.Active = true
    Main.Draggable = true
    addCorner(Main, 18)

    -- Título Rainbow
    local UserTitle = Instance.new("TextLabel", Main)
    UserTitle.Size = UDim2.new(1, -40, 0, 50)
    UserTitle.Position = UDim2.new(0, 20, 0, 5)
    UserTitle.Text = "EDSON MODZ"
    UserTitle.BackgroundTransparency = 1
    UserTitle.TextColor3 = Color3.new(1, 1, 1)
    UserTitle.Font = Enum.Font.GothamBold
    UserTitle.TextSize = 24
    UserTitle.TextXAlignment = Enum.TextXAlignment.Left

    local RainbowGradient = Instance.new("UIGradient", UserTitle)
    RainbowGradient.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0, Color3.fromRGB(255, 0, 0)),
        ColorSequenceKeypoint.new(0.5, Color3.fromRGB(0, 255, 255)),
        ColorSequenceKeypoint.new(1, Color3.fromRGB(255, 0, 255))
    })
    RunService.RenderStepped:Connect(function() RainbowGradient.Offset = Vector2.new(tick() % 2 / 2, 0) end)

    -- Sidebar
    local Side = Instance.new("Frame", Main)
    Side.Name = "Side"
    Side.Size = UDim2.new(0, 120, 1, -70)
    Side.Position = UDim2.new(0, 10, 0, 60)
    Side.BackgroundColor3 = Colors.Surface
    addCorner(Side, 15)

    local Content = Instance.new("Frame", Main)
    Content.Name = "Content"
    Content.Position = UDim2.new(0, 140, 0, 60)
    Content.Size = UDim2.new(1, -150, 1, -70)
    Content.BackgroundTransparency = 1

    local function createTab(parent)
        local tab = Instance.new("ScrollingFrame", parent)
        tab.Size = UDim2.new(1, 0, 1, 0)
        tab.BackgroundTransparency = 1
        tab.Visible = false
        tab.ScrollBarThickness = 2
        tab.AutomaticCanvasSize = Enum.AutomaticSize.Y
        local list = Instance.new("UIListLayout", tab)
        list.Padding = UDim.new(0, 8)
        return tab
    end

    local AimTab = createTab(Content); AimTab.Visible = true
    local VisualTab = createTab(Content)
    local MiscTab = createTab(Content)

    local function createNav(text, y, tab)
        local btn = Instance.new("TextButton", Side)
        btn.Size = UDim2.new(1, -16, 0, 40)
        btn.Position = UDim2.new(0, 8, 0, y)
        btn.Text = text
        btn.Font = Enum.Font.GothamBold
        btn.TextSize = 12
        btn.TextColor3 = Colors.Text
        btn.BackgroundColor3 = Colors.Surface
        btn.BackgroundTransparency = 0.5
        addCorner(btn, 8)
        btn.MouseButton1Click:Connect(function()
            AimTab.Visible = false; VisualTab.Visible = false; MiscTab.Visible = false
            tab.Visible = true
        end)
    end
    createNav("AIMBOT", 15, AimTab)
    createNav("VISUAL", 65, VisualTab)
    createNav("MISC", 115, MiscTab)

    -- Componentes UI (Toggles e Sliders)
    local function createToggle(parent, text, key)
        local btn = Instance.new("TextButton", parent)
        btn.Size = UDim2.new(1, -10, 0, 35)
        btn.Font = Enum.Font.GothamBold
        btn.TextColor3 = Colors.Text
        btn.TextSize = 12
        addCorner(btn, 8)
        local function update()
            btn.Text = text .. ": " .. (Config[key] and "ON" or "OFF")
            btn.BackgroundColor3 = Config[key] and Colors.Success or Colors.Danger
        end
        btn.MouseButton1Click:Connect(function() Config[key] = not Config[key]; update() end)
        update()
    end

    local function createSlider(parent, label, min, max, key)
        local frame = Instance.new("Frame", parent)
        frame.Size = UDim2.new(1, -10, 0, 50)
        frame.BackgroundTransparency = 1
        local lbl = Instance.new("TextLabel", frame)
        lbl.Size = UDim2.new(1, 0, 0, 20); lbl.Text = label .. ": " .. Config[key]; lbl.TextColor3 = Colors.Text; lbl.BackgroundTransparency = 1; lbl.Font = Enum.Font.Gotham; lbl.TextSize = 11; lbl.TextXAlignment = Enum.TextXAlignment.Left
        local track = Instance.new("Frame", frame); track.Size = UDim2.new(1, 0, 0, 6); track.Position = UDim2.new(0, 0, 0, 25); track.BackgroundColor3 = Colors.Surface; addCorner(track, 3)
        local fill = Instance.new("Frame", track); fill.Size = UDim2.new((Config[key]-min)/(max-min), 0, 1, 0); fill.BackgroundColor3 = Colors.Primary; addCorner(fill, 3)
        
        track.InputBegan:Connect(function(i)
            if i.UserInputType == Enum.UserInputType.MouseButton1 or i.UserInputType == Enum.UserInputType.Touch then
                local function move()
                    local newX = math.clamp((UserInputService:GetMouseLocation().X - track.AbsolutePosition.X) / track.AbsoluteSize.X, 0, 1)
                    local val = math.floor(min + (max - min) * newX + 0.5)
                    Config[key] = val
                    lbl.Text = label .. ": " .. val
                    fill.Size = UDim2.new(newX, 0, 1, 0)
                end
                move()
                local conn; conn = UserInputService.InputChanged:Connect(function(input)
                    if input.UserInputType == Enum.UserInputType.MouseMovement or input.UserInputType == Enum.UserInputType.Touch then move() end
                end)
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

    createToggle(MiscTab, "Ativar Speed", "SpeedEnabled")
    createSlider(MiscTab, "Velocidade", 16, 250, "WalkSpeed")

    -- LÓGICA DE AIMBOT E ESP (USANDO APENAS DRAWING SE DISPONÍVEL)
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
        end)
    end

    RunService.RenderStepped:Connect(function()
        if FOV_Circle then
            FOV_Circle.Position = Vector2.new(Camera.ViewportSize.X/2, Camera.ViewportSize.Y/2)
            FOV_Circle.Radius = Config.FOVSize
            FOV_Circle.Visible = Config.AimEnabled and Config.FOVVisible
        end

        if Config.AimEnabled and (Config.Platform == "Mobile" or UserInputService:IsMouseButtonPressed(Enum.UserInputType.MouseButton2)) then
            local target = GetClosest()
            if target then
                local part = target.Character[Config.SelectedPart]
                local pos = Camera:WorldToViewportPoint(part.Position + (part.Velocity * Config.Prediction))
                mousemoverel((pos.X - Camera.ViewportSize.X/2)/Config.Smoothness, (pos.Y - Camera.ViewportSize.Y/2)/Config.Smoothness)
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
                    if Config.LineEnabled then esp.Line.Visible = true; esp.Line.From = Vector2.new(Camera.ViewportSize.X/2, Camera.ViewportSize.Y/2); esp.Line.To = Vector2.new(pos.X, pos.Y + h/2) else esp.Line.Visible = false end
                else for _, v in pairs(esp) do if type(v) == "table" then for _, x in pairs(v) do x.Visible = false end else v.Visible = false end end end
            else for _, v in pairs(esp) do if type(v) == "table" then for _, x in pairs(v) do x.Visible = false end else v.Visible = false end end end
        end
        if Config.SpeedEnabled and LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("Humanoid") then LocalPlayer.Character.Humanoid.WalkSpeed = Config.WalkSpeed end
    end)

    Players.PlayerAdded:Connect(createESP)
    for _, p in ipairs(Players:GetPlayers()) do if p ~= LocalPlayer then createESP(p) end end
end
