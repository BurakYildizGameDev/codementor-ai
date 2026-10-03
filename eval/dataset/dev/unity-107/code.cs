using System.Collections.Generic;
using UnityEngine;

public class EnemyRadar : MonoBehaviour {
    void Update() {
        List<Vector3> patrolPoints = new List<Vector3>();
        patrolPoints.Add(transform.position);
    }
}
