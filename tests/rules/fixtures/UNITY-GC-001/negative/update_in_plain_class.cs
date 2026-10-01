using System.Collections.Generic;
using UnityEngine;

// Tabanı olmayan sınıf: Unity bu Update'i her karede çağırmaz (yalnızca adı benziyor)
public class Simulation
{
    public void Update()
    {
        var snapshot = new List<int>();
        snapshot.Add(Time.frameCount);
    }
}
