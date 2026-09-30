using System.Collections.Generic;

public static class Stats
{
    public static int Max(List<int> values)
    {
        int best = values[0];
        foreach (var v in values)
        {
            if (v > best)
            {
                best = v;
            }
        }
        return best;
    }
}
