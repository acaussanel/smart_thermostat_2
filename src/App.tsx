```tsx
import React, { useState } from 'react';
import { Settings, Moon, Clock, ThermometerSun } from 'lucide-react';
import WeatherForecast from './components/WeatherForecast';
import HeaterControl from './components/HeaterControl';
import TemperatureControl from './components/TemperatureControl';

function App() {
  const [currentTemp, setCurrentTemp] = useState(19.5);
  const [targetTemp, setTargetTemp] = useState(20.5);
  const [mode, setMode] = useState('constant');
  const [isHeaterOn, setIsHeaterOn] = useState(false);
  const [nightMode, setNightMode] = useState({
    enabled: false,
    startTime: "22:00",
    endTime: "06:00",
    temperature: 17.0
  });
  const [arrivalMode, setArrivalMode] = useState({
    enabled: false,
    arrivalTime: "17:30",
    temperature: 20.0
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-md p-6 space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-semibold text-gray-800">Smart Thermostat</h2>
        </div>

        {/* Temperature Control */}
        <TemperatureControl
          currentTemp={currentTemp}
          targetTemp={targetTemp}
          onTargetTempChange={setTargetTemp}
        />

        {/* Mode Selection */}
        <div className="grid grid-cols-3 gap-3">
          {['fast', 'constant', 'intermittent'].map((modeOption) => (
            <button
              key={modeOption}
              onClick={() => setMode(modeOption)}
              className={`px-4 py-2 rounded-lg capitalize ${
                mode === modeOption 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              } transition-colors`}
            >
              {modeOption}
            </button>
          ))}
        </div>

        {/* Night Mode */}
        <div className="bg-gray-50 rounded-lg p-4 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Moon className="w-5 h-5 text-blue-500" />
              <span className="font-medium">Night Mode</span>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                className="sr-only peer"
                checked={nightMode.enabled}
                onChange={(e) => setNightMode({...nightMode, enabled: e.target.checked})}
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-500"></div>
            </label>
          </div>
          {nightMode.enabled && (
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Start Time</label>
                  <input
                    type="time"
                    value={nightMode.startTime}
                    onChange={(e) => setNightMode({...nightMode, startTime: e.target.value})}
                    className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-600 mb-1">End Time</label>
                  <input
                    type="time"
                    value={nightMode.endTime}
                    onChange={(e) => setNightMode({...nightMode, endTime: e.target.value})}
                    className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm text-gray-600 mb-1">Night Temperature: {nightMode.temperature}°C</label>
                <input
                  type="range"
                  min="10"
                  max="30"
                  step="0.5"
                  value={nightMode.temperature}
                  onChange={(e) => setNightMode({...nightMode, temperature: parseFloat(e.target.value)})}
                  className="w-full"
                />
              </div>
            </div>
          )}
        </div>

        {/* Arrival Mode */}
        <div className="bg-gray-50 rounded-lg p-4 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Clock className="w-5 h-5 text-blue-500" />
              <span className="font-medium">Arrival Mode</span>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                className="sr-only peer"
                checked={arrivalMode.enabled}
                onChange={(e) => setArrivalMode({...arrivalMode, enabled: e.target.checked})}
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-500"></div>
            </label>
          </div>
          {arrivalMode.enabled && (
            <div className="space-y-3">
              <div>
                <label className="block text-sm text-gray-600 mb-1">Arrival Time</label>
                <input
                  type="time"
                  value={arrivalMode.arrivalTime}
                  onChange={(e) => setArrivalMode({...arrivalMode, arrivalTime: e.target.value})}
                  className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-600 mb-1">Target Temperature: {arrivalMode.temperature}°C</label>
                <input
                  type="range"
                  min="10"
                  max="30"
                  step="0.5"
                  value={arrivalMode.temperature}
                  onChange={(e) => setArrivalMode({...arrivalMode, temperature: parseFloat(e.target.value)})}
                  className="w-full"
                />
              </div>
            </div>
          )}
        </div>

        {/* Heater Status */}
        <HeaterControl
          isOn={isHeaterOn}
          onToggle={() => setIsHeaterOn(!isHeaterOn)}
          power={isHeaterOn ? 1000 : 0}
        />
      </div>
    </div>
  );
}

export default App;
```