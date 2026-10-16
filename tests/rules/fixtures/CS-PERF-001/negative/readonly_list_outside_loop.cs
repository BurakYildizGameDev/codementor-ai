using System.Collections.Generic;
using System.Linq;

public class Once
{
    private readonly IReadOnlyList<int> ids = new List<int>();

    public bool Has(int target)
    {
        return ids.Contains(target);  // döngü dışı: tek O(n) çağrı, bulgu yok
    }
}
