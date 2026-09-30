import { SseParser } from "./sse";

describe("SseParser", () => {
  it("tek kaydı ayrıştırır", () => {
    const parser = new SseParser();
    expect(parser.push('event: stage\ndata: {"a":1}\n\n')).toEqual([
      { event: "stage", data: '{"a":1}' },
    ]);
  });

  it("parçalara bölünmüş kaydı tamponlar", () => {
    const parser = new SseParser();
    expect(parser.push("event: rep")).toEqual([]);
    expect(parser.push('ort\ndata: {"id"')).toEqual([]);
    expect(parser.push(':"x"}\n\n')).toEqual([{ event: "report", data: '{"id":"x"}' }]);
  });

  it("tek parçada birden çok olay ve CRLF", () => {
    const parser = new SseParser();
    const events = parser.push("event: stage\r\ndata: 1\r\n\r\nevent: error\ndata: 2\n\n");
    expect(events.map((e) => e.event)).toEqual(["stage", "error"]);
    expect(events.map((e) => e.data)).toEqual(["1", "2"]);
  });

  it("olay adı yoksa message; çok satırlı data birleştirilir; yorum atlanır", () => {
    const parser = new SseParser();
    expect(parser.push(": ping\ndata: a\ndata: b\n\n")).toEqual([
      { event: "message", data: "a\nb" },
    ]);
  });
});
