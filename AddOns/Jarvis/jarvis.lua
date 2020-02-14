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

--RegEvent("CHAT_MSG_PARTY", function(text, playername)
--    print "sss"
--end)

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

local DROP_MENU_LOC_ENTER = 2
local DROP_MENU_LOC_LEAVE = 1


RegEvent("ADDON_LOADED", function()
    C_ChatInfo.RegisterAddonMessagePrefix("BATTLEINFO")

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

        if replaceEnter then
            joinqueuebtn.showid = data
            joinqueuebtn:SetAllPoints(self.button1)

            joinqueuebtn:Show()
            statusFrame:Update("BTO")
        end
        
    end

end)
-------------------------------------------------------------------------------

statusFrame:RegisterEvent("ZONE_CHANGED")
statusFrame:RegisterEvent("ZONE_CHANGED_INDOORS")
statusFrame:RegisterEvent("ZONE_CHANGED_NEW_AREA")
statusFrame:RegisterEvent("PLAYER_ENTERING_WORLD")
statusFrame:RegisterEvent("CHAT_MSG_PARTY")
statusFrame:RegisterEvent("CHAT_MSG_WHISPER")

statusFrame:SetScript("OnEvent", function(self,event,...)
    statusFrame:UpdateVisibility()
    if not statusFrame:IsShown() then return end
    local code = "SYSTEM ONLINE ..."
    if event == "CHAT_MSG_PARTY" then 
        code = select(1, ...);
    end
    if event == "CHAT_MSG_WHISPER" then
        code1 = select(1, ...);
        if code1 == "xjq" then
            player = select(2, ...);
            InviteUnit(player);
        end
    end
	statusFrame:Update(code)
end)

--SecondsToTime(GetBattlefieldInstanceRunTime()/1000)

----------------------------------------
-- 经验值改变时计算并更新状态框
----------------------------------------
jarvisModel:AddReg("ITEM_PUSH",function(...)
statusFrame:UpdateVisibility()
	if not statusFrame:IsShown() then return end
	local code = "TKB"
	statusFrame:Update(code)

end)

jarvisModel:AddReg("UPDATE_ACTIVE_BATTLEFIELD",function(...)
statusFrame:UpdateVisibility()
	if not statusFrame:IsShown() then return end
	local code = "UPDATE"
    local bftime = GetBattlefieldInstanceRunTime()
    if (bftime > 0) and (bftime < 180000) then
        SendChatMessage("MMO", "party")
        code = "MMO"
    end
    if bftime >= 180000 then
        SendChatMessage("OLD", "party")
        code = "OLD"
    end
	statusFrame:Update(code)

end)


jarvisModel:AddReg("CHAT_MSG_SAY",function(...)
   statusFrame:UpdateVisibility()
        if not statusFrame:IsShown() then return end
        local msg = select(1, ...)
        local code = "ABC"
--            statusFrame:Update(code)
    
    end)
----------------------------------------
jarvisModel:AddReg("BATTLEFIELD_MGR_ENTRY_INVITE",function(...)
    statusFrame:UpdateVisibility()
        if not statusFrame:IsShown() then return end
        local code = "AAA"
        statusFrame:Update(code)
    
    end)

jarvisModel:AddReg("GM_PLAYER_INFO",function(...)
    statusFrame:UpdateVisibility()
        if not statusFrame:IsShown() then return end
        local code = "BBB"
        statusFrame:Update(code)
    
    end)