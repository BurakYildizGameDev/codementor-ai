// EXPECT: 10, 11, 12
using System.Collections.Generic;

public class Journal {
    private string log = "";
    public string Build(List<string> items) {
        var s = "";
        string reversed = "";
        foreach (var item in items) {
            s += item;
            this.log += item;
            reversed = item + reversed;
        }
        return s + reversed;
    }
}
