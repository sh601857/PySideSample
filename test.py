import win32com.client


ihAPP = win32com.client.Dispatch('iHeatServer.Application')
re = ihAPP.init()
ihAPP.visible = 1;
ihAPP.openFile('D:\\Workspace\\matlab\\demo-revamping.ihf')
ihAPP.runCMD('Revamp','some params in JSON')
#re = ihAPP.quit()