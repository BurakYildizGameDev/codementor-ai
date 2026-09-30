using UnityEngine;

public class Health : MonoBehaviour
{
    [SerializeField private int maxHealth = 100;
    private int current;

    private void Awake()
    {
        current = maxHealth;
    }
}
