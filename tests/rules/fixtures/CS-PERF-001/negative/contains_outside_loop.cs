using System.Collections.Generic;

public class Inventory {
    private List<string> items = new List<string>();
    public bool Has(string name) {
        return items.Contains(name);
    }
    public int Total(int[] weights) {
        int sum = 0;
        for (int i = 0; i < weights.Length; i++) sum += weights[i];
        return sum;
    }
}
