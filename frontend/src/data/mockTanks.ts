import type { Tank } from '../types/tank';

export const mockTanks: Tank[] = [
  { tank_id: 'tank-alpha', capacity_liters: 12000, ammonia_ppm: 0.018, ph: 7.2, temp_c: 27.4 },
  { tank_id: 'tank-bravo', capacity_liters: 18000, ammonia_ppm: 0.061, ph: 7.1, temp_c: 28.2 },
  { tank_id: 'tank-charlie', capacity_liters: 10000, ammonia_ppm: 0.024, ph: 6.3, temp_c: 26.8 },
  { tank_id: 'tank-delta', capacity_liters: 24000, ammonia_ppm: 0.012, ph: 7.4, temp_c: 27.9 },
  { tank_id: 'tank-echo', capacity_liters: 15000, ammonia_ppm: 0.031, ph: 7.0, temp_c: 28.5 },
];