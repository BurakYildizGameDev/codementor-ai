public static class Search
{
    public static int IndexOf(int[] sorted, int key)
    {
        int lo = 0;
        int hi = sorted.Length - 1;
        while (lo <= hi)
        {
            int mid = (lo + hi) / 2;
            if (sorted[mid] == key)
            {
                return mid;
            }
            if (sorted[mid] < key)
            {
                lo = mid + 1;
            }
            else
            {
                hi = mid - 1;
            }
        }
        return -1;
    }
}
