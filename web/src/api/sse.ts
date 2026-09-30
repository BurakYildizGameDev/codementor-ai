/** Sunucu gönderimli olay (SSE) metni için artımlı ayrıştırıcı. `POST /v1/analyze/stream`
 * `EventSource` ile okunamadığı için (yalnızca GET) akış `fetch` ile parça parça gelir. */

export interface SseEvent {
  event: string;
  data: string;
}

export class SseParser {
  private buffer = "";

  /** Yeni metin parçasını ekler; tamamlanan olayları döndürür (yarım kayıt tamponda kalır). */
  push(chunk: string): SseEvent[] {
    this.buffer += chunk.replace(/\r\n?/g, "\n");
    const events: SseEvent[] = [];
    let end: number;
    while ((end = this.buffer.indexOf("\n\n")) !== -1) {
      const record = this.buffer.slice(0, end);
      this.buffer = this.buffer.slice(end + 2);
      const parsed = parseRecord(record);
      if (parsed) events.push(parsed);
    }
    return events;
  }
}

function parseRecord(record: string): SseEvent | null {
  let event = "message";
  const data: string[] = [];
  for (const line of record.split("\n")) {
    if (line === "" || line.startsWith(":")) continue;
    const colon = line.indexOf(":");
    const field = colon === -1 ? line : line.slice(0, colon);
    const value = colon === -1 ? "" : line.slice(colon + 1).replace(/^ /, "");
    if (field === "event") event = value;
    else if (field === "data") data.push(value);
  }
  return data.length ? { event, data: data.join("\n") } : null;
}
