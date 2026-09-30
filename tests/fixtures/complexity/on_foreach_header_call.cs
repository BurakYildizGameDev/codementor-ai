// expect-hint: n | medium
using System;
using System.Collections.Generic;

public static class WordCounter
{
    public static Dictionary<string, int> Count(string text)
    {
        var counts = new Dictionary<string, int>();
        foreach (var word in text.Split(' '))
        {
            counts.TryGetValue(word, out int current);
            counts[word] = current + 1;
        }
        return counts;
    }
}
