using System;

public class Log {
    public string Run(int n) {
        string summary = "";
        int total = 0;
        for (int i = 0; i < n; i++)
        {
            Console.WriteLine("adim " + i);
            total += i;
        }
        summary += "toplam: " + total;
        return summary;
    }
}
