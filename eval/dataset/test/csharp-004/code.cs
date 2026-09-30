using System.Collections.Generic;

public static class Tally
{
    public static Dictionary<string, int> Count(string[] words)
    {
        var counts = new Dictionary<string, int();
        foreach (var w in words)
        {
            counts[w] = counts.GetValueOrDefault(w) + 1;
        }
        return counts;
    }
}
