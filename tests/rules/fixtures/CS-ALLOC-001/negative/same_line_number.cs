public class Stats {
    public string label;
    public float Sum(float[] values) {
        float total = 0f;
        foreach (var v in values) { total += v; label = "son: " + v; }
        return total;
    }
}
