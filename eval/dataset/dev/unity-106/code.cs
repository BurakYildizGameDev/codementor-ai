using System;
using UnityEngine;

public class LevelListener : MonoBehaviour {
    public static event Action OnLevelCompleted;

    void OnEnable() {
        OnLevelCompleted += HandleCompleted;
    }

    private void HandleCompleted() {
        Debug.Log("Level finished!");
    }
}
