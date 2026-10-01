// EXPECT: 10
using System.Collections.Generic;

public class Filter
{
    public int CountKnown(IList<int> known, int[] values)
    {
        int count = 0;
        foreach (int v in values)
            if (known.Contains(v)) count++;
        return count;
    }
}
