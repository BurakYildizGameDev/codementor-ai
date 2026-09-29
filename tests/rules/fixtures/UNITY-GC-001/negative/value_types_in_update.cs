using UnityEngine;

public class Mover : MonoBehaviour
{
    public float speed = 2f;
    void Update()
    {
        var step = new Vector3(0f, 0f, speed * Time.deltaTime);
        transform.rotation = new Quaternion(0f, 0f, 0f, 1f);
        transform.position += step;
    }
}
