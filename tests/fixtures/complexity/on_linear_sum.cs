// expect-hint: n | high
public class Stats
{
    public static int Sum(int[] values)
    {
        int total = 0;
        foreach (var v in values)
        {
            total += v;
        }
        return total;
    }
}
