from json import dump, load
def main_loop():
    
    print("SELECT OPTIONS:")
    print("1. Run Scraper for links")
    print("2. Run Scraper for listing information")
    print("3. Run Scraper for listing avalibility")
    print("4. Change output config")
    print("INPUT q TO EXIT")
    option = input("> ")
    config = load_config()
    
    if option == "4":
        change_config(config)
    if option == "q":
        return
        

def load_config():
    config = {
        "query": "",
        "links": "",
        "data": "",
        "temp": ""
    }
    try:
        with open("./config.json", "r") as f:
            config = load(f)           
    except:
        save_config(config)
    return config 

def save_config(config):
    with open("./config.json", "w") as f:
        dump(config, f)
    
def change_config(config):
    print("CURRENT CONFIG:")
    print("[Q] [" + config['query'] + "] - search queries (txt file for multiple queries)")
    print("[L] [" + config['links'] + "] - output of found links from search")
    print("[D] [" + config['data'] + "] - folder to store accomendation information and avalibility")
    print("[T] [" + config['temp'] + "] - folder for intermediate or temp data")
    print("INPUT q TO GO BACK TO MAIN")
    try:
        get = input("INPUT [OPTION] [DEST] TO CHNAGE CONFIG\n> ")
        if get == "q":
            main_loop()
            return
        t, v = get.split(" ")
        target = {'Q': 'query', 'L': 'links', 'D': 'data', 'T': 'temp'}
        if t in ['Q', 'L', 'D', 'T']:
            config[target[t]] = v
            save_config(config)
            change_config(config)
    except: 
        pass
if __name__ == "__main__":
    main_loop()