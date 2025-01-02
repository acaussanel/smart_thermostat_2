const LitElement = Object.getPrototypeOf(customElements.get("ha-panel-lovelace"));
const html = LitElement.prototype.html;
const css = LitElement.prototype.css;

class SmartThermostatCard extends LitElement {
  static get properties() {
    return {
      hass: {},
      config: {},
      _scheduleMode: { type: Boolean },
    };
  }

  static get styles() {
    return css`
      :host {
        background: var(--ha-card-background, var(--card-background-color, white));
        border-radius: var(--ha-card-border-radius, 4px);
        box-shadow: var(--ha-card-box-shadow, 0 2px 2px 0 rgba(0, 0, 0, 0.14));
        color: var(--primary-text-color);
        display: block;
        transition: all 0.3s ease-out;
        padding: 16px;
      }

      .temperature {
        font-size: 48px;
        text-align: center;
        margin: 16px 0;
      }

      .modes {
        display: flex;
        justify-content: space-around;
        margin: 16px 0;
      }

      .mode-btn {
        background: var(--primary-color);
        border: none;
        border-radius: 4px;
        color: var(--text-primary-color);
        cursor: pointer;
        padding: 8px 16px;
        transition: background 0.3s ease;
      }

      .mode-btn.active {
        background: var(--accent-color);
      }

      .schedule {
        margin-top: 16px;
      }

      .schedule-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
      }

      .schedule-content {
        background: var(--primary-background-color);
        border-radius: 4px;
        padding: 16px;
      }

      .schedule-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 8px 0;
      }
    `;
  }

  constructor() {
    super();
    this._scheduleMode = false;
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
          ${this._renderModeButtons(stateObj)}
        </div>

        <div class="controls">
          <ha-slider
            .min=${stateObj.attributes.min_temp}
            .max=${stateObj.attributes.max_temp}
            .value=${stateObj.attributes.temperature}
            .step=${0.5}
            @change=${this._handleTemperatureChange}
          ></ha-slider>
        </div>

        <div class="schedule">
          <div class="schedule-header">
            <span>Schedule</span>
            <ha-switch
              .checked=${this._scheduleMode}
              @change=${this._toggleScheduleMode}
            ></ha-switch>
          </div>

          ${this._scheduleMode ? this._renderSchedule() : ''}
        </div>
      </ha-card>
    `;
  }

  _renderModeButtons(stateObj) {
    const modes = ['fast', 'constant', 'intermittent'];
    return modes.map(
      mode => html`
        <button
          class="mode-btn ${stateObj.attributes.mode === mode ? 'active' : ''}"
          @click=${() => this._handleModeChange(mode)}
        >
          ${mode}
        </button>
      `
    );
  }

  _renderSchedule() {
    return html`
      <div class="schedule-content">
        ${(stateObj.attributes.schedule || []).map(
          item => html`
            <div class="schedule-row">
              <span>${item.time}</span>
              <span>${item.temp}°C</span>
              <span>${item.mode}</span>
              <ha-icon-button
                icon="hass:pencil"
                @click=${() => this._editScheduleItem(item)}
              ></ha-icon-button>
            </div>
          `
        )}
        <ha-icon-button
          icon="hass:plus"
          @click=${this._addScheduleItem}
        ></ha-icon-button>
      </div>
    `;
  }

  _handleTemperatureChange(e) {
    const temperature = e.target.value;
    this.hass.callService("climate", "set_temperature", {
      entity_id: this.config.entity,
      temperature: temperature
    });
  }

  _handleModeChange(mode) {
    this.hass.callService("smart_thermostat_2", "set_mode", {
      entity_id: this.config.entity,
      mode: mode
    });
  }

  _toggleScheduleMode(e) {
    this._scheduleMode = e.target.checked;
  }

  _editScheduleItem(item) {
    // Implement schedule item editing
  }

  _addScheduleItem() {
    // Implement new schedule item addition
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error("You need to define an entity");
    }
    this.config = config;
  }

  getCardSize() {
    return 3;
  }
}

customElements.define("smart-thermostat-card", SmartThermostatCard);