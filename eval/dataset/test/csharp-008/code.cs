using System;

public static class AgeReader
{
    public static int ReadAge()
    {
        Console.Write("Yaşınız: ");
        string line = Console.ReadLine();
        int age = int.Parse(line);
        return age;
    }
}
