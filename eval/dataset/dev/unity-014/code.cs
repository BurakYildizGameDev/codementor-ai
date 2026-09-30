using UnityEngine;
using UnityEngine.UI;

public class ScoreLabel : MonoBehaviour
{
    [SerializeField] private Text label;
    public int score;

    private void Update()
    {
        label.text = "Skor: " + score;
    }
}
