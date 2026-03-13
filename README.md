-- EDSON SCRIPT V2 (3 ABAS) - COMPLETO COM AIMBOT E ESP

local TweenService = game:GetService("TweenService")
local UIS = game:GetService("UserInputService")
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local Camera = workspace.CurrentCamera
local LocalPlayer = Players.LocalPlayer

local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Parent = game.CoreGui
ScreenGui.ResetOnSpawn = false

-- VARIÁVEIS GLOBAIS
local AimEnabled = false
local ESPEnabled = false
local TeamCheck = false
local SelectedPart = "Head"
local Smoothness = 0.3
local FOVSize = 200
local FOVVisible = false
local MainColor = Color3.fromRGB(200, 0, 0)

-- MAIN
local Main = Instance.new("Frame")
Main.Parent = ScreenGui
Main.Size = UDim2.new(0,450,0,270)
Main.Position = UDim2.new(0.5,-225,0.5,-135)
Main.BackgroundColor3 = Color3.fromRGB(15,15,15)
Main.Active = true
Main.Draggable = true

-- TOP BAR
local Top = Instance.new("Frame")
Top.Parent = Main
Top.Size = UDim2.new(1,0,0,35)
Top.BackgroundColor3 = MainColor

local Title = Instance.new("TextLabel")
Title.Parent = Top
Title.Size = UDim2.new(1,0,1,0)
Title.Text = "EDSON SCRIPT"
Title.BackgroundTransparency = 1
Title.TextColor3 = Color3.new(1,1,1)
Title.Font = Enum.Font.GothamBold
Title.TextSize = 18

-- SIDE MENU
local Side = Instance.new("Frame")
Side.Parent = Main
Side.Size = UDim2.new(0,90,1,-35)
Side.Position = UDim2.new(0,0,0,35)
Side.BackgroundColor3 = Color3.fromRGB(20,20,20)

-- CONTENT AREA
local Content = Instance.new("Frame")
Content.Parent = Main
Content.Position = UDim2.new(0,90,0,35)
Content.Size = UDim2.new(1,-90,1,-35)
Content.BackgroundTransparency = 1

-- ABAS
local AimTab = Instance.new("Frame",Content)
AimTab.Size = UDim2.new(1,0,1,0)
AimTab.BackgroundTransparency = 1

local VisualTab = Instance.new("Frame",Content)
VisualTab.Size = UDim2.new(1,0,1,0)
VisualTab.BackgroundTransparency = 1
VisualTab.Visible = false

local SettingsTab = Instance.new("Frame",Content)
SettingsTab.Size = UDim2.new(1,0,1,0)
SettingsTab.BackgroundTransparency = 1
SettingsTab.Visible = false

-- BOTÕES DAS ABAS
local function createTabButton(name,pos)
	local b = Instance.new("TextButton")
	b.Parent = Side
	b.Size = UDim2.new(1,0,0,60)
	b.Position = UDim2.new(0,0,0,pos)
	b.Text = name
	b.Font = Enum.Font.GothamBold
	b.TextColor3 = Color3.new(1,1,1)
	b.BackgroundColor3 = Color3.fromRGB(40,40,40)
	return b
end

local AimButton = createTabButton("AIM",0)
local VisualButton = createTabButton("VISUAL",70)
local SettingsButton = createTabButton("SET",140)

-- FUNÇÃO TROCAR ABA
local function switch(tab)
	AimTab.Visible = false
	VisualTab.Visible = false
	SettingsTab.Visible = false
	tab.Visible = true
end

AimButton.MouseButton1Click:Connect(function()
	switch(AimTab)
end)

VisualButton.MouseButton1Click:Connect(function()
	switch(VisualTab)
end)

SettingsButton.MouseButton1Click:Connect(function()
	switch(SettingsTab)
end)

-- ==================== ABA AIM ====================
-- TÍTULO
local AimTitle = Instance.new("TextLabel",AimTab)
AimTitle.Size = UDim2.new(1,0,0,30)
AimTitle.Position = UDim2.new(0,10,0,5)
AimTitle.Text = "AIMBOT CONFIG"
AimTitle.TextColor3 = Color3.new(1,1,1)
AimTitle.BackgroundTransparency = 1
AimTitle.Font = Enum.Font.GothamBold
AimTitle.TextXAlignment = Enum.TextXAlignment.Left

-- AIMBOT TOGGLE
local AimToggle = Instance.new("TextButton",AimTab)
AimToggle.Size = UDim2.new(0,160,0,30)
AimToggle.Position = UDim2.new(0,10,0,40)
AimToggle.Text = "AIMBOT: OFF"
AimToggle.BackgroundColor3 = Color3.fromRGB(60,60,60)
AimToggle.TextColor3 = Color3.new(1,1,1)

AimToggle.MouseButton1Click:Connect(function()
	AimEnabled = not AimEnabled
	AimToggle.Text = AimEnabled and "AIMBOT: ON" or "AIMBOT: OFF"
	AimToggle.BackgroundColor3 = AimEnabled and Color3.fromRGB(0,200,0) or Color3.fromRGB(60,60,60)
end)

-- TEAM CHECK
local TeamCheckBtn = Instance.new("TextButton",AimTab)
TeamCheckBtn.Size = UDim2.new(0,160,0,30)
TeamCheckBtn.Position = UDim2.new(0,10,0,80)
TeamCheckBtn.Text = "TEAM CHECK: OFF"
TeamCheckBtn.BackgroundColor3 = Color3.fromRGB(60,60,60)
TeamCheckBtn.TextColor3 = Color3.new(1,1,1)

TeamCheckBtn.MouseButton1Click:Connect(function()
	TeamCheck = not TeamCheck
	TeamCheckBtn.Text = TeamCheck and "TEAM CHECK: ON" or "TEAM CHECK: OFF"
	TeamCheckBtn.BackgroundColor3 = TeamCheck and Color3.fromRGB(0,200,0) or Color3.fromRGB(60,60,60)
end)

-- TARGET PART
local PartLabel = Instance.new("TextLabel",AimTab)
PartLabel.Size = UDim2.new(0,80,0,30)
PartLabel.Position = UDim2.new(0,10,0,120)
PartLabel.Text = "PART:"
PartLabel.TextColor3 = Color3.new(1,1,1)
PartLabel.BackgroundTransparency = 1

local PartDropdown = Instance.new("TextButton",AimTab)
PartDropdown.Size = UDim2.new(0,100,0,30)
PartDropdown.Position = UDim2.new(0,80,0,120)
PartDropdown.Text = SelectedPart
PartDropdown.BackgroundColor3 = Color3.fromRGB(60,60,60)
PartDropdown.TextColor3 = Color3.new(1,1,1)

local parts = {"Head", "Torso", "HumanoidRootPart"}
local currentPart = 1

PartDropdown.MouseButton1Click:Connect(function()
	currentPart = currentPart % #parts + 1
	SelectedPart = parts[currentPart]
	PartDropdown.Text = SelectedPart
end)

-- FOV TOGGLE
local FovToggle = Instance.new("TextButton",AimTab)
FovToggle.Size = UDim2.new(0,160,0,30)
FovToggle.Position = UDim2.new(0,10,0,160)
FovToggle.Text = "EXIBIR FOV: OFF"
FovToggle.BackgroundColor3 = Color3.fromRGB(60,60,60)
FovToggle.TextColor3 = Color3.new(1,1,1)

-- CIRCULO FOV
local FOV = Instance.new("Frame",ScreenGui)
FOV.Size = UDim2.new(0,200,0,200)
FOV.Position = UDim2.new(0.5,-100,0.5,-100)
FOV.BackgroundTransparency = 1
FOV.BorderColor3 = MainColor
FOV.BorderSizePixel = 2
FOV.Visible = false
FOV.ZIndex = 10

local fovcorner = Instance.new("UICorner",FOV)
fovcorner.CornerRadius = UDim.new(1,0)

FovToggle.MouseButton1Click:Connect(function()
	FOVVisible = not FOVVisible
	FOV.Visible = FOVVisible
	FovToggle.Text = FOVVisible and "EXIBIR FOV: ON" or "EXIBIR FOV: OFF"
	FovToggle.BackgroundColor3 = FOVVisible and Color3.fromRGB(0,200,0) or Color3.fromRGB(60,60,60)
end)

-- SLIDER FOV SIZE
local SliderLabel = Instance.new("TextLabel",AimTab)
SliderLabel.Size = UDim2.new(0,100,0,20)
SliderLabel.Position = UDim2.new(0,10,0,200)
SliderLabel.Text = "FOV SIZE: 200"
SliderLabel.TextColor3 = Color3.new(1,1,1)
SliderLabel.BackgroundTransparency = 1
SliderLabel.TextXAlignment = Enum.TextXAlignment.Left

local Slider = Instance.new("Frame",AimTab)
Slider.Size = UDim2.new(0,200,0,6)
Slider.Position = UDim2.new(0,10,0,225)
Slider.BackgroundColor3 = Color3.fromRGB(60,60,60)

local Fill = Instance.new("Frame",Slider)
Fill.Size = UDim2.new(0.5,0,1,0)
Fill.BackgroundColor3 = MainColor

local Knob = Instance.new("Frame",Slider)
Knob.Size = UDim2.new(0,14,0,14)
Knob.Position = UDim2.new(0.5,-7,-0.5,0)
Knob.BackgroundColor3 = MainColor

local corner = Instance.new("UICorner",Knob)
corner.CornerRadius = UDim.new(1,0)

-- SLIDER FUNCIONANDO
local dragging = false

Knob.InputBegan:Connect(function(input)
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
			(input.Position.X - Slider.AbsolutePosition.X) /
			Slider.AbsoluteSize.X,
			0,1
		)

		Fill.Size = UDim2.new(pos,0,1,0)
		Knob.Position = UDim2.new(pos,-7,-0.5,0)

		FOVSize = 100 + (pos * 300)
		SliderLabel.Text = "FOV SIZE: " .. math.floor(FOVSize)
		
		FOV.Size = UDim2.new(0,FOVSize,0,FOVSize)
		FOV.Position = UDim2.new(0.5,-FOVSize/2,0.5,-FOVSize/2)
	end
end)

-- ==================== ABA VISUAL (ESP) ====================
local VisualTitle = Instance.new("TextLabel",VisualTab)
VisualTitle.Size = UDim2.new(1,0,0,30)
VisualTitle.Position = UDim2.new(0,10,0,5)
VisualTitle.Text = "ESP CONFIG"
VisualTitle.TextColor3 = Color3.new(1,1,1)
VisualTitle.BackgroundTransparency = 1
VisualTitle.Font = Enum.Font.GothamBold
VisualTitle.TextXAlignment = Enum.TextXAlignment.Left

-- ESP TOGGLE
local ESPToggle = Instance.new("TextButton",VisualTab)
ESPToggle.Size = UDim2.new(0,160,0,30)
ESPToggle.Position = UDim2.new(0,10,0,40)
ESPToggle.Text = "ESP: OFF"
ESPToggle.BackgroundColor3 = Color3.fromRGB(60,60,60)
ESPToggle.TextColor3 = Color3.new(1,1,1)

ESPToggle.MouseButton1Click:Connect(function()
	ESPEnabled = not ESPEnabled
	ESPToggle.Text = ESPEnabled and "ESP: ON" or "ESP: OFF"
	ESPToggle.BackgroundColor3 = ESPEnabled and Color3.fromRGB(0,200,0) or Color3.fromRGB(60,60,60)
	
	if ESPEnabled then
		CreateESPForAll()
	else
		ClearAllESP()
	end
end)

-- BOX TOGGLE
local BoxToggle = Instance.new("TextButton",VisualTab)
BoxToggle.Size = UDim2.new(0,160,0,30)
BoxToggle.Position = UDim2.new(0,10,0,80)
BoxToggle.Text = "BOX: ON"
BoxToggle.BackgroundColor3 = Color3.fromRGB(0,200,0)
BoxToggle.TextColor3 = Color3.new(1,1,1)

local BoxEnabled = true
BoxToggle.MouseButton1Click:Connect(function()
	BoxEnabled = not BoxEnabled
	BoxToggle.Text = BoxEnabled and "BOX: ON" or "BOX: OFF"
	BoxToggle.BackgroundColor3 = BoxEnabled and Color3.fromRGB(0,200,0) or Color3.fromRGB(60,60,60)
end)

-- NAME TOGGLE
local NameToggle = Instance.new("TextButton",VisualTab)
NameToggle.Size = UDim2.new(0,160,0,30)
NameToggle.Position = UDim2.new(0,10,0,120)
NameToggle.Text = "NAME: ON"
NameToggle.BackgroundColor3 = Color3.fromRGB(0,200,0)
NameToggle.TextColor3 = Color3.new(1,1,1)

local NameEnabled = true
NameToggle.MouseButton1Click:Connect(function()
	NameEnabled = not NameEnabled
	NameToggle.Text = NameEnabled and "NAME: ON" or "NAME: OFF"
	NameToggle.BackgroundColor3 = NameEnabled and Color3.fromRGB(0,200,0) or Color3.fromRGB(60,60,60)
end)

-- HEALTH TOGGLE
local HealthToggle = Instance.new("TextButton",VisualTab)
HealthToggle.Size = UDim2.new(0,160,0,30)
HealthToggle.Position = UDim2.new(0,10,0,160)
HealthToggle.Text = "HEALTH: ON"
HealthToggle.BackgroundColor3 = Color3.fromRGB(0,200,0)
HealthToggle.TextColor3 = Color3.new(1,1,1)

local HealthEnabled = true
HealthToggle.MouseButton1Click:Connect(function()
	HealthEnabled = not HealthEnabled
	HealthToggle.Text = HealthEnabled and "HEALTH: ON" or "HEALTH: OFF"
	HealthToggle.BackgroundColor3 = HealthEnabled and Color3.fromRGB(0,200,0) or Color3.fromRGB(60,60,60)
end)

-- DISTANCE TOGGLE
local DistToggle = Instance.new("TextButton",VisualTab)
DistToggle.Size = UDim2.new(0,160,0,30)
DistToggle.Position = UDim2.new(0,10,0,200)
DistToggle.Text = "DISTANCE: ON"
DistToggle.BackgroundColor3 = Color3.fromRGB(0,200,0)
DistToggle.TextColor3 = Color3.new(1,1,1)

local DistEnabled = true
DistToggle.MouseButton1Click:Connect(function()
	DistEnabled = not DistEnabled
	DistToggle.Text = DistEnabled and "DISTANCE: ON" or "DISTANCE: OFF"
	DistToggle.BackgroundColor3 = DistEnabled and Color3.fromRGB(0,200,0) or Color3.fromRGB(60,60,60)
end)

-- ==================== ABA SETTINGS ====================
local SettingsTitle = Instance.new("TextLabel",SettingsTab)
SettingsTitle.Size = UDim2.new(1,0,0,30)
SettingsTitle.Position = UDim2.new(0,10,0,5)
SettingsTitle.Text = "CONFIGURAÇÕES"
SettingsTitle.TextColor3 = Color3.new(1,1,1)
SettingsTitle.BackgroundTransparency = 1
SettingsTitle.Font = Enum.Font.GothamBold
SettingsTitle.TextXAlignment = Enum.TextXAlignment.Left

-- COR DO PAINEL
local ColorLabel = Instance.new("TextLabel",SettingsTab)
ColorLabel.Size = UDim2.new(0,80,0,30)
ColorLabel.Position = UDim2.new(0,10,0,50)
ColorLabel.Text = "COR:"
ColorLabel.TextColor3 = Color3.new(1,1,1)
ColorLabel.BackgroundTransparency = 1

local ColorDisplay = Instance.new("Frame",SettingsTab)
ColorDisplay.Size = UDim2.new(0,30,0,30)
ColorDisplay.Position = UDim2.new(0,80,0,50)
ColorDisplay.BackgroundColor3 = MainColor

local ColorPickerBtn = Instance.new("TextButton",SettingsTab)
ColorPickerBtn.Size = UDim2.new(0,100,0,30)
ColorPickerBtn.Position = UDim2.new(0,120,0,50)
ColorPickerBtn.Text = "MUDAR COR"
ColorPickerBtn.BackgroundColor3 = Color3.fromRGB(60,60,60)
ColorPickerBtn.TextColor3 = Color3.new(1,1,1)

-- CORES DISPONÍVEIS
local colors = {
	Color3.fromRGB(200,0,0),    -- Vermelho
	Color3.fromRGB(0,200,0),    -- Verde
	Color3.fromRGB(0,0,200),    -- Azul
	Color3.fromRGB(200,200,0),  -- Amarelo
	Color3.fromRGB(200,0,200),  -- Roxo
	Color3.fromRGB(0,200,200),  -- Ciano
	Color3.fromRGB(255,255,255) -- Branco
}
local colorIndex = 1

ColorPickerBtn.MouseButton1Click:Connect(function()
	colorIndex = colorIndex % #colors + 1
	MainColor = colors[colorIndex]
	
	-- Atualiza cores
	Top.BackgroundColor3 = MainColor
	Fill.BackgroundColor3 = MainColor
	Knob.BackgroundColor3 = MainColor
	FOV.BorderColor3 = MainColor
	ColorDisplay.BackgroundColor3 = MainColor
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

local function CreateESPForPlayer(player)
	if ESPObjects[player] then return end
	
	local esp = {
		Box = Drawing.new("Square"),
		Name = Drawing.new("Text"),
		Health = Drawing.new("Text"),
		Distance = Drawing.new("Text")
	}
	
	-- Configurações padrão
	esp.Box.Visible = false
	esp.Box.Thickness = 2
	esp.Box.Color = MainColor
	
	esp.Name.Visible = false
	esp.Name.Size = 16
	esp.Name.Center = true
	esp.Name.Outline = true
	esp.Name.Color = Color3.new(1,1,1)
	
	esp.Health.Visible = false
	esp.Health.Size = 14
	esp.Health.Center = true
	esp.Health.Outline = true
	esp.Health.Color = Color3.new(0,1,0)
	
	esp.Distance.Visible = false
	esp.Distance.Size = 12
	esp.Distance.Center = true
	esp.Distance.Outline = true
	esp.Distance.Color = Color3.new(1,1,1)
	
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
	end
	ESPObjects = {}
end

-- Atualizar ESP quando novos jogadores entrarem
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
		ESPObjects[player] = nil
	end
end)

-- LOOP DO ESP
RunService.RenderStepped:Connect(function()
	if not ESPEnabled then return end
	
	for player, esp in pairs(ESPObjects) do
		if player and player.Character and player.Character:FindFirstChild("Humanoid") then
			local char = player.Character
			local hum = char.Humanoid
			local root = char:FindFirstChild("HumanoidRootPart") or char:FindFirstChild("Head")
			
			if root and hum.Health > 0 then
				local pos, onScreen = Camera:WorldToViewportPoint(root.Position)
				local headPos, _ = Camera:WorldToViewportPoint((char:FindFirstChild("Head") or root).Position)
				
				if onScreen then
					local scale = 1 / (pos.Z * 0.1)
					local boxSize = Vector2.new(2000 / pos.Z, 2500 / pos.Z)
					local boxPos = Vector2.new(pos.X - boxSize.X/2, headPos.Y - boxSize.Y)
					
					-- BOX
					esp.Box.Visible = BoxEnabled
					esp.Box.Size = boxSize
					esp.Box.Position = boxPos
					esp.Box.Color = MainColor
					
					-- NAME
					esp.Name.Visible = NameEnabled
					esp.Name.Text = player.Name
					esp.Name.Position = Vector2.new(pos.X, boxPos.Y - 20)
					
					-- HEALTH
					if HealthEnabled then
						local healthPercent = hum.Health / hum.MaxHealth
						esp.Health.Visible = true
						esp.Health.Text = string.format("%.0f/%.0f", hum.Health, hum.MaxHealth)
						esp.Health.Position = Vector2.new(pos.X, boxPos.Y + boxSize.Y + 5)
						esp.Health.Color = Color3.new(1 - healthPercent, healthPercent, 0)
					else
						esp.Health.Visible = false
					end
					
					-- DISTANCE
					if DistEnabled then
						local distance = (root.Position - Camera.CFrame.Position).Magnitude
						esp.Distance.Visible = true
						esp.Distance.Text = math.floor(distance) .. "m"
						esp.Distance.Position = Vector2.new(pos.X, boxPos.Y + boxSize.Y + 25)
					else
						esp.Distance.Visible = false
					end
				else
					esp.Box.Visible = false
					esp.Name.Visible = false
					esp.Health.Visible = false
					esp.Distance.Visible = false
				end
			else
				esp.Box.Visible = false
				esp.Name.Visible = false
				esp.Health.Visible = false
				esp.Distance.Visible = false
			end
		end
	end
end)

-- Criar ESP para jogadores existentes
CreateESPForAll()
