using System.Collections.Generic;
using UnityEngine;

public class Radar : MonoBehaviour
{
    List<Collider> nearby;
    void Start()
    {
        nearby = new List<Collider>();
    }
    void Update()
    {
        nearby.Clear();
    }
}
