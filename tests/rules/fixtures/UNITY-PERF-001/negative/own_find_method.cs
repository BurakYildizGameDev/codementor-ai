using UnityEngine;

public class Grid : MonoBehaviour
{
    int[] cells = new int[64];
    int Find(int value)
    {
        for (int i = 0; i < cells.Length; i++) if (cells[i] == value) return i;
        return -1;
    }
    void Update()
    {
        int index = Find(3);
        Debug.Log(index);
    }
}
