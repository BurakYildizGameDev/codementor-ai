import { useEffect, useState } from "react";
import { deleteAllAnalyses, deleteAnalysis, getAnalysis, listAnalyses } from "../api/client";
import { formatCount } from "../lib/usage";
import type { AnalysisSummary } from "../types/analysis_page";
import type { AnalysisReport } from "../types/report";

interface HistoryPanelProps {
  onSelectReport: (report: AnalysisReport) => void;
  currentReportId?: string | null;
  onClearReport?: () => void;
}

export function HistoryPanel({
  onSelectReport,
  currentReportId,
  onClearReport,
}: HistoryPanelProps) {
  const [items, setItems] = useState<AnalysisSummary[]>([]);
  const [nextCursor, setNextCursor] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    listAnalyses()
      .then((page) => {
        if (!cancelled) {
          setItems(page.items);
          setNextCursor(page.next_cursor ?? null);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : String(err));
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  async function handleLoadMore() {
    if (!nextCursor || loadingMore) return;
    setLoadingMore(true);
    try {
      const page = await listAnalyses(20, nextCursor);
      setItems((prev) => [...prev, ...page.items]);
      setNextCursor(page.next_cursor ?? null);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoadingMore(false);
    }
  }

  async function handleDelete(id: string, e: React.MouseEvent) {
    e.stopPropagation();
    try {
      await deleteAnalysis(id);
      setItems((prev) => prev.filter((it) => it.analysis_id !== id));
      if (currentReportId === id) {
        onClearReport?.();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    }
  }

  async function handleClearAll() {
    const confirmed = window.confirm("Tüm analiz geçmişi silinecek. Emin misin?");
    if (!confirmed) return;
    try {
      await deleteAllAnalyses();
      setItems([]);
      setNextCursor(null);
      if (currentReportId) {
        onClearReport?.();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    }
  }

  async function handleRowClick(id: string) {
    try {
      const report = await getAnalysis(id);
      onSelectReport(report);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    }
  }

  return (
    <div className="card history-panel" role="region" aria-label="Analiz geçmişi">
      <div className="history-header">
        <h3>Geçmiş Analizler</h3>
        {items.length > 0 && (
          <button
            type="button"
            className="btn-danger-outline"
            onClick={() => void handleClearAll()}
          >
            Tümünü temizle
          </button>
        )}
      </div>

      {error && (
        <div className="card error">
          {error}
        </div>
      )}

      {loading ? (
        <p className="muted">Geçmiş yükleniyor…</p>
      ) : items.length === 0 ? (
        <p className="muted">Henüz analiz yok.</p>
      ) : (
        <ul className="history-list">
          {items.map((item) => {
            const dateStr = new Date(item.created_at).toLocaleString("tr-TR");
            const tokenCount = formatCount(item.tokens_in + item.tokens_out);
            return (
              <li
                key={item.analysis_id}
                className={`history-item ${item.analysis_id === currentReportId ? "selected" : ""}`}
                onClick={() => void handleRowClick(item.analysis_id)}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    void handleRowClick(item.analysis_id);
                  }
                }}
              >
                <div className="history-item-content">
                  <div className="history-item-top">
                    <span className="history-date">{dateStr}</span>
                    <span className="badge badge-lang">{item.language}</span>
                  </div>
                  <div className="history-item-sub">
                    <span>{item.question_id || "Serbest çalışma"}</span>
                    <span> · {item.provider || "-"}</span>
                    <span> · {tokenCount} token</span>
                  </div>
                </div>
                <button
                  type="button"
                  className="btn-delete"
                  aria-label="Sil"
                  onClick={(e) => void handleDelete(item.analysis_id, e)}
                >
                  Sil
                </button>
              </li>
            );
          })}
        </ul>
      )}

      {nextCursor && (
        <div className="history-footer">
          <button
            type="button"
            className="btn-secondary"
            disabled={loadingMore}
            onClick={() => void handleLoadMore()}
          >
            {loadingMore ? "Yükleniyor…" : "Daha fazla"}
          </button>
        </div>
      )}
    </div>
  );
}
