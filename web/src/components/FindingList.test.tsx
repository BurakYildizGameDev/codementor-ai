import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { finding } from "../test-fixtures";
import { FindingList } from "./FindingList";

it("hatalar açık, öneriler katlı bölümde (Faz 36)", async () => {
  const user = userEvent.setup();
  render(
    <FindingList
      findings={[
        finding({ id: "F-1", line_start: 4 }),
        finding({ id: "F-2", line_start: 7, severity: "low", kind: "suggestion", description: "Bir öneri." }),
      ]}
      diagnostics={[]}
      selectedLine={null}
      onSelect={() => {}}
    />,
  );
  const region = screen.getByRole("region", { name: "Bulgular" });
  expect(within(region).getByRole("heading", { name: "Hatalar (1)" })).toBeInTheDocument();
  const details = region.querySelector("details");
  expect(details).not.toBeNull();
  expect(details?.open).toBe(false);
  expect(within(region).getByText("Öneriler (1)")).toBeInTheDocument();
  await user.click(within(region).getByText("Öneriler (1)"));
  expect(details?.open).toBe(true);
  expect(within(details as HTMLElement).getByText("Bir öneri.")).toBeInTheDocument();
});

it("yalnız öneri varsa hata yok der", () => {
  render(
    <FindingList
      findings={[finding({ id: "F-2", severity: "low", kind: "suggestion" })]}
      diagnostics={[]}
      selectedLine={null}
      onSelect={() => {}}
    />,
  );
  expect(screen.getByText("Hata yok.")).toBeInTheDocument();
  expect(screen.getByText("Öneriler (1)")).toBeInTheDocument();
});
