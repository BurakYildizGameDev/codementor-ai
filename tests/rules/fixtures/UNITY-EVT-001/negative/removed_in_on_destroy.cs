using System;
using UnityEngine;

public class HealthBar : MonoBehaviour
{
    public static event Action<int> Damaged;
    void Awake()
    {
        Damaged += OnDamaged;
    }
    void OnDestroy()
    {
        Damaged -= OnDamaged;
    }
    void OnDamaged(int amount) { }
}
