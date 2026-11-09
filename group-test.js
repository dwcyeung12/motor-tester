import {duration, range} from './protocol.js';

export function validateGroup(rows, maxId) {
  const active = rows.filter(row => row.enabled);
  if (active.length < 2) throw new Error('Select at least two devices.');
  const ids = new Set();
  return active.map(({id, speed}) => {
    if (String(id).trim() === '' || String(speed).trim() === '') throw new Error('ID and speed are required.');
    id = range(id, 0, maxId, 'Device ID');
    speed = range(speed, -1000, 1000, 'Speed');
    if (ids.has(id)) throw new Error('Each device must have a unique ID.');
    ids.add(id);
    return [id, speed];
  });
}

// Track every device before attempting a command, including an uncertain write.
export class ServoGroup {
  constructor(send, makeRun, makeStop, onTimerError = () => {}) {
    this.send = send;
    this.makeRun = makeRun;
    this.makeStop = makeStop;
    this.onTimerError = onTimerError;
    this.active = new Map();
    this.generation = 0;
    this.timer = null;
  }
  async stop() {
    ++this.generation;
    clearTimeout(this.timer);
    this.timer = null;
    const targets = [...this.active];
    let firstError;
    for (const [id, spinning] of targets) {
      let stopped = true;
      for (const command of this.makeStop(id, spinning)) {
        try { await this.send(command); }
        catch (error) { stopped = false; firstError ||= error; }
      }
      if (stopped) this.active.delete(id);
    }
    if (firstError) throw firstError;
  }
  async startPosition(id, pos, ms) {
    const stopping = this.stop();
    const generation = this.generation;
    await stopping;
    if (generation !== this.generation) return false;
    try {
      this.active.set(id, false);
      for (const command of this.makeRun(id, {pos, ms}, false)) {
        if (generation !== this.generation) return false;
        await this.send(command);
      }
      if (generation === this.generation) {
        this.timer = setTimeout(() => { this.active.delete(id); this.timer = null; }, ms);
      }
      return generation === this.generation;
    } catch (error) {
      try { await this.stop(); } catch (stopError) { this.onTimerError(stopError); }
      throw error;
    }
  }
  async start(outputs, seconds, spinning = true) {
    duration(seconds);
    const stopping = this.stop();
    const generation = this.generation;
    await stopping;
    if (generation !== this.generation) return false;
    try {
      // Start the watchdog before any writes, so a slow bus does not extend the run.
      this.timer = setTimeout(() => this.stop().catch(this.onTimerError), seconds * 1000);
      for (const [id, value] of outputs) {
        if (generation !== this.generation) return false;
        this.active.set(id, spinning);
        for (const command of this.makeRun(id, value, spinning)) {
          if (generation !== this.generation) return false;
          await this.send(command);
        }
      }
      return generation === this.generation;
    } catch (error) {
      try { await this.stop(); } catch (stopError) { this.onTimerError(stopError); }
      throw error;
    }
  }
}
