import time
import json

# Define the flow trigger class
class FlowTrigger:
    def __init__(self, name, interval_seconds, action, connection_reference):
        self.name = name
        self.interval_seconds = interval_seconds  # Directly in seconds
        self.action = action
        self.connection_reference = connection_reference
        self.enabled = True

    def start(self):
        """Start the polling mechanism."""
        print(f"Starting flow trigger: {self.name}")
        while self.enabled:
            print(f"Triggering action for {self.name}...")
            self.action(self.connection_reference)  # Perform the action when the trigger is fired
            print(f"Waiting for {self.interval_seconds} seconds...")
            time.sleep(self.interval_seconds)  # Wait for the next interval

    def stop(self):
        """Stop the polling mechanism."""
        print(f"Stopping flow trigger: {self.name}")
        self.enabled = False

# Example of an action function that gets triggered
def perform_action(connection_reference):
    print(f"Performing the flow action using connection: {connection_reference}")

# Function to process the JSON and extract trigger details
def process_trigger_from_json(json_data):
    # Extract the trigger details from JSON
    trigger_info = json_data["pipelines"][0]["settings"]["triggers"][0]
    
    trigger_name = trigger_info["name"]
    interval_seconds = trigger_info["config"]["flowEvaluation"]["interval"]["duration"]  # Interval in seconds
    
    # Simulate extracting the connection reference
    connection_reference = trigger_info["config"]["inReferences"][0]  # Extract the connection reference
    # Replace the placeholder with an actual reference (this could be dynamic based on your system)
    connection_reference = connection_reference.replace("{{Connection.Your_Connection_Name.Your_Flow_Reference}}", "ActualConnectionReference123")
    
    # Create and start the flow trigger
    flow_trigger = FlowTrigger(name=trigger_name, interval_seconds=interval_seconds, action=perform_action, connection_reference=connection_reference)
    
    return flow_trigger

# Sample JSON configuration (you can load this from a file or use directly)
json_data = {
  "pipelines": [
    {
      "name": "Sample_Flow_Pipeline",
      "uri": "pipeline",
      "groupAs": "/TestGroup",
      "description": "Sample_Flow_Pipeline",
      "tags": [],
      "settings": {
        "inputStages": [
          "start_stage"
        ],
        "trackActivity": True,
        "triggers": [
          {
            "name": "Flow_Trigger_Example",
            "config": {
              "type": ".TriggerFlow",
              "enabled": True,
              "flowEvaluation": {
                "type": "Polled",
                "interval": {
                  "duration": 10,  # Reduced to 10 seconds
                  "units": "Seconds"
                },
                "mode": "Always",
                "expression": "",
                "delay": {
                  "duration": 0,
                  "units": "Seconds"
                }
              },
              "inReferences": [
                "{{Connection.Your_Connection_Name.Your_Flow_Reference}}"
              ],
              "publishMode": "All",
              "template": {
                "type": "Off"
              }
            },
            "display": {
              "position": {
                "x": -400,
                "y": 0
              }
            }
          }
        ]
      }
    }
  ]
}

# Process the trigger based on JSON data
flow_trigger = process_trigger_from_json(json_data)

# Start the flow trigger (no threading, just a continuous loop)
flow_trigger.start()

# Optionally, you can stop the trigger after some time for demonstration:
# time.sleep(20)  # Let it run for 20 seconds to see the trigger in action
# flow_trigger.stop()  # Uncomment to stop after a certain time
