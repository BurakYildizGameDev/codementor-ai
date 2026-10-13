import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as client from "../api/client";
import { HistoryPanel } from "./HistoryPanel";
import type { AnalysisSummary } from "../types/analysis_page";
import type { AnalysisReport } from "../types/report";

const mockSummary1: AnalysisSummary = {
  analysis_id: "01TEST1",
  created_at: "2026-10-13T10:00:00Z",
  degraded: false,
  early_exit: false,
  engine: "none",
  language: "c",
  provider: "claude",
  question_id: "c-q1",
  tokens_in: 100,
  tokens_out: 200,
};

const mockSummary2: AnalysisSummary = {
  analysis_id: "01TEST2",
  created_at: "2026-10-13T11:00:00Z",
  degraded: false,
  early_exit: false,
  engine: "none",
  language: "c",
  provider: "codex",
  question_id: null,
  tokens_in: 50,
  tokens_out: 150,
};

afterEach(() => {
  vi.restoreAllMocks();
});

describe("HistoryPanel", () => {
  it("boş liste durumunda 'Henüz analiz yok.' gösterir", async () => {
    vi.spyOn(client, "listAnalyses").mockResolvedValue({ items: [], next_cursor: null });

    render(<HistoryPanel onSelectReport={() => {}} />);

    await waitFor(() => {
      expect(screen.getByText("Henüz analiz yok.")).toBeInTheDocument();
    });
  });

  it("analizleri listeler, soru kimliği yoksa 'Serbest çalışma' yazar", async () => {
    vi.spyOn(client, "listAnalyses").mockResolvedValue({
      items: [mockSummary1, mockSummary2],
      next_cursor: null,
    });

    render(<HistoryPanel onSelectReport={() => {}} />);

    await waitFor(() => {
      expect(screen.getByText("c-q1")).toBeInTheDocument();
      expect(screen.getByText("Serbest çalışma")).toBeInTheDocument();
    });
  });

  it("'Daha fazla' düğmesi sonraki sayfayı ekler", async () => {
    vi.spyOn(client, "listAnalyses")
      .mockResolvedValueOnce({
        items: [mockSummary1],
        next_cursor: "CURSOR1",
      })
      .mockResolvedValueOnce({
        items: [mockSummary2],
        next_cursor: null,
      });

    render(<HistoryPanel onSelectReport={() => {}} />);

    await waitFor(() => {
      expect(screen.getByText("c-q1")).toBeInTheDocument();
    });

    const moreBtn = screen.getByRole("button", { name: "Daha fazla" });
    fireEvent.click(moreBtn);

    await waitFor(() => {
      expect(screen.getByText("Serbest çalışma")).toBeInTheDocument();
      expect(screen.queryByRole("button", { name: "Daha fazla" })).not.toBeInTheDocument();
    });
  });

  it("'Sil' düğmesi analizi siler ve listeden kaldırır", async () => {
    vi.spyOn(client, "listAnalyses").mockResolvedValue({
      items: [mockSummary1],
      next_cursor: null,
    });
    const deleteSpy = vi.spyOn(client, "deleteAnalysis").mockResolvedValue();
    const onClearReport = vi.fn();

    render(
      <HistoryPanel
        onSelectReport={() => {}}
        currentReportId="01TEST1"
        onClearReport={onClearReport}
      />,
    );

    await waitFor(() => {
      expect(screen.getByText("c-q1")).toBeInTheDocument();
    });

    const deleteBtn = screen.getByRole("button", { name: "Sil" });
    fireEvent.click(deleteBtn);

    await waitFor(() => {
      expect(deleteSpy).toHaveBeenCalledWith("01TEST1");
      expect(screen.queryByText("c-q1")).not.toBeInTheDocument();
      expect(onClearReport).toHaveBeenCalled();
    });
  });

  it("'Tümünü temizle' confirm iptal edilirse silmez, kabul edilirse siler", async () => {
    vi.spyOn(client, "listAnalyses").mockResolvedValue({
      items: [mockSummary1],
      next_cursor: null,
    });
    const deleteAllSpy = vi.spyOn(client, "deleteAllAnalyses").mockResolvedValue({ deleted: 1 });
    const confirmSpy = vi.spyOn(window, "confirm");

    // İptal durumu
    confirmSpy.mockReturnValueOnce(false);
    render(<HistoryPanel onSelectReport={() => {}} />);

    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Tümünü temizle" })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole("button", { name: "Tümünü temizle" }));
    expect(deleteAllSpy).not.toHaveBeenCalled();

    // Onay durumu
    confirmSpy.mockReturnValueOnce(true);
    fireEvent.click(screen.getByRole("button", { name: "Tümünü temizle" }));

    await waitFor(() => {
      expect(deleteAllSpy).toHaveBeenCalled();
      expect(screen.getByText("Henüz analiz yok.")).toBeInTheDocument();
    });
  });

  it("satıra tıklayınca getAnalysis çağrılır ve onSelectReport tetiklenir", async () => {
    vi.spyOn(client, "listAnalyses").mockResolvedValue({
      items: [mockSummary1],
      next_cursor: null,
    });
    const fakeReport = { analysis_id: "01TEST1" } as AnalysisReport;
    const getSpy = vi.spyOn(client, "getAnalysis").mockResolvedValue(fakeReport);
    const onSelect = vi.fn();

    render(<HistoryPanel onSelectReport={onSelect} />);

    await waitFor(() => {
      expect(screen.getByText("c-q1")).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText("c-q1"));

    await waitFor(() => {
      expect(getSpy).toHaveBeenCalledWith("01TEST1");
      expect(onSelect).toHaveBeenCalledWith(fakeReport);
    });
  });
});
