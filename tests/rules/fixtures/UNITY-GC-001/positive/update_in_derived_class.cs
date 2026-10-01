// EXPECT: 10
using System.Collections.Generic;
using UnityEngine;

// Kullanıcı tabanı (BaseEnemy muhtemelen MonoBehaviour'dan türer): sıcak yol sayılır
public class Enemy : BaseEnemy
{
    void Update()
    {
        var targets = new List<Transform>();
        Track(targets);
    }
}
