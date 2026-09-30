// Test için referans çözüm (EnemyRadar, golden unity-03). Gerçek referanslar private/ altında
// tutulur; bu dosya yalnızca sızıntı korumasının fixture'larında kullanılır.
using System;
using System.Collections.Generic;
using UnityEngine;

public class EnemyRadar : MonoBehaviour
{
    public event Action<Transform> OnTargetFound;

    [SerializeField] private float radius = 10f;
    private readonly List<Transform> enemies = new List<Transform>();
    private readonly List<Transform> nearbyBuffer = new List<Transform>();
    private readonly HashSet<Transform> seenTargets = new HashSet<Transform>();
    private Health health;

    void OnEnable()
    {
        health = GetComponent<Health>();
        if (health != null) health.OnDeath += HandleDeath;
    }

    void OnDisable()
    {
        if (health != null) health.OnDeath -= HandleDeath;
    }

    void Update()
    {
        float sqrRadius = radius * radius;
        Vector3 origin = transform.position;
        nearbyBuffer.Clear();
        foreach (var enemy in enemies)
        {
            if (enemy != null && (enemy.position - origin).sqrMagnitude < sqrRadius)
                nearbyBuffer.Add(enemy);
        }
        foreach (var target in nearbyBuffer)
        {
            if (seenTargets.Add(target))
                OnTargetFound?.Invoke(target);
        }
    }

    void HandleDeath()
    {
        enemies.Clear();
        seenTargets.Clear();
    }
}
