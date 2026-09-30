using System.Collections.Generic;
using UnityEngine;

public class InventoryView : MonoBehaviour
{
    [SerializeField] private InventoryData data;
    private readonly List<string> shown = new List<string>();

    public void Refresh()
    {
        foreach (string itemId in data.itemIds)
        {
            if (!shown.Contains(itemId))
            {
                shown.Add(itemId);
                SpawnSlot(itemId);
            }
        }
    }

    private void SpawnSlot(string itemId)
    {
        Debug.Log("Yuva: " + itemId);
    }
}
