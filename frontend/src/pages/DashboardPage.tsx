import { useEffect, useState } from 'react';
import { ArrowRight, CircleAlert, Droplets, Fish, Thermometer, Waves } from 'lucide-react';
import { Link } from 'react-router-dom';
import { EmptyState, ErrorState, LoadingState } from '../components/Feedback';
import { TankStatusCard } from '../components/TankStatusCard';
import { tankService } from '../services/tankService';
import type { Tank } from '../types/tank';
import { getWaterStatus } from '../types/tank';

export function DashboardPage() {
  const [tanks, setTanks] = useState<Tank[]>([]);
  const [loading, setLoading] = useState(true);
  const [failed, setFailed] = useState(false);

  async function loadTanks() {
    setLoading(true);
    setFailed(false);
    try {
      setTanks(await tankService.listTanks());
    } catch {
      setFailed(true);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { void loadTanks(); }, []);

  const attentionCount = tanks.filter((tank) => getWaterStatus(tank) === 'attention').length;
  const averageTemp = tanks.length ? tanks.reduce((total, tank) => total + tank.temp_c, 0) / tanks.length : 0;
  const averagePh = tanks.length ? tanks.reduce((total, tank) => total + tank.ph, 0) / tanks.length : 0;
  const attentionTanks = tanks.filter((tank) => getWaterStatus(tank) === 'attention');
  const overviewTanks = attentionTanks.length ? attentionTanks.slice(0, 2) : tanks.slice(0, 2);

  return (
    <div className="page-stack">
      <section className="page-heading page-heading--dashboard">
        <div><p className="eyebrow"><span /> SAMPLE WORKSPACE</p><h1>Good morning.</h1><p className="page-subtitle">A quick read on the water across your tanks.</p></div>
        <Link className="button button--dark" to="/tanks">View all tanks <ArrowRight size={16} /></Link>
      </section>

      {loading ? <LoadingState label="Loading farm overview" /> : failed ? <ErrorState onRetry={() => void loadTanks()} /> : tanks.length === 0 ? <EmptyState /> : <>
        <section className="summary-grid" aria-label="Current farm summary">
          <article className="summary-tile summary-tile--ink"><div className="summary-top"><span>TANKS IN VIEW</span><span className="summary-icon"><Waves size={17} /></span></div><strong>{String(tanks.length).padStart(2, '0')}</strong><small>Current sample records</small></article>
          <article className={`summary-tile ${attentionCount ? 'summary-tile--alert' : ''}`}><div className="summary-top"><span>NEEDS ATTENTION</span><span className="summary-icon"><CircleAlert size={17} /></span></div><strong>{String(attentionCount).padStart(2, '0')}</strong><small>{attentionCount ? 'Readings outside monitored range' : 'All readings within range'}</small></article>
          <article className="summary-tile"><div className="summary-top"><span>AVERAGE WATER TEMP</span><span className="summary-icon summary-icon--green"><Thermometer size={17} /></span></div><strong>{averageTemp.toFixed(1)}<small>°C</small></strong><small>Across tanks in this view</small></article>
          <article className="summary-tile"><div className="summary-top"><span>AVERAGE pH</span><span className="summary-icon summary-icon--coral"><Droplets size={17} /></span></div><strong>{averagePh.toFixed(1)}</strong><small>Across tanks in this view</small></article>
        </section>

        <section className="dashboard-section">
          <div className="section-heading"><div><p className="eyebrow"><span /> WATER QUALITY</p><h2>{attentionCount ? 'A closer look' : 'Looking steady'}</h2></div><Link to="/tanks" className="text-link">Tank inventory <ArrowRight size={15} /></Link></div>
          <div className="tank-card-grid">{overviewTanks.map((tank) => <TankStatusCard key={tank.tank_id} tank={tank} />)}</div>
        </section>

        <section className="overview-strip"><span className="overview-strip-icon"><Fish size={19} /></span><div><strong>Current readings, one place.</strong><p>These summaries are calculated from the tank readings currently shown.</p></div><Link to="/tanks" aria-label="Open tank inventory"><ArrowRight size={18} /></Link></section>
        <p className="data-note"><Waves size={13} /> Sample data for interface preview <span>·</span> No live readings connected</p>
      </>}
    </div>
  );
}