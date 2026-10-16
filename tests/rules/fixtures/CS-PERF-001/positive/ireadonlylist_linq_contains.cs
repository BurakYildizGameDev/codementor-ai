// EXPECT: 11
using System.Collections.Generic;
using System.Linq;

public class Known
{
    public int CountIn(IReadOnlyList<int> ids, int[] values)
    {
        int hits = 0;
        foreach (int v in values)
            if (ids.Contains(v)) hits++;
        return hits;
    }
}
