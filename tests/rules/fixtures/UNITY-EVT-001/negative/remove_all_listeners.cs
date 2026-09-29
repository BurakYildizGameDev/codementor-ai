using UnityEngine;
using UnityEngine.UI;

public class Menu : MonoBehaviour
{
    public Button quit;
    void OnEnable()
    {
        quit.onClick.AddListener(Quit);
    }
    void OnDisable()
    {
        quit.onClick.RemoveAllListeners();
    }
    void Quit() { }
}
