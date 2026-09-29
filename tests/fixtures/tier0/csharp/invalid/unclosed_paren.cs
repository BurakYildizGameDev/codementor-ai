using System;
using System.Linq;

namespace Mentor.Samples
{
    public static class Stats
    {
        public static double Average(int[] values)
        {
            if (values.Length == 0 return 0; // expect-error
            return values.Average();
        }
    }
}
