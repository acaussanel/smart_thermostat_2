import React from 'react';
import { ThermometerSun } from 'lucide-react';

type TemperatureControlProps = {
  currentTemp: number;
  targetTemp: number;
  onTargetTempChange: (temp: number) => void;
}

const TemperatureControl: React.FC<TemperatureControlProps> = ({
  currentTemp,
  targetTemp,
  onTargetTempChange
}) => {
  return (
    <div className="flex flex-col items-center py-8">
      <div className="relative">
        <ThermometerSun className="w-16 h-16 text-blue-500 mb-4" />
        <div className="absolute -right-2 -top-2 bg-green-500 w-4 h-4 rounded-full"></div>
      </div>
      <div className="text-sm text-gray-500 mb-1">Current: {currentTemp}°C</div>
      <div className="text-4xl font-bold text-gray-800 mb-2">
        {targetTemp}°C
      </div>
      <div className="flex items-center gap-4">
        <button 
          onClick={() => onTargetTempChange(Math.min(30, targetTemp + 0.5))}
          className="bg-blue-500 text-white w-10 h-10 rounded-full flex items-center justify-center text-2xl hover:bg-blue-600 transition-colors"
        >
          +
        </button>
        <button 
          onClick={() => onTargetTempChange(Math.max(10, targetTemp - 0.5))}
          className="bg-blue-500 text-white w-10 h-10 rounded-full flex items-center justify-center text-2xl hover:bg-blue-600 transition-colors"
        >
          -
        </button>
      </div>
    </div>
  );
};

export default TemperatureControl;