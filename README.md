--[[
  EDSON SCRIPT v2.0 – MOBILE READY
  Features:
  - ESP: box, line, health bar, name
  - Aimbot: snap na cabeça (botão AIM)
  - Aimkill: mata o alvo (botão KILL)
  - Magnet: puxa inimigo pra frente (botão MAGNET)
  - UI estilo iPhone, botões grandes para toque
--]]

local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")
local LP = Players.LocalPlayer
local Camera = workspace.CurrentCamera

-- ========== CONFIGURAÇÕES ==========
local cfg = {
    enabled = true,
    esp = true,
    aimbotEnabled = true,      -- se false, o botão AIM não faz nada
    aimkillOnSnap = true,      -- mata ao usar AIM (se true)
    magnetDistance = 8,
}

-- ========== ESP COM DRAWING ==========
local espData = {} -- [player] = {box, line, name, healthBar}

local function createESP(plr)
    if espData[plr] then return end
    local box = Drawing.new("Square")
    box.Visible = false
    box.Color = Color3.fromRGB(255, 255, 255)
    box.Thickness = 1.5
    box.Filled = false
    box.Transparency = 0.5
    
    local line = Drawing.new("Line")
    line.Visible = false
    line.Color = Color3.fromRGB(0, 255, 0)
    line.Thickness = 1
    
    local nameTag = Drawing.new("Text")
    nameTag.Visible = false
    nameTag.Color = Color3.fromRGB(255, 255, 255)
    nameTag.Size = 13
    nameTag.Center = true
    nameTag.Outline = true
    nameTag.OutlineColor = Color3.fromRGB(0,0,0)
    
    local healthBar = Drawing.new("Rectangle")
    healthBar.Visible = false
    healthBar.Color = Color3.fromRGB(0, 255, 0)
    healthBar.Filled = true
    healthBar.Thickness = 0
    
    espData[plr] = {box, line, nameTag, healthBar}
end

local function updateESP()
    for plr, objs in pairs(espData) do
        local char = plr.Character
        if char and char:FindFirstChild("HumanoidRootPart") and char:FindFirstChild("Humanoid") then
            local humanoid = char.Humanoid
            if humanoid.Health > 0 then
                local root = char.HumanoidRootPart
                local head = char:FindFirstChild("Head")
                local pos, onScreen = Camera:WorldToViewportPoint(root.Position)
                if onScreen then
                    local x, y = pos.X, pos.Y
                    local boxWidth, boxHeight = 60, 100
                    objs[1].Size = Vector2.new(boxWidth, boxHeight)
                    objs[1].Position = Vector2.new(x - boxWidth/2, y - boxHeight/2)
                    objs[1].Visible = cfg.esp
                    
                    objs[2].From = Vector2.new(Camera.ViewportSize.X/2, Camera.ViewportSize.Y)
                    objs[2].To = Vector2.new(x, y)
                    objs[2].Visible = cfg.esp
                    
                    objs[3].Text = plr.Name .. " [" .. math.floor(humanoid.Health) .. "]"
                    objs[3].Position = Vector2.new(x, y - boxHeight/2 - 12)
                    objs[3].Visible = cfg.esp
                    
                    local healthPercent = humanoid.Health / humanoid.MaxHealth
                    objs[4].Size = Vector2.new(boxWidth * healthPercent, 4)
                    objs[4].Position = Vector2.new(x - boxWidth/2, y + boxHeight/2 + 2)
                    objs[4].Visible = cfg.esp
                    objs[4].Color = Color3.fromRGB(255 * (1 - healthPercent), 255 * healthPercent, 0)
                else
                    for _, obj in ipairs(objs) do obj.Visible = false end
                end
            else
                for _, obj in ipairs(objs) do obj.Visible = false end
            end
        else
            for _, obj in ipairs(objs) do obj.Visible = false end
        end
    end
end

-- ========== AIMBOT (SNAP HEAD) ==========
local function getClosestToCrosshair()
    local closest, bestDist = nil, math.huge
    local center = Vector2.new(Camera.ViewportSize.X/2, Camera.ViewportSize.Y/2)
    for _, plr in ipairs(Players:GetPlayers()) do
        if plr ~= LP and plr.Character and plr.Character:FindFirstChild("Head") then
            local headPos, onScreen = Camera:WorldToViewportPoint(plr.Character.Head.Position)
            if onScreen then
                local dist = (Vector2.new(headPos.X, headPos.Y) - center).Magnitude
                if dist < bestDist then
                    bestDist = dist
                    closest = plr
                end
            end
        end
    end
    return closest
end

local function aimAtHead(plr)
    if not plr or not plr.Character or not plr.Character:FindFirstChild("Head") then return end
    local headPos = plr.Character.Head.Position
    Camera.CFrame = CFrame.new(Camera.CFrame.Position, headPos)
    if cfg.aimkillOnSnap then
        local tool = LP.Character and LP.Character:FindFirstChildOfClass("Tool")
        if tool then tool:Activate() end
    end
end

local function killTarget(plr)
    if plr and plr.Character and plr.Character:FindFirstChild("Humanoid") then
        plr.Character.Humanoid.Health = 0
    end
end

-- ========== MAGNET ==========
local function magnetPull(plr)
    if not plr or not plr.Character or not plr.Character:FindFirstChild("HumanoidRootPart") then return end
    if not LP.Character or not LP.Character:FindFirstChild("HumanoidRootPart") then return end
    local targetRoot = plr.Character.HumanoidRootPart
    local playerRoot = LP.Character.HumanoidRootPart
    local newPos = playerRoot.Position + (playerRoot.CFrame.LookVector * cfg.magnetDistance)
    targetRoot.CFrame = CFrame.new(newPos)
end

-- ========== UI ESTILO IPHONE COM BOTÕES ==========
local screenGui = Instance.new("ScreenGui")
screenGui.Name = "EdsonScriptUI"
screenGui.Parent = game:GetService("CoreGui")

-- Frame principal (janela)
local mainFrame = Instance.new("Frame")
mainFrame.Size = UDim2.new(0, 320, 0, 540)
mainFrame.Position = UDim2.new(0.5, -160, 0.5, -270)
mainFrame.BackgroundColor3 = Color3.fromRGB(20, 20, 25)
mainFrame.BackgroundTransparency = 0.15
mainFrame.BorderSizePixel = 0
mainFrame.ClipsDescendants = true
mainFrame.Parent = screenGui

-- Blur
local blur = Instance.new("BlurEffect")
blur.Size = 10
blur.Parent = mainFrame

-- Cantos arredondados
local corner = Instance.new("UICorner")
corner.CornerRadius = UDim.new(0, 20)
corner.Parent = mainFrame

-- Borda
local stroke = Instance.new("UIStroke")
stroke.Color = Color3.fromRGB(100, 100, 110)
stroke.Thickness = 1
stroke.Parent = mainFrame

-- Título
local title = Instance.new("TextLabel")
title.Size = UDim2.new(1, 0, 0, 50)
title.Position = UDim2.new(0, 0, 0, 0)
title.BackgroundTransparency = 1
title.Text = "EDSON SCRIPT"
title.TextColor3 = Color3.fromRGB(255, 255, 255)
title.Font = Enum.Font.GothamBold
title.TextSize = 24
title.Parent = mainFrame

-- Subtítulo
local sub = Instance.new("TextLabel")
sub.Size = UDim2.new(1, 0, 0, 20)
sub.Position = UDim2.new(0, 0, 0, 45)
sub.BackgroundTransparency = 1
sub.Text = "•  MOBILE CONTROLS  •"
sub.TextColor3 = Color3.fromRGB(150, 150, 170)
sub.Font = Enum.Font.Gotham
sub.TextSize = 12
sub.Parent = mainFrame

-- Scroll container
local scrolling = Instance.new("ScrollingFrame")
scrolling.Size = UDim2.new(1, 0, 1, -80)
scrolling.Position = UDim2.new(0, 0, 0, 70)
scrolling.BackgroundTransparency = 1
scrolling.CanvasSize = UDim2.new(0, 0, 0, 400)
scrolling.ScrollBarThickness = 4
scrolling.Parent = mainFrame

local uiList = Instance.new("UIListLayout")
uiList.Padding = UDim.new(0, 12)
uiList.SortOrder = Enum.SortOrder.LayoutOrder
uiList.Parent = scrolling

-- Função para criar toggle (botão ON/OFF)
local function createToggle(labelText, defaultValue, callback)
    local frame = Instance.new("Frame")
    frame.Size = UDim2.new(1, -20, 0, 50)
    frame.BackgroundColor3 = Color3.fromRGB(30, 30, 35)
    frame.BackgroundTransparency = 0.4
    frame.BorderSizePixel = 0
    local corner2 = Instance.new("UICorner")
    corner2.CornerRadius = UDim.new(0, 12)
    corner2.Parent = frame
    frame.Parent = scrolling
    
    local label = Instance.new("TextLabel")
    label.Size = UDim2.new(0.7, 0, 1, 0)
    label.BackgroundTransparency = 1
    label.Text = labelText
    label.TextColor3 = Color3.fromRGB(240, 240, 245)
    label.Font = Enum.Font.Gotham
    label.TextSize = 16
    label.TextXAlignment = Enum.TextXAlignment.Left
    label.Parent = frame
    
    local toggle = Instance.new("TextButton")
    toggle.Size = UDim2.new(0, 60, 0, 30)
    toggle.Position = UDim2.new(1, -70, 0.5, -15)
    toggle.BackgroundColor3 = defaultValue and Color3.fromRGB(52, 199, 89) or Color3.fromRGB(90, 90, 100)
    toggle.BackgroundTransparency = 0.2
    toggle.Text = defaultValue and "ON" or "OFF"
    toggle.TextColor3 = Color3.fromRGB(255,255,255)
    toggle.Font = Enum.Font.GothamBold
    toggle.TextSize = 14
    local corner3 = Instance.new("UICorner")
    corner3.CornerRadius = UDim.new(0, 15)
    corner3.Parent = toggle
    toggle.Parent = frame
    
    local state = defaultValue
    toggle.MouseButton1Click:Connect(function()
        state = not state
        toggle.BackgroundColor3 = state and Color3.fromRGB(52, 199, 89) or Color3.fromRGB(90, 90, 100)
        toggle.Text = state and "ON" or "OFF"
        callback(state)
    end)
    return frame
end

-- Função para criar botão de ação (grande, estilo iPhone)
local function createActionButton(labelText, color, callback)
    local btn = Instance.new("TextButton")
    btn.Size = UDim2.new(1, -20, 0, 55)
    btn.BackgroundColor3 = color
    btn.BackgroundTransparency = 0.3
    btn.Text = labelText
    btn.TextColor3 = Color3.fromRGB(255,255,255)
    btn.Font = Enum.Font.GothamBold
    btn.TextSize = 18
    local cornerBtn = Instance.new("UICorner")
    cornerBtn.CornerRadius = UDim.new(0, 15)
    cornerBtn.Parent = btn
    btn.Parent = scrolling
    btn.MouseButton1Click:Connect(callback)
    return btn
end

-- Criar toggles
createToggle("ESP (Box, Line, Health, Name)", cfg.esp, function(v) cfg.esp = v end)
createToggle("Aimbot (botão AIM)", cfg.aimbotEnabled, function(v) cfg.aimbotEnabled = v end)
createToggle("Aimkill on Snap", cfg.aimkillOnSnap, function(v) cfg.aimkillOnSnap = v end)

-- Espaço visual
local spacer = Instance.new("Frame")
spacer.Size = UDim2.new(1, 0, 0, 10)
spacer.BackgroundTransparency = 1
spacer.Parent = scrolling

-- Botões de ação
createActionButton("🎯 AIMBOT (SNAP HEAD)", Color3.fromRGB(255, 69, 58), function()
    if not cfg.aimbotEnabled then return end
    local target = getClosestToCrosshair()
    if target then aimAtHead(target) end
end)

createActionButton("💀 KILL TARGET", Color3.fromRGB(255, 45, 85), function()
    local target = getClosestToCrosshair()
    if target then killTarget(target) end
end)

createActionButton("🧲 MAGNET (PULL ENEMY)", Color3.fromRGB(88, 86, 214), function()
    local target = getClosestToCrosshair()
    if target then magnetPull(target) end
end)

-- Botão de fechar (x)
local closeBtn = Instance.new("TextButton")
closeBtn.Size = UDim2.new(0, 30, 0, 30)
closeBtn.Position = UDim2.new(1, -40, 0, 10)
closeBtn.BackgroundColor3 = Color3.fromRGB(255, 70, 70)
closeBtn.BackgroundTransparency = 0.2
closeBtn.Text = "✕"
closeBtn.TextColor3 = Color3.fromRGB(255,255,255)
closeBtn.Font = Enum.Font.GothamBold
closeBtn.TextSize = 18
local cornerClose = Instance.new("UICorner")
cornerClose.CornerRadius = UDim.new(1, 0)
cornerClose.Parent = closeBtn
closeBtn.Parent = mainFrame
closeBtn.MouseButton1Click:Connect(function()
    mainFrame.Visible = false
end)

-- Botão flutuante para abrir (no canto da tela)
local openBtn = Instance.new("TextButton")
openBtn.Size = UDim2.new(0, 55, 0, 55)
openBtn.Position = UDim2.new(1, -70, 1, -70)
openBtn.BackgroundColor3 = Color3.fromRGB(30, 30, 35)
openBtn.BackgroundTransparency = 0.2
openBtn.Text = "ES"
openBtn.TextColor3 = Color3.fromRGB(255,255,255)
openBtn.Font = Enum.Font.GothamBold
openBtn.TextSize = 22
local cornerOpen = Instance.new("UICorner")
cornerOpen.CornerRadius = UDim.new(1, 0)
cornerOpen.Parent = openBtn
openBtn.Parent = screenGui
openBtn.MouseButton1Click:Connect(function()
    mainFrame.Visible = true
end)

-- Arrastar a janela (toque)
local dragging = false
local dragStart, startPos
title.InputBegan:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.Touch or input.UserInputType == Enum.UserInputType.MouseButton1 then
        dragging = true
        dragStart = input.Position
        startPos = mainFrame.Position
    end
end)
UserInputService.InputChanged:Connect(function(input)
    if dragging and (input.UserInputType == Enum.UserInputType.Touch or input.UserInputType == Enum.UserInputType.MouseMovement) then
        local delta = input.Position - dragStart
        mainFrame.Position = UDim2.new(startPos.X.Scale, startPos.X.Offset + delta.X, startPos.Y.Scale, startPos.Y.Offset + delta.Y)
    end
end)
UserInputService.InputEnded:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.Touch or input.UserInputType == Enum.UserInputType.MouseButton1 then
        dragging = false
    end
end)

-- ========== INICIALIZAÇÃO ==========
for _, plr in ipairs(Players:GetPlayers()) do
    createESP(plr)
end
Players.PlayerAdded:Connect(createESP)
Players.PlayerRemoving:Connect(function(plr)
    if espData[plr] then
        for _, obj in ipairs(espData[plr]) do obj:Remove() end
        espData[plr] = nil
    end
end)

RunService.RenderStepped:Connect(function()
    if cfg.enabled then
        updateESP()
    end
end)

print("✅ EDSON SCRIPT MOBILE carregado | Toque nos botões para usar")
