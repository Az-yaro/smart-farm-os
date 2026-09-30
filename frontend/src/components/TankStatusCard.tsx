import { ArrowUpRight, Droplets, Thermometer, Waves } from 'lucide-react';
import { Link } from 'react-router-dom';
import type { Tank } from '../types/tank';
import { getWaterStatus } from '../types/tank';

export function TankStatusCard({ tank, compact = false }: { tank: Tank; compact?: boolean }) {
  const status = getWaterStatus(tank);

  return (
    <Link to={`/tanks/${tank.tank_id}`} className={`tank-card ${compact ? 'tank-card--compact' : ''}`}>
      <div className="tank-card-top">
        <span className="tank-icon"><Waves size={18} /></span>
        <span className={`status-chip ${status === 'attention' ? 'status-chip--attention' : 'status-chip--good'}`}>
          <span />{status === 'attention' ? 'Attention' : 'Within range'}
        </span>
        <ArrowUpRight className="tank-card-arrow" size={16} />
      </div>
      <div className="tank-card-heading"><span>{tank.tank_id}</span><small>{tank.capacity_liters.toLocaleString()} L capacity</small></div>
      <div className="tank-card-metrics">
        <div><span><Droplets size={13} /> Ammonia</span><strong className={tank.ammonia_ppm >= 0.05 ? 'value-alert' : ''}>{tank.ammonia_ppm.toFixed(3)} <small>ppm</small></strong></div>
        <div><span><Waves size={13} /> pH</span><strong className={tank.ph < 6.5 || tank.ph > 8.5 ? 'value-alert' : ''}>{tank.ph.toFixed(1)}</strong></div>
        {!compact && <div><span><Thermometer size={13} /> Water temp</span><strong>{tank.temp_c.toFixed(1)} <small>°C</small></strong></div>}
      </div>
      {status === 'attention' && <div className="tank-card-notice">One or more readings are outside the monitored range.</div>}
    </Link>
  );
}