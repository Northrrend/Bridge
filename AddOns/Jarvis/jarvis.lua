local _, ADDONSELF = ...
local L = ADDONSELF.L
local RegEvent = ADDONSELF.regevent
local BattleZoneHelper = ADDONSELF.BattleZoneHelper
local RegisterKeyChangedCallback = ADDONSELF.RegisterKeyChangedCallback 

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

--GameWidth = GetScreenWidth()
--GameHeight = GetScreenHeight()

--print(GameWidth)
--print(GameHeight)
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
----------------------------------------

RegEvent("BATTLEFIELDS_SHOW", function()
    C_ChatInfo.SendAddonMessage("BATTLEINFO", "ELAPSE_WANTED", "GUILD")
end)

RegEvent("CHAT_MSG_ADDON", function(prefix, text, channel, sender)
    if prefix ~= "BATTLEINFO" then
        return
    end

    sender = strsplit("-", sender)

    if sender == UnitName("player") then
        return
    end

    --print(sender)
    --print(text)
    local cmd, arg1, arg2, arg3 = strsplit(" ", text)

    if cmd == "ELAPSE_WANTED" then
        local battleGroundID, instanceID = BattleZoneHelper:GetCurrentBG()

        if battleGroundID and instanceID then
            local key = battleGroundID .. "-" .. instanceID
            local elapse = -1
            if not GetBattlefieldWinner() then
                elapse = floor(GetBattlefieldInstanceRunTime() / 1000)
            end
            C_ChatInfo.SendAddonMessage("BATTLEINFO", "ELAPSE_SYNC " .. key .. " " .. elapse .. " " .. GetServerTime(), "GUILD")
        end
    elseif cmd == "ELAPSE_SYNC" then

        local key = arg1
        local elapse = tonumber(arg2)
        local time = tonumber(arg3)

        if (not key) or (not elapse) or (not time) then
            return
        end
      
        if elapseCache[key] then
            if elapseCache[key].time > time then
                return
            end
        end

        if elapse < 0 then
            elapseCache[key] = nil
        else
            elapseCache[key] = {
                sender = sender,
                elapse = elapse,
                time = time,
            }
        end

        --UpdateInstanceButtonText()
    end


end)
local battleList = {}
local function UpdateBattleListCache()
    local mapName = GetBattlegroundInfo()

    if not mapName then
        return
    end

    if not battleList[mapName] then
        battleList[mapName] = {}
    end
    table.wipe(battleList[mapName])
    
    local n = GetNumBattlefields()
    for i = 1, n  do
        local instanceID = GetBattlefieldInstanceInfo(i)
        battleList[mapName][tonumber(instanceID)] = { i = i , n = n }
    end

    --UpdateInstanceButtonText()
end

local DROP_MENU_LOC_ENTER = 2
local DROP_MENU_LOC_LEAVE = 1

local function SearchDropMenuLoc(showid, offset)
    local queued = 0

    for i = 1, MAX_BATTLEFIELD_QUEUES do
        local status, mapName, instanceID = GetBattlefieldStatus(i)
        local current = i == showid 

        if current then
            return i * 4 - offset - queued;
        end

        if status == "queued" then
            queued = queued + 1
        end
    end    
end

RegEvent("ADDON_LOADED", function()
    C_ChatInfo.RegisterAddonMessagePrefix("BATTLEINFO")

    hooksecurefunc("JoinBattlefield", UpdateBattleListCache)
    hooksecurefunc("BattlefieldFrame_Update", UpdateBattleListCache)

    local joinqueuebtn
    do
        local t = CreateFrame("Button", nil, nil, "UIPanelButtonTemplate, SecureActionButtonTemplate")
        t:SetFrameStrata("TOOLTIP")
        t:SetText(ENTER_BATTLE)
        t:SetAttribute("type", "macro") -- left click causes macro
        t:Hide()

        t.updateMacro = function()
            local loc = SearchDropMenuLoc(t.showid, DROP_MENU_LOC_ENTER)
            if loc then
                t:SetAttribute("macrotext", "/click MiniMapBattlefieldFrame RightButton" .. "\r\n" .. "/click [nocombat]DropDownList1Button" .. (loc)) -- text for macro on left click
            end
        end        

        t:SetScript("OnUpdate", function()
            t.updateMacro()

            for i = 1, MAX_BATTLEFIELD_QUEUES do
                local time = GetBattlefieldPortExpiration(i)
                if time > 0 then
                    t:SetText(ENTER_BATTLE .. "(" .. GREEN_FONT_COLOR:WrapTextInColorCode(time) .. ")")
                    return
                end
            end
            t:SetText(ENTER_BATTLE .. "(" .. GREEN_FONT_COLOR:WrapTextInColorCode("?") .. ")")
        end)

        joinqueuebtn = t
    end

    local leavequeuebtn
    do
        local t = CreateFrame("Button", nil, nil, "UIPanelButtonTemplate, SecureActionButtonTemplate")
        t:SetFrameStrata("TOOLTIP")
        t:SetText(L["CTRL+Hide=Leave"])
        t:SetAttribute("type", "macro") -- left click causes macro
        t:Hide()

        t.updateMacro = function()
            local loc = SearchDropMenuLoc(t.showid, DROP_MENU_LOC_LEAVE)
            if loc then
                t:SetAttribute("macrotext", "/click MiniMapBattlefieldFrame RightButton" .. "\r\n" .. "/click [nocombat]DropDownList1Button" .. (loc)) -- text for macro on left click
            end
        end

        leavequeuebtn = t
    end

    StaticPopupDialogs["CONFIRM_BATTLEFIELD_ENTRY"].OnHide = function()
        joinqueuebtn:Hide()
        joinqueuebtn:ClearAllPoints()
        leavequeuebtn:Hide()
        leavequeuebtn:ClearAllPoints()
    end

	local replaceEnter = true
	local replaceHide = true
    local flashIcon = true

    RegisterKeyChangedCallback("replace_enter_battle", function(v)
        replaceEnter = v
    end)
    RegisterKeyChangedCallback("replace_hide_battle", function(v)
        replaceHide = v
        if v then
            StaticPopupDialogs["CONFIRM_BATTLEFIELD_ENTRY"].button2 = L["CTRL+Hide=Leave"]
        else
            StaticPopupDialogs["CONFIRM_BATTLEFIELD_ENTRY"].button2 = HIDE
        end
    end)
    RegisterKeyChangedCallback("flash_icon", function(v)
        flashIcon = v
    end)


    -- hooksecurefunc(StaticPopupDialogs["CONFIRM_BATTLEFIELD_ENTRY"], "OnShow", function(self)
    StaticPopupDialogs["CONFIRM_BATTLEFIELD_ENTRY"].OnShow = function(self, data)
        if flashIcon then
            FlashClientIcon()
        end

        local tx = self.text:GetText()
        if InCombatLockdown() then
            ADDONSELF.Print(L["Button may not work properly during combat"])
            return
        end

        if replaceEnter then
            joinqueuebtn.showid = data
            joinqueuebtn:SetAllPoints(self.button1)

            joinqueuebtn:Show()
        end

        if replaceHide then
            leavequeuebtn.showid = data
            leavequeuebtn:SetAllPoints(self.button2)

            if not self.button2.batteinfohooked then
                self.button2:SetScript("OnUpdate", function()
                    leavequeuebtn.updateMacro()

                    if IsControlKeyDown() then
                        leavequeuebtn:Show()
                    else
                        leavequeuebtn:Hide()
                    end
                end)
                self.button2.batteinfohooked = true
            end
        end

        if string.find(tx, L["List Position"], 1, 1) or string.find(tx, L["New"], 1 , 1) then			
            return
        end    

        for mapName, instanceIDs in pairs(battleList) do
            local _, _ ,toJ = string.find(tx, ".+" .. mapName .. " (%d+).+")
            toJ = tonumber(toJ)
            if toJ then
                if instanceIDs[toJ] then
					
                    -- first half 0 - rate -> red (0)
                    -- second half rate - 100% -> red(0) -> yellow (1)
                    local rate = 0.45
                    local pos = instanceIDs[toJ].i
                    local total = instanceIDs[toJ].n
					local i = total - pos
					if i > 4 then 
						statusFrame:Update("OLD")
					else
						statusFrame:Update("BTO")
					end
                    local pos0 = math.max(pos - total * rate - 1, 0)

                    local color = CreateColor(1.0, math.min(pos0 / (total * (1 - rate)), 1) , 0)
                    local text = color:WrapTextInColorCode(L["List Position"] .. " " .. string.format("%d/%d", pos, total))

                    local elp = GetElapseFromCache(mapName, toJ)
                    if elp then
                        text = RED_FONT_COLOR:WrapTextInColorCode(SecondsToTime(elp))
                    end

                    self.text:SetText(string.gsub(tx ,toJ , YELLOW_FONT_COLOR:WrapTextInColorCode(toJ) .. "(" .. text .. ")"))
			else
				statusFrame:Update("BTO")
                local text = GREEN_FONT_COLOR:WrapTextInColorCode(L["New"])
                self.text:SetText(string.gsub(tx ,toJ , YELLOW_FONT_COLOR:WrapTextInColorCode(toJ) .. "(" .. text .. ")"))

                end
                break
            end
        end
        
    end

end)
-------------------------------------------------------------------------------

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
	local code = "TKB"
	statusFrame:Update(code)

end)

----------------------------------------
