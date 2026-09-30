using UnityEngine;

public class Mover : MonoBehaviour
{
    [SerializeField] private float speed = 3f;

    private void Update()
    {
        transform.Translate(Vector3.forward * speed * Time.deltaTime)
    }
}
