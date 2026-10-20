import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { QUESTIONS } from "../test-fixtures";
import { QuestionDetails } from "./QuestionDetails";

const question = QUESTIONS[0]!;

describe("QuestionDetails", () => {
  it("soru seçili değilse hiçbir şey çizmez", () => {
    const { container } = render(<QuestionDetails question={undefined} />);
    expect(container).toBeEmptyDOMElement();
  });

  it("soru metnini, kısıtları ve örnek giriş/çıkışı gösterir (tam tarama #6)", () => {
    render(<QuestionDetails question={question} />);
    const card = screen.getByRole("region", { name: "Soru" });
    expect(within(card).getByRole("heading", { name: "Dizi toplamı" })).toBeInTheDocument();
    expect(within(card).getByText("Bir dizinin toplamını hesapla.")).toBeInTheDocument();
    expect(within(card).getByText("n ≤ 10^5")).toBeInTheDocument();
    expect(within(card).getByText("Örnekler (1)")).toBeInTheDocument();
    expect(within(card).getByText((_, el) => el?.tagName === "PRE" && el.textContent === "3\n1 2 3")).toBeInTheDocument();
    expect(within(card).getByText("6")).toBeInTheDocument();
    expect(within(card).getByText("1 + 2 + 3")).toBeInTheDocument();
  });

  it("örnek yoksa örnek bölümü yoktur", () => {
    const { sample_io: _omit, ...withoutSamples } = question;
    render(<QuestionDetails question={withoutSamples} />);
    expect(screen.queryByText(/Örnekler/)).not.toBeInTheDocument();
  });
});
