jarvisModel=CreateFrame("frame")
jarvisModel.Round = 0
jarvisModel:SetScript('OnEvent',function(_, event, ...) return jarvisModel[event](jarvisModel, event, ...) end)
jarvisModel.AddReg = function(self,event,func)
	if not jarvisModel[event] then
		jarvisModel:RegisterEvent(event)
		jarvisModel[event]=func
	else
		hooksecurefunc(jarvisModel,event,func)
	end
end

local statusFrame = CreateFrame("Frame", "petStatusFrame")

----------------------------------------
-- 状态框初始化函数
----------------------------------------
statusFrame.Initialize = function(self)
	-- 设置状态框
	statusFrame:SetWidth(200)
	statusFrame:SetHeight(30)
	statusFrame:SetPoint("TOPLEFT", 0, 0)
	statusFrame:SetBackdrop({
		bgFile = [["Interface\\AddOns\\Jarvis\\black-background.tga"]],
	    --edgeFile = [["Interface\\AddOns\\Jarvis\\black-background.tga"]],
	    tile = true, tileSize = 0, edgeSize = 0,
	    insets = { left = 0, right = 0, top = 0, bottom = 0 }
	})
	statusFrame:SetBackdropColor(0, 0, 0, 1.0)
	--statusFrame:SetBackdropBorderColor(0.8, 0.8, 0.8, 1.0);
	statusFrame:SetMovable(true)
	statusFrame:EnableMouse(true)
	statusFrame:RegisterForDrag("LeftButton")
	statusFrame:SetScript("OnDragStart", function() statusFrame:StartMoving() end)
	statusFrame:SetScript("OnDragStop", function() statusFrame:StopMovingOrSizing() end)

	-- 创建状态文字
	local text1 = statusFrame:CreateFontString(nil, "OVERLAY", "GameFontHighlightLarge")
	text1:SetPoint("TOPLEFT", 2, -6)
	statusFrame.text1 = text1

	statusFrame.Initialize = nil
end

----------------------------------------
-- 更新状态框 
----------------------------------------
statusFrame.Update = function(self, code)
	self.text1:SetText(format("%s", code))
	self:SetWidth(200)

	if not self:IsShown() then self:Show() end
end


----------------------------------------
statusFrame.UpdateVisibility = function(self)
		if self.Initialize then
			self:Initialize()
			self:Update("SYSTEM ONLINE ...")
		end
end

statusFrame:RegisterEvent("ZONE_CHANGED")
statusFrame:RegisterEvent("ZONE_CHANGED_INDOORS")
statusFrame:RegisterEvent("ZONE_CHANGED_NEW_AREA")
statusFrame:RegisterEvent("PLAYER_ENTERING_WORLD")
--statusFrame:RegisterEvent("BAG_UPDATE")

statusFrame:SetScript("OnEvent", function(self,event,...)
	statusFrame:UpdateVisibility()
end)

----------------------------------------
-- 经验值改变时计算并更新状态框
----------------------------------------
jarvisModel:AddReg("ITEM_PUSH",function(...)
statusFrame:UpdateVisibility()
	if not statusFrame:IsShown() then return end
	local code = "ITEM_PUSH"
	statusFrame:Update(code)

end)

----------------------------------------
