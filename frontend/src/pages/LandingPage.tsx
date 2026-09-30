import { ArrowDown, ArrowRight, ArrowUpRight, Fish, Leaf, Waves } from 'lucide-react';
import { Link } from 'react-router-dom';

export function LandingPage() {
  return (
    <main className="landing-page">
      <section className="landing-hero">
        <img
          className="landing-image"
          src="https://images.unsplash.com/photo-1500375592092-40eb2168fd21?auto=format&fit=crop&w=2400&q=88"
          alt="Open water catching the light"
        />
        <div className="landing-shade" />
        <header className="landing-nav">
          <Link className="landing-brand" to="/">
            <span className="brand-mark brand-mark--light"><Fish size={20} /></span>
            <span>smart farm<span>OS</span></span>
          </Link>
          <nav aria-label="Public navigation">
            <a href="#platform">Platform</a>
            <Link className="landing-login" to="/login">Sign in <ArrowUpRight size={15} /></Link>
          </nav>
        </header>
        <div className="landing-copy">
          <p className="eyebrow eyebrow--light"><span /> AQUACULTURE OPERATIONS</p>
          <h1>Clarity for every<br /><em>waterway.</em></h1>
          <p className="landing-description">A calmer way to keep an eye on the water, the tanks, and the work behind a healthy farm.</p>
          <div className="landing-actions">
            <Link to="/login" className="button button--lime">Enter the workspace <ArrowRight size={17} /></Link>
            <a href="#platform" className="text-link text-link--light">Explore the platform <ArrowDown size={15} /></a>
          </div>
        </div>
        <div className="landing-footnote"><span>01</span><span>Built around the water</span><span className="footnote-line" /></div>
      </section>

      <section className="landing-platform" id="platform">
        <div className="platform-heading">
          <p className="eyebrow"><span /> A CLEARER DAILY VIEW</p>
          <h2>Know what’s happening<br />across your tanks.</h2>
        </div>
        <div className="platform-detail">
          <p>Bring everyday farm monitoring into one focused workspace. See tank readings at a glance and spot water-quality values that need a closer look.</p>
          <Link className="text-link" to="/login">Go to the application <ArrowRight size={16} /></Link>
        </div>
        <div className="platform-points">
          <div><span className="platform-icon"><Waves size={20} /></span><strong>Tank overview</strong><small>Keep current readings in view.</small></div>
          <div><span className="platform-icon platform-icon--coral"><Leaf size={20} /></span><strong>Water status</strong><small>See values that merit attention.</small></div>
          <div><span className="platform-icon platform-icon--yellow"><Fish size={20} /></span><strong>One workspace</strong><small>Find the operational picture quickly.</small></div>
        </div>
        <footer className="landing-footer"><Link className="landing-brand landing-brand--dark" to="/"><span className="brand-mark"><Fish size={17} /></span><span>smart farm<span>OS</span></span></Link><span>A better view of the water.</span><Link to="/login">Application <ArrowUpRight size={13} /></Link></footer>
      </section>
    </main>
  );
}