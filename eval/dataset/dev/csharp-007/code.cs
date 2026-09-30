using System.IO;

public static class LineCounter
{
    public static int Count(string path)
    {
        var reader = new StreamReader(path);
        int lines = 0;
        while (reader.ReadLine() != null)
        {
            lines++;
        }
        return lines;
    }
}
