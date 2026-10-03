// expect-hint: n^2 | high
public class Report
{
    public static string Join(string[] words)
    {
        string result = "";
        foreach (var w in words)
        {
            result += w + ",";
        }
        return result;
    }
}
