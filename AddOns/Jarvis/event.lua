local frm = CreateFrame("Frame")    
frm:Hide()                         
frm:RegisterEvent("BAG_UPDATE")  
local function EventHandler(self, event, ...)

    if event == "BAG_UPDATE" then
        local name = ...
        for i= 1, 7 do
            SELECTED_CHAT_FRAME:AddMessage("\n")
        end
        SELECTED_CHAT_FRAME:AddMessage("mpo")
    end
end

frm:SetScript("OnEvent", EventHandler)
