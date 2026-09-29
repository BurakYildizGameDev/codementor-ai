using UnityEngine;

public class Mover : MonoBehaviour
{
    [SerializeField] private float speed = 3f;

    private void Update()
    {
        var input = new Vector3(Input.GetAxis("Horizontal"), 0f, Input.GetAxis("Vertical"));
        transform.Translate(input * speed * Time.deltaTime;  // expect-error
    }
}
