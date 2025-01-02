"""Heating models for different modes."""
from dataclasses import dataclass
from typing import List, Optional
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from ..const import MODE_FAST, MODE_CONSTANT, MODE_INTERMITTENT

@dataclass
class HeatingProfile:
    """Represents a heating profile with learned parameters."""
    thermal_inertia: float
    heat_loss_rate: float
    power_efficiency: float
    optimal_cycle_time: Optional[float] = None  # Pour le mode intermittent

class HeatingModel:
    """Advanced heating model with mode-specific behavior."""
    
    def __init__(self, mode: str):
        """Initialize the heating model."""
        self.mode = mode
        self.model = RandomForestRegressor(n_estimators=100)
        self.profile = None
        self._is_trained = False
        
    def train(self, 
              temperatures: List[float],
              outside_temps: List[float],
              heating_powers: List[float],
              time_deltas: List[float]):
        """Train the model and learn heating profile."""
        X = np.column_stack([temperatures, outside_temps, heating_powers, time_deltas])
        y = temperatures[1:]  # Target is next temperature
        
        self.model.fit(X[:-1], y)
        self._is_trained = True
        
        # Calculate heating profile parameters
        self.profile = self._calculate_profile(
            temperatures, outside_temps, heating_powers, time_deltas
        )
        
    def _calculate_profile(self, temps, ext_temps, powers, deltas) -> HeatingProfile:
        """Calculate heating profile parameters based on historical data."""
        # Calcul de l'inertie thermique
        temp_changes = np.diff(temps)
        power_changes = np.diff(powers)
        thermal_inertia = np.mean(np.abs(power_changes / (temp_changes + 1e-6)))
        
        # Calcul du taux de perte de chaleur
        temp_diff = np.array(temps) - np.array(ext_temps)
        heat_loss_rate = np.mean(temp_diff[1:] - temp_diff[:-1]) / np.mean(deltas)
        
        # Calcul de l'efficacité énergétique
        power_efficiency = np.mean(temp_changes / (np.array(powers)[:-1] + 1e-6))
        
        # Pour le mode intermittent, calculer le cycle optimal
        optimal_cycle = None
        if self.mode == MODE_INTERMITTENT:
            # Analyse des cycles naturels de température
            temp_peaks = self._find_peaks(temps)
            if len(temp_peaks) > 1:
                optimal_cycle = np.mean(np.diff(temp_peaks))
        
        return HeatingProfile(
            thermal_inertia=thermal_inertia,
            heat_loss_rate=heat_loss_rate,
            power_efficiency=power_efficiency,
            optimal_cycle_time=optimal_cycle
        )
    
    def _find_peaks(self, temps: List[float]) -> List[int]:
        """Find temperature peaks for cycle analysis."""
        peaks = []
        for i in range(1, len(temps) - 1):
            if temps[i] > temps[i-1] and temps[i] > temps[i+1]:
                peaks.append(i)
        return peaks
    
    def predict_heating_power(self, 
                            current_temp: float,
                            target_temp: float,
                            outside_temp: float,
                            time_delta: float) -> float:
        """Predict required heating power based on mode and conditions."""
        if not self._is_trained or not self.profile:
            return 0.0
            
        if self.mode == MODE_FAST:
            return self._fast_mode_power(
                current_temp, target_temp, outside_temp
            )
        elif self.mode == MODE_CONSTANT:
            return self._constant_mode_power(
                current_temp, target_temp, outside_temp
            )
        else:  # MODE_INTERMITTENT
            return self._intermittent_mode_power(
                current_temp, target_temp, outside_temp, time_delta
            )
    
    def _fast_mode_power(self, current_temp, target_temp, outside_temp):
        """Calculate power for fast heating mode."""
        temp_diff = target_temp - current_temp
        outside_factor = max(0, (current_temp - outside_temp) * self.profile.heat_loss_rate)
        
        # Puissance maximale si l'écart est important
        if temp_diff > 2:
            return 1.0
        
        return max(0.0, min(1.0, (
            temp_diff * self.profile.thermal_inertia + 
            outside_factor
        ) / self.profile.power_efficiency))
    
    def _constant_mode_power(self, current_temp, target_temp, outside_temp):
        """Calculate power for constant temperature mode."""
        temp_diff = target_temp - current_temp
        outside_factor = max(0, (current_temp - outside_temp) * self.profile.heat_loss_rate)
        
        return max(0.0, min(0.8, (
            temp_diff * self.profile.thermal_inertia * 0.7 + 
            outside_factor
        ) / self.profile.power_efficiency))
    
    def _intermittent_mode_power(self, current_temp, target_temp, outside_temp, time_delta):
        """Calculate power for intermittent mode."""
        if not self.profile.optimal_cycle_time:
            return self._constant_mode_power(current_temp, target_temp, outside_temp)
            
        # Determine si nous sommes dans une phase de chauffe du cycle
        cycle_position = (time_delta % self.profile.optimal_cycle_time) / self.profile.optimal_cycle_time
        
        if cycle_position < 0.3:  # 30% du temps en chauffe
            return self._fast_mode_power(current_temp, target_temp + 1, outside_temp)
        else:
            return 0.0  # Phase de refroidissement