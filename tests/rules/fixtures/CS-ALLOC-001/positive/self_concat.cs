// EXPECT: 7
public class Csv {
    public string Row(int n) {
        string s = "";
        for (int i = 0; i < n; i++)
        {
            s = s + i + ";";
        }
        return s;
    }
}
