import time
import json
from croniter import croniter
from datetime import datetime

class TriggerProcessor:
    def __init__(self, pipelines_config):
        # Initialize with pipelines configuration loaded from JSON
        self.pipelines = pipelines_config.get("pipelines", [])

    def run(self):
        # Iterate through each pipeline and check for triggers
        for pipeline in self.pipelines:
            triggers = pipeline.get("settings", {}).get("triggers", [])
            for trigger in triggers:
                config = trigger.get("config", {})
                # Check if trigger is enabled and its type
                if config.get("enabled"):
                    trigger_type = config.get("type", "")
                    if trigger_type == ".TriggerPolled":
                        self.handle_polled_trigger(trigger)
                    elif trigger_type == ".TriggerCron":
                        self.handle_cron_trigger(trigger)
                    else:
                        print(f"Trigger '{trigger.get('name')}' has an unsupported type: {trigger_type}")
                else:
                    print(f"Trigger '{trigger.get('name')}' is not enabled.")

    def handle_polled_trigger(self, trigger):
        # Handle the Polled trigger type
        config = trigger.get("config", {})
        interval = config.get("interval", {}).get("duration", 10)
        name = trigger.get("name", "Unnamed Trigger")
        print(f"Running Polled Trigger: {name} every {interval} seconds")
        
        # Run trigger task in a loop
        self.run_trigger_task(name, interval)

    def handle_cron_trigger(self, trigger):
        # Handle the Cron trigger type
        config = trigger.get("config", {})
        cron_string = config.get("schedule", {}).get("cronString", "0 0 * * *")  # Default: Midnight every day
        timezone = config.get("schedule", {}).get("timezone", "UTC")  # Handle timezone if needed
        logging = config.get("schedule", {}).get("logging", "None")
        name = trigger.get("name", "Unnamed Cron Trigger")
        
        # Initialize croniter with the cron string and current time
        base_time = datetime.now()
        cron = croniter(cron_string, base_time)
        
        print(f"Running Cron Trigger: {name} with cron expression: {cron_string}")
        
        # Run the cron task in a loop
        self.run_cron_trigger_task(name, cron)

    def run_trigger_task(self, name, interval):
        # This will keep running and print a message every interval
        while True:
            print(f"[{name}] Trigger Fired!")
            time.sleep(interval)

    def run_cron_trigger_task(self, name, cron):
        # This will calculate the next trigger time and wait until it's time to fire
        while True:
            # Get the next scheduled trigger time from croniter
            next_trigger_time = cron.get_next(datetime)
            time_until_next_trigger = (next_trigger_time - datetime.now()).total_seconds()
            
            # Wait until the next trigger time
            if time_until_next_trigger > 0:
                print(f"[{name}] Next trigger at: {next_trigger_time}")
                time.sleep(time_until_next_trigger)
                print(f"[{name}] Trigger Fired!")
            else:
                print(f"[{name}] Trigger Fired immediately!")

# Load the JSON data from 'config.json'
def load_json_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    # Load config data from the file
    config_data = load_json_config('highbyte-pipelines.json')
    
    # Initialize the TriggerProcessor with loaded pipelines configuration
    processor = TriggerProcessor(config_data.get("project", {}))
    
    # Run the triggers from the loaded configuration
    processor.run()

   
