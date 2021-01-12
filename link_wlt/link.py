import time
from selenium import webdriver

def print_ts(message):  
    print("[%s] %s"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message))
def run(interval, command, str_name, str_password):  
    print_ts("-"*100)  
    print_ts("Command %s"%command)  
    print_ts("Starting every %s seconds."%interval)  
    print_ts("-"*100)  
    while True:  
        try:  
            # sleep for the remaining seconds of interval  
            #time_remaining = interval-time.time()%interval  
            time_remaining = interval
            print_ts("Starting command.")
            
            chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
            driver = webdriver.Chrome(chromedriver)
            driver.get("http://wlt.ustc.edu.cn")
            time.sleep(3)
            #
            name = driver.find_element_by_name("name")
            name.send_keys(str_name)
            pwd = driver.find_element_by_name("password")
            pwd.send_keys(str_password)
            login_button = driver.find_element_by_name("set")
            login_button.click()

            time.sleep(10)
            driver.quit()
            
            print_ts("Sleeping until %s (%s seconds)..."%((time.ctime(time.time()+time_remaining)), time_remaining))  
            time.sleep(time_remaining)  
            # execute the command  
            #status = os.system(command)  
            #print_ts("-"*100)  
            #print_ts("Command status = %s."%status)  
        except Exception:  
            pass
            
if __name__=="__main__":  
    interval = 11000
    #interval = 20
    command = r"ls"  
    run(interval, command, str_name="name", str_password="password")  
    