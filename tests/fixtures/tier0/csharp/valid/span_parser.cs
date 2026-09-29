using System;
using System.Globalization;

namespace Mentor.Samples;

public ref struct CsvLine
{
    private readonly ReadOnlySpan<char> line;

    public CsvLine(ReadOnlySpan<char> line) => this.line = line;

    public bool TryGetField(int index, out ReadOnlySpan<char> field)
    {
        var rest = line;
        for (var i = 0; ; i++)
        {
            var comma = rest.IndexOf(',');
            var current = comma < 0 ? rest : rest[..comma];
            if (i == index)
            {
                field = current;
                return true;
            }
            if (comma < 0) break;
            rest = rest[(comma + 1)..];
        }
        field = default;
        return false;
    }

    public bool TryGetInt(int index, out int value)
    {
        value = 0;
        return TryGetField(index, out var f) && int.TryParse(f, NumberStyles.Integer, CultureInfo.InvariantCulture, out value);
    }
}

public record Measurement(string Name, double Value)
{
    public override string ToString() => $"{Name}={Value:F2}";
}
