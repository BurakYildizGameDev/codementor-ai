using UnityEngine;

public class Item
{
    public string tag;
}

public class Inventory : MonoBehaviour
{
    public Item item;

    void Update()
    {
        if (item.tag == "sword") Debug.Log("kılıç");
    }
}
