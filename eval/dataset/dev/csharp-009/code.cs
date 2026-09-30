using System.Collections.Generic;
using System.Linq;

public static class Scores
{
    public static List<int> AboveAverage(List<int> scores)
    {
        var result = new List<int>();
        for (int i = 0; i < scores.Count; i++)
        {
            if (scores[i] > scores.Average())
            {
                result.Add(scores[i]);
            }
        }
        return result;
    }
}
