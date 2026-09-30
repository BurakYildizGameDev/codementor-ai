using UnityEngine;

public class Jumper : MonoBehaviour
{
    [SerializeField] private Rigidbody body;
    [SerializeField] private float jumpForce = 5f;

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space)
        {
            body.AddForce(Vector3.up * jumpForce, ForceMode.Impulse);
        }
    }
}
