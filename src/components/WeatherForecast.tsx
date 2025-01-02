import React from 'react';
import { Cloud, Sun, CloudRain } from 'lucide-react';

type ForecastData = {
  time: string;
  temperature: number;
  condition: 'sunny' | 'cloudy' | 'rainy';
}

const WeatherForecast: React.FC<{ forecasts: ForecastData[] }> = ({ forecasts }) => {
  const getWeatherIcon = (condition: string) => {
    switch (condition) {
      case 'sunny': return <Sun className="w-5 h-5" />;
      case 'cloudy': return <Cloud className="w-5 h-5" />;
      case 'rainy': return <CloudRain className="w-5 h-5" />;
      default: return <Sun className="w-5 h-5" />;
    }
  };

  return (
    <div className="bg-gray-50 rounded-lg p-4">
      <h3 className="text-sm font-medium text-gray-700 mb-3">24h Forecast</h3>
      <div className="flex gap-4 overflow-x-auto pb-2">
        {forecasts.map((forecast, index) => (
          <div key={index} className="flex flex-col items-center min-w-[60px]">
            <span className="text-xs text-gray-500">{forecast.time}</span>
            {getWeatherIcon(forecast.condition)}
            <span className="text-sm font-medium">{forecast.temperature}°C</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default WeatherForecast;