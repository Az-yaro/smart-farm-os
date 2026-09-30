import { mockTanks } from '../data/mockTanks';
import type { Tank } from '../types/tank';

export interface TankService {
  listTanks(): Promise<Tank[]>;
  getTank(tankId: string): Promise<Tank | null>;
}

const mockTankService: TankService = {
  async listTanks() {
    await new Promise((resolve) => window.setTimeout(resolve, 420));
    return mockTanks.map((tank) => ({ ...tank }));
  },
  async getTank(tankId) {
    await new Promise((resolve) => window.setTimeout(resolve, 320));
    const tank = mockTanks.find((record) => record.tank_id === tankId);
    return tank ? { ...tank } : null;
  },
};

export const tankService: TankService = mockTankService;