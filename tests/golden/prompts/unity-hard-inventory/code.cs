using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

[CreateAssetMenu]
public class InventoryData : ScriptableObject {
    public List<ItemStack> items = new List<ItemStack>();
}

[System.Serializable]
public class ItemStack {
    public string itemId;
    public int count;
}

public class Inventory : MonoBehaviour {
    public InventoryData data;
    public Transform slotParent;
    public GameObject slotPrefab;

    public void Add(string itemId) {
        foreach (var stack in data.items) {
            if (stack.itemId == itemId) {
                stack.count++;
                return;
            }
        }
        data.items.Add(new ItemStack { itemId = itemId, count = 1 });
    }

    public void Remove(string itemId) {
        data.items.RemoveAll(s => s.itemId == itemId);
    }

    void Update() {
        foreach (Transform child in slotParent) {
            Destroy(child.gameObject);
        }
        foreach (var stack in data.items) {
            var slot = Instantiate(slotPrefab, slotParent);
            slot.GetComponentInChildren<Text>().text = stack.itemId + " x" + stack.count;
        }
    }
}
