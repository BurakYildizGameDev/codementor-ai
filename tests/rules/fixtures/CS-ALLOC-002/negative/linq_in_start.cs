// ENGINE: unity
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class Radar : MonoBehaviour
{
    public List<string> names = new List<string>();
    private int unique;

    void Start()
    {
        unique = names.Distinct().Count();
    }

    void Update()
    {
        int n = names.Count;
        float m = Mathf.Max(n, unique);
        Debug.Log(m);
    }
}
