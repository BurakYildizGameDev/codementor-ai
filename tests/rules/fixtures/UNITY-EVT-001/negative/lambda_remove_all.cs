using UnityEngine;
using UnityEngine.UI;

public class Menu : MonoBehaviour
{
    public Button play;
    void OnEnable()
    {
        play.onClick.AddListener(() => Debug.Log("play"));
    }
    void OnDisable()
    {
        play.onClick.RemoveAllListeners();
    }
}
