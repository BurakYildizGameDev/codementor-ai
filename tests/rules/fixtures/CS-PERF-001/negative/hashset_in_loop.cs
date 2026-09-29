using System.Collections.Generic;

public class Dedup {
    public List<int> Unique(int[] items) {
        var seen = new HashSet<int>();
        var result = new List<int>();
        var counts = new Dictionary<int, int>();
        foreach (int x in items)
        {
            if (seen.Contains(x)) continue;
            if (!counts.ContainsKey(x)) counts[x] = 0;
            seen.Add(x);
            result.Add(x);
        }
        return result;
    }
}
