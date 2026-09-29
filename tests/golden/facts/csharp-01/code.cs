using System;
using System.Text;

namespace Mentor.Samples
{
    public static class FizzBuzz
    {
        public static string BuildReport(int n)
        {
            if (n <= 0) return string.Empty;
            var sb = new StringBuilder(capacity: n * 5);
            for (var i = 1; i <= n; i++)
            {
                var line = (i % 15) switch
                {
                    0 => "FizzBuzz",
                    3 or 6 or 9 or 12 => "Fizz",
                    5 or 10 => "Buzz",
                    _ => i.ToString(),
                };
                sb.AppendLine(line);
            }
            return sb.ToString();
        }

        public static void Main()
        {
            Console.Write(BuildReport(15));
        }
    }
}
