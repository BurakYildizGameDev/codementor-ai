// expect-hint: log n | high
public class Bits
{
    public static int Levels(int n)
    {
        int levels = 0;
        for (int size = 1; size < n; size *= 2)
        {
            levels++;
        }
        return levels;
    }
}
