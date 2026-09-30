import { useState } from 'react';
import {
  Activity,
  ArrowUpRight,
  ChevronDown,
  Fish,
  LayoutDashboard,
  Menu,
  Waves,
  X,
} from 'lucide-react';
import { NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom';

const navigation = [
  { to: '/dashboard', label: 'Overview', icon: LayoutDashboard },
  { to: '/tanks', label: 'Tanks', icon: Waves },
];

function pageTitle(pathname: string) {
  if (pathname.startsWith('/tanks/')) return 'Tank status';
  if (pathname === '/tanks') return 'Tank inventory';
  return 'Farm overview';
}

export function AppShell() {
  const [menuOpen, setMenuOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  return (
    <div className="app-frame">
      <button
        className="mobile-menu-button icon-button"
        aria-label={menuOpen ? 'Close navigation' : 'Open navigation'}
        aria-expanded={menuOpen}
        onClick={() => setMenuOpen((open) => !open)}
      >
        {menuOpen ? <X size={20} /> : <Menu size={20} />}
      </button>
      {menuOpen && <button className="nav-scrim" aria-label="Close navigation" onClick={() => setMenuOpen(false)} />}

      <aside className={`sidebar ${menuOpen ? 'sidebar--open' : ''}`}>
        <div className="brand-lockup">
          <span className="brand-mark"><Fish size={20} strokeWidth={2.2} /></span>
          <span className="brand-name">smart farm<span>OS</span></span>
          <button className="sidebar-close icon-button" aria-label="Close navigation" onClick={() => setMenuOpen(false)}>
            <X size={18} />
          </button>
        </div>

        <div className="workspace-select">
          <span className="workspace-glyph">SF</span>
          <span className="workspace-copy"><strong>Farm workspace</strong><small>Preview environment</small></span>
          <ChevronDown size={15} />
        </div>

        <p className="nav-caption">WORKSPACE</p>
        <nav className="primary-nav" aria-label="Main navigation">
          {navigation.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) => `nav-link ${isActive ? 'nav-link--active' : ''}`}
              onClick={() => setMenuOpen(false)}
            >
              <Icon size={18} strokeWidth={1.8} />
              <span>{label}</span>
              {label === 'Tanks' && <span className="nav-count">05</span>}
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="connection-note"><span className="connection-dot" /><span>Sample data active</span></div>
          <button className="sidebar-account" onClick={() => navigate('/login')}>
            <span className="account-avatar">SF</span>
            <span className="account-copy"><strong>Farm operator</strong><small>Demo workspace</small></span>
            <ArrowUpRight size={15} />
          </button>
          <button className="sidebar-public-link" onClick={() => navigate('/')}>
            <Activity size={15} /> Public site <ArrowUpRight size={13} />
          </button>
        </div>
      </aside>

      <main className="app-main">
        <header className="topbar">
          <div className="breadcrumb"><span>Workspace</span><span className="breadcrumb-slash">/</span><strong>{pageTitle(location.pathname)}</strong></div>
          <div className="topbar-right"><span className="preview-pill"><span /> Preview data</span><button className="topbar-avatar" aria-label="Open login page" onClick={() => navigate('/login')}>SF</button></div>
        </header>
        <div className="page-content"><Outlet /></div>
      </main>
    </div>
  );
}