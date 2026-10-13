import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { Controls } from "./Controls";
import { QUESTIONS } from "../test-fixtures";

const mockQuestion = QUESTIONS[0]!;

const defaultProps = {
  language: "c" as const,
  engine: "none" as const,
  questionId: "",
  questions: [],
  difficulty: "" as const,
  providers: [],
  provider: "",
  mode: "" as const,
  busy: false,
  onLanguage: () => {},
  onEngine: () => {},
  onQuestion: () => {},
  onDifficulty: () => {},
  onProvider: () => {},
  onMode: () => {},
  onAnalyze: () => {},
};

describe("Controls", () => {
  it("soru listesi boş olduğunda uyarı metnini gösterir (Faz E: E10)", () => {
    render(<Controls {...defaultProps} questions={[]} />);
    expect(screen.getByText("Bu filtrelerle eşleşen soru yok.")).toBeInTheDocument();
  });

  it("soru listesinde eleman varken uyarı metnini göstermez (Faz E: E10)", () => {
    render(<Controls {...defaultProps} questions={[mockQuestion]} />);
    expect(screen.queryByText("Bu filtrelerle eşleşen soru yok.")).not.toBeInTheDocument();
  });

  it("zorluk filtresi sonucu boş olduğunda uyarı metnini gösterir (Faz E: E10)", () => {
    render(
      <Controls
        {...defaultProps}
        questions={[mockQuestion]}
        difficulty="hard"
      />,
    );
    expect(screen.getByText("Bu filtrelerle eşleşen soru yok.")).toBeInTheDocument();
  });
});
