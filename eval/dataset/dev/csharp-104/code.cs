using System.Collections.Generic;

public class FilterService {
    public static List<int> RemoveDuplicates(int[] items) {
        var unique = new List<int>();
        foreach (var item in items) {
            if (!unique.Contains(item)) {
                unique.Add(item);
            }
        }
        return unique;
    }
}
