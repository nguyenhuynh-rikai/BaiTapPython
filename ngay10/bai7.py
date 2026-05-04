from tqdm import tqdm
import time

def process_tasks():
    
    for i in tqdm(range(100), desc="Processing data"):
        time.sleep(0.05)

if __name__ == '__main__':
    process_tasks()