// EXPECT: 9
using System.Collections.Generic;

public class Dedup {
    public List<int> Unique(int[] items) {
        List<int> seen = new List<int>();
        foreach (int x in items)
        {
            if (!seen.Contains(x)) seen.Add(x);
        }
        return seen;
    }
}
