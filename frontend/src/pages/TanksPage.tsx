import { useEffect, useMemo, useState } from 'react';
import { ArrowRight, Search, SlidersHorizontal, Waves } from 'lucide-react';
import { Link } from 'react-router-dom';
import { EmptyState, ErrorState, LoadingState } from '../components/Feedback';
import { TankStatusCard } from '../components/TankStatusCard';
import { tankService } from '../services/tankService';
import type { Tank } from '../types/tank';
import { getWaterStatus } from '../types/tank';

type Filter = 'all' | 'attention' | 'within-range';

export function TanksPage() {
  const [tanks, setTanks] = useState<Tank[]>([]);
  const [loading, setLoading] = useState(true);
  const [failed, setFailed] = useState(false);
  const [filter, setFilter] = useState<Filter>('all');
  const [query, setQuery] = useState('');

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

  const filteredTanks = useMemo(() => tanks.filter((tank) => {
    const matchesFilter = filter === 'all' || getWaterStatus(tank) === filter;
    return matchesFilter && tank.tank_id.toLowerCase().includes(query.trim().toLowerCase());
  }), [filter, query, tanks]);

  return (
    <div className="page-stack">
      <section className="page-heading">
        <div><p className="eyebrow"><span /> TANK MONITORING</p><h1>Tank inventory</h1><p className="page-subtitle">Current water readings from the tanks in this workspace.</p></div>
        <div className="inventory-total"><span><Waves size={16} /></span><strong>{loading ? '—' : String(tanks.length).padStart(2, '0')}</strong><small>tanks in view</small></div>
      </section>

      <section className="inventory-tools" aria-label="Tank inventory filters">
        <label className="search-field"><Search size={17} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Find a tank" aria-label="Find a tank" /></label>
        <div className="filter-control"><SlidersHorizontal size={15} /><span>Show</span><select value={filter} onChange={(event) => setFilter(event.target.value as Filter)} aria-label="Filter tanks by status"><option value="all">All tanks</option><option value="attention">Needs attention</option><option value="within-range">Within range</option></select></div>
      </section>

      {loading ? <LoadingState label="Loading tank inventory" /> : failed ? <ErrorState onRetry={() => void loadTanks()} /> : tanks.length === 0 ? <EmptyState /> : filteredTanks.length === 0 ? <EmptyState title="No matching tanks" message="Try a different name or status filter." /> : <>
        <div className="inventory-result-row"><span>{filteredTanks.length} {filteredTanks.length === 1 ? 'tank' : 'tanks'}</span><span>Readings shown from sample data</span></div>
        <div className="tank-card-grid tank-card-grid--inventory">{filteredTanks.map((tank) => <TankStatusCard key={tank.tank_id} tank={tank} />)}</div>
        <div className="inventory-bottom"><span>Showing current tank readings</span><Link to="/dashboard">Back to overview <ArrowRight size={14} /></Link></div>
      </>}
    </div>
  );
}