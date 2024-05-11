import psutil
import time
import logging
import wmi

# Initialize logging
logging.basicConfig(filename='game_monitor.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# A list of known game process names for demonstration, adjust these for Windows processes
known_games = ['Valorant.exe']

# Set to keep track of currently running games
current_games = set()

# Initialize WMI client
wmi_client = wmi.WMI()

# Function to get CPU usage
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

# Function to get temperature readings (best effort on Windows)
def get_temperature():
    temperatures = {}
    try:
        for sensor in wmi_client.Sensor():
            if sensor.SensorType == 'Temperature':
                temperatures[sensor.Name] = sensor.Value
    except Exception as e:
        logging.error(f"Error fetching temperatures: {e}")
    return temperatures

# Placeholder for optimizing performance
def optimize_performance(game):
    logging.info(f"Optimizing performance for {game}")
    print(f"Optimizing performance for {game}")

# Placeholder for reverting optimizations
def revert_optimizations(game):
    logging.info(f"Reverting optimizations for {game}")
    print(f"Reverting optimizations for {game}")

def update_game_status():
    # Scan all running processes
    running_games = {proc.info['name'] for proc in psutil.process_iter(['pid', 'name']) if proc.info['name'].lower() in map(str.lower, known_games)}
    
    # Identify newly launched games
    new_games = running_games - current_games
    for game in new_games:
        print(f"Game detected: {game}")
        logging.info(f"Game detected: {game}")
        optimize_performance(game)
        current_games.add(game)
    
    # Identify games that have terminated
    terminated_games = current_games - running_games
    for game in terminated_games:
        print(f"Game terminated: {game}")
        logging.info(f"Game terminated: {game}")
        revert_optimizations(game)
        current_games.remove(game)

def main():
    print("Monitoring for game launches and terminations...")
    while True:
        update_game_status()
        cpu_usage = get_cpu_usage()
        temperatures = get_temperature()
        print(f"Current CPU Usage: {cpu_usage}%")
        for sensor_name, temperature in temperatures.items():
            print(f"{sensor_name}: {temperature}°C")
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    main()
