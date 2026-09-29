using System.Collections.Generic;
using UnityEngine;

public class Picker : MonoBehaviour
{
    public List<int> ids = new List<int>();
    public int wanted;
    int FindWanted()
    {
        return ids.IndexOf(wanted);
    }
    void Update()
    {
        int index = FindWanted();
        Debug.Log(index);
    }
}
