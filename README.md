-- EDSON SCRIPT V3 - PROFESSIONAL EDITION
-- By: Edson | Design Moderno com Animacoes

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

-- VARIÁVEIS GLOBAIS
local AimEnabled = false
local ESPEnabled = false
local TeamCheck = false
local SelectedPart = "Head"
local Smoothness = 0.3
local FOVSize = 200
local FOVVisible = false
local MainColor = Color3.fromRGB(220, 40, 80) -- Rosa/vermelho moderno
local Minimized = false
local MainSize = UDim2.new(0,450,0,270)
local MinSize = UDim2.new(0,450,0,40)

-- FUNÇÃO PARA CRIAR CANTO ARREDONDADO
local function addCorner(obj, radius)
	local corner = Instance.new("UICorner")
	corner.CornerRadius = UDim.new(0, radius)
	corner.Parent = obj
end

-- FUNÇÃO PARA CRIAR SOMBRA
local function addStroke(obj, thickness, color)
	local stroke = Instance.new("UIStroke")
	stroke.Thickness = thickness
	stroke.Color = color or Color3.new(0,0,0)
	stroke.Transparency = 0.5
	stroke.Parent = obj
end

-- MAIN FRAME
local Main = Instance.new("Frame")
Main.Parent = ScreenGui
Main.Size = MainSize
Main.Position = UDim2.new(0.5,-225,0.5,-135)
Main.BackgroundColor3 = Color3.fromRGB(18, 18, 22) -- Cinza escuro moderno
Main.Active = true
Main.Draggable = true
addCorner(Main, 12)
addStroke(Main, 1, Color3.fromRGB(60,60,60))

-- TOP BAR MODERNA
local Top = Instance.new("Frame")
Top.Parent = Main
Top.Size = UDim2.new(1,0,0,45)
Top.BackgroundColor3 = MainColor
Top.BorderSizePixel = 0
addCorner(Top, 12)
-- Faz apenas as bordas superiores serem arredondadas
local topCorner = Instance.new("UICorner")
topCorner.CornerRadius = UDim.new(0,12)
topCorner.Parent = Top

local Title = Instance.new("TextLabel")
Title.Parent = Top
Title.Size = UDim2.new(1,-80,1,0)
Title.Position = UDim2.new(0,15,0,0)
Title.Text = "⚡ EDSON SCRIPT V3 ⚡"
Title.BackgroundTransparency = 1
Title.TextColor3 = Color3.new(1,1,1)
Title.Font = Enum.Font.GothamBold
Title.TextSize = 18
Title.TextXAlignment = Enum.TextXAlignment.Left

-- BOTÕES DA TOP BAR
local MinimizeBtn = Instance.new("TextButton")
MinimizeBtn.Parent = Top
MinimizeBtn.Size = UDim2.new(0,30,0,30)
MinimizeBtn.Position = UDim2.new(1,-70,0.5,-15)
MinimizeBtn.BackgroundColor3 = Color3.fromRGB(255,255,255)
MinimizeBtn.BackgroundTransparency = 0.9
MinimizeBtn.Text = "−"
MinimizeBtn.TextColor3 = Color3.new(1,1,1)
MinimizeBtn.TextSize = 20
MinimizeBtn.Font = Enum.Font.GothamBold
addCorner(MinimizeBtn, 8)

local CloseBtn = Instance.new("TextButton")
CloseBtn.Parent = Top
CloseBtn.Size = UDim2.new(0,30,0,30)
CloseBtn.Position = UDim2.new(1,-35,0.5,-15)
CloseBtn.BackgroundColor3 = Color3.fromRGB(255,70,70)
CloseBtn.BackgroundTransparency = 0.2
CloseBtn.Text = "✕"
CloseBtn.TextColor3 = Color3.new(1,1,1)
CloseBtn.TextSize = 16
CloseBtn.Font = Enum.Font.GothamBold
addCorner(CloseBtn, 8)

CloseBtn.MouseButton1Click:Connect(function()
	ScreenGui:Destroy()
end)

-- SIDE MENU MODERNO
local Side = Instance.new("Frame")
Side.Parent = Main
Side.Size = UDim2.new(0,100,1,-45)
Side.Position = UDim2.new(0,0,0,45)
Side.BackgroundColor3 = Color3.fromRGB(24, 24, 30)
Side.BorderSizePixel = 0
addCorner(Side, 0) -- Sem borda inferior esquerda
-- Canto inferior esquerdo
local sideCorner = Instance.new("UICorner")
sideCorner.CornerRadius = UDim.new(0,12)
sideCorner.Parent = Side

-- CONTENT AREA
local Content = Instance.new("Frame")
Content.Parent = Main
Content.Position = UDim2.new(0,100,0,45)
Content.Size = UDim2.new(1,-100,1,-45)
Content.BackgroundColor3 = Color3.fromRGB(18, 18, 22)
Content.BorderSizePixel = 0
addCorner(Content, 12)

-- ABAS
local AimTab = Instance.new("ScrollingFrame",Content)
AimTab.Size = UDim2.new(1,0,1,0)
AimTab.BackgroundTransparency = 1
AimTab.ScrollBarThickness = 4
AimTab.ScrollBarImageColor3 = MainColor
AimTab.CanvasSize = UDim2.new(0,0,0,400)

local VisualTab = Instance.new("ScrollingFrame",Content)
VisualTab.Size = UDim2.new(1,0,1,0)
VisualTab.BackgroundTransparency = 1
VisualTab.ScrollBarThickness = 4
VisualTab.ScrollBarImageColor3 = MainColor
VisualTab.CanvasSize = UDim2.new(0,0,0,350)
VisualTab.Visible = false

local SettingsTab = Instance.new("ScrollingFrame",Content)
SettingsTab.Size = UDim2.new(1,0,1,0)
SettingsTab.BackgroundTransparency = 1
SettingsTab.ScrollBarThickness = 4
SettingsTab.ScrollBarImageColor3 = MainColor
SettingsTab.CanvasSize = UDim2.new(0,0,0,300)
SettingsTab.Visible = false

-- BOTÕES DAS ABAS COM EMOJIS
local function createTabButton(emoji, name, pos)
	local b = Instance.new("TextButton")
	b.Parent = Side
	b.Size = UDim2.new(1,0,0,65)
	b.Position = UDim2.new(0,0,0,pos)
	b.Text = emoji .. "  " .. name
	b.Font = Enum.Font.GothamBold
	b.TextColor3 = Color3.new(0.8,0.8,0.8)
	b.BackgroundColor3 = Color3.fromRGB(30, 30, 36)
	b.BorderSizePixel = 0
	addCorner(b, 8)
	
	-- Efeito hover
	b.MouseEnter:Connect(function()
		TweenService:Create(b, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(40, 40, 46)}):Play()
	end)
	b.MouseLeave:Connect(function()
		TweenService:Create(b, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(30, 30, 36)}):Play()
	end)
	
	return b
end

local AimButton = createTabButton("🎯", "AIM", 10)
local VisualButton = createTabButton("👁️", "VISUAL", 85)
local SettingsButton = createTabButton("⚙️", "SET", 160)

-- FUNÇÃO TROCAR ABA COM ANIMAÇÃO
local function switch(tab)
	-- Anima saída
	local function animateOut(t)
		if t.Visible then
			TweenService:Create(t, TweenInfo.new(0.2), {BackgroundTransparency = 1}):Play()
			wait(0.1)
			t.Visible = false
		end
	end
	
	animateOut(AimTab)
	animateOut(VisualTab)
	animateOut(SettingsTab)
	
	wait(0.1)
	tab.Visible = true
	tab.BackgroundTransparency = 1
	TweenService:Create(tab, TweenInfo.new(0.3), {BackgroundTransparency = 0}):Play()
end

-- Efeitos nos botões das abas
local function setActiveButton(btn)
	TweenService:Create(btn, TweenInfo.new(0.3), {
		BackgroundColor3 = MainColor,
		TextColor3 = Color3.new(1,1,1)
	}):Play()
end

local function resetButton(btn)
	TweenService:Create(btn, TweenInfo.new(0.3), {
		BackgroundColor3 = Color3.fromRGB(30, 30, 36),
		TextColor3 = Color3.new(0.8,0.8,0.8)
	}):Play()
end

AimButton.MouseButton1Click:Connect(function()
	switch(AimTab)
	setActiveButton(AimButton)
	resetButton(VisualButton)
	resetButton(SettingsButton)
end)

VisualButton.MouseButton1Click:Connect(function()
	switch(VisualTab)
	setActiveButton(VisualButton)
	resetButton(AimButton)
	resetButton(SettingsButton)
end)

SettingsButton.MouseButton1Click:Connect(function()
	switch(SettingsTab)
	setActiveButton(SettingsButton)
	resetButton(AimButton)
	resetButton(VisualButton)
end)

-- FUNÇÃO MINIMIZAR
MinimizeBtn.MouseButton1Click:Connect(function()
	Minimized = not Minimized
	
	if Minimized then
		TweenService:Create(Main, TweenInfo.new(0.3), {Size = MinSize}):Play()
		MinimizeBtn.Text = "+"
		Side.Visible = false
		Content.Visible = false
	else
		TweenService:Create(Main, TweenInfo.new(0.3), {Size = MainSize}):Play()
		MinimizeBtn.Text = "−"
		wait(0.3)
		Side.Visible = true
		Content.Visible = true
	end
end)

-- FUNÇÃO PARA CRIAR BOTÕES MODERNOS
local function createModernButton(parent, text, posY, defaultColor)
	local btn = Instance.new("TextButton")
	btn.Parent = parent
	btn.Size = UDim2.new(0,180,0,40)
	btn.Position = UDim2.new(0,20,0,posY)
	btn.Text = text
	btn.Font = Enum.Font.GothamBold
	btn.TextColor3 = Color3.new(1,1,1)
	btn.BackgroundColor3 = defaultColor or Color3.fromRGB(60,60,70)
	btn.BorderSizePixel = 0
	addCorner(btn, 8)
	
	-- Hover effect
	btn.MouseEnter:Connect(function()
		TweenService:Create(btn, TweenInfo.new(0.2), {
			BackgroundColor3 = defaultColor and defaultColor:Lerp(Color3.new(1,1,1), 0.2) or Color3.fromRGB(80,80,90)
		}):Play()
	end)
	btn.MouseLeave:Connect(function()
		TweenService:Create(btn, TweenInfo.new(0.2), {
			BackgroundColor3 = defaultColor or Color3.fromRGB(60,60,70)
		}):Play()
	end)
	
	return btn
end

-- FUNÇÃO PARA CRIAR SLIDER MODERNO
local function createModernSlider(parent, label, posY, minVal, maxVal, defaultVal, callback)
	local yOffset = posY
	
	local lbl = Instance.new("TextLabel")
	lbl.Parent = parent
	lbl.Size = UDim2.new(0,100,0,20)
	lbl.Position = UDim2.new(0,20,0,yOffset)
	lbl.Text = label .. ": " .. defaultVal
	lbl.TextColor3 = Color3.new(1,1,1)
	lbl.BackgroundTransparency = 1
	lbl.Font = Enum.Font.Gotham
	lbl.TextXAlignment = Enum.TextXAlignment.Left
	
	local slider = Instance.new("Frame")
	slider.Parent = parent
	slider.Size = UDim2.new(0,200,0,6)
	slider.Position = UDim2.new(0,20,0,yOffset + 25)
	slider.BackgroundColor3 = Color3.fromRGB(60,60,70)
	addCorner(slider, 3)
	
	local fill = Instance.new("Frame")
	fill.Parent = slider
	fill.Size = UDim2.new((defaultVal-minVal)/(maxVal-minVal),0,1,0)
	fill.BackgroundColor3 = MainColor
	addCorner(fill, 3)
	
	local knob = Instance.new("Frame")
	knob.Parent = slider
	knob.Size = UDim2.new(0,16,0,16)
	knob.Position = UDim2.new(fill.Size.X.Scale, -8, -0.5, 0)
	knob.BackgroundColor3 = MainColor
	addCorner(knob, 8)
	
	local dragging = false
	
	knob.InputBegan:Connect(function(input)
		if input.UserInputType == Enum.UserInputType.MouseButton1 then
			dragging = true
		end
	end)
	
	UIS.InputEnded:Connect(function(input)
		if input.UserInputType == Enum.UserInputType.MouseButton1 then
			dragging = false
		end
	end)
	
	UIS.InputChanged:Connect(function(input)
		if dragging and input.UserInputType == Enum.UserInputType.MouseMovement then
			local pos = math.clamp(
				(input.Position.X - slider.AbsolutePosition.X) / slider.AbsoluteSize.X,
				0, 1
			)
			fill.Size = UDim2.new(pos,0,1,0)
			knob.Position = UDim2.new(pos, -8, -0.5, 0)
			
			local value = minVal + (pos * (maxVal - minVal))
			lbl.Text = label .. ": " .. math.floor(value)
			callback(value)
		end
	end)
	
	return slider
end

-- ==================== ABA AIM ====================
local yPos = 10

-- Título
local aimTitle = Instance.new("TextLabel")
aimTitle.Parent = AimTab
aimTitle.Size = UDim2.new(1,0,0,40)
aimTitle.Position = UDim2.new(0,0,0,yPos)
aimTitle.Text = "🎯 CONFIGURAÇÕES DE AIM"
aimTitle.TextColor3 = MainColor
aimTitle.BackgroundTransparency = 1
aimTitle.Font = Enum.Font.GothamBold
aimTitle.TextSize = 18
yPos = yPos + 50

-- Aimbot Toggle
local aimToggle = createModernButton(AimTab, "⚡ AIMBOT: OFF", yPos, Color3.fromRGB(60,60,70))
yPos = yPos + 50

aimToggle.MouseButton1Click:Connect(function()
	AimEnabled = not AimEnabled
	aimToggle.Text = AimEnabled and "⚡ AIMBOT: ON" or "⚡ AIMBOT: OFF"
	TweenService:Create(aimToggle, TweenInfo.new(0.3), {
		BackgroundColor3 = AimEnabled and Color3.fromRGB(0,180,0) or Color3.fromRGB(60,60,70)
	}):Play()
end)

-- Team Check
local teamToggle = createModernButton(AimTab, "🛡️ TEAM CHECK: OFF", yPos, Color3.fromRGB(60,60,70))
yPos = yPos + 50

teamToggle.MouseButton1Click:Connect(function()
	TeamCheck = not TeamCheck
	teamToggle.Text = TeamCheck and "🛡️ TEAM CHECK: ON" or "🛡️ TEAM CHECK: OFF"
	TweenService:Create(teamToggle, TweenInfo.new(0.3), {
		BackgroundColor3 = TeamCheck and Color3.fromRGB(0,180,0) or Color3.fromRGB(60,60,70)
	}):Play()
end)

-- Target Part
local partLabel = Instance.new("TextLabel")
partLabel.Parent = AimTab
partLabel.Size = UDim2.new(0,80,0,30)
partLabel.Position = UDim2.new(0,20,0,yPos)
partLabel.Text = "🎯 PART:"
partLabel.TextColor3 = Color3.new(1,1,1)
partLabel.BackgroundTransparency = 1

local partBtn = createModernButton(AimTab, SelectedPart, yPos, Color3.fromRGB(80,80,90))
partBtn.Size = UDim2.new(0,100,0,30)
partBtn.Position = UDim2.new(0,90,0,yPos)
yPos = yPos + 50

local parts = {"Head", "Torso", "HumanoidRootPart", "Left Arm", "Right Arm"}
local currentPart = 1

partBtn.MouseButton1Click:Connect(function()
	currentPart = currentPart % #parts + 1
	SelectedPart = parts[currentPart]
	partBtn.Text = SelectedPart
end)

-- FOV Toggle
local fovToggle = createModernButton(AimTab, "👁️ EXIBIR FOV: OFF", yPos, Color3.fromRGB(60,60,70))
yPos = yPos + 50

-- FOV Circle
local FOV = Instance.new("Frame")
FOV.Parent = ScreenGui
FOV.Size = UDim2.new(0,200,0,200)
FOV.Position = UDim2.new(0.5,-100,0.5,-100)
FOV.BackgroundTransparency = 1
FOV.BorderColor3 = MainColor
FOV.BorderSizePixel = 3
FOV.Visible = false
FOV.ZIndex = 10
addCorner(FOV, 100)

fovToggle.MouseButton1Click:Connect(function()
	FOVVisible = not FOVVisible
	FOV.Visible = FOVVisible
	fovToggle.Text = FOVVisible and "👁️ EXIBIR FOV: ON" or "👁️ EXIBIR FOV: OFF"
	TweenService:Create(fovToggle, TweenInfo.new(0.3), {
		BackgroundColor3 = FOVVisible and Color3.fromRGB(0,180,0) or Color3.fromRGB(60,60,70)
	}):Play()
end)

-- FOV Slider
createModernSlider(AimTab, "FOV SIZE", yPos, 50, 500, 200, function(val)
	FOVSize = val
	FOV.Size = UDim2.new(0,val,0,val)
	FOV.Position = UDim2.new(0.5,-val/2,0.5,-val/2)
end)
yPos = yPos + 80

-- Smoothness Slider
createModernSlider(AimTab, "SMOOTHNESS", yPos, 0.1, 1, 0.3, function(val)
	Smoothness = val
end)

-- ==================== ABA VISUAL (ESP) ====================
local vYPos = 10

local visualTitle = Instance.new("TextLabel")
visualTitle.Parent = VisualTab
visualTitle.Size = UDim2.new(1,0,0,40)
visualTitle.Position = UDim2.new(0,0,0,vYPos)
visualTitle.Text = "👁️ CONFIGURAÇÕES DE VISUAL"
visualTitle.TextColor3 = MainColor
visualTitle.BackgroundTransparency = 1
visualTitle.Font = Enum.Font.GothamBold
visualTitle.TextSize = 18
vYPos = vYPos + 50

-- ESP Toggle
local espToggle = createModernButton(VisualTab, "🔄 ESP: OFF", vYPos, Color3.fromRGB(60,60,70))
vYPos = vYPos + 50

espToggle.MouseButton1Click:Connect(function()
	ESPEnabled = not ESPEnabled
	espToggle.Text = ESPEnabled and "🔄 ESP: ON" or "🔄 ESP: OFF"
	TweenService:Create(espToggle, TweenInfo.new(0.3), {
		BackgroundColor3 = ESPEnabled and Color3.fromRGB(0,180,0) or Color3.fromRGB(60,60,70)
	}):Play()
	
	if ESPEnabled then
		CreateESPForAll()
	else
		ClearAllESP()
	end
end)

-- ESP Options
local boxToggle = createModernButton(VisualTab, "📦 BOX: ON", vYPos, Color3.fromRGB(0,180,0))
vYPos = vYPos + 50
local BoxEnabled = true

boxToggle.MouseButton1Click:Connect(function()
	BoxEnabled = not BoxEnabled
	boxToggle.Text = BoxEnabled and "📦 BOX: ON" or "📦 BOX: OFF"
	TweenService:Create(boxToggle, TweenInfo.new(0.3), {
		BackgroundColor3 = BoxEnabled and Color3.fromRGB(0,180,0) or Color3.fromRGB(60,60,70)
	}):Play()
end)

local nameToggle = createModernButton(VisualTab, "🏷️ NAME: ON", vYPos, Color3.fromRGB(0,180,0))
vYPos = vYPos + 50
local NameEnabled = true

nameToggle.MouseButton1Click:Connect(function()
	NameEnabled = not NameEnabled
	nameToggle.Text = NameEnabled and "🏷️ NAME: ON" or "🏷️ NAME: OFF"
	TweenService:Create(nameToggle, TweenInfo.new(0.3), {
		BackgroundColor3 = NameEnabled and Color3.fromRGB(0,180,0) or Color3.fromRGB(60,60,70)
	}):Play()
end)

local healthToggle = createModernButton(VisualTab, "❤️ HEALTH: ON", vYPos, Color3.fromRGB(0,180,0))
vYPos = vYPos + 50
local HealthEnabled = true

healthToggle.MouseButton1Click:Connect(function()
	HealthEnabled = not HealthEnabled
	healthToggle.Text = HealthEnabled and "❤️ HEALTH: ON" or "❤️ HEALTH: OFF"
	TweenService:Create(healthToggle, TweenInfo.new(0.3), {
		BackgroundColor3 = HealthEnabled and Color3.fromRGB(0,180,0) or Color3.fromRGB(60,60,70)
	}):Play()
end)

local distToggle = createModernButton(VisualTab, "📏 DISTANCE: ON", vYPos, Color3.fromRGB(0,180,0))
vYPos = vYPos + 50
local DistEnabled = true

distToggle.MouseButton1Click:Connect(function()
	DistEnabled = not DistEnabled
	distToggle.Text = DistEnabled and "📏 DISTANCE: ON" or "📏 DISTANCE: OFF"
	TweenService:Create(distToggle, TweenInfo.new(0.3), {
		BackgroundColor3 = DistEnabled and Color3.fromRGB(0,180,0) or Color3.fromRGB(60,60,70)
	}):Play()
end)

-- Skeleton ESP Toggle
local skeletonToggle = createModernButton(VisualTab, "🦴 SKELETON: OFF", vYPos, Color3.fromRGB(60,60,70))
vYPos = vYPos + 50
local SkeletonEnabled = false

skeletonToggle.MouseButton1Click:Connect(function()
	SkeletonEnabled = not SkeletonEnabled
	skeletonToggle.Text = SkeletonEnabled and "🦴 SKELETON: ON" or "🦴 SKELETON: OFF"
	TweenService:Create(skeletonToggle, TweenInfo.new(0.3), {
		BackgroundColor3 = SkeletonEnabled and Color3.fromRGB(0,180,0) or Color3.fromRGB(60,60,70)
	}):Play()
end)

-- ==================== ABA SETTINGS ====================
local sYPos = 10

local settingsTitle = Instance.new("TextLabel")
settingsTitle.Parent = SettingsTab
settingsTitle.Size = UDim2.new(1,0,0,40)
settingsTitle.Position = UDim2.new(0,0,0,sYPos)
settingsTitle.Text = "⚙️ CONFIGURAÇÕES"
settingsTitle.TextColor3 = MainColor
settingsTitle.BackgroundTransparency = 1
settingsTitle.Font = Enum.Font.GothamBold
settingsTitle.TextSize = 18
sYPos = sYPos + 50

-- Cor do painel
local colorLabel = Instance.new("TextLabel")
colorLabel.Parent = SettingsTab
colorLabel.Size = UDim2.new(0,80,0,30)
colorLabel.Position = UDim2.new(0,20,0,sYPos)
colorLabel.Text = "🎨 COR:"
colorLabel.TextColor3 = Color3.new(1,1,1)
colorLabel.BackgroundTransparency = 1

local colorDisplay = Instance.new("Frame")
colorDisplay.Parent = SettingsTab
colorDisplay.Size = UDim2.new(0,30,0,30)
colorDisplay.Position = UDim2.new(0,90,0,sYPos)
colorDisplay.BackgroundColor3 = MainColor
addCorner(colorDisplay, 6)
addStroke(colorDisplay, 1, Color3.new(1,1,1))

local colorBtn = createModernButton(SettingsTab, "🌈 MUDAR COR", sYPos, Color3.fromRGB(60,60,70))
colorBtn.Size = UDim2.new(0,120,0,30)
colorBtn.Position = UDim2.new(0,130,0,sYPos)

local colors = {
	Color3.fromRGB(220, 40, 80),  -- Rosa
	Color3.fromRGB(0, 150, 255),  -- Azul
	Color3.fromRGB(50, 205, 50),  -- Verde
	Color3.fromRGB(255, 165, 0),  -- Laranja
	Color3.fromRGB(147, 0, 211),  -- Roxo
	Color3.fromRGB(255, 255, 255) -- Branco
}
local colorIndex = 1

colorBtn.MouseButton1Click:Connect(function()
	colorIndex = colorIndex % #colors + 1
	MainColor = colors[colorIndex]
	
	Top.BackgroundColor3 = MainColor
	colorDisplay.BackgroundColor3 = MainColor
	FOV.BorderColor3 = MainColor
	AimTab.ScrollBarImageColor3 = MainColor
	VisualTab.ScrollBarImageColor3 = MainColor
	SettingsTab.ScrollBarImageColor3 = MainColor
	aimTitle.TextColor3 = MainColor
	visualTitle.TextColor3 = MainColor
	settingsTitle.TextColor3 = MainColor
end)

-- ==================== FUNÇÕES DO AIMBOT ====================
local function IsPlayerValid(player)
	if not player or player == LocalPlayer then return false end
	if not player.Character or not player.Character:FindFirstChild("Humanoid") then return false end
	local hum = player.Character.Humanoid
	if hum.Health <= 0 then return false end
	if TeamCheck and player.Team == LocalPlayer.Team then return false end
	return true
end

local function GetClosestPlayerToMouse()
	local mousePos = UIS:GetMouseLocation()
	local closest = nil
	local shortestDist = FOVSize / 2
	
	for _, player in ipairs(Players:GetPlayers()) do
		if IsPlayerValid(player) then
			local char = player.Character
			local part = char:FindFirstChild(SelectedPart) or char:FindFirstChild("Head")
			
			if part then
				local vector, onScreen = Camera:WorldToViewportPoint(part.Position)
				if onScreen then
					local dist = (Vector2.new(vector.X, vector.Y) - mousePos).Magnitude
					if dist < shortestDist then
						shortestDist = dist
						closest = player
					end
				end
			end
		end
	end
	
	return closest
end

-- AIMBOT LOOP
RunService.RenderStepped:Connect(function()
	if AimEnabled then
		local target = GetClosestPlayerToMouse()
		if target then
			local char = target.Character
			local part = char:FindFirstChild(SelectedPart) or char:FindFirstChild("Head")
			if part then
				local targetPos = part.Position
				local camPos = Camera.CFrame.Position
				local direction = (targetPos - camPos).Unit
				local newCF = CFrame.lookAt(camPos, camPos + direction)
				Camera.CFrame = Camera.CFrame:Lerp(newCF, Smoothness)
			end
		end
	end
end)

-- ==================== FUNÇÕES DO ESP ====================
local ESPObjects = {}
local SkeletonLines = {}

local function CreateESPForPlayer(player)
	if ESPObjects[player] then return end
	
	local esp = {
		Box = Drawing.new("Square"),
		Name = Drawing.new("Text"),
		Health = Drawing.new("Text"),
		Distance = Drawing.new("Text"),
		Skeleton = {}
	}
	
	-- Configurações do Box
	esp.Box.Visible = false
	esp.Box.Thickness = 2
	esp.Box.Color = MainColor
	esp.Box.Filled = false
	
	-- Configurações do Name
	esp.Name.Visible = false
	esp.Name.Size = 16
	esp.Name.Center = true
	esp.Name.Outline = true
	esp.Name.Color = Color3.new(1,1,1)
	
	-- Configurações do Health
	esp.Health.Visible = false
	esp.Health.Size = 14
	esp.Health.Center = true
	esp.Health.Outline = true
	esp.Health.Color = Color3.new(0,1,0)
	
	-- Configurações do Distance
	esp.Distance.Visible = false
	esp.Distance.Size = 12
	esp.Distance.Center = true
	esp.Distance.Outline = true
	esp.Distance.Color = Color3.new(1,1,1)
	
	-- Criar linhas do esqueleto
	for i = 1, 10 do
		local line = Drawing.new("Line")
		line.Visible = false
		line.Thickness = 2
		line.Color = MainColor
		line.Transparency = 0.5
		table.insert(esp.Skeleton, line)
	end
	
	ESPObjects[player] = esp
end

local function CreateESPForAll()
	for _, player in ipairs(Players:GetPlayers()) do
		if player ~= LocalPlayer then
			CreateESPForPlayer(player)
		end
	end
end

local function ClearAllESP()
	for player, esp in pairs(ESPObjects) do
		if esp.Box then esp.Box:Remove() end
		if esp.Name then esp.Name:Remove() end
		if esp.Health then esp.Health:Remove() end
		if esp.Distance then esp.Distance:Remove() end
		for _, line in ipairs(esp.Skeleton) do
			line:Remove()
		end
	end
	ESPObjects = {}
end

-- Função para desenhar esqueleto
local function DrawSkeleton(player, esp)
	local char = player.Character
	if not char then return end
	
	local parts = {
		Head = char:FindFirstChild("Head"),
		Torso = char:FindFirstChild("Torso") or char:FindFirstChild("UpperTorso"),
		LeftArm = char:FindFirstChild("Left Arm") or char:FindFirstChild("LeftUpperArm"),
		RightArm = char:FindFirstChild("Right Arm") or char:FindFirstChild("RightUpperArm"),
		LeftLeg = char:FindFirstChild("Left Leg") or char:FindFirstChild("LeftUpperLeg"),
		RightLeg = char:FindFirstChild("Right Leg") or char:FindFirstChild("RightUpperLeg")
	}
	
	-- Verificar se todas as partes existem
	for _, part in pairs(parts) do
		if not part then return end
	end
	
	-- Posições das partes
	local headPos, _ = Camera:WorldToViewportPoint(parts.Head.Position)
	local torsoPos, _ = Camera:WorldToViewportPoint(parts.Torso.Position)
	local leftArmPos, _ = Camera:WorldToViewportPoint(parts.LeftArm.Position)
	local rightArmPos, _ = Camera:WorldToViewportPoint(parts.RightArm.Position)
	local leftLegPos, _ = Camera:WorldToViewportPoint(parts.LeftLeg.Position)
	local rightLegPos, _ = Camera:WorldToViewportPoint(parts.RightLeg.Position)
	
	-- Configurar linhas do esqueleto
	local lines = esp.Skeleton
	local connections = {
		{headPos, torsoPos},  -- Cabeça ao torso
		{torsoPos, leftArmPos}, -- Torso ao braço esquerdo
		{torsoPos, rightArmPos}, -- Torso ao braço direito
		{torsoPos, leftLegPos}, -- Torso à perna esquerda
		{torsoPos, rightLegPos} -- Torso à perna direita
	}
	
	for i, connection in ipairs(connections) do
		if i <= #lines then
			lines[i].From = Vector2.new(connection[1].X, connection[1].Y)
			lines[i].To = Vector2.new(connection[2].X, connection[2].Y)
			lines[i].Visible = true
			lines[i].Color = MainColor
		end
	end
end

-- LOOP DO ESP
RunService.RenderStepped:Connect(function()
	if not ESPEnabled then 
		-- Esconder todos os ESP se desativado
		for _, esp in pairs(ESPObjects) do
			esp.Box.Visible = false
			esp.Name.Visible = false
			esp.Health.Visible = false
			esp.Distance.Visible = false
			for _, line in ipairs(esp.Skeleton) do
				line.Visible = false
			end
		end
		return 
	end
	
	for player, esp in pairs(ESPObjects) do
		if player and player.Character and player.Character:FindFirstChild("Humanoid") then
			local char = player.Character
			local hum = char.Humanoid
			local root = char:FindFirstChild("HumanoidRootPart") or char:FindFirstChild("Head")
			local head = char:FindFirstChild("Head")
			
			if root and hum and hum.Health > 0 then
				local pos, onScreen = Camera:WorldToViewportPoint(root.Position)
				local headPos = head and Camera:WorldToViewportPoint(head.Position) or pos
				
				if onScreen then
					-- Calcular tamanho do box baseado na distância
					local distance = (root.Position - Camera.CFrame.Position).Magnitude
					local boxHeight = math.clamp(6000 / distance, 30, 200)
					local boxWidth = boxHeight * 0.6
					
					local boxPos = Vector2.new(
						pos.X - boxWidth/2,
						headPos.Y - boxHeight - 10
					)
					
					-- BOX
					if BoxEnabled then
						esp.Box.Visible = true
						esp.Box.Size = Vector2.new(boxWidth, boxHeight)
						esp.Box.Position = boxPos
						esp.Box.Color = MainColor
					else
						esp.Box.Visible = false
					end
					
					-- NAME
					if NameEnabled then
						esp.Name.Visible = true
						esp.Name.Text = player.Name
						esp.Name.Position = Vector2.new(pos.X, boxPos.Y - 20)
					else
						esp.Name.Visible = false
					end
					
					-- HEALTH
					if HealthEnabled then
						local healthPercent = hum.Health / hum.MaxHealth
						esp.Health.Visible = true
						esp.Health.Text = string.format("%.0f/%.0f", hum.Health, hum.MaxHealth)
						esp.Health.Position = Vector2.new(pos.X, boxPos.Y + boxHeight + 5)
						esp.Health.Color = Color3.new(1 - healthPercent, healthPercent, 0)
					else
						esp.Health.Visible = false
					end
					
					-- DISTANCE
					if DistEnabled then
						esp.Distance.Visible = true
						esp.Distance.Text = math.floor(distance) .. "m"
						esp.Distance.Position = Vector2.new(pos.X, boxPos.Y + boxHeight + 25)
					else
						esp.Distance.Visible = false
					end
					
					-- SKELETON
					if SkeletonEnabled then
						DrawSkeleton(player, esp)
					else
						for _, line in ipairs(esp.Skeleton) do
							line.Visible = false
						end
					end
				else
					esp.Box.Visible = false
					esp.Name.Visible = false
					esp.Health.Visible = false
					esp.Distance.Visible = false
					for _, line in ipairs(esp.Skeleton) do
						line.Visible = false
					end
				end
			else
				esp.Box.Visible = false
				esp.Name.Visible = false
				esp.Health.Visible = false
				esp.Distance.Visible = false
				for _, line in ipairs(esp.Skeleton) do
					line.Visible = false
				end
			end
		end
	end
end)

-- Criar ESP para jogadores existentes
CreateESPForAll()

-- Atualizar quando novos jogadores entrarem
Players.PlayerAdded:Connect(function(player)
	player.CharacterAdded:Connect(function()
		if ESPEnabled then
			CreateESPForPlayer(player)
		end
	end)
end)

Players.PlayerRemoving:Connect(function(player)
	if ESPObjects[player] then
		local esp = ESPObjects[player]
		if esp.Box then esp.Box:Remove() end
		if esp.Name then esp.Name:Remove() end
		if esp.Health then esp.Health:Remove() end
		if esp.Distance then esp.Distance:Remove() end
		for _, line in ipairs(esp.Skeleton) do
			line:Remove()
		end
		ESPObjects[player] = nil
	end
end)
