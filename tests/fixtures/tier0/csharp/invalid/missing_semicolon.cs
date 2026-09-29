using System;

namespace Mentor.Samples
{
    public static class Calc
    {
        public static int Sum(int[] values)
        {
            var total = 0;
            foreach (var v in values)
            {
                total += v // expect-error
            }
            return total;
        }
    }
}
