// EXPECT: 13
using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class Radar : MonoBehaviour
{
    public List<Transform> enemies = new List<Transform>();

    void Update()
    {
        var near = enemies.Where(e => e != null).ToList(); Action log = () => Debug.Log(near.Count);
        log();
    }
}
