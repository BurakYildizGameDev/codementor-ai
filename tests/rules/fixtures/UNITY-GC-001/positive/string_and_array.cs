// EXPECT: 10, 11
using UnityEngine;
using UnityEngine.UI;

public class ScoreLabel : MonoBehaviour
{
    public Text label;
    int score;
    void LateUpdate() {
        label.text = "Skor: " + score;
        var slots = new int[4];
    }
}
