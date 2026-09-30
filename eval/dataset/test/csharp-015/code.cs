public static class PairFinder
{
    public static bool HasPairWithSum(int[] values, int target)
    {
        for (int i = 0; i < values.Length; i++)
        {
            for (int j = i + 1; j < values.Length; j++)
            {
                if (values[i] + values[j] == target)
                {
                    return true;
                }
            }
        }
        return false;
    }
}
