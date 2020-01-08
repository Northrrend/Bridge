local frm = CreateFrame("Frame")    
frm:Hide()                         
frm:RegisterEvent("BAG_UPDATE")  
local function EventHandler(self, event, ...)

    if event == "BAG_UPDATE" then
        local name = ...
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        --print("")
        print("mpo")
    end
end

frm:SetScript("OnEvent", EventHandler)
