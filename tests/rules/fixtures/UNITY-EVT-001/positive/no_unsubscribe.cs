// EXPECT: 10
using System;
using UnityEngine;

public class HealthBar : MonoBehaviour
{
    public static event Action<int> Damaged;
    void OnEnable()
    {
        Damaged += OnDamaged;
    }
    void OnDamaged(int amount) { }
}
