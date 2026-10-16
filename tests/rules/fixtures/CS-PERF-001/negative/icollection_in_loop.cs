using System.Collections.Generic;
using System.Linq;

public class Bucket
{
    public bool HasAny(ICollection<int> items, int[] values)
    {
        foreach (int v in values)
        {
            if (items.Contains(v)) return true;  // örnek metot: HashSet de olabilir, sus
        }
        return false;
    }
}
