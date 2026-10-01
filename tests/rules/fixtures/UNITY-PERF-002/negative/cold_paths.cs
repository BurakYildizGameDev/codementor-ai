using UnityEngine;

public class Door : MonoBehaviour
{
    private bool isPlayer;

    void Start()
    {
        isPlayer = tag == "Player";
    }

    void OnTriggerEnter(Collider other)
    {
        if (other.tag == "Player") Debug.Log("kapı açıldı");
    }
}
