- EDSON SCRIPT V5 - ULTIMATE EDITION
-- COR: AZUL FORTE | ESP DETALHADO | BOX CORRIGIDA

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

-- VARIÁVEIS GLOBAIS
local AimMode = "Legit"
local AimEnabled = false
local ESPEnabled = false
local TeamCheck = false
local SelectedPart = "Head"
local Smoothness = 0.3
local FOVSize = 150
local FOVVisible = false
local MainColor = Color3.fromRGB(0, 100, 255) -- AZUL FORTE
local Minimized = false
local VisibleCheck = true
local MainSize = UDim2.new(0,480,0,400)
local MinSize = UDim2.new(0,480,0,40)

-- VARIÁVEIS ESP
local ESPObjects = {}
local BoxEnabled = true
local NameEnabled = true
local HealthEnabled = true
local DistEnabled = true
local SkeletonEnabled = true

-- FUNÇÕES DE UTILIDADE
local function addCorner(obj, radius)
    local corner = Instance.new("UICorner")
    corner.CornerRadius = UDim.new(0, radius)
    corner.Parent = obj
end

local function addStroke(obj, thickness, color)
    local stroke = Instance.new("UIStroke")
    stroke.Thickness = thickness
    stroke.Color = color or Color3.new(0,0,0)
    stroke.Transparency = 0.5
    stroke.Parent = obj
end

local function IsPlayerVisible(player)
    if not VisibleCheck then return true end
    if not player or not player.Character then return false end
    
    local character = player.Character
    local head = character:FindFirstChild("Head")
    
    if not head then return false end
    
    local origin = Camera.CFrame.Position
    local direction = (head.Position - origin).Unit * (head.Position - origin).Magnitude
    
    local raycastParams = RaycastParams.new()
    raycastParams.FilterDescendantsInstances = {LocalPlayer.Character, character}
    raycastParams.FilterType = Enum.RaycastFilterType.Blacklist
    
    local result = workspace:Raycast(origin, direction, raycastParams)
    
    return result == nil
end

-- ==================== FUNÇÕES DO ESP ====================
local function CreateESPForPlayer(player)
    if ESPObjects[player] then return end
    
    local esp = {
        Box = Drawing.new("Square"),
        Name = Drawing.new("Text"),
        HealthText = Drawing.new("Text"),
        HealthBar = Drawing.new("Square"),
        HealthBarBack = Drawing.new("Square"),
        Distance = Drawing.new("Text"),
        Skeleton = {}
    }
    
    -- Box
    esp.Box.Visible = false
    esp.Box.Thickness = 2
    esp.Box.Color = MainColor
    esp.Box.Filled = false
    esp.Box.Transparency = 1
    
    -- Name
    esp.Name.Visible = false
    esp.Name.Size = 16
    esp.Name.Center = true
    esp.Name.Outline = true
    esp.Name.Color = Color3.new(1,1,1)
    
    -- Health
    esp.HealthText.Visible = false
    esp.HealthText.Size = 14
    esp.HealthText.Center = true
    esp.HealthText.Outline = true

    esp.HealthBar.Visible = false
    esp.HealthBar.Thickness = 1
    esp.HealthBar.Filled = true
    esp.HealthBar.Transparency = 0.3

    esp.HealthBarBack.Visible = false
    esp.HealthBarBack.Thickness = 1
    esp.HealthBarBack.Filled = true
    esp.HealthBarBack.Color = Color3.new(0.1, 0.1, 0.1)
    esp.HealthBarBack.Transparency = 0.5
    
    -- Distance
    esp.Distance.Visible = false
    esp.Distance.Size = 12
    esp.Distance.Center = true
    esp.Distance.Outline = true
    esp.Distance.Color = Color3.new(1,1,1)
    
    ESPObjects[player] = esp
end

local function ClearESPForPlayer(player)
    if ESPObjects[player] then
        local esp = ESPObjects[player]
        esp.Box:Remove()
        esp.Name:Remove()
        esp.HealthText:Remove()
        esp.HealthBar:Remove()
        esp.HealthBarBack:Remove()
        esp.Distance:Remove()
        for _, line in ipairs(esp.Skeleton) do
            line:Remove()
        end
        ESPObjects[player] = nil
    end
end

local function ClearAllESP()
    for player, _ in pairs(ESPObjects) do
        ClearESPForPlayer(player)
    end
    ESPObjects = {}
end

-- FUNÇÃO PARA DESENHAR ESQUELETO COMPLETO
local function DrawSkeleton(player, esp, color)
    local char = player.Character
    if not char then return end
    
    local parts = {
        Head = char:FindFirstChild("Head"),
        UpperTorso = char:FindFirstChild("UpperTorso"),
        LowerTorso = char:FindFirstChild("LowerTorso"),
        LeftUpperArm = char:FindFirstChild("LeftUpperArm"),
        LeftLowerArm = char:FindFirstChild("LeftLowerArm"),
        LeftHand = char:FindFirstChild("LeftHand"),
        RightUpperArm = char:FindFirstChild("RightUpperArm"),
        RightLowerArm = char:FindFirstChild("RightLowerArm"),
        RightHand = char:FindFirstChild("RightHand"),
        LeftUpperLeg = char:FindFirstChild("LeftUpperLeg"),
        LeftLowerLeg = char:FindFirstChild("LeftLowerLeg"),
        LeftFoot = char:FindFirstChild("LeftFoot"),
        RightUpperLeg = char:FindFirstChild("RightUpperLeg"),
        RightLowerLeg = char:FindFirstChild("RightLowerLeg"),
        RightFoot = char:FindFirstChild("RightFoot"),
        HumanoidRootPart = char:FindFirstChild("HumanoidRootPart")
    }

    local connections = {
        {"Head", "UpperTorso"},
        {"UpperTorso", "LowerTorso"},
        {"UpperTorso", "LeftUpperArm"},
        {"LeftUpperArm", "LeftLowerArm"},
        {"LeftLowerArm", "LeftHand"},
        {"UpperTorso", "RightUpperArm"},
        {"RightUpperArm", "RightLowerArm"},
        {"RightLowerArm", "RightHand"},
        {"LowerTorso", "LeftUpperLeg"},
        {"LeftUpperLeg", "LeftLowerLeg"},
        {"LeftLowerLeg", "LeftFoot"},
        {"LowerTorso", "RightUpperLeg"},
        {"RightUpperLeg", "RightLowerLeg"},
        {"RightLowerLeg", "RightFoot"}
    }

    -- Garantir que temos linhas suficientes
    while #esp.Skeleton < #connections do
        local line = Drawing.new("Line")
        line.Thickness = 2
        line.Color = color
        line.Transparency = 0.5
        table.insert(esp.Skeleton, line)
    end

    local allVisible = true
    local screenPoints = {}
    for name, part in pairs(parts) do
        if part then
            local pos, onScreen = Camera:WorldToViewportPoint(part.Position)
            if not onScreen then
                allVisible = false
                break
            end
            screenPoints[name] = Vector2.new(pos.X, pos.Y)
        else
            allVisible = false
            break
        end
    end

    if allVisible then
        for i, conn in ipairs(connections) do
            local p1 = screenPoints[conn[1]]
            local p2 = screenPoints[conn[2]]
            if p1 and p2 then
                esp.Skeleton[i].From = p1
                esp.Skeleton[i].To = p2
                esp.Skeleton[i].Color = color
                esp.Skeleton[i].Visible = true
            else
                esp.Skeleton[i].Visible = false
            end
        end
    else
        for i = 1, #esp.Skeleton do
            esp.Skeleton[i].Visible = false
        end
    end
end

-- LOOP PRINCIPAL DO ESP
RunService.RenderStepped:Connect(function()
    if not ESPEnabled then 
        ClearAllESP()
        return 
    end
    
    local validPlayers = {}
    for _, player in ipairs(Players:GetPlayers()) do
        if player ~= LocalPlayer and player.Character and player.Character:FindFirstChild("Humanoid") and player.Character.Humanoid.Health > 0 then
            if not ESPObjects[player] then CreateESPForPlayer(player) end
            table.insert(validPlayers, player)
        end
    end

    -- Limpar ESP de jogadores que saíram
    for player, _ in pairs(ESPObjects) do
        local found = false
        for _, vp in ipairs(validPlayers) do
            if vp == player then
                found = true
                break
            end
        end
        if not found then
            ClearESPForPlayer(player)
        end
    end

    for _, player in ipairs(validPlayers) do
        local esp = ESPObjects[player]
        local char = player.Character
        local hum = char.Humanoid
        local root = char:FindFirstChild("HumanoidRootPart")
        local head = char:FindFirstChild("Head")

        local isVisible = IsPlayerVisible(player)
        local color = isVisible and Color3.fromRGB(0, 255, 0) or MainColor

        local headPos, headOnScreen = Camera:WorldToViewportPoint(head.Position)
        local rootPos, rootOnScreen = Camera:WorldToViewportPoint(root.Position)

        if headOnScreen and rootOnScreen then
            local scale = 1 / (headPos - rootPos).Magnitude
            local height = math.abs(headPos.Y - rootPos.Y)
            local width = height / 2

            local boxY = headPos.Y
            local boxX = headPos.X - width / 2

            -- Box
            if BoxEnabled then
                esp.Box.Visible = true
                esp.Box.Size = Vector2.new(width, height)
                esp.Box.Position = Vector2.new(boxX, boxY)
                esp.Box.Color = color
            else
                esp.Box.Visible = false
            end

            -- Name
            if NameEnabled then
                esp.Name.Visible = true
                esp.Name.Text = player.Name
                esp.Name.Position = Vector2.new(boxX + width / 2, boxY - 20)
                esp.Name.Color = Color3.new(1,1,1)
            else
                esp.Name.Visible = false
            end

            -- Health Bar
            if HealthEnabled then
                local healthPercent = hum.Health / hum.MaxHealth
                local barWidth = width
                local barHeight = 5
                local barX = boxX
                local barY = boxY + height + 3

                esp.HealthBarBack.Visible = true
                esp.HealthBarBack.Size = Vector2.new(barWidth, barHeight)
                esp.HealthBarBack.Position = Vector2.new(barX, barY)

                esp.HealthBar.Visible = true
                esp.HealthBar.Size = Vector2.new(barWidth * healthPercent, barHeight)
                esp.HealthBar.Position = Vector2.new(barX, barY)
                esp.HealthBar.Color = Color3.fromHSV(healthPercent / 3, 1, 1)

                esp.HealthText.Visible = false -- Opcional: pode remover se não quiser o texto
            else
                esp.HealthBar.Visible = false
                esp.HealthBarBack.Visible = false
                esp.HealthText.Visible = false
            end

            -- Distance
            if DistEnabled then
                local distance = (Camera.CFrame.Position - root.Position).Magnitude
                esp.Distance.Visible = true
                esp.Distance.Text = string.format("%.0fm", distance)
                esp.Distance.Position = Vector2.new(boxX + width / 2, boxY + height + (HealthEnabled and 12 or 5))
            else
                esp.Distance.Visible = false
            end

            -- Skeleton
            if SkeletonEnabled then
                DrawSkeleton(player, esp, color)
            else
                 for i = 1, #esp.Skeleton do
                    esp.Skeleton[i].Visible = false
                end
            end
        else
            ClearESPForPlayer(player) -- Limpa se o jogador não estiver na tela
        end
    end
end)

-- Ativar/Desativar ESP (exemplo)
UIS.InputBegan:Connect(function(input, gameProcessed)
    if gameProcessed then return end
    if input.KeyCode == Enum.KeyCode.RightControl then
        ESPEnabled = not ESPEnabled
        if not ESPEnabled then
            ClearAllESP()
        end
    end
end)

print("✅ EDSON SCRIPT V5 CORRIGIDO CARREGADO - ESP DETALHADO E VIDA CORRIGIDA")
