using System;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(menuName = "Envanter/Öğe")]
public class ItemDefinition : ScriptableObject
{
    public string displayName;
    public int maxStack = 99;
}

[Serializable]
public struct Slot
{
    public ItemDefinition item;
    public int count;
}

public class Inventory : MonoBehaviour
{
    [SerializeField] private List<ItemDefinition> startingItems = new();

    private readonly Dictionary<ItemDefinition, int> counts = new();
    public event Action<IReadOnlyDictionary<ItemDefinition, int>> Changed;

    private void Start()
    {
        foreach (var item in startingItems)
        {
            Add(item);
        }
    }

    public void Add(ItemDefinition item, int amount = 1)
    {
        counts.TryGetValue(item, out var current);
        counts[item] = Mathf.Min(current + amount, item.maxStack);
        Changed?.Invoke(counts);
    }

    public bool Remove(ItemDefinition item)
    {
        if (!counts.TryGetValue(item, out var current)) return false;
        if (current <= 1) counts.Remove(item);
        else counts[item] = current - 1;
        Changed?.Invoke(counts);
        return true;
    }
}
