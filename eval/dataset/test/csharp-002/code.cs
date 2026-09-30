using System.Collections.Generic;

public class Inventory
{
    private readonly List<string> _items = new List<string>();

    public void Add(string item)
    {
        _items.Add(item);
    }
