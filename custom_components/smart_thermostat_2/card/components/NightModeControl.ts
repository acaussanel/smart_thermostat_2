```typescript
import { html, css } from 'lit';
import { Moon } from 'lucide-react';

export const NightModeControl = ({
  enabled,
  startTime,
  endTime,
  temperature,
  onUpdate,
}) => html`
  <div class="mode-section">
    <div class="mode-header">
      <h3>
        <ha-icon icon="mdi:weather-night"></ha-icon>
        Night Mode
      </h3>
      <ha-switch
        .checked=${enabled}
        @change=${(e) => onUpdate({ enabled: e.target.checked })}
      ></ha-switch>
    </div>
    
    ${enabled ? html`
      <div class="mode-content">
        <div class="time-range">
          <ha-time-input
            .value=${startTime}
            @change=${(e) => onUpdate({ startTime: e.target.value })}
            label="Start Time"
          ></ha-time-input>
          <ha-time-input
            .value=${endTime}
            @change=${(e) => onUpdate({ endTime: e.target.value })}
            label="End Time"
          ></ha-time-input>
        </div>
        <div class="temperature-input">
          <ha-slider
            .min=${10}
            .max=${30}
            .step=${0.5}
            .value=${temperature}
            @change=${(e) => onUpdate({ temperature: e.target.value })}
          ></ha-slider>
          <span>${temperature}°C</span>
        </div>
      </div>
    ` : ''}
  </div>
`;
```