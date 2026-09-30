import { AlertTriangle, Fish, RefreshCw } from 'lucide-react';

export function LoadingState({ label = 'Loading tank data' }: { label?: string }) {
  return (
    <div className="loading-grid" role="status" aria-label={label}>
      <span className="sr-only">{label}</span>
      {[0, 1, 2].map((item) => <div className="loading-card" key={item} />)}
    </div>
  );
}

export function EmptyState({
  title = 'No tanks to show',
  message = 'Tank records will appear here when they are available.',
}: {
  title?: string;
  message?: string;
}) {
  return (
    <div className="feedback-panel">
      <span className="feedback-icon"><Fish size={20} /></span>
      <h2>{title}</h2>
      <p>{message}</p>
    </div>
  );
}

export function ErrorState({ onRetry }: { onRetry: () => void }) {
  return (
    <div className="feedback-panel" role="alert">
      <span className="feedback-icon feedback-icon--warning"><AlertTriangle size={20} /></span>
      <h2>We couldn’t load this view</h2>
      <p>Try again. Your tank information has not been changed.</p>
      <button className="button button--secondary button--small" onClick={onRetry}>
        <RefreshCw size={15} /> Try again
      </button>
    </div>
  );
}