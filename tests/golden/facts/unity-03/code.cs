using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class EnemyRadar : MonoBehaviour
{
    public event Action<Transform> OnTargetFound;

    [SerializeField] private float radius = 10f;
    private List<Transform> enemies = new List<Transform>();
    private Health health;
    private string status;

    void OnEnable()
    {
        health = GetComponent<Health>();
        health.OnDeath += HandleDeath;
    }

    void Update()
    {
        var nearby = enemies.Where(e => Vector3.Distance(e.position, transform.position) < radius).ToList();
        for (int i = 0; i < nearby.Count; i++)
        {
            for (int j = 0; j < nearby.Count; j++)
            {
                if (i != j && nearby[i] == nearby[j])
                {
                    status = "Duplicate: " + nearby[i].name;
                }
            }
            if (!enemies.Contains(nearby[i]))
            {
                OnTargetFound?.Invoke(nearby[i]);
            }
        }
    }

    void HandleDeath()
    {
        enemies.Clear();
    }
}
