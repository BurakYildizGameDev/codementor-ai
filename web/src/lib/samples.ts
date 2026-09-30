/** Dil/motor seçenekleri ve editörün başlangıç örnekleri. Motor–dil uyumu mimari §6.2:
 * Unity yalnızca C#, Unreal yalnızca C++. */
import type { Engine, Language } from "../types/request";

export const LANGUAGES: { value: Language; label: string; monaco: string }[] = [
  { value: "c", label: "C", monaco: "c" },
  { value: "cpp", label: "C++", monaco: "cpp" },
  { value: "csharp", label: "C#", monaco: "csharp" },
];

export const ENGINE_LABELS: Record<Engine, string> = {
  none: "Yok",
  unity: "Unity",
  unreal: "Unreal",
};

export function enginesFor(language: Language): Engine[] {
  if (language === "cpp") return ["none", "unreal"];
  if (language === "csharp") return ["none", "unity"];
  return ["none"];
}

export function monacoLanguage(language: Language): string {
  return LANGUAGES.find((l) => l.value === language)?.monaco ?? "plaintext";
}

export const SAMPLES: Record<Language, string> = {
  c: `#include <stdlib.h>

int average(const int *values, int n) {
    int *tmp = malloc(n * sizeof(int));
    int sum = 0;
    for (int i = 0; i < n; i++) {
        tmp[i] = values[i] * 2;
        sum += tmp[i] / 2;
    }
    return sum / n;
}
`,
  cpp: `#include <vector>

bool hasDuplicate(const std::vector<int>& items) {
    for (size_t i = 0; i < items.size(); ++i) {
        for (size_t j = 0; j < items.size(); ++j) {
            if (i != j && items[i] == items[j]) {
                return true;
            }
        }
    }
    return false;
}
`,
  csharp: `using System.Collections.Generic;

public static class Scores
{
    public static int CountAbove(List<int> scores, int limit)
    {
        var result = new List<int>();
        foreach (var s in scores)
        {
            if (s > limit) result.Add(s);
        }
        return result.Count;
    }
}
`,
};
