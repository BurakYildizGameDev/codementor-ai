using UnityEngine;

public class Thruster : MonoBehaviour
{
    [SerializeField] private Rigidbody body;
    [SerializeField] private float thrust = 20f;

    private void Update()
    {
        if (Input.GetKey(KeyCode.W))
        {
            body.AddForce(transform.forward * thrust);
        }
    }
}
