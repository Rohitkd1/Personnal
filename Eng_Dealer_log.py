from ATS.Plugins.IVIHKMC6thPlugin.IVIHKMC6thProtocol import *
from ccIC27_Library.HardKeys import *
from ccIC27_Library.ShellCommands import *
from ccIC27_Library.BasicFunctions import *
import os
from pathlib import Path
import json
import threading
import tempfile
from ATS.Plugins.ImageAnalyser.Enums import MatchingMethod
import re
from BasicRequirements import *
from ccIC27_Library import config 
import csv
from datetime import datetime, date


config.variant = System.GetScenarioParameter("Variant") 
config.region = System.GetScenarioParameter("Region")
config.swVer = System.GetScenarioParameter("Software Version")



def EngModeEntry():

    startTestCase()
    System.Sleep(1000)

    MKBD_SETUP_SHORT()
    System.Sleep(1500)

    for i in range(12):

        DEV1.lcdTouch(3762, 63, None)
        System.Sleep(200)
        DEV1.lcdTouch(3909, 65, None)
        System.Sleep(200)

    System.Sleep(3000)
    PasswordEntry=[(1721,560),(1929,657),(1521,652),(1207,360),(2129,366),(2021,374),(1216,290),(1221,370)] 

    for x, y in PasswordEntry:
        DEV1.lcdTouch(x+1920,y, None)
        System.Sleep(200)

    #selecting OK
    DEV1.lcdTouch(2015+1920, 236, None)
    System.Sleep(1000)    
    
    print("ENGINEERING MODE ENTERED")


def Enter_System():        
                
    DEV1.lcdTouch(234+1920, 236, None)    #Entering System
    System.Sleep(1000)


    testcaseID = "SystemEntry"
    capturedImagePath = create_image_path(testcaseID)
    System.Sleep(1000)

    Image_Capture(capturedImagePath)
    System.Sleep(3000)

    print("STARTING EXTRACTION")
        
def checkswdetails():
        variant=System.GetScenarioParameter("Variant")
        region=System.GetScenarioParameter("Region")
        software_version = System.GetScenarioParameter("Software Version")
        
        parts2 = software_version.split('_')
        
        
        base = [variant, region, *parts2]
        print(base)
        return base

def TC_25741428():
    
    try:
        testcaseID=25741428
        EngModeEntry()
        Enter_System()
        print("HW CPU Version")
        
        #HW CPU Version.
        (returnCode, result) = PluginOCREngine.GetTextLines(r'E:\CapturedScreenShots\JK\GEN\000_001_250630\SystemEntry.png', 710 , 220, 220 , 36)
        print(result)
        entry = result[0]  # Get the first (and only) item in the list
        key, value = entry.split(':', 1)
        value = value.strip()
        if value in ["REV_H", "REV_D", "REV_E"]:
            
            print("CPU Version is valid")
            print(value)
            CPU_Version_flag=True

        else:
            print("CPU Version is Invalid")
            CPU_Version_flag=False
    
        if CPU_Version_flag == True  :
            updateTCResult(testcaseID, "PASSED")
        else:
            updateTCResult(testcaseID, "FAILED")


    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        endTestCase()

def TC_25741429():
    
    try:
        testcaseID=25741429
        EngModeEntry()
        Enter_System()
        base=checkswdetails()


        (returnCode, result) = PluginOCREngine.GetTextLines(r'E:\CapturedScreenShots\JK\GEN\000_001_250630\SystemEntry.png', 1067 , 220, 320 , 40)
        print(result)

        parts = result[0].split('.')
        print(parts)

        Result_Flag=True
        if base == parts[:2] + parts[3:]:
            print("S/W Version is Present and same")
            Result_Flag=True
        else:
            print("S/W Version is not MATCHING ")
            Result_Flag=False
            
        if Result_Flag == True  :
            updateTCResult(testcaseID, "PASSED")
        else:
            updateTCResult(testcaseID, "FAILED")

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        endTestCase()


def TC_25741430():
    try:
        testcaseID=25741430
        EngModeEntry()
        Enter_System()
        (returnCode, result) = PluginOCREngine.GetTextLines(r'E:\CapturedScreenShots\JK\GEN\000_001_250630\SystemEntry.png', 1780 , 215, 171 , 40)
        print(result)

        
        date_str = result[0].strip() #cleaning whitespaces
        parsed_date=datetime.strptime(date_str,"%Y-%m-%d")
        parsed_date=parsed_date.strftime("%Y-%m-%d")
        
        end_date = date.today()
        Result_Flag = False
        if parsed_date <= end_date.strftime("%Y-%m-%d"):
            Result_Flag = True
            print("Date is valid and within the range")
        else:
            print("Date parsing failed")
            Result_Flag = False

               
        if Result_Flag == True  :
            updateTCResult(testcaseID, "PASSED")
        else:
            updateTCResult(testcaseID, "FAILED")
            

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        endTestCase()

def TC_25741431():
    testcaseID=25741431

    EngModeEntry()
    Enter_System()

    (returnCode, SW_Ver) = PluginOCREngine.GetTextLines(r'E:\CapturedScreenShots\JK\GEN\000_001_250630\SystemEntry.png', 2140 , 220, 300 , 40)
    print(SW_Ver)

    (returnCode, Build_Date) = PluginOCREngine.GetTextLines(r'E:\CapturedScreenShots\JK\GEN\000_001_250630\SystemEntry.png', 710 , 335, 92 , 30)
    print(Build_Date)
    
    #creating Base version
    Base_Micom=[]
    Base_Micom.append(System.GetScenarioParameter("Variant"))
    Base_Micom.append(System.GetScenarioParameter("Region"))
    Base_Micom.append(Build_Date[0])
    Base_Micom.append('MICOM')

    print(Base_Micom)

    parts = SW_Ver[0].split('.')
    parts.remove(parts[2])
    print(parts)
    flag=False
    if parts ==  Base_Micom:
        flag=True
        print("Micom SW Version is confirmed")
    else:
        print("Micom SW Version is not confirmed")

    if flag == True  :
        updateTCResult(testcaseID, "PASSED")
    else:
        updateTCResult(testcaseID, "FAILED")   


def TC_25741432():
    testcaseID=25741432
    (returnCode, DB_Ver_1) = PluginOCREngine.GetTextLines(r'E:\CapturedScreenShots\JK\GEN\000_001_250630\SystemEntry.png', 706 , 443, 140 , 40)
    print(DB_Ver_1)

    (returnCode, DB_Ver_2) = PluginOCREngine.GetTextLines(r'E:\CapturedScreenShots\JK\GEN\000_001_250630\SystemEntry.png', 706 , 505, 140 , 30)
    print(DB_Ver_2)

    DB_Ver=[]
    

    parts1 = DB_Ver_1[0].replace('.', ',').split(',')
 
    parts1=parts1[1:]
    print(parts1) 
    parts2 = DB_Ver_2[0].replace('.', ',').split(',')
   
    parts2=parts2[1:]
    print(parts2)
    


    DB_Ver=parts1+parts2
    int_DB_Ver=[int(x) for x in DB_Ver]
    print(DB_Ver)
    flag=False
    if 0 not in int_DB_Ver:
        flag=True
        print("Valid CAN-DB Version")
    else:
        print("Invalid CAN DB Version")

    if flag == True  :
        updateTCResult(testcaseID, "PASSED")
    else:
        updateTCResult(testcaseID, "FAILED")



def TC_25741448():
    testcaseID=25741448

    (returnCode, Eth_Ver) = PluginOCREngine.GetTextLines(r'E:\CapturedScreenShots\JK\GEN\000_001_250630\SystemEntry.png', 1070 , 330, 102 , 34)
    print(Eth_Ver)
    
    parts = Eth_Ver[0].replace('.', ',').split(',')
    Int_Eth_Ver=[int(x) for x in parts]
    print(Int_Eth_Ver)

    flag=False
    if 0 not in Int_Eth_Ver:
        flag=True
        print("Valid Ethernet DB Version")
    else:
        print("Invalid Ethernet DB Version")   

    if flag == True  :
        updateTCResult(testcaseID, "PASSED")
    else:
        updateTCResult(testcaseID, "FAILED")

        
def TC_25741449():
    testcaseID=25741449

    (returnCode, DSP_SW_Ver) = PluginOCREngine.GetTextLines(r'E:\CapturedScreenShots\JK\GEN\000_001_250630\SystemEntry.png', 1431 , 338, 130 , 30)
    print(DSP_SW_Ver)

    parts=DSP_SW_Ver[0].replace(':',',').split(',')
    print(parts)

    parts=parts[1].replace('.',',').split(',')
    print(parts)
    if 0 not in parts:
        flag=True
        print("Valid DSP Version")
    else:
        print("Invalid DSP Version")

    if flag == True  :
        updateTCResult(testcaseID, "PASSED")
    else:
        updateTCResult(testcaseID, "FAILED")

def TC_25741450():
    testcaseID=25741450


    (returnCode, ADAU_Ver) = PluginOCREngine.GetTextLines(r'E:\CapturedScreenShots\JK\GEN\000_001_250630\SystemEntry.png', 1776 , 338, 112 , 30)
    print(ADAU_Ver)

    parts=ADAU_Ver[0].replace('.',',').split(',')
    print(parts)

    if 0 not in parts:
        flag=True
        print("Valid ADAU Version")
    else:
        print("Invalid ADAU Version")

    if flag == True  :
        updateTCResult(testcaseID, "PASSED")
    else:
        updateTCResult(testcaseID, "FAILED")

def TC_25741453():

    EngModeEntry()
    Enter_System()
    #Entering ModuleInfo    
    testcaseID = 25741453
    DEV1.lcdTouch(208+1920, 396, None)
    capturedImagePath = create_image_path(testcaseID)
    System.Sleep(1000)

    Image_Capture(capturedImagePath)
    System.Sleep(3000)

    (returnCode, BT_Version) = PluginOCREngine.GetTextLines(r'E:\CapturedScreenShots\JX\KOR\000_001_250630\25741453.png', 712 , 493, 400 , 36)
    print(BT_Version)

    parts=BT_Version[0].split('-')

    flag =True
    if 'BSA0107_00.66.00@4.1.7' == parts[0]:
        print("BT Stack Version is Present")
    else:
        flag=False
        print("BT Stack version is not present") 

    if flag == True  :
        updateTCResult(testcaseID, "PASSED")
    else:
        updateTCResult(testcaseID, "FAILED")

def GetWifiVersions():
    testcaseID="GetWifiVersions"
        
    EngModeEntry()
    #Entering Dynamics
    
    DEV1.lcdTouch(762+1920, 257, None)
    System.Sleep(5000)
    DEV1.lcdTouch(500+1920, 472, None)
    System.Sleep(5000)
    DEV1.lcdTouch(145+1920, 400, None)    
    System.Sleep(5000)
    capturedImagePath = create_image_path(testcaseID)
    System.Sleep(1000)

    Image_Capture(capturedImagePath)
    System.Sleep(3000)
    (returnCode, Wifi_SW_Version) = PluginOCREngine.GetTextLines(f'E:\CapturedScreenShots\{config.variant}\{config.region}\{config.swVer}\{testcaseID}.png', 714 , 218, 529 , 73)
    print(Wifi_SW_Version)

    result = {}
    for item in Wifi_SW_Version:
        parts = item.split()
        if len(parts) >= 3:
            key = ' '.join(parts[:2])  # 'F/W Ver' or 'S/W Ver'
            value = parts[2]           # version number
            result[key] = value
    
    return result
    



def TC_25741620():
    testcaseID="25741620"
    
    set_=GetWifiVersions()
    
    if set_.get('S/W Ver') :
        print("S/W version is present")
        flag =True
    else:
        print("S/W version is not present or NULL")
        flag =False

    if flag == True  :
        updateTCResult(testcaseID, "PASSED")
    else:
        updateTCResult(testcaseID, "FAILED")


def TC_25741621():
    testcaseID="25741621"
    set_=GetWifiVersions()
    print(set_)
    flag=None
    if set_.get('H/W Ver') :
        print("H/W version is present")
        flag =True
    else:
        print("H/W version is not present or NULL")
        flag =False

    if flag == True  :
        updateTCResult(testcaseID, "PASSED")
    else:
        updateTCResult(testcaseID, "FAILED")


def TC_25741462():
