// EXPECT: 9
using System.Collections.Generic;
using UnityEngine;

public class Radar : MonoBehaviour
{
    void Update()
    {
        var nearby = new List<Collider>();
        nearby.AddRange(Physics.OverlapSphere(transform.position, 5f));
    }
}
