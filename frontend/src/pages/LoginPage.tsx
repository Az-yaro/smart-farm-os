import { useState, type FormEvent } from 'react';
import { ArrowLeft, ArrowRight, Fish, LockKeyhole, UserRound } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';

export function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [notice, setNotice] = useState('');
  const navigate = useNavigate();

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setNotice('Sign-in is not connected yet. Preview the dashboard with sample data instead.');
  }

  return (
    <main className="login-page">
      <section className="login-visual">
        <img src="https://images.unsplash.com/photo-1500375592092-40eb2168fd21?auto=format&fit=crop&w=1600&q=85" alt="Water moving across a broad blue surface" />
        <div className="login-visual-shade" />
        <Link className="landing-brand" to="/"><span className="brand-mark brand-mark--light"><Fish size={19} /></span><span>smart farm<span>OS</span></span></Link>
        <div className="login-visual-copy"><p className="eyebrow eyebrow--light"><span /> YOUR FARM, IN FOCUS</p><h1>Every reading<br />has a place.</h1><p>Bring a little more clarity to the daily rhythm of your farm.</p></div>
        <span className="login-visual-caption">AQUACULTURE OPERATIONS · SMART FARM OS</span>
      </section>
      <section className="login-content">
        <Link to="/" className="back-link"><ArrowLeft size={15} /> Back to home</Link>
        <div className="login-form-wrap">
          <span className="login-mark"><Fish size={21} /></span>
          <p className="eyebrow"><span /> WORKSPACE ACCESS</p>
          <h2>Welcome back.</h2>
          <p className="login-subtitle">Sign in to continue to your farm workspace.</p>
          <form className="login-form" onSubmit={handleSubmit}>
            <label htmlFor="username">Username</label>
            <div className="input-wrap"><UserRound size={17} /><input id="username" name="username" autoComplete="username" placeholder="Your username" value={username} onChange={(event) => setUsername(event.target.value)} required /></div>
            <div className="label-row"><label htmlFor="password">Password</label></div>
            <div className="input-wrap"><LockKeyhole size={17} /><input id="password" name="password" type="password" autoComplete="current-password" placeholder="Enter your password" value={password} onChange={(event) => setPassword(event.target.value)} required /></div>
            <button type="submit" className="button button--dark login-submit">Sign in <ArrowRight size={17} /></button>
          </form>
          {notice && <p className="login-notice" role="status">{notice}</p>}
          <div className="login-divider"><span /> <small>OR</small> <span /></div>
          <button className="button button--outline login-preview" onClick={() => navigate('/dashboard')}>Preview with sample data <ArrowRight size={16} /></button>
          <p className="login-footnote">New to Smart Farm OS? <Link to="/">Learn about the platform</Link></p>
        </div>
        <p className="login-legal">SMART FARM OS <span>·</span> AQUACULTURE OPERATIONS</p>
      </section>
    </main>
  );
}