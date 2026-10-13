/** Monaco hover'ına düz metin olarak girecek metindeki markdown özel karakterlerini kaçışlar. */
export function escapeMarkdown(text: string): string {
  return text.replace(/[\\`*_{}\[\]()#+\-.!|<>~]/g, (c) => `\\${c}`);
}
