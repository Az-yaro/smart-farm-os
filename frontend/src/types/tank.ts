export interface Tank {
  tank_id: string;
  capacity_liters: number;
  ammonia_ppm: number;
  ph: number;
  temp_c: number;
}

export type WaterStatus = 'within-range' | 'attention';

export function getWaterStatus(tank: Tank): WaterStatus {
  return tank.ammonia_ppm >= 0.05 || tank.ph < 6.5 || tank.ph > 8.5
    ? 'attention'
    : 'within-range';
}