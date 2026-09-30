using System;

public static class CsvSum
{
    public static long SumFields(ReadOnlySpan<char> line)
    {
        long total = 0;
        while (!line.IsEmpty)
        {
            int comma = line.IndexOf(',');
            ReadOnlySpan<char> field = comma < 0 ? line : line.Slice(0, comma);
            if (long.TryParse(field, out long value))
            {
                total += value;
            }
            line = comma < 0 ? ReadOnlySpan<char>.Empty : line.Slice(comma + 1);
        }
        return total;
    }
}
