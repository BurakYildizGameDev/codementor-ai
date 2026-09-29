// EXPECT: 11, 12
using UnityEngine;
using UnityEngine.UI;

public class Menu : MonoBehaviour
{
    public Button play;
    public Button quit;
    void OnEnable()
    {
        play.onClick.AddListener(() => Debug.Log("play"));
        quit.onClick.AddListener(Quit);
    }
    void OnDisable()
    {
        play.onClick.RemoveListener(() => Debug.Log("play"));
    }
    void Quit() { }
}
