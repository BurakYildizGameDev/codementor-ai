// expect-hint: n^2 | high
using System.Collections.Generic;

public class Dedup
{
    public static List<int> Unique(List<int> input)
    {
        var result = new List<int>();
        foreach (var x in input)
        {
            if (!result.Contains(x))
            {
                result.Add(x);
            }
        }
        return result;
    }
}
