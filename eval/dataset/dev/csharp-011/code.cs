using System;
using System.Collections.Generic;

public static class WordCounter
{
    public static Dictionary<string, int> Count(string text)
    {
        var counts = new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase);
        foreach (var word in text.Split(' ', StringSplitOptions.RemoveEmptyEntries))
        {
            counts.TryGetValue(word, out int current);
            counts[word] = current + 1;
        }
        return counts;
    }
}
