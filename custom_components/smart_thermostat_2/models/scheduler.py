"""Schedule management for Smart Thermostat 2.0."""
from datetime import datetime, time
from typing import Dict, List, Optional
import json

class ThermostatScheduler:
    """Manages heating schedules with multiple profiles."""
    
    def __init__(self):
        """Initialize the scheduler."""
        self.schedules: Dict[str, List[Dict]] = {}
        self.active_profile: str = "default"
        
    def add_profile(self, name: str, schedule: List[Dict]):
        """Add or update a schedule profile."""
        self.schedules[name] = schedule
        
    def get_current_settings(self) -> Optional[Dict]:
        """Get the current temperature and mode based on active schedule."""
        if not self.schedules or self.active_profile not in self.schedules:
            return None
            
        current_time = datetime.now().time()
        day_type = "weekend" if datetime.now().weekday() >= 5 else "weekday"
        schedule = self.schedules[self.active_profile]
        
        # Trouver le dernier événement passé
        current_settings = None
        for event in schedule:
            event_time = datetime.strptime(event["time"], "%H:%M").time()
            if event_time <= current_time:
                current_settings = event
            else:
                break
                
        return current_settings
        
    def set_active_profile(self, profile_name: str):
        """Set the active schedule profile."""
        if profile_name in self.schedules:
            self.active_profile = profile_name
            
    def export_schedules(self) -> str:
        """Export schedules as JSON string."""
        return json.dumps(self.schedules)
        
    def import_schedules(self, schedules_json: str):
        """Import schedules from JSON string."""
        try:
            self.schedules = json.loads(schedules_json)
        except json.JSONDecodeError:
            pass