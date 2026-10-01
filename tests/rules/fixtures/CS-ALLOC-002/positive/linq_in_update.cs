// EXPECT: 13
// ENGINE: unity
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class Radar : MonoBehaviour
{
    public List<string> names = new List<string>();

    void Update()
    {
        int unique = names.Distinct().Count();
        Debug.Log(unique);
    }
}
