using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class Radar : MonoBehaviour
{
    public List<Transform> enemies = new List<Transform>();
    public float radius = 5f;

    void Update()
    {
        // LINQ ve ona verilen lambda CS-ALLOC-002 ile raporlanır (Faz 17)
        var near = enemies.Where(e => Vector3.Distance(e.position, transform.position) < radius).ToList();
        Debug.Log(near.Count);
    }
}
