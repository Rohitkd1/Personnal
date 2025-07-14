from Eng_Dealer_log import *
from ENG_Dealer_structured import *
import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "pytest"])
 
class Config:
    variant = "JX"
    region = "KOR"

 
def set_config(variant_value, region_value):
    Config.variant = variant_value
    Config.region = region_value
 
 
def TestMain():
    try:

        with open('Result.txt','w') as f:
            f.write(f"Test Case ID - RESULT")
        getSoftwareDetails()     
        #TC_25741428()
        #TC_25741429()
        #TC_25741430()
        #TC_25741431()
        #TC_25741432()
        #TC_25741448()
        #TC_25741449()
        #TC_25741450()
        #TC_25741453()
        #TC_25741620()
        #TC_25741621()
        TC_25741462()

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        endTestCase()

    
 
