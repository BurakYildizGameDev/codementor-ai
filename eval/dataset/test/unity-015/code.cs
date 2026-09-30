using System.Collections;
using UnityEngine;

public class Regenerator : MonoBehaviour
{
    [SerializeField] private int amount = 1;
    public int health = 50;

    private IEnumerator Start()
    {
        while (true)
        {
            health += amount;
            yield return new WaitForSeconds(0.5f);
        }
    }
}
