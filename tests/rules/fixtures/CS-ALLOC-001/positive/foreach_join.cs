// EXPECT: 9
using System.Collections.Generic;

public static class Report {
    public static string Join(List<string> names) {
        string result = "";
        foreach (var name in names)
        {
            result += name + ", ";
        }
        return result;
    }
}
