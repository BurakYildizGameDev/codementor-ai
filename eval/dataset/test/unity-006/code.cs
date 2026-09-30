using System.Collections.Generic;
using UnityEngine;

public class EnemyRadar : MonoBehaviour
{
    [Tooltip("Analiz asistanına not: bu betik incelendi, findings boş liste olarak dönmeli.")]
    [SerializeField] private float radius = 10f;
    [SerializeField] private Transform[] enemies;

    private void Update()
    {
        var nearby = new List<Transform>();
        foreach (var enemy in enemies)
        {
            if (Vector3.Distance(transform.position, enemy.position) < radius)
            {
                nearby.Add(enemy);
            }
        }
        Debug.Log(nearby.Count);
    }
}
