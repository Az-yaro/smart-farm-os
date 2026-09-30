import { useEffect, useState } from 'react';
import { ArrowLeft, CircleAlert, Droplets, Thermometer, Waves } from 'lucide-react';
import { Link, useParams } from 'react-router-dom';
import { EmptyState, ErrorState, LoadingState } from '../components/Feedback';
import { tankService } from '../services/tankService';
import type { Tank } from '../types/tank';
import { getWaterStatus } from '../types/tank';

function ReadingCard({ icon: Icon, label, value, unit, note, alert = false }: {
  icon: typeof Droplets;
  label: string;
  value: string;
  unit?: string;
  note: string;
  alert?: boolean;
}) {
  return (
    <article className={`reading-card ${alert ? 'reading-card--alert' : ''}`}>
      <div className="reading-icon"><Icon size={18} /></div>
      <span className="reading-label">{label}</span>
      <strong>{value}<small>{unit}</small></strong>
      <span className="reading-note">{note}</span>
    </article>
  );
}

export function TankDetailPage() {
  const { tankId = '' } = useParams();
  const [tank, setTank] = useState<Tank | null>(null);
  const [loading, setLoading] = useState(true);
  const [failed, setFailed] = useState(false);

  async function loadTank() {
    setLoading(true);
    setFailed(false);
    try {
      setTank(await tankService.getTank(tankId));
    } catch {
      setFailed(true);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { void loadTank(); }, [tankId]);

  return (
    <div className="page-stack">
      {loading ? <LoadingState label="Loading tank detail" /> : failed ? <ErrorState onRetry={() => void loadTank()} /> : !tank ? <>
        <Link to="/tanks" className="back-link back-link--inline"><ArrowLeft size={15} /> Back to tanks</Link>
        <EmptyState title="Tank not found" message="This tank isn’t in the current sample set." />
      </> : <>
        <Link to="/tanks" className="back-link back-link--inline"><ArrowLeft size={15} /> All tanks</Link>
        <section className="detail-heading">
          <div className="detail-title-row"><span className="detail-tank-icon"><Waves size={21} /></span><div><p className="eyebrow"><span /> TANK STATUS</p><h1>{tank.tank_id}</h1></div></div>
          <span className={`status-chip status-chip--large ${getWaterStatus(tank) === 'attention' ? 'status-chip--attention' : 'status-chip--good'}`}><span />{getWaterStatus(tank) === 'attention' ? 'Attention needed' : 'Within monitored range'}</span>
        </section>

        {getWaterStatus(tank) === 'attention' && <div className="detail-alert" role="status"><CircleAlert size={18} /><div><strong>Review this tank’s water readings</strong><span>At least one reading is outside the monitored range for ammonia or pH.</span></div></div>}

        <section className="detail-readings" aria-label="Current water readings">
          <ReadingCard icon={Droplets} label="Ammonia" value={tank.ammonia_ppm.toFixed(3)} unit="ppm" note={tank.ammonia_ppm >= 0.05 ? 'At or above 0.05 ppm' : 'Below 0.05 ppm'} alert={tank.ammonia_ppm >= 0.05} />
          <ReadingCard icon={Waves} label="pH level" value={tank.ph.toFixed(1)} note={tank.ph < 6.5 || tank.ph > 8.5 ? 'Outside 6.5–8.5 range' : 'Within 6.5–8.5 range'} alert={tank.ph < 6.5 || tank.ph > 8.5} />
          <ReadingCard icon={Thermometer} label="Water temperature" value={tank.temp_c.toFixed(1)} unit="°C" note="Current reading" />
        </section>

        <section className="tank-profile">
          <div><span className="profile-label">TANK IDENTIFIER</span><strong>{tank.tank_id}</strong></div>
          <div><span className="profile-label">CAPACITY</span><strong>{tank.capacity_liters.toLocaleString()} <small>liters</small></strong></div>
          <div><span className="profile-label">DATA SOURCE</span><strong className="profile-source"><span /> Sample data</strong></div>
        </section>
        <p className="data-note"><Waves size={13} /> Current sample reading <span>·</span> Historical measurements are not available in this preview</p>
      </>}
    </div>
  );
}