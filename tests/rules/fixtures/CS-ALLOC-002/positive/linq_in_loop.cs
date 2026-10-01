// EXPECT: 12
using System.Collections.Generic;
using System.Linq;

public class Report
{
    public int CountBig(List<List<int>> groups)
    {
        int total = 0;
        foreach (List<int> g in groups)
        {
            total += g.Where(x => x > 10).Count();
        }
        return total;
    }
}
