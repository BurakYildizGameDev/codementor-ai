using UnityEngine;

public class Regen : MonoBehaviour
{
    public int health;
    public float timer;
    void OnEnable()
    {
        health += 10;
        timer += 0.5f;
    }
}
