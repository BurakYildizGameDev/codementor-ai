using System.Collections.Generic;
using System.Linq;

public class Report
{
    public List<int> Big(List<int> values)
    {
        return values.Where(x => x > 10).ToList();
    }

    public int Sum(List<int> values)
    {
        int total = 0;
        for (int i = 0; i < values.Count; i++) total += values[i];
        return total;
    }
}
