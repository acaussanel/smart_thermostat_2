```typescript
import { html, css } from 'lit';
import { Clock } from 'lucide-react';

export const ArrivalModeControl = ({
  enabled,
  arrivalTime,
  temperature,
  onUpdate,
}) => html`
  <div class="mode-section">
    <div class="mode-header">
      <h3>
        <ha-icon icon="mdi:clock-outline"></ha-icon>
        Arrival Mode
      </h3>
      <ha-switch
        .checked=${enabled}
        @change=${(e) => onUpdate({ enabled: e.target.checked })}
      ></ha-switch>
    </div>
    
    ${enabled ? html`
      <div class="mode-content">
        <ha-time-input
          .value=${arrivalTime}
          @change=${(e) => onUpdate({ arrivalTime: e.target.value })}
          label="Arrival Time"
        ></ha-time-input>
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