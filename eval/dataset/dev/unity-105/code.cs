using System;
using UnityEngine;

public class ScoreDisplay : MonoBehaviour {
    public static event Action<int> OnScoreUpdated;

    private int currentScore;

    void OnEnable() {
        OnScoreUpdated += HandleScore;
    }

    void OnDisable() {
        OnScoreUpdated -= HandleScore;
    }

    private void HandleScore(int newScore) {
        currentScore = newScore;
    }
}
