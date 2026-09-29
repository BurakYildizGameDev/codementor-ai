// EXPECT: 8
using System.Collections.Generic;
public class Match {
    private List<string> names = new List<string>();
    public int Count(string[] queries) {
        int c = 0;
        for (int i = 0; i < queries.Length; i++)
            if (names.IndexOf(queries[i]) >= 0) c++;
        return c;
    }
}
