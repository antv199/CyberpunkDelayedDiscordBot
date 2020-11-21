import time, discord, os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

client=discord.Client()

Status=["d","d",0] #1. Text Status 2.URL, if one exists 3.Last time it got refreshed, in Unix Time
test=os.environ.get("Test")
#test=true

def getStatus():
    if Status[2]==0 or Status[2]+60<=int(time.time()):
        if test:
            driver=webdriver.Edge()
        else:
            driver=webdriver.Chrome(executable_path="/app/.apt/usr/bin/google-chrome")

        driver.get("https://hascyberpunkbeendelayedagain.com")

        try:
            text=WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="block-f4b50678503b972d2bc9"]/div/h2[2]'))) #Getting message of the day
            Status[0]=text.text

            try:
                text=WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="block-bfa7abb905ef1685a30f"]/div/h4/a'))) #Getting message of the day
                Status[0]+=" "+text.text
                Status[1]=text.get_attribute('href')
                Status[2]=int(time.time())
                driver.quit()
            except:
                print("No link!")
                Status[1]=""

        except:
            print("Didn't find anything. Maybe the page took too long to load or did the XPATH change?")
            Status[0]="Failed to get status!"
            Status[1]=""
            Status[2]=int(time.time())
            driver.quit()
    
    return Status

@client.event
async def on_ready():
    print("Ready")
    await client.change_presence(activity=discord.Game(name="Cyberpunk 2077"))

@client.event
async def on_message(msg):
    if msg.content==".cp":
        state=getStatus()
        await msg.channel.send(state[0]+"\n"+state[1])

client.run(os.environ.get("BOT_TOKEN"))