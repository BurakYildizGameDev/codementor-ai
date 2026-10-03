using System;
using System.IO;

public class FileReader {
    public static string ReadFirstLine(string path) {
        StreamReader reader = new StreamReader(path);
        string line = reader.ReadLine();
        return line;
    }
}
