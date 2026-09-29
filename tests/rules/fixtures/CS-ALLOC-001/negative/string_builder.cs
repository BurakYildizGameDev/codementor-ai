using System.Text;

public class Csv {
    public string Row(int n) {
        var sb = new StringBuilder();
        for (int i = 0; i < n; i++)
        {
            sb.Append(i).Append(';');
        }
        return sb.ToString();
    }
}
