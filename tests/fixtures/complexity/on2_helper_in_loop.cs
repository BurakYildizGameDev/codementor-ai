// expect-hint: n^2 | medium
public class Report
{
    static int CountAbove(int[] values, int limit)
    {
        int count = 0;
        for (int i = 0; i < values.Length; i++)
        {
            if (values[i] > limit) count++;
        }
        return count;
    }

    public static int[] Ranks(int[] values)
    {
        var ranks = new int[values.Length];
        for (int i = 0; i < values.Length; i++)
        {
            ranks[i] = CountAbove(values, values[i]);
        }
        return ranks;
    }
}
