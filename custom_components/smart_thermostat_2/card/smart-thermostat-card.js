```javascript
const LitElement = Object.getPrototypeOf(customElements.get("ha-panel-lovelace"));
const html = LitElement.prototype.html;
const css = LitElement.prototype.css;

class SmartThermostatCard extends LitElement {
  static get properties() {
    return {
      hass: {},
      config: {},
      _scheduleMode: { type: Boolean },
      _nightMode: { type: Object },
      _arrivalMode: { type: Object },
    };
  }

  constructor() {
    super();
    this._scheduleMode = false;
    this._nightMode = {
      enabled: false,
      startTime: "22:00",
      endTime: "06:00",
      temperature: 17.0
    };
    this._arrivalMode = {
      enabled: false,
      arrivalTime: "17:30",
      temperature: 20.0
    };
  }

  static get styles() {
    return css`
      :host {
        background: var(--ha-card-background, var(--card-background-color, white));
        border-radius: var(--ha-card-border-radius, 12px);
        box-shadow: var(--ha-card-box-shadow, 0 2px 2px 0 rgba(0, 0, 0, 0.14));
        color: var(--primary-text-color);
        display: block;
        padding: 16px;
        transition: all 0.3s ease-out;
      }

      .temperature {
        font-size: 48px;
        text-align: center;
        margin: 24px 0;
        font-weight: 300;
      }

      .modes {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
        margin: 16px 0;
      }

      .mode-btn {
        background: var(--primary-color);
        border: none;
        border-radius: 8px;
        color: var(--text-primary-color);
        cursor: pointer;
        padding: 8px 16px;
        transition: all 0.3s ease;
        text-transform: capitalize;
      }

      .mode-btn.active {
        background: var(--accent-color);
        font-weight: 500;
      }

      .mode-section {
        background: var(--ha-card-background);
        border-radius: 8px;
        padding: 16px;
        margin-top: 16px;
        border: 1px solid var(--divider-color);
      }

      .mode-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
      }

      .mode-header h3 {
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 0;
        font-size: 16px;
        color: var(--primary-text-color);
      }

      .mode-content {
        display: flex;
        flex-direction: column;
        gap: 16px;
      }

      .time-inputs {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
      }

      .temperature-slider {
        --mdc-theme-primary: var(--primary-color);
        width: 100%;
      }

      .temp-display {
        text-align: right;
        color: var(--secondary-text-color);
        font-size: 14px;
      }

      ha-icon {
        color: var(--primary-color);
      }

      ha-switch {
        --mdc-theme-secondary: var(--primary-color);
      }
    `;
  }

  render() {
    if (!this.hass || !this.config) {
      return html``;
    }

    const stateObj = this.hass.states[this.config.entity];
    if (!stateObj) {
      return html`
        <ha-card>
          <div class="not-found">Entity not found: ${this.config.entity}</div>
        </ha-card>
      `;
    }

    return html`
      <ha-card>
        <div class="temperature">
          ${stateObj.attributes.current_temperature}°C
          <div class="target">
            Target: ${stateObj.attributes.temperature}°C
          </div>
        </div>

        <div class="modes">
          ${['fast', 'constant', 'intermittent'].map(mode => html`
            <button
              class="mode-btn ${stateObj.attributes.mode === mode ? 'active' : ''}"
              @click=${() => this._handleModeChange(mode)}
            >
              ${mode}
            </button>
          `)}
        </div>

        <!-- Night Mode -->
        <div class="mode-section">
          <div class="mode-header">
            <h3>
              <ha-icon icon="mdi:weather-night"></ha-icon>
              Night Mode
            </h3>
            <ha-switch
              .checked=${this._nightMode.enabled}
              @change=${(e) => this._updateNightMode({ enabled: e.target.checked })}
            ></ha-switch>
          </div>
          
          ${this._nightMode.enabled ? html`
            <div class="mode-content">
              <div class="time-inputs">
                <div>
                  <ha-textfield
                    label="Start Time"
                    type="time"
                    .value=${this._nightMode.startTime}
                    @change=${(e) => this._updateNightMode({ startTime: e.target.value })}
                  ></ha-textfield>
                </div>
                <div>
                  <ha-textfield
                    label="End Time"
                    type="time"
                    .value=${this._nightMode.endTime}
                    @change=${(e) => this._updateNightMode({ endTime: e.target.value })}
                  ></ha-textfield>
                </div>
              </div>
              <div>
                <div class="temp-display">Night Temperature: ${this._nightMode.temperature}°C</div>
                <ha-slider
                  class="temperature-slider"
                  min="10"
                  max="30"
                  step="0.5"
                  pin
                  .value=${this._nightMode.temperature}
                  @change=${(e) => this._updateNightMode({ temperature: Number(e.target.value) })}
                ></ha-slider>
              </div>
            </div>
          ` : ''}
        </div>

        <!-- Arrival Mode -->
        <div class="mode-section">
          <div class="mode-header">
            <h3>
              <ha-icon icon="mdi:clock-outline"></ha-icon>
              Arrival Mode
            </h3>
            <ha-switch
              .checked=${this._arrivalMode.enabled}
              @change=${(e) => this._updateArrivalMode({ enabled: e.target.checked })}
            ></ha-switch>
          </div>
          
          ${this._arrivalMode.enabled ? html`
            <div class="mode-content">
              <div>
                <ha-textfield
                  label="Arrival Time"
                  type="time"
                  .value=${this._arrivalMode.arrivalTime}
                  @change=${(e) => this._updateArrivalMode({ arrivalTime: e.target.value })}
                ></ha-textfield>
              </div>
              <div>
                <div class="temp-display">Target Temperature: ${this._arrivalMode.temperature}°C</div>
                <ha-slider
                  class="temperature-slider"
                  min="10"
                  max="30"
                  step="0.5"
                  pin
                  .value=${this._arrivalMode.temperature}
                  @change=${(e) => this._updateArrivalMode({ temperature: Number(e.target.value) })}
                ></ha-slider>
              </div>
            </div>
          ` : ''}
        </div>
      </ha-card>
    `;
  }

  _handleModeChange(mode) {
    this.hass.callService("smart_thermostat_2", "set_mode", {
      entity_id: this.config.entity,
      mode: mode
    });
  }

  _updateNightMode(changes) {
    this._nightMode = { ...this._nightMode, ...changes };
    this.hass.callService("smart_thermostat_2", "set_night_mode", {
      entity_id: this.config.entity,
      ...this._nightMode
    });
  }

  _updateArrivalMode(changes) {
    this._arrivalMode = { ...this._arrivalMode, ...changes };
    this.hass.callService("smart_thermostat_2", "set_arrival_mode", {
      entity_id: this.config.entity,
      ...this._arrivalMode
    });
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error("You need to define an entity");
    }
    this.config = config;
  }

  getCardSize() {
    return 4;
  }
}

customElements.define("smart-thermostat-card", SmartThermostatCard);
```